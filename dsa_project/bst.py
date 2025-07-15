class TaskNode:
    def __init__(self, task):
        self.task = task
        self.left = None#stores the task, and left and right pointers
        self.right = None


class BST:#handles traversal, insertion and search
    def __init__(self):#stores nodes
        self.root = None

    def insert(self, task):
        def _insert(node, task):
            if not node:
                return TaskNode(task)
            if task.priority < node.task.priority:
                node.left = _insert(node.left, task)
            else:
                node.right = _insert(node.right, task)
            return node
        self.root = _insert(self.root, task)

    def delete(self, priority):
        def _delete(node, priority):
            if not node:
                return node
            if priority < node.task.priority:
                node.left = _delete(node.left, priority)
            elif priority > node.task.priority:
                node.right = _delete(node.right, priority)
            else:
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                temp = self._min_value_node(node.right)
                node.task = temp.task
                node.right = _delete(node.right, temp.task.priority)
            return node
        self.root = _delete(self.root, priority)

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def inorder_traversal(self):
        result = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.task)
                _inorder(node.right)
        _inorder(self.root)
        return result

    def search(self, priority):
        def _search(node, priority):
            if not node:
                return None
            if node.task.priority == priority:#sets the root node as the priority
                return node.task
            elif priority < node.task.priority:
                return _search(node.left, priority)
            else:
                return _search(node.right, priority)
        return _search(self.root, priority)
  