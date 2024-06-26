from collections import deque

class RBNode:
    ''' The node for a red-black tree. A color of 0 is red, a color of 1 is black.'''

    def __init__(self, data, parent = None, left = None, right = None):
        self.data = data
        self.color = 0
        self.parent = parent
        self.left = left
        self.right = right

class RedBlackTree:

    # Sets the root of the tree to none
    def __init__(self):
        self.root = None
        self.black_height = 0

    # Inserts a new node into the tree exactly like a binary search tree, then calls
    #   balance(RBNode) method to handle any necessary re-balancing
    def insert(self, data):
        # Check if the tree is empty, then add the node as the root, set the root to be black
        if self.root is None:
            new_node = RBNode(data)
            new_node.color = 1
            self.root = new_node
            self.black_height += 1
            return
        
        current = self.root
        # This loop finds the leaf node to be replaced with the new value and inserts
        #   the new node at that location. It escapes after adding the node and reaching
        #   one of 2 break statements
        while True:
            # New value is less than the value of the current node
            if data < current.data:
                # Check if the left subtree is not empty
                if current.left is not None:
                    # Continue the search in the left sub tree 
                    current = current.left
                else:
                    # Add the new value at this location
                    current.left = RBNode(data, current)
                    current = current.left
                    break
            # New value is greater than or equal to the value of the current node
            else:
                # Check if the right subtree is not empty
                if current.right is not None:
                    # Continue the search in the right sub tree
                    current = current.right
                else:
                    # Add the new value at this location
                    current.right = RBNode(data, current)
                    current = current.right
                    break

        # Newly added nodes are red, so now we check if the newly added node has a red
        #   parent and therefor breaks the no red-red parent-child rule
        if current.parent.color == 0:
            self.insert_rebalance(current)

    # This method re-balances the tree based on red-black tree rules, it is called
    #   after insertions and may recursively call itself in some circumstances
    def insert_rebalance(self, current):
        # Get the parent and grandparent of the current node. Note that the root node is always 
        #   black so if the no red-red parent-child rule is broken, then the parent is never
        #   the root node and the existence of a grandparent is guarenteed.
        parent = current.parent
        grandparent = parent.parent

        # Get the uncle of the current node
        if grandparent.left == parent:
            uncle = grandparent.right
        else:
            uncle = grandparent.left

        # Check the color of the current node's uncle
        if uncle is not None and uncle.color == 0:
            # Uncle is red, this is insertion case 1. Set the parent and uncle of the current
            #   node to black and the grandparent to red.
            parent.color, uncle.color, grandparent.color = 1, 1, 0

            # Check if the grandparent is the root node
            if grandparent is self.root:
                # Change the color back to black, increase the blackheight by 1. This is 
                #   a terminal case because we've re-balanced all the way up the tree.
                grandparent.color = 1
                self.black_height += 1
            # Check if great grandparent is the root node
            elif grandparent.parent is self.root:
                # This is a terminal case because we've re-balanced all the way up the tree.
                return
            else:
                # Continue up the tree re-balancing from the position of the grandparent if there is 
                #   still a red-red parent-child conflict, otherwise this is a terminal case
                if (grandparent.parent.color == 0):
                    self.insert_rebalance(grandparent)

        else: # All paths below are terminal cases
            # Uncle is black. Now we have to check if the current node is the 'inside child' 
            #   of its parent. To find this we compare the relationship between grandparent
            #   and parent to the relation between parent and current. If they are different
            #   then the current node is an inside child. ex: parent is left child of grandparent
            #   and current is right child of parent. If there is an inside child then it is
            #   case 2 and we perform a rotation to get an outside child. An outside child is case 3
            if parent is grandparent.left and current is parent.right:
                # Perform a left rotation on the child and parent to create an outside child. 
                self.rotation(current)
                # Swap current and parent name
                current, parent = parent, current

            # This is the other inside child condition
            elif parent is grandparent.right and current is parent.left:
                # Perform a right rotation on the child and parent to create an outside child.
                self.rotation(current)
                # Swap current and parent name
                current, parent = parent, current

            # At this point we have an outside child and are in case 3. We perform a rotation
            #   on the parent and grandparent, then we are finished re-balancing.
            self.rotation(parent)
            # Recolor parent and grandparent
            grandparent.color = 0
            parent.color = 1
    
    # Searches calls search and delete_helper methods to delete a specific value, returns True
    #   on success or False if the value is not in the tree.
    def delete(self, data):
        # Search the tree for the value, return False if it does not exist in the tree
        current = self.search(data)
        if current is False:
            return False
        return self.delete_helper(current)
        
    # Deletes a specific node in the tree, returns True on success or False if the node is not 
    #   in the tree. This method will recursively call itself when the node to be deleted has 2 children.
    #   In such a case, this method will swap the node marked for deletion with its inorder successor,
    #   Then attempt to delete the inorder successor which is guarenteed to have at most 1 child. A 
    #   deleted black node with 1 child will force the tree to be rebalanced. A deleted red node or
    #   a deleted black node with no children does not cause the tree to be rebalanced.
    def delete_helper(self, current):
        # Set the parent node
        parent = current.parent
        # Check how many children the node to be deleted has, first perform a deletion as a normal
        #   Binary search tree, then recolor and rotate as necessary to repair red-black properties
        if current.left is None:
            if current.right is None:
                # Node has no children, simply delete it
                if parent is not None:
                    # Rebalance if needed (if the node being deleted is black)
                    if current.color == 1:
                        self.delete_rebalance(current)
                    # Finish deleting the node
                    if parent.left == current:
                        parent.left = None
                    else:
                        parent.right = None
                    current.parent = None
                # Node to be deleted is the root node
                else:
                    self.root = None
            else: # Node has a right child only
                # Rebalance if needed (if the node being deleted is black)
                if current.color == 1:
                    self.delete_rebalance(current)
                # Replace current with its right child
                if parent is not None:
                    if parent.left == current:
                        parent.left = current.right
                        parent.left.parent = parent
                    else:
                        parent.right = current.right
                        parent.right.parent = parent
                # Node to be deleted is the root node        
                else:
                    self.root = current.right
                    self.root.parent = None
                # Set current to the child that took its place, this is needed for rebalancing later
                current = current.right
        elif current.right is None:  # Node has a left child only
            # Rebalance if needed (if the node being deleted is black)
            if current.color == 1:
                self.delete_rebalance(current)
            # Replace current with its left child
            if parent is not None:
                if parent.left == current:
                    parent.left = current.left
                    parent.left.parent = parent
                else:
                    parent.right = current.left
                    parent.right.parent = parent
            # Node to be deleted is the root node
            else:
                self.root = current.left
                self.root.parent = None
            # Set current to the child that took its place, this is needed for rebalancing later
            current = current.left
        else:
            # Node has 2 children, replace the value in target node with its inorder predecessor or inorder 
            #   successor, whichever is further down the tree. Then repeat this deletion from the location of 
            #   the replaced predecessor or successor. Inorder predecessor is the rightmost node in the target's 
            #   left sub tree and inorder successor is the leftmost node in the target's right sub tree
            inorder_predecessor = current.left
            inorder_predecessor_count = 0
            inorder_successor = current.right
            inorder_successor_count = 0
            # Find the predecessor
            while inorder_predecessor.right is not None:
                inorder_predecessor = inorder_predecessor.right
                inorder_predecessor_count += 1
            # Find the successor
            while inorder_successor.left is not None:
                inorder_successor = inorder_successor.left
                inorder_successor_count += 1
            # Compare predecessor depth to successor depth, take the one that is deeper
            if inorder_predecessor_count > inorder_successor_count:
                # Swap the values in current and inorder predecessor
                current.data, inorder_predecessor.data = inorder_predecessor.data, current.data
                # Recursively call this function from the inorder node location
                return self.delete_helper(inorder_predecessor)
            else:
                # Swap the values in current and inorder successor
                current.data, inorder_successor.data = inorder_successor.data, current.data
                # Recursively call this function from the inorder node location
                return self.delete_helper(inorder_successor)
        # Node has been removed
        return True
    
    # Rebalances the tree to repair red-black tree properties after a deletion. When this method gets
    #   control the node passed in is the only child of the previously deleted node, it has already 
    #   been raised up into the place of the deleted node.
    def delete_rebalance(self, current):
        # Check if the current node has a red child, if it does then color it black and return, this is a trivial case
        if current.left is not None and current.left.color == 0:
            current.left.color = 1
            return True
        if current.right is not None and current.right.color == 0:
            current.right.color = 1
            return True
        # Current node is the root node, this is another trivial case
        if current is self.root:
            return True
        else: # Current node is black and not the root node
            # Set parent, sibling, and sibling-parent relationship (left or right child of parent)
            parent = current.parent
            if parent.left == current:
                sibling = parent.right
                sibling_parent_relationship = 'right'
            else:
                sibling = parent.left
                sibling_parent_relationship = 'left'
            # Check if sibling of current node is red, this is case 1 and transforms into case 2b. 
            #   Current node of interest remains the same.
            if sibling.color == 0:
                # Parent and sibling preform a rotation (left or right) depending on their relationship
                self.rotation(sibling)
                # Parent and sibling recolor
                parent.color = 0
                sibling.color = 1
                # Reset the sibling and parent sibling relationship, note that the new sibling must be 
                #   black after the above transformation is complete
                if parent.left == current:
                    sibling = parent.right
                    sibling_parent_relationship = 'right'
                else:
                    sibling = parent.left
                    sibling_parent_relationship = 'left'
            # The color of sibling is black, so now we check the color of sibling children starting
            #   with checking if both are black, this is to maintain the simplest logic
            if (sibling.left is None or sibling.left.color == 1) and (sibling.right is None or sibling.right.color == 1):
                # Parent is black, sibling is black, and both children of sibling are black, 
                #   this is case 2a. Recursively call this method in which parent becomes the new node 
                #   of interest, recolor sibling to red, then return.
                if parent.color == 1:
                    success = self.delete_rebalance(parent)
                    sibling.color = 0
                    return success
                # Parent is red and sibling is black, and both children of sibling are black, this 
                #   is case 2b. This is a terminal case, recolor both parent and sibling, then return.
                else:
                    sibling.color = 0
                    parent.color = 1
                    return True
            # Now we look at cases where the children of sibling are not both black. For these cases
            #   parent may be either color. We start by examining the 'outside child'
            if sibling_parent_relationship == 'right':
                # Check if the outside child of sibling is black
                if sibling.right is None or sibling.right.color == 1:
                    # Outside child is black and inside child is red (since we know both can't be black
                    #   if we made it to this point in the algorithm), this is case 3. This transforms 
                    #   into case 4, sibling and its left child perform a right rotation, then they 
                    #   each change color
                    nephew = sibling.left
                    self.rotation(nephew)
                    # Update the colors of sibling and nephew
                    nephew.color = 1
                    sibling.color = 0
                    # Reset sibling
                    sibling = nephew
                # Outside child is red and inside child may be either color, this is case 4. This is a
                #   terminal case. Sibling and parent perform a left rotation. Sibling acquires the color
                #   of parent, parent becomes black, and sibling's outside child becomes black.
                self.rotation(sibling)
                sibling.color = parent.color
                parent.color = 1
                sibling.right.color = 1
            else: # Sibling is the left child of parent and we need the mirror algorithms
                # Check if the outside child of sibling is black
                if sibling.left is None or sibling.left.color == 1:
                    # Outside child is black and inside child is red (since we know both can't be black
                    #   if we made it to this point in the algorithm), this is case 3. This transforms 
                    #   into case 4, sibling and its right child perform a left rotation, then they 
                    #   each change color
                    nephew = sibling.right
                    self.rotation(nephew)
                    # Update the colors of sibling and nephew
                    nephew.color = 1
                    sibling.color = 0
                    # Reset sibling
                    sibling = nephew
                # Outside child is red and inside child may be either color, this is case 4. This is a
                #   terminal case. Sibling and parent perform a right rotation. Sibling acquires the color
                #   of parent, parent becomes black, and sibling's outside child becomes black.
                self.rotation(sibling)
                sibling.color = parent.color
                parent.color = 1
                sibling.left.color = 1
        return True

    # This method rotates a node with its parent. The type of rotation (left or right) depends
    #   on whether the node is the right or left child of its parent. A parent and left child
    #   will be right rotated and vice versa.
    def rotation(self, current):
        parent = current.parent
        # Check if the parent is None, this mean the current node is the root and we return without rotating
        if parent is None:
            return
        # Check if parent's right child is the current node so we can perform the correct rotation.
        if parent.right == current: # This is a left rotation
            # Swap the middle sub tree from current to parent
            parent.right = current.left
            # Check if the middle sub tree has at least 1 node, update its parent if it does
            if parent.right is not None:
                parent.right.parent = parent
            # Check if parent is the root node, if it is, make current the new root node
            if self.root == parent:
                self.root = current
                current.parent = None
            # Otherwise make current the new child of grandparent
            else:
                grandparent = parent.parent
                # Update the correct child of grandparent
                if grandparent.left == parent:
                    grandparent.left = current
                else:
                    grandparent.right = current
                # Update the parent of the current node
                current.parent = grandparent
            # Make parent the child of the current node and update parent's parent
            current.left = parent
            parent.parent = current
        else: # This is a right rotation
            # Swap the middle sub tree from current to parent
            parent.left = current.right
            # Check if the middle sub tree has at least 1 node, update its parent if it does
            if parent.left is not None:
                parent.left.parent = parent
                current.parent = None
            # Check if parent is the root node, if it is, make current the new root node
            if self.root == parent:
                self.root = current
                current.parent = None
            # Otherwise make current the new child of grandparent
            else:
                grandparent = parent.parent
                # Update the correct child of grandparent
                if grandparent.left == parent:
                    grandparent.left = current
                else:
                    grandparent.right = current
                # Update the parent of the current node
                current.parent = grandparent
            # Make parent the child of the current node and update parent's parent
            current.right = parent
            parent.parent = current
    
    # Searches the red-black tree for a given value and returns the node with the value
    #   or returns False if the value is not in the tree.
    def search(self, data):
        current = self.root
        # While loop travels the tree until it finds the value or reaches a leaf node
        while current is not None:
            # Check if the data in the current node is what we are searching for
            if data == current.data:
                return current
            # Compare the data we are searching for to the data in the current node
            elif data < current.data:
                current = current.left
            else:
                current = current.right
        # The value is not in the tree
        return False

    # Calls a helper method to print the left sub tree, then prints the root, then 
    #   calls the helper method again to print the right sub tree.
    def inorder_traverse(self):
        if self.root is not None:
            self.inorder_traverse_helper(self.root.left, 1)
            # print(self.root.data)
            print(str(self.root.data) + ', ' + str(self.root.color) + ', ' + '0')
            self.inorder_traverse_helper(self.root.right, 1)

    # Recursive helper method that prints out the entire tree except the root
    def inorder_traverse_helper(self, current, depth):
        if current is not None:
            self.inorder_traverse_helper(current.left, depth + 1)
            # print(current.data)
            print(str(current.data) + ', ' + str(current.color) + ', ' + str(depth))
            self.inorder_traverse_helper(current.right, depth + 1)

    # Breadth first traverse of the tree
    def breadth_traverse(self):
        # Initialize 2 synced deques, one for nodes and one for node depths
        nodes = deque()
        depths = deque()
        nodes.append(self.root)
        depths.append(0)

        # Loop will continue until the queue is empty
        while len(nodes) > 0:
            current = nodes.popleft()
            depth = depths.popleft()

            # Check if the current node is not none
            if current is not None:
                # Add the children of the current node and their depths to the queues
                nodes.append(current.left)
                nodes.append(current.right)
                depths.append(depth + 1)
                depths.append(depth + 1)

                # Print out the current node as well as its color and depth
                if depths and depths[0] == depth:
                    print('(' + str(current.data) + ', ' + str(current.color) + ', ' + str(depth) + ')', end = ' , ')
                else:
                    print('(' + str(current.data) + ', ' + str(current.color) + ', ' + str(depth) + ')')
            else:
                # Print out None at leaf nodes
                if depths and depths[0] == depth:
                    print('None', end = ' , ')
                else:
                    print('None')
