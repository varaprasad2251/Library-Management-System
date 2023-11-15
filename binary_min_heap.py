import datetime


class Reservation:
    def __init__(self, patron_id, priority_number, time_of_reservation):
        self.patron_id = patron_id
        self.priority_number = priority_number
        self.time_of_reservation = time_of_reservation


class ReservationHeap:
    def __init__(self):
        self.nodes = []

    def fetch_parent(self, child_index):
        # To fetch the parent index for a given child index
        if child_index % 2 == 0:
            parent = (child_index // 2) - 1
        else:
            parent = child_index // 2
        return parent

    def fetch_children(self, parent_index):
        # To fetch the children indexes for a given parent index
        left_child = 2 * parent_index + 1
        right_child = 2 * parent_index + 2
        # if left_child > len(self.nodes) - 1:
        #     return None, None
        # elif left_child == len(self.nodes) - 1:
        #     return left_child, None
        #     parent = child_index / 2
        return left_child, right_child

    def swap_nodes(self, index_one, index_two):
        # To swap two nodes in the ReservationHeap
        temp = self.nodes[index_one]
        self.nodes[index_one] = self.nodes[index_two]
        self.nodes[index_two] = temp

    def fetch_priority_child(self, left_child, right_child):
        if self.nodes[left_child].priority_number == self.nodes[right_child].priority_number:
            if self.nodes[left_child].time_of_reservation <= self.nodes[right_child].time_of_reservation:
                return left_child
            return right_child
        elif self.nodes[left_child].priority_number < self.nodes[right_child].priority_number:
            return left_child
        return right_child

    def insert_reservation(self, reservation):
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
        parent = 0
        remove_index = len(self.nodes) - 1
        self.swap_nodes(parent, remove_index)
        removed_reservation = self.nodes.pop(remove_index)
        left_child, right_child = self.fetch_children(parent)
        cnt = 0
        while left_child < len(self.nodes) and right_child < len(self.nodes):
            priority_child = self.fetch_priority_child(left_child, right_child)
            if self.nodes[parent].priority_number == self.nodes[priority_child].priority_number:
                if self.nodes[parent].time_of_reservation > self.nodes[priority_child].time_of_reservation:
                    self.swap_nodes(parent, priority_child)
                    parent = priority_child
                    left_child, right_child = self.fetch_children(parent)
                else:
                    print("Breaking at this step {}".format(cnt))
                    break
            elif self.nodes[parent].priority_number > self.nodes[priority_child].priority_number:
                self.swap_nodes(parent, priority_child)
                parent = priority_child
                left_child, right_child = self.fetch_children(parent)
            else:
                print("Breaking at this step {}".format(cnt))
                break
            cnt+=1
        return removed_reservation

def print_heap(heap_list):
    levels = []
    i = 0
    while 2 ** i - 1 < len(heap_list):
        level = heap_list[2 ** i - 1: 2 ** (i + 1) - 1]
        levels.append(level)
        i += 1

    for i, level in enumerate(levels):
        spaces = " " * (2 ** (len(levels) - i - 1) - 1)
        level1 = [x.__dict__ for x in level]
        print(spaces.join(map(str, level1)))

if __name__ == '__main__':
    res_heap = ReservationHeap()
    reservation1 = Reservation("C", 3, datetime.datetime.now())
    reservation2 = Reservation("B", 2, datetime.datetime.now())
    reservation3 = Reservation("A", 1, datetime.datetime.now())
    reservation4 = Reservation("D", 4, datetime.datetime.now())
    reservation5 = Reservation("E", 1, datetime.datetime.now())
    res_heap.insert_reservation(reservation1)
    res_heap.insert_reservation(reservation2)
    res_heap.insert_reservation(reservation3)
    res_heap.insert_reservation(reservation4)
    res_heap.insert_reservation(reservation5)
    x = res_heap.remove_reservation()
    # print([str(x.__dict__)+"\n" for x in res_heap.nodes])
    # for x in res_heap.nodes:
    print_heap(res_heap.nodes)
    print("")
    print(x.__dict__)
