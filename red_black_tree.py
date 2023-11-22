from datetime import datetime
from binary_min_heap import Reservation, ReservationHeap


class Book:
    # To create a book object for given bookID, bookName, authorName, availabilityStatus
    def __init__(self, book_id, book_name, author_name, availability_status):
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.availability_status = availability_status
        self.borrowed_by = None
        self.reservation_heap = ReservationHeap()


class RedBlackNode:
    # To create a node in red black tree for a given book object, new node will always be created as red node
    def __init__(self, book):
        self.color = 'red'
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.val = book


class RedBlackTree:
    # To create a Red Black tree for managing books. Initially root will be empty.
    def __init__(self):
        self.root = None     # Root of the Red Black Tree
        self.flip_count = 0  # To keep track of color flips happening due to insert and delete operations.

    def search_node(self, book_id):
        # To search for a node with given bookID, returns node object if exists else None
        node = self.root
        if node is None:
            return None
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
        # To search for all nodes with bookID values between bookID1 and bookID2, appends all the nodes found to result.
        if node is None:
            return
        if book_id_one < node.val.book_id:
            self.search_nodes(node.left_child, book_id_one, book_id_two, result)
        if (node.val.book_id >= book_id_one) and (node.val.book_id <= book_id_two):
            result.append(node)
        if book_id_two > node.val.book_id:
            self.search_nodes(node.right_child, book_id_one, book_id_two, result)

    def find_closest_book(self, node, target_id, least_difference, closest_books):
        # To find nodes with closest bookID value to given targetID, appends all the closest book nodes to closest_books
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

    def ll_rotation(self, node, is_insert=True):
        # To perform LL rotation
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
        if is_insert:
            y.color = 'black'
            node.color = 'red'


    def rr_rotation(self, node, is_insert=True):
        # To perform RR rotation
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
        if is_insert:
            y.color = 'black'
            node.color = 'red'


    def lr_rotation(self, node):
        # To perform LR rotation
        self.rr_rotation(node.left_child)
        self.ll_rotation(node)

    def rl_rotation(self, node):
        # To perform RL rotation
        self.ll_rotation(node.right_child)
        self.rr_rotation(node)

    def insert_node(self, new_node):
        # Helper function to insert new_node into the red black tree. Called inside InsertBook() function.
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
                            self.update_color(node.parent, 'black')
                            if node.parent.parent != self.root:
                                self.update_color(node.parent.parent, 'red')
                            self.update_color(d, 'black')
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
                            self.update_color(node.parent, 'black')
                            if node.parent.parent != self.root:
                                self.update_color(node.parent.parent, 'red')
                            self.update_color(d, 'black')
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
                    self.update_color(self.root, 'black')

    def find_max_in_left_subtree(self, root):
        # Helper function - To find max bookID node in left subtree of given root.
        max_node = root.left_child
        node = max_node.right_child
        while node is not None:
            max_node = node
            node = node.right_child
        return max_node

    def swap_book_values(self, node1, node2):
        # To swap values of Book in two nodes.
        # color flip count is incremented if node that remains in the tree color changes
        temp = Book(node1.val.book_id, node1.val.book_name, node1.val.author_name, node1.val.availability_status)
        node1.val = node2.val
        node2.val = temp
        if node1.color != node2.color:
            self.flip_count += 1

    def update_color(self, node, new_color):
        # To update the color of a node based on its existing color.
        # If color changed, flip count is incremented. This applies to root node as well.
        if node is not None and node.color != new_color:
            node.color = new_color
            self.flip_count += 1

    def delete_fix(self, y, py=None):
        # To perform the fix after deleting a node. Checks the case and apply the transformations accordingly.
        if y is None and py is not None:  # py is passed only when y is external node. To eliminate case of y being None
            return
        if y.parent is None:  # parent of y is None => y has become root of tree, so set color of y to black and return
            self.root = y
            self.update_color(self.root, 'black')
            return
        py = y.parent
        if py.left_child == y:  # y is left child of py
            v = py.right_child
            if v is not None and v.color == 'red':  # if y sibling exists and is red
                self.rr_rotation(py, is_insert=False)
                self.update_color(v, 'black')
                self.update_color(py, 'red')
                self.delete_fix(y)
            elif v is not None and v.color == 'black':  # if y sibling exists and is black
                if ((v.left_child is None) or (v.left_child is not None and v.left_child.color == 'black')) and (
                            (v.right_child is None) or (v.right_child is not None and v.right_child.color == 'black')):
                    self.update_color(v, 'red')
                    if py.color == 'red':
                        self.update_color(py, 'black')
                    else:
                        self.delete_fix(py)
                else:
                    if v.right_child is None or (v.right_child is not None and v.right_child.color == 'black'):
                        # if right child of sibling is black
                        self.ll_rotation(v, is_insert=False)
                        self.update_color(v, 'red')
                        self.update_color(v.parent, 'black')
                        v = v.parent
                    self.rr_rotation(py, is_insert=False)
                    self.update_color(v, py.color)
                    self.update_color(py, 'black')
                    if v.right_child is not None:
                        self.update_color(v.right_child, 'black')
        elif py.right_child == y:  # y is right child of py
            v = py.left_child
            if v is not None and v.color == 'red':  # sibling of y exists and is red
                self.ll_rotation(py, is_insert=False)
                self.update_color(v, 'black')
                self.update_color(py, 'red')
                self.delete_fix(y)
            elif v is not None and v.color == 'black':  # sibling of y exists and is black
                if ((v.left_child is None) or (v.left_child is not None and v.left_child.color == 'black')) and (
                            (v.right_child is None) or (v.right_child is not None and v.right_child.color == 'black')):
                    # children of sibling are black
                    self.update_color(v, 'red')
                    if py.color == 'red':
                        self.update_color(py, 'black')
                    else:
                        self.delete_fix(py)
                else:
                    if v.left_child is None or (v.left_child is not None and v.left_child.color == 'black'):
                        # left child of sibling is black
                        self.rr_rotation(v, is_insert=False)
                        self.update_color(v, 'red')
                        self.update_color(v.parent, 'black')
                        v = v.parent
                    self.ll_rotation(py, is_insert=False)
                    v.color = py.color
                    self.update_color(py, 'black')
                    if v.left_child is not None:
                        self.update_color(v.left_child, 'black')

    def delete_leaf(self, node_to_delete):
        # To delete a leaf node or node with one child
        if node_to_delete.left_child is None and node_to_delete.right_child is None:
            if node_to_delete == self.root:
                self.root = None
            else:
                x = node_to_delete
                if node_to_delete.color == 'black':
                    self.delete_fix(x)
                if node_to_delete.parent.left_child == node_to_delete:
                    node_to_delete.parent.left_child = None
                else:
                    node_to_delete.parent.right_child = None
        elif (node_to_delete.left_child is not None and node_to_delete.left_child.color == 'red') and node_to_delete.right_child is None:
            if node_to_delete == self.root:
                self.root = node_to_delete.left_child
                node_to_delete.left_child.parent = node_to_delete.parent
                self.update_color(self.root, 'black')
            else:
                if node_to_delete.parent.left_child == node_to_delete:
                    node_to_delete.parent.left_child = node_to_delete.left_child
                else:
                    node_to_delete.parent.right_child = node_to_delete.left_child
                node_to_delete.left_child.parent = node_to_delete.parent
                if node_to_delete.left_child.color == 'red':
                    self.update_color(node_to_delete.left_child, 'black')
                else:
                    self.delete_fix(node_to_delete.left_child)
        elif (node_to_delete.right_child is not None and node_to_delete.righ_child.color == 'red') and node_to_delete.left_child is None:
            if node_to_delete == self.root:
                self.root = node_to_delete.right_child
                node_to_delete.right_child.parent = node_to_delete.parent
                self.update_color(self.root, 'black')
            else:
                if node_to_delete.parent.left_child == node_to_delete:
                    node_to_delete.parent.left_child = node_to_delete.right_child
                else:
                    node_to_delete.parent.right_child = node_to_delete.right_child
                node_to_delete.right_child.parent = node_to_delete.parent
                self.delete_fix(node_to_delete.right_child)
        return node_to_delete

    def delete_node(self, book_id):
        # To delete a node from redblack tree. Converts deleting a 2 children node to a leaf node deletion case.
        node_to_delete = self.search_node(book_id)
        if node_to_delete is None:
            return None
        else:
            if node_to_delete.left_child is not None and node_to_delete.right_child is not None:
                replacement_node = self.find_max_in_left_subtree(node_to_delete)
                self.swap_book_values(replacement_node, node_to_delete)
                node_to_delete = replacement_node
            x = self.delete_leaf(node_to_delete)
            return x

    def PrintBook(self, book_id):
        # To Print information about a specific book identified by its unique bookID.
        # Returns the string to be printed in output file.
        found_node = self.search_node(book_id)
        if found_node is not None:
            reservations = []
            found_node.val.reservation_heap.fetch_all_reservations(reservations)
            return """BookID = {}\nTitle = "{}"\nAuthor = "{}"\nAvailability = "{}"\nBorrowedBy = {}\nReservations = {}\n""".format(
                    found_node.val.book_id, found_node.val.book_name, found_node.val.author_name,
                    found_node.val.availability_status,
                    found_node.val.borrowed_by if found_node.val.borrowed_by is not None else "None", reservations)
        else:
            return "Book {} not found in the Library\n".format(book_id)

    def PrintBooks(self, book_id_one, book_id_two):
        # To Print information about all books with bookIDs in the range [bookID1, bookID2]
        # Returns the string to be printed in output file.
        books = []
        self.search_nodes(self.root, book_id_one, book_id_two, books)
        result = []
        for book in books:
            reservations = []
            book.val.reservation_heap.fetch_all_reservations(reservations)
            result.append("""BookID = {}\nTitle = "{}"\nAuthor = "{}"\nAvailability = "{}"\nBorrowedBy = {}\nReservations = {}\n""".format(
                    book.val.book_id, book.val.book_name, book.val.author_name,
                    book.val.availability_status,
                    book.val.borrowed_by if book.val.borrowed_by is not None else "None", reservations))
        return "\n".join(result)

    def InsertBook(self, book_id, book_name, author_name, availability_status):
        # To Add a new book to the library.
        new_book = Book(book_id, book_name, author_name, availability_status)
        new_node = RedBlackNode(new_book)
        self.insert_node(new_node)

    def BorrowBook(self, patron_id, book_id, patron_priority):
        # To Check Book availability status and allow patron to borrow or reserve the book
        # Returns the string to be printed in output file.
        book = self.search_node(book_id)
        if book is not None:
            if book.val.availability_status == 'Yes':
                book.val.availability_status = 'No'
                book.val.borrowed_by = patron_id
                return "Book {0} Borrowed by Patron {1}\n".format(book_id, patron_id)
            else:
                reservation = Reservation(patron_id, patron_priority, datetime.now())
                book.val.reservation_heap.insert_reservation(reservation)
                return "Book {0} Reserved by Patron {1}\n".format(book_id, patron_id)

    def ReturnBook(self, patron_id, book_id):
        # To Allow patron to return a book and reassign the book to prioritized patron in the reservation heap if any
        # Returns the string to be printed in output file.
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

    def DeleteBook(self, book_id):
        # To Delete the Book from red black tree
        # and notify patrons in the reservation list that the book is no longer available to borrow
        # Returns the string to be printed in output file.
        book = self.delete_node(book_id)
        if book is None:
            result = "Book {} is not found in Library\n".format(book_id)
        else:
            if book.val.reservation_heap.fetch_size() == 0:
                result = "Book {} is no longer available\n".format(book_id)
            elif book.val.reservation_heap.fetch_size() == 1:
                result = "Book {} is no longer available. Reservation made by Patron {} has been cancelled!\n".format(
                    book_id, str(book.val.reservation_heap.fetch_min().patron_id))
            else:
                reservations = []
                book.val.reservation_heap.fetch_all_reservations(reservations)
                result = "Book {} is no longer available. Reservations made by Patrons {} have been cancelled!\n".format(
                    book_id, ", ".join(map(str, reservations)))
        return result

    def FindClosestBook(self, target_id):
        # To Find the book with an ID closest to the given ID
        # Returns the string to be printed in output file.
        closest_books = []
        least_difference = self.root.val.book_id
        least_difference, closest_books = self.find_closest_book(self.root, target_id, least_difference, closest_books)
        result = []
        for book in closest_books:
            reservations = []
            book.val.reservation_heap.fetch_all_reservations(reservations)
            result.append(
                """BookID = {}\nTitle = "{}"\nAuthor = "{}"\nAvailability = "{}"\nBorrowedBy = {}\nReservations = {}\n""".format(
                    book.val.book_id, book.val.book_name, book.val.author_name,
                    book.val.availability_status,
                    book.val.borrowed_by if book.val.borrowed_by is not None else "None", reservations))
        return "\n".join(result)

    def ColorFlipCount(self):
        # Returns the string with color flip count to be printed in output file.
        return "Colour Flip Count: {}\n".format(str(self.flip_count))

    def Quit(self):
        # Returns the string to be printed when Quit() is called
        return "Program Terminated!!"
