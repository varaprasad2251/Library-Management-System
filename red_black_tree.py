from binary_min_heap import ReservationHeap


class Book:
    def __init__(self, book_id, book_name, author_name, availability_status):
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.availability_status = availability_status
        self.borrowed_by = None
        self.reservation_heap = ReservationHeap()

class RedBlackNode:
    def __init__(self, book):
        self.color = 'red'
        self.left_child = None
        self.right_child = None
        self.val = book

class RedBlackTree:
    def __init__(self):
        self.root = None


    def rank(self, node):
        return

    def search_node(self, book_id):
        node = self.root
        if node.val.book_id == book_id:
            return node
        else:
            while node is not None:
                if book_id < node.val.book_id:
                    node = node.left_child
                elif book_id > node.val.book_id:
                    node = node.right_child
                else:
                    print("Book Found - {}".format(node.val.book_name))
                    return node
            return None

    def insert_node(self, new_node):
        if self.root is None:
            self.root = new_node
        else:
            node = self.root
            parent = None
            while node is not None:
                parent = node
                if new_node.val.book_id < node.val.book_id:
                    node = node.left_child
                else:
                    node = node.right_child
            if new_node.val.book_id < parent.val.book_id:
                parent.left_child = new_node
            else:
                parent.right_child = new_node



    def delete_node(self, node):

        return


    def print_book(self, book_id):
        return

    def print_books(self, book_id_one, book_id_two):

        return

    def insert_book(self, book_id, book_name, author_name, availability_status, borrowed_by):
        # new_book = Book(book_id, book_name, author_name, availability_status, borrowed_by)
        # self.books.append(new_book)
        return

    def borrow_book(self, patron_id, book_id, patron_priority):
        return

    def return_book(self, patron_id, book_id):
        return

    def delete_book(self, book_id):
        return

    def find_closest_book(self, target_id):
        return

    def color_flip_count(self):
        return

    def _print_tree(self, root, level=0, prefix="Root: "):
        if root is not None:
            print(" " * (level * 4) + prefix + str(root.val.__dict__))
            if root.left_child is not None or root.right_child is not None:
                self._print_tree(root.left_child, level + 1, "L--- ")
                self._print_tree(root.right_child, level + 1, "R--- ")
if __name__ == '__main__':
    rbtree = RedBlackTree()
    book1 = Book(1, "Book1", "Author1", "Yes")
    book2 = Book(2, "Book2", "Author2", "Yes")
    book3 = Book(3, "Book3", "Author3", "Yes")
    book4 = Book(4, "Book4", "Author4", "Yes")
    node1 = RedBlackNode(book1)
    node2 = RedBlackNode(book2)
    node3 = RedBlackNode(book3)
    node4 = RedBlackNode(book4)
    rbtree.insert_node(node2)
    rbtree.insert_node(node3)
    rbtree.insert_node(node1)
    rbtree.insert_node(node4)
    rbtree._print_tree(rbtree.root)
    x = rbtree.search_node(3)
    print(x.val.__dict__)