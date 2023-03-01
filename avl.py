import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

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
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
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
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        new_node = AVLNode(value)

        # if tree is empty, set new_node as root
        if not self._root:
            self._root = new_node
            return

        # traverse the tree to find the appropriate place to insert new_node
        curr_node = self._root
        while True:
            if value < curr_node.value:
                if curr_node.left:
                    curr_node = curr_node.left
                else:
                    curr_node.left = new_node
                    new_node.parent = curr_node
                    break
            else:
                if curr_node.right:
                    curr_node = curr_node.right
                else:
                    curr_node.right = new_node
                    new_node.parent = curr_node
                    break

        # update the heights of all ancestors of the new node
        node = new_node
        while node:
            left_height = node.left.height if node.left else -1
            right_height = node.right.height if node.right else -1
            node.height = 1 + max(left_height, right_height)
            node = node.parent

        # perform AVL rotations if necessary
        node = new_node
        while node:
            balance_factor = self._balance_factor(node)
            if balance_factor < -1:
                if self._balance_factor(node.right) > 0:
                    self._rotate_right(node.right)
                self._rotate_left(node)
            elif balance_factor > 1:
                if self._balance_factor(node.left) < 0:
                    self._rotate_left(node.left)
                self._rotate_right(node)
            node = node.parent

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Return the balance factor of a given node
        """
        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1
        return left_height - right_height

    def _rotate_left(self, node: AVLNode) -> None:
        """
        Perform a left rotation at the given node
        """
        pivot = node.right  # y = z.right
        left = pivot.left  # T2 = y.left

        pivot.left = node  # y.left = z
        node.right = left  # z.right = t2

        node.height = 1 + max(node.left.height if node.left else -1, node.right.height if node.right else -1)
        pivot.height = 1 + max(node.height, pivot.right.height if pivot.right else -1)

        if node == self._root:
            self._root = pivot

    def _rotate_right(self, node: AVLNode) -> None:
        """
        Perform a right rotation at the given node
        """
        pivot = node.left # y = z.left        z = node
        right = pivot.right # t3 = y.right

        pivot.right = node # y.right = z
        node.left = right    # z.left = T3
        node.height = 1 + max(node.left.height if node.left else -1, node.right.height if node.right else -1)
        pivot.height = 1 + max(pivot.left.height if pivot.left else -1, node.height)

        if node == self._root:
            self._root = pivot

    def remove(self, value: object) -> bool:
        node = self.find(value)
        if not node:
            return False

        self._remove(node)
        return True

    def _remove(self, node: AVLNode) -> None:
        # if node has no children, simply remove it
        if not node.left and not node.right:
            if node.parent:
                if node is node.parent.left:
                    node.parent.left = None
                else:
                    node.parent.right = None
                self._update_height(node.parent)
            else:
                self._root = None

        # if node has only one child, replace it with its child
        elif not node.left:
            if node is node.parent.left:
                node.parent.left = node.right
            else:
                node.parent.right = node.right
            node.right.parent = node.parent
            self._update_height(node.right)

        elif not node.right:
            if node is node.parent.left:
                node.parent.left = node.left
            else:
                node.parent.right = node.left
            node.left.parent = node.parent
            self._update_height(node.left)

        # if node has two children, replace it with its in-order successor
        else:
            successor = self._find_min(node.right)
            node.value = successor.value
            self._remove(successor)

        # rebalance the tree
        self._rebalance(node.parent)

    def _rebalance(self, node: AVLNode) -> None:
        while node:
            left_height = node.left.height if node.left else -1
            right_height = node.right.height if node.right else -1
            node.height = 1 + max(left_height, right_height)

            balance_factor = self._balance_factor(node)

            # left-left case
            if balance_factor > 1 and self._balance_factor(node.left) >= 0:
                self._rotate_right(node)

            # left-right case
            elif balance_factor > 1 and self._balance_factor(node.left) < 0:
                self._rotate_left(node.left)
                self._rotate_right(node)

            # right-right case
            elif balance_factor < -1 and self._balance_factor(node.right) <= 0:
                self._rotate_left(node)

            # right-left case
            elif balance_factor < -1 and self._balance_factor(node.right) > 0:
                self._rotate_right(node.right)
                self._rotate_left(node)

            node = node.parent

    def _update_height(self, node: AVLNode) -> None:
        while node:
            left_height = node.left.height if node.left else -1
            right_height = node.right.height if node.right else -1
            node.height = 1 + max(left_height, right_height)
            node = node.parent

    def _find_min(self, node: AVLNode) -> AVLNode:
        while node.left:
            node = node.left
        return node

    def find(self, value: object) -> AVLNode:
        node = self._root
        while node:
            if value == node.value:
                return node
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        return None
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
        tree = AVL(case)
        print(tree)

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
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
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
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
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
