# Name: Katie Schaumleffle
# OSU Email: schaumlk@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5
# Due Date: 11/16/2021
# Description: This assignment implements an AVL tree. Includes methods for add(), remove()
#               contains(), inorder_traversal(), find_min(), find_max(), is_empty(), and
#               make_empty(). Also includes several helper methods to assist these methods.


import random


class Stack:
    """
    Class implementing STACK ADT.
    Supported methods are: push, pop, top, is_empty

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """
    def __init__(self):
        """ Initialize empty stack based on Python list """
        self._data = []

    def push(self, value: object) -> None:
        """ Add new element on top of the stack """
        self._data.append(value)

    def pop(self):
        """ Remove element from top of the stack and return its value """
        return self._data.pop()

    def top(self):
        """ Return value of top element without removing from stack """
        return self._data[-1]

    def is_empty(self):
        """ Return True if the stack is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "STACK: { " + ", ".join(data_str) + " }"


class Queue:
    """
    Class implementing QUEUE ADT.
    Supported methods are: enqueue, dequeue, is_empty

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """
    def __init__(self):
        """ Initialize empty queue based on Python list """
        self._data = []

    def enqueue(self, value: object) -> None:
        """ Add new element to the end of the queue """
        self._data.append(value)

    def dequeue(self):
        """ Remove element from the beginning of the queue and return its value """
        return self._data.pop(0)

    def is_empty(self):
        """ Return True if the queue is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "QUEUE { " + ", ".join(data_str) + " }"


class TreeNode:
    """
    AVL Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

    def __str__(self):
        return 'AVL Node: {}'.format(self.value)


class AVL:
    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.root = None

        # populate AVL with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of AVL in human-readable form using pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self.root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, cur, values):
        """
        Helper method for __str__. Does pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if cur:
            values.append(str(cur.value))
            self._str_helper(cur.left, values)
            self._str_helper(cur.right, values)

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        s = Stack()
        s.push(self.root)
        while not s.is_empty():
            node = s.pop()
            if node:
                # check for correct height (relative to children)
                l = node.left.height if node.left else -1
                r = node.right.height if node.right else -1
                if node.height != 1 + max(l, r):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self.root:
                        return False
                s.push(node.right)
                s.push(node.left)
        return True

    # -----------------------------------------------------------------------

    def updateHeight(self, node):
        """
        Helper method that takes in a node and updates the height of the node and 
        ancestors before it. Calculated by using max(node.left.height + node.right.height) + 1, 
        for non-leaf. For leaves height = 0
        """
        #update node based on if it has children or not.
        if node.left is not None and node.right is not None:
            #If left heavy, use height from left
            if node.left.height > node.right.height:
                node.height = node.left.height + 1
            #If right heavy, use height from right
            else:
                node.height = node.right.height + 1
        #If a leaf, height = 0
        elif node.left is None and node.right is None:
            node.height = 0
        #If no left children, use height from right +1
        elif node.left is None:  
            node.height = node.right.height + 1
        #If no right children, use height from left +1
        elif node.right is None:
            node.height = node.left.height + 1
        
        while node.parent is not None:
            # parents are at least of height one
            parent = node.parent
            left, right = parent.left, parent.right
            #If have both parents, use height from parent with largest height
            if left is not None and right is not None:
                if left.height > right.height:
                    parent.height = left.height + 1
                else:
                    parent.height = right.height + 1
            #If no right parent, use height from left
            elif right is None:
                parent.height = left.height + 1
            #If we get here, then we have no left parent, so use right parents height
            else:
                parent.height = right.height + 1
            node = node.parent

    def rotateRight(self, node):
        """
        Takes in a node and performs a right rotation assuming that all pre-conditions 
        are met. Updates the parent for all nodes involved. 
        """
        # point the parents to the node 
        parent = None
        if node.parent is not None:
            parent = node.parent
        leftNode = node.left
        node.left = leftNode.right
        #Point left nodes parent to node
        if node.left is not None:
            node.left.parent = node
        leftNode.right = node
        #If parent is none, left child becomes the root
        if parent is None:
            self.root = leftNode
            self.root.parent = None
        else:
            leftNode.parent = parent
            if parent.right == node:
                parent.right = leftNode
            else:
                parent.left = leftNode
        #update parent to the left child
        node.parent = leftNode
        self.updateHeight(node)

    def rotateLeft(self,node):
        """
        Takes in a node and performs a left rotation assuming that all pre-conditions 
        are met. Updates the parent for all nodes involved. 
        """
        # Like a linked list! 
        parent = None
        #point parents to node
        if node.parent is not None:
            parent = node.parent 
        rightNode = node.right
        node.right = rightNode.left
        #point right nodes parent to node
        if node.right is not None:
            node.right.parent = node
        rightNode.left = node
        #If parent is none, right node become the root
        if parent is None:
            self.root = rightNode
            self.root.parent = None
        else:
            rightNode.parent = parent
            if parent.right == node:
                parent.right = rightNode
            else:
                parent.left = rightNode 
        #update parent to right child
        node.parent = rightNode
        self.updateHeight(node)

    def rebalance(self, node):
        """
        Takes in a node and rebalances the node starting from that node and all parents involved
        Everything below that node is assumed to already be balanced.
        """
        # Starting from the node we just added in, so everything below that should already be balanced. 
        # We mainly need to focus on the case where node.left and node.right are both not None.

        if node is not None:
            #If we have both L&R children
            if node.left is not None and node.right is not None:
                height = node.right.height - node.left.height
                #If right heavy, check if RR or RL
                if height == 2: 
                    if node.right.left is None or (node.right.right is not None and node.right.left.height <= node.right.right.height):
                        self.rotateLeft(node) 
                    else:  
                        self.rotateRight(node.right)  # this step is required to make it RR heavy
                        self.rotateLeft(node) 
                #If left heavy, check if its LL or LR
                elif height == -2: 
                    if node.left.right is None or (node.left.left is not None or node.left.left.height >= node.left.right.height):
                        self.rotateRight(node)
                    #LR, rotate L then R
                    else:  
                        self.rotateLeft(node.left)  # this step is required to make it LL heavy
                        self.rotateRight(node)
            #If we have left child
            elif node.right is None and node.height == 2:
                # Make sure that it is left left 
                if node.left.right is None or (node.left.left is not None and node.left.left.height >= node.left.right.height):
                    self.rotateRight(node)
                else:
                    self.rotateLeft(node.left)  # required to make it LL heavy
                    self.rotateRight(node)
            #If we have right child
            elif node.left is None and node.height == 2:
                # we need to make sure that it is RR 
                if node.right.left is None or (node.right.right is not None and node.right.right.height >= node.right.left.height): 
                    self.rotateLeft(node)
                else:
                    self.rotateRight(node.right)  # required to make it RR heavy
                    self.rotateLeft(node)
            self.rebalance(node.parent)
        
    def find(self, node, value, tof = True):
        """
        Takes in a value and returns the node which matches the value. If false it will 
        return the parent node or the node if already exists.
        """
        if node is not None:
            #If the value we're looking for is smaller than the nodes value, traverse left
            if node.value > value:
                if node.left is not None:
                    return self.find(node.left, value, tof)
                else:
                    return node
            else:
                #If false and values match, return node
                if not tof and node.value == value:
                    return node
                #traverse right
                elif node.right is not None:
                    return self.find(node.right, value, tof)
                else:
                    return node    

    def add(self, value: object) -> None:
        """
        Adds a node containing value to the AVL tree, if it doesn't already exist
        """
        node = TreeNode(value)
        #If tree is empty, node becomes the root
        if self.root is None:
            self.root = node
            return
        # If we get here, we are dealing with parents
        parentNode = self.find(self.root, value, False)
        #Duplicate values not allowed
        if parentNode.value == value: 
            return
        if parentNode.value > value:
            parentNode.left = node
        #If here, then parentNode.value < value
        else:
            parentNode.right = node
        #update parent node
        node.parent = parentNode
        self.updateHeight(node)
        self.rebalance(node)

    def removeRoot(self):
        """
        A helper method which removes a node that is a root.
        """
        #If tree is empty
        if self.root.left is None and self.root.right is None:
            self.root = None 
            return
        #If no left child, make right child the root
        elif self.root.left is None:
            self.root = self.root.right
        #If no right child, make left child root
        elif self.root.right is None:
            self.root = self.root.left
        #If we have both right and left children
        else: 
            #inorder successor is the leftmost node in the right subtree
            succ = self.root.right
            while succ.left is not None:
                succ = succ.left
            succ.left = self.root.left
            succ.left.parent = succ
            parent = None
            #find the parent
            if succ.parent is not self.root:
                parent = succ.parent
                parent.left = succ.right
                if parent.left is not None:
                    parent.left.parent = parent
                succ.right = self.root.right
                succ.right.parent = succ
            else:
                succ.right = self.root.right.right
                if succ.right is not None:
                    succ.right.parent = succ
            #successor becomes parent, remove roots parent
            self.root = succ
            self.root.parent = None 
            if parent is not None:
                self.updateHeight(parent)
                self.rebalance(parent)
                return
        
        self.root.parent = None
        self.updateHeight(self.root)
        self.rebalance(self.root)

    def removeNonRoot(self, node):
        """
        A helper method to remove a node if it is not a root.
        """
        parent = node.parent
        #If no children, parent node points to None
        if node.left is None and node.right is None:
            if node == parent.left:
                parent.left = None 
            else:
                parent.right = None
            #update and rebalance because everything below is already balanced
            self.updateHeight(parent)  
            self.rebalance(parent)    
        #If only right child, update parent node to point to nodes child
        elif node.left is None:
            if node == parent.left:
                parent.left = node.right
            else:
                parent.right = node.right
            node.right.parent = parent
            self.updateHeight(parent)
            self.rebalance(parent)
        #If only left child, update parent node to point to nodes child
        elif node.right is None:
            if node == parent.left:
                parent.left = node.left
            else:
                parent.right = node.left
            node.left.parent = parent
            self.updateHeight(parent)
            self.rebalance(parent)
        #node has both left and right children
        else: 
            #inorder successor is the leftmost node in the right subtree 
            succ = node.right
            #find inorder successor
            while succ.left is not None:
                succ = succ.left
            succ.left = node.left
            succ.left.parent = succ
            succParent = None
            #Find successors parent
            if succ.parent is not node:
                succParent = succ.parent
                succ.parent.left = succ.right
                if succParent.left is not None:
                    succParent.left.parent = succParent
            if node.right != succ:
                succ.right = node.right
            else:
                succ.right = node.right.right
            #update parent node to point to successor
            if succ.right is not None:
                succ.right.parent = succ
            if parent.left == node:
                parent.left = succ
            else:
                parent.right = succ
            succ.parent = parent 
            if succParent is not None:
                self.updateHeight(succParent)
                self.rebalance(succParent)
            else:
                self.updateHeight(succ)
                self.rebalance(succ)
        return

    def remove(self, value: object) -> bool:
        """
        Removes a node containing value from the tree and returns True if it successfully removes
        the value. Otherwise it returns False.
        """
        #Returns false if tree is empty
        if self.root is None:
            return False 
        node = self.find(self.root, value, False)
        #Returns false if no values match
        if node.value != value:
            return False
        #If the value we're looking for is the root, call the removeRoot method
        if node == self.root:
            self.removeRoot()
        #If we get here, the value is in the tree but isn't the root. Call removeNonRoot method
        else:
            self.removeNonRoot(node)
        return True 

    def contains(self, value: object) -> bool:
        """
        This method returns true if the value parameter is in the tree or False if it is not.
        If the tree is empty, the method returns False.
        """
        #Returns false if tree is empty
        if self.root is None:
            return False
        node = self.find(self.root, value, False)
        #returns true if we are able to find the matching value in the tree
        if node.value == value:
            return True
        else:
            return False

    def inorder_traversal(self) -> Queue:
        """
        Performs inorder traversal of tree and returns a Queue object that contains 
        the values of the visited nodes, in the order they were visited.
        """
        # If tree is empty, return empty Queue
        if self.root is None:
            return Queue()

        # call recursive helper method to process a non-empty tree and return resulting Queue
        return self.inorder_helper(self.root, Queue())
        

    def inorder_helper(self, node, q):
        """
        Recursive helper to inorder_traversal()
        """
        if node is not None:
            # traverse to node.left then process current node
            self.inorder_helper(node.left, q)
            q.enqueue(node.value)
            #once leftmost node is processed, process right node
            self.inorder_helper(node.right, q)
        return q

    def find_min(self) -> object:
        """
        This method returns the smallest value in the tree
        """
        node = self.root
        #returns None if tree is empty
        if node is None:
            return
        #traverse left, returning leftmost value
        while node.left is not None:
            node = node.left
        return node.value
       

    def find_max(self) -> object:
        """
        This method returns the highest value in the tree
        """
        node = self.root
        #returns none if tree is empty
        if node is None:
            return
        #Traverse right, returning rightmost value
        while node.right is not None:
            node = node.right   
        return node.value
    
    def is_empty(self) -> bool:
        """
        This method returns true if the tree is empty, otherwise returns false
        """
        #If the tree doesn't have a root, the tree is empty
        if self.root is None:
            return True
        return False

    def make_empty(self) -> None:
        """
        This method removes all of the nodes from the tree
        """
        if self.is_empty() == True:
            return
        #recursively remove the root until tree is empty
        self.removeRoot()
        self.make_empty()
        


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        avl = AVL(case)
        print(avl)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        avl = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', avl)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        avl = AVL()
        for value in case:
            avl.add(value)
        if not avl.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    avl = AVL(case)
    for del_value in case:
        print('INPUT  :', avl, del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    avl = AVL(case)
    for _ in case[:-2]:
        print('INPUT  :', avl, avl.root.value)
        avl.remove(avl.root.value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        avl = AVL(case)
        for value in case[::2]:
            avl.remove(value)
        if not avl.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

