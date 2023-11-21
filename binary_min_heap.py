class Reservation:
    # To create a reservation object for given patronID, priorityNumber and timeOfReservation
    def __init__(self, patron_id, priority_number, time_of_reservation):
        self.patron_id = patron_id
        self.priority_number = priority_number
        self.time_of_reservation = time_of_reservation


class ReservationHeap:
    # To create Priority Queue that store all the reservations. Each Book will have its own ReservationHeap
    def __init__(self):
        # Initializes an empty list to store reservations.
        self.nodes = []  # Stores all the reservations according to min heap property

    def fetch_min(self):
        # To fetch the first element in the ReservationHeap
        if len(self.nodes):
            return self.nodes[0]
        else:
            return None

    def fetch_size(self):
        # To fetch the number of reservations in the ReservationHeap
        return len(self.nodes)

    def fetch_parent(self, child_index):
        # To fetch the parent index for a given child index
        if child_index % 2 == 0:
            parent = (child_index // 2) - 1
        else:
            parent = child_index // 2
        return parent

    def fetch_children(self, parent_index):
        # To fetch the children indices for a given parent index
        left_child = 2 * parent_index + 1
        right_child = 2 * parent_index + 2
        return left_child, right_child

    def swap_nodes(self, index_one, index_two):
        # To swap two Reservations in the ReservationHeap
        temp = Reservation(self.nodes[index_two].patron_id, self.nodes[index_two].priority_number,
                           self.nodes[index_two].time_of_reservation)
        self.nodes[index_two] = self.nodes[index_one]
        self.nodes[index_one] = temp

    def fetch_priority_child(self, left_child, right_child):
        # To fetch the priority child among the given two children of a node
        if self.nodes[left_child].priority_number == self.nodes[right_child].priority_number:
            if self.nodes[left_child].time_of_reservation <= self.nodes[right_child].time_of_reservation:
                return left_child
            return right_child
        elif self.nodes[left_child].priority_number < self.nodes[right_child].priority_number:
            return left_child
        return right_child

    def fetch_all_reservations(self, all_reservations):
        # To fetch all the patronIDs from reservations in the order of their priority
        n = len(self.nodes)
        reservations = [self.nodes[i].patron_id for i in range(n)]
        all_reservations += reservations

    def insert_reservation(self, reservation):
        # To insert a new Reservation into the ReservationHeap
        new_index = len(self.nodes)
        self.nodes.append(reservation)
        if new_index != 0:
            child = new_index
            parent = self.fetch_parent(child)
            if parent == 0:
                if self.nodes[parent].priority_number == self.nodes[child].priority_number:
                    if self.nodes[parent].time_of_reservation > self.nodes[child].time_of_reservation:
                        self.swap_nodes(parent, child)
                elif self.nodes[parent].priority_number > self.nodes[child].priority_number:
                    self.swap_nodes(parent, child)
            else:
                while child != 0:
                    if self.nodes[parent].priority_number == self.nodes[child].priority_number:
                        if self.nodes[parent].time_of_reservation >= self.nodes[child].time_of_reservation:
                            self.swap_nodes(parent, child)
                    elif self.nodes[parent].priority_number > self.nodes[child].priority_number:
                        self.swap_nodes(parent, child)
                    child = parent
                    parent = self.fetch_parent(child)

    def remove_reservation(self):
        # To remove a Reservation from the ReservationHeap
        parent = 0
        remove_index = len(self.nodes) - 1
        self.swap_nodes(parent, remove_index)
        removed_reservation = self.nodes.pop(remove_index)
        left_child, right_child = self.fetch_children(parent)
        while left_child < len(self.nodes) and right_child < len(self.nodes):
            priority_child = self.fetch_priority_child(left_child, right_child)
            if self.nodes[parent].priority_number == self.nodes[priority_child].priority_number:
                if self.nodes[parent].time_of_reservation > self.nodes[priority_child].time_of_reservation:
                    self.swap_nodes(parent, priority_child)
                    parent = priority_child
                    left_child, right_child = self.fetch_children(parent)
                else:
                    break
            elif self.nodes[parent].priority_number > self.nodes[priority_child].priority_number:
                self.swap_nodes(parent, priority_child)
                parent = priority_child
                left_child, right_child = self.fetch_children(parent)
            else:
                break
        return removed_reservation
