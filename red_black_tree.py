from datetime import datetime

from binary_min_heap import Reservation, ReservationHeap


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
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.val = book if book else -999


class RedBlackTree:
    def __init__(self):
        self.root = None
        self.flip_count = 0

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
                    # print("Book Found - {}".format(node.val.book_name))
                    return node
            return None

    def search_nodes(self, node, book_id_one, book_id_two, result):
        if node is None:
            return
        if book_id_one < node.val.book_id:
            self.search_nodes(node.left_child, book_id_one, book_id_two, result)
        if (node.val.book_id >= book_id_one) and (node.val.book_id <= book_id_two):
            result.append(node)
        if book_id_two > node.val.book_id:
            self.search_nodes(node.right_child, book_id_one, book_id_two, result)

    def find_closest_book(self, node, target_id, least_difference, closest_books):
        if node is None:
            return least_difference, closest_books
        least_difference, closest_books = self.find_closest_book(node.left_child, target_id, least_difference,
                                                                 closest_books)
        difference = abs(node.val.book_id - target_id)
        if difference == least_difference:
            closest_books.append(node)
        elif difference < least_difference:
            least_difference = difference
            closest_books.clear()
            closest_books.append(node)
        least_difference, closest_books = self.find_closest_book(node.right_child, target_id, least_difference,
                                                                 closest_books)
        return least_difference, closest_books

    def ll_rotation(self, node):
        node_parent = node.parent
        y = node.left_child
        c = y.right_child
        y.right_child = node
        node.parent = y
        node.left_child = c
        if node.left_child is not None:
            node.left_child.parent = node
        if node_parent is None:
            self.root = y
            y.parent = None
        else:
            y.parent = node_parent
            if y.parent.right_child == node:
                y.parent.right_child = y
            else:
                y.parent.left_child = y
        y.color = 'black'
        node.color = 'red'

    def rr_rotation(self, node):
        node_parent = node.parent
        y = node.right_child
        c = y.left_child
        y.left_child = node
        node.parent = y
        node.right_child = c
        if node.right_child is not None:
            node.right_child.parent = node
        if node_parent is None:
            self.root = y
            y.parent = None
        else:
            y.parent = node_parent
            if y.parent.right_child == node:
                y.parent.right_child = y
            else:
                y.parent.left_child = y
        y.color = 'black'
        node.color = 'red'

    def lr_rotation(self, node):
        self.rr_rotation(node.left_child)
        self.ll_rotation(node)

    def rl_rotation(self, node):
        self.ll_rotation(node.right_child)
        self.rr_rotation(node)

    def insert_node(self, new_node):
        if self.root is None:
            self.root = new_node
            self.root.color = 'black'
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
                parent.left_child.parent = parent
                node = parent.left_child
            else:
                parent.right_child = new_node
                parent.right_child.parent = parent
                node = parent.right_child
            if node.parent.color == 'red':
                while node.parent.color == 'red' and node.parent.parent is not None:
                    if (node.parent.parent.left_child is not None) and (node.parent == node.parent.parent.left_child):
                        d = node.parent.parent.right_child
                        if d is not None and d.color == 'red':
                            node.parent.color = 'black'
                            self.flip_count += 1
                            node.parent.parent.color = 'red'
                            self.flip_count += 1
                            d.color = 'black'
                            self.flip_count += 1
                            node = node.parent.parent
                        else:
                            if node.parent.left_child == node:
                                self.ll_rotation(node.parent.parent)
                                self.flip_count += 2
                            else:
                                self.lr_rotation(node.parent.parent)
                                self.flip_count += 2
                    elif (node.parent.parent.right_child is not None) and (
                            node.parent == node.parent.parent.right_child):
                        d = node.parent.parent.left_child
                        if d is not None and d.color == 'red':
                            node.parent.color = 'black'
                            if node.parent.parent != self.root:
                                node.parent.parent.color = 'red'
                                self.flip_count += 1
                            d.color = 'black'
                            self.flip_count += 2
                            node = node.parent.parent
                        else:
                            if node.parent.right_child == node:
                                self.rr_rotation(node.parent.parent)
                                self.flip_count += 2
                            else:
                                self.rl_rotation(node.parent.parent)
                                self.flip_count += 2
                    if node == self.root:
                        break
                if self.root.color == 'red':
                    self.root.color = 'black'
                    # self.flip_count += 1

    def delete_fix(self, y, py=None):
        # if node_to_fix is None:   # node_to_fix is external node
        # else:
        if y.parent is None: # parent of y is None => y has become root of tree, so set color of y to black and return
            self.root = y
            self.root.color = 'black'
            return
        if y is None and py is not None:  # py is passed only when y is external node


        elif y.color == 'red': # y is red node => making it black
            y.color = 'black'
            self.flip_count += 1
            return
        else:  # y is black node, checking different cases
            py = y.parent
            if py.right_child == y: #R
                v = py.left_child
                if (v is not None and v.color == 'black'): #Rb
                    if ( ((v.left_child is None) or (v.left_child is not None and v.left_child.color == 'black')) and
                            ((v.right_child is None) or (v.right_child is not None and v.right_child.color == 'black'))): #Rb0
                        if py.color == 'black': #Rb0, py is black
                            v.color = 'red'
                            self.flip_count += 1
                            self.delete_fix(y=py)
                        else:  #Rb0, py is red
                            py.color = 'black'
                            v.color = 'red'
                            self.flip_count += 2
                            return
                    elif (v.left_child is not None and v.left_child.color == 'red') and (
                            (v.right_child is None) or (v.right_child is not None and v.right_child.color == 'black')): #Rb1 Case1 v.left is red
                        v.left_child.color = 'red'
                        self.flip_count += 1
                        b = v.right_child
                        ppy = py.parent
                        py.left_child = b
                        v.right_child = py
                        if b is not None:
                            b.parent = py
                        py.parent = v
                        v.parent = ppy
                        if ppy is not None:
                            if ppy.left_child == py:
                                ppy.left_child = v
                            else:
                                ppy.right_child = v
                        else:
                            self.root = v
                        return
                    elif ((v.right_child is not None and v.right_child.color == 'red') and (
                            (v.left_child is None) or (v.left_child is not None and v.left_child.color == 'black'))\
                            or ((v.left_child is not None and v.left_child.color == 'red')) and (
                            v.right_child is not None and v.right_child.color == 'red')):  #Rb1 Case2 v.right is red or # Rb2 v.left, v.right are red:
                        w = v.right_child
                        w.color = 'black'
                        self.flip_count += 1
                        b = w.left_child
                        c = w.right_child
                        ppy = py.parent
                        v.right_child = b
                        w.left_child = v
                        py.left_child = c
                        w.right_child = py
                        if b is not None:
                            b.parent = v
                        v.parent = w
                        if c is not None:
                            c.parent = py
                        py.parent = w
                        w.parent = ppy
                        if ppy is not None:
                            if ppy.left_child == py:
                                ppy.left_child = w
                            else:
                                ppy.right_child = w
                        else:
                            self.root = w
                        return
                elif (v is not None and v.color == 'red'): #Rr
                    



    def delete_node(self, node):
        node_to_delete = self.search_node(node)
        if node_to_delete is None:
            return None
        elif node_to_delete == self.root:
            self.root = None
            return node_to_delete
        else:
            if node_to_delete.left_child is None and node_to_delete.right_child is None:
                if node_to_delete.parent.left_child == node_to_delete:
                    node_to_delete.parent.left_child = None
                else:
                    node_to_delete.parent.right_child = None
                if node_to_delete.color == 'red':
                    return node_to_delete
                else:
                    self.delete_fix(None, py=node_to_delete.parent)
            elif node_to_delete.left_child is not None and node_to_delete.right_child is None:
                if node_to_delete.parent.left_child == node_to_delete:
                    node_to_delete.parent.left_child = node_to_delete.left_child
                else:
                    node_to_delete.parent.right_child = node_to_delete.left_child
                node_to_delete.left_child.parent = node_to_delete.parent
                self.delete_fix(node_to_delete.left_child)
            elif node_to_delete.left_child is not None and node_to_delete.ri

        return

    def PrintBook(self, book_id):
        found_node = self.search_node(book_id)
        if found_node is not None:
            reservations = []
            found_node.val.reservation_heap.fetch_all_reservations(0, reservations)
            # print(
            #     """BookID = {}\nTitle = "{}"\nAuthor = "{}"\nAvailability = "{}"\nBorrowedBy = {}\nReservations = {}\n""".format(
            #         found_node.val.book_id, found_node.val.book_name, found_node.val.author_name,
            #         found_node.val.availability_status,
            #         found_node.val.borrowed_by if found_node.val.borrowed_by is not None else "None", reservations))
            # print("BookID = {}".format(found_node.val.book_id))
            # print("Title = {}".format(found_node.val.book_name))
            # print("Author = {}".format(found_node.val.author_name))
            # print("Availability = {}".format(found_node.val.availability_status))
            return """BookID = {}\nTitle = "{}"\nAuthor = "{}"\nAvailability = "{}"\nBorrowedBy = {}\nReservations = {}\n""".format(
                    found_node.val.book_id, found_node.val.book_name, found_node.val.author_name,
                    found_node.val.availability_status,
                    found_node.val.borrowed_by if found_node.val.borrowed_by is not None else "None", reservations)
        else:
            print("Book {} not found in the Library\n".format(book_id))
            return "Book {} not found in the Library\n".format(book_id)

    def PrintBooks(self, book_id_one, book_id_two):
        books = []
        self.search_nodes(self.root, book_id_one, book_id_two, books)
        result = []
        for book in books:
            reservations = []
            book.val.reservation_heap.fetch_all_reservations(0, reservations)
            result.append("""BookID = {}\nTitle = "{}"\nAuthor = "{}"\nAvailability = "{}"\nBorrowedBy = {}\nReservations = {}\n""".format(
                    book.val.book_id, book.val.book_name, book.val.author_name,
                    book.val.availability_status,
                    book.val.borrowed_by if book.val.borrowed_by is not None else "None", reservations))
        return "\n".join(result)

    def InsertBook(self, book_id, book_name, author_name, availability_status):
        new_book = Book(book_id, book_name, author_name, availability_status)
        new_node = RedBlackNode(new_book)
        self.insert_node(new_node)

    def DeleteBook(self, bookID):
        return


    def BorrowBook(self, patron_id, book_id, patron_priority):
        book = self.search_node(book_id)
        if book is not None:
            if book.val.availability_status == 'Yes':
                book.val.availability_status = 'No'
                book.val.borrowed_by = patron_id
                print("Book {0} Borrowed by Patron {1}\n".format(book_id, patron_id))
                return "Book {0} Borrowed by Patron {1}\n".format(book_id, patron_id)
            else:
                reservation = Reservation(patron_id, patron_priority, datetime.now())
                book.val.reservation_heap.insert_reservation(reservation)
                print("Book {0} Reserved by Patron {1}\n".format(book_id, patron_id))
                return "Book {0} Reserved by Patron {1}\n".format(book_id, patron_id)

    def ReturnBook(self, patron_id, book_id):
        book = self.search_node(book_id)
        result = "Book {0} Returned by Patron {1}\n".format(book_id, patron_id)
        if book is not None:
            next_reserved = book.val.reservation_heap.fetch_min()
            if next_reserved is not None:
                next_reserved = book.val.reservation_heap.remove_reservation()
                book.val.borrowed_by = next_reserved.patron_id
                book.val.availability_status = 'No'
                result += "\nBook {0} Allotted to Patron {1}\n".format(book_id, next_reserved.patron_id)
            else:
                book.val.borrowed_by = None
                book.val.availability_status = 'Yes'
        return result

    def Quit(self):
        return "Program Terminated!!"

    def delete_book(self, book_id):
        return

    def FindClosestBook(self, target_id):
        closest_books = []
        least_difference = self.root.val.book_id
        least_difference, closest_books = self.find_closest_book(self.root, target_id, least_difference, closest_books)
        result = []
        for book in closest_books:
            reservations = []
            book.val.reservation_heap.fetch_all_reservations(0, reservations)
            result.append(
                """BookID = {}\nTitle = "{}"\nAuthor = "{}"\nAvailability = "{}"\nBorrowedBy = {}\nReservations = {}\n""".format(
                    book.val.book_id, book.val.book_name, book.val.author_name,
                    book.val.availability_status,
                    book.val.borrowed_by if book.val.borrowed_by is not None else "None", reservations))
        return "\n".join(result)

    def ColorFlipCount(self):
        return "Colour Flip Count: {}".format(str(self.flip_count))

    def _print_tree(self, root, level=0, prefix="Root: "):
        if root is not None:
            print(" " * (level * 4) + prefix + root.color + str(root.val.__dict__))
            if root.left_child is not None or root.right_child is not None:
                self._print_tree(root.left_child, level + 1, "L--- ")
                self._print_tree(root.right_child, level + 1, "R--- ")


if __name__ == '__main__':
    rbtree = RedBlackTree()
    book1 = Book(1, "Book1", "Author1", "Yes")
    book2 = Book(2, "Book2", "Author2", "Yes")
    book3 = Book(3, "Book3", "Author3", "Yes")
    book4 = Book(4, "Book4", "Author4", "Yes")
    book5 = Book(5, "Book5", "Author5", "Yes")
    book6 = Book(6, "Book4", "Author4", "Yes")
    book7 = Book(7, "Book5", "Author5", "Yes")
    book8 = Book(8, "Book4", "Author4", "Yes")
    book9 = Book(9, "Book5", "Author5", "Yes")
    book10 = Book(10, "Book4", "Author4", "Yes")
    node1 = RedBlackNode(book1)
    node2 = RedBlackNode(book2)
    node3 = RedBlackNode(book3)
    node4 = RedBlackNode(book4)
    node5 = RedBlackNode(book5)
    node6 = RedBlackNode(book6)
    node7 = RedBlackNode(book7)
    node8 = RedBlackNode(book8)
    node9 = RedBlackNode(book9)
    node10 = RedBlackNode(book10)

    # rbtree.insert_node(node3)
    # rbtree.insert_node(node1)
    # rbtree.insert_node(node2)
    # rbtree.insert_node(node5)
    # rbtree.insert_node(node4)
    # rbtree.insert_node(node7)
    # rbtree.insert_node(node8)
    # rbtree.insert_node(node9)
    # rbtree.insert_node(node10)
    # rbtree.insert_node(node6)
    # rbtree.insert_node(node4)

    rbtree.InsertBook(1, "Book1", "Author1", "Yes")
    rbtree.InsertBook(2, "Book2", "Author2", "Yes")
    rbtree.InsertBook(3, "Book3", "Author3", "Yes")
    rbtree.InsertBook(4, "Book4", "Author4", "Yes")
    rbtree.PrintBook(1)
    rbtree.BorrowBook(101, 1, 1)
    # rbtree._print_tree(rbtree.root)
    rbtree.PrintBook(1)
    rbtree.BorrowBook(102, 1, 2)
    rbtree.PrintBook(1)
    # x = rbtree.search_node(3)
    # print(x.val.__dict__)
    # if rbtree.root.right_child == rbtree.root.right_child.right_child.parent:
    #     print("Equal")
    # print(rbtree.root.right_child.right_child.parent.val.book_id)
