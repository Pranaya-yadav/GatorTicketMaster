"""
GatorTicketMaster - A Seat Reservation System

This program implements a ticket booking system using the following data structures:
1. Red-Black Tree: For managing seat reservations with O(log n) operations
2. Binary Min-Heap: For managing the waitlist with priority-based ordering
3. Binary Min-Heap: For managing available seats with lowest-number-first allocation

Key Features:
- Priority-based seat allocation for waitlisted users
- Efficient seat management and reservation tracking
- Support for cancellations and priority updates
- Range-based seat release operations
"""

import sys
import re


class Color:
    """
    Enum class for Red-Black Tree node colors.
    Used to maintain Red-Black Tree properties for balanced operations.
    """

    RED = 1
    BLACK = 2


class RBNode:
    """
    Node class for Red-Black Tree implementation.

    Attributes:
        user_id: Unique identifier for the user (acts as key)
        seat_id: Unique identifier for the seat (value)
        parent: Reference to parent node
        left: Reference to left child
        right: Reference to right child
        color: Color of the node (RED or BLACK)
    """

    def __init__(self, user_id, seat_id):
        self.user_id = user_id  # Key
        self.seat_id = seat_id  # Value
        self.parent = None
        self.left = None
        self.right = None
        self.color = Color.RED


class RedBlackTree:
    """
    Red-Black Tree implementation for managing seat reservations.
    Ensures O(log n) complexity for insert, delete, and search operations.

    Properties maintained:
    1. Root is always black
    2. No red node has a red child
    3. Every path from root to leaf has same number of black nodes
    4. New insertions are always red
    """

    def __init__(self):
        self.NIL = RBNode(None, None)
        self.NIL.color = Color.BLACK
        self.root = self.NIL

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert_fixup(self, z):
        while z.parent.color == Color.RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.left_rotate(z.parent.parent)
            if z == self.root:
                break
        self.root.color = Color.BLACK

    def insert(self, user_id, seat_id):
        z = RBNode(user_id, seat_id)
        y = self.NIL
        x = self.root

        while x != self.NIL:
            y = x
            if z.user_id < x.user_id:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.user_id < y.user_id:
            y.left = z
        else:
            y.right = z

        z.left = self.NIL
        z.right = self.NIL
        z.color = Color.RED
        self.insert_fixup(z)

    def inorder_traversal(self, node, result):
        """Helper method for sorted traversal"""
        if node != self.NIL:
            self.inorder_traversal(node.left, result)
            result.append((node.seat_id, node.user_id))
            self.inorder_traversal(node.right, result)

    def get_sorted_reservations(self):
        """Get reservations sorted by seat_id"""
        result = []
        self.inorder_traversal(self.root, result)
        return sorted(result, key=lambda x: x[0])

    def find_by_user_id(self, user_id):
        """Find a node by user_id"""
        current = self.root
        while current != self.NIL:
            if user_id == current.user_id:
                return current
            elif user_id < current.user_id:
                current = current.left
            else:
                current = current.right
        return None

    def find_by_seat_id(self, seat_id):
        """Find a node by seat_id using inorder traversal"""

        def search_seat(node):
            if node == self.NIL:
                return None
            left_result = search_seat(node.left)
            if left_result:
                return left_result
            if node.seat_id == seat_id:
                return node
            return search_seat(node.right)

        return search_seat(self.root)

    def delete_node(self, z):
        """Delete a node from the tree"""
        if not z:
            return

        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == Color.BLACK:
            self._delete_fixup(x)

    def _transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def _delete_fixup(self, x):
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right.color == Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = Color.BLACK


class MinHeapNode:
    """
    Node class for Binary Min-Heap implementation.
    Used in both waitlist and available seats management.

    Attributes:
        priority: User's priority level (negative for max-heap behavior)
        timestamp: Order of arrival for tie-breaking
        user_id: Unique identifier for the user
    """

    def __init__(self, priority, timestamp, user_id):
        self.priority = priority
        self.timestamp = timestamp
        self.user_id = user_id


class MinHeap:
    """
    Binary Min-Heap implementation for waitlist management.
    Provides O(log n) insert and extract-min operations.

    Features:
    - Priority-based ordering (higher priority numbers get preference)
    - FIFO ordering within same priority level using timestamps
    - Direct access to user positions for updates
    """

    def __init__(self):
        self.heap = []
        self.position = {}

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position[self.heap[i].user_id] = i
        self.position[self.heap[j].user_id] = j

    def compare(self, i, j):
        """Compare nodes based on priority first, then timestamp
        Returns True if node i should be above node j in the heap"""
        if self.heap[i].priority == self.heap[j].priority:
            return self.heap[i].timestamp < self.heap[j].timestamp
        return self.heap[i].priority < self.heap[j].priority

    def heapify_up(self, i):
        while i > 0:
            parent = self.parent(i)
            if self.compare(i, parent):
                self.swap(i, parent)
                i = parent
            else:
                break

    def heapify_down(self, i):
        min_idx = i
        n = len(self.heap)

        left = self.left_child(i)
        right = self.right_child(i)

        if left < n and self.compare(left, min_idx):
            min_idx = left

        if right < n and self.compare(right, min_idx):
            min_idx = right

        if min_idx != i:
            self.swap(i, min_idx)
            self.heapify_down(min_idx)

    def insert(self, priority, timestamp, user_id):
        node = MinHeapNode(priority, timestamp, user_id)
        self.heap.append(node)
        self.position[user_id] = len(self.heap) - 1
        self.heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None

        min_node = self.heap[0]
        last_node = self.heap.pop()

        if self.heap:
            self.heap[0] = last_node
            self.position[last_node.user_id] = 0
            self.heapify_down(0)

        del self.position[min_node.user_id]
        return min_node

    def remove_user(self, user_id):
        """Remove a user from the heap by their user_id"""
        if user_id not in self.position:
            return False

        # Get the index of the user to remove
        idx = self.position[user_id]

        # Replace with the last element
        last_node = self.heap.pop()
        if self.heap and idx < len(self.heap):
            self.heap[idx] = last_node
            self.position[last_node.user_id] = idx

            # Fix heap property
            parent = self.parent(idx)
            if parent >= 0 and self.compare(idx, parent):
                self.heapify_up(idx)
            else:
                self.heapify_down(idx)

        del self.position[user_id]
        return True


class AvailableSeatsHeap:
    """
    Special Min-Heap implementation for managing available seats.
    Ensures lowest-numbered seats are assigned first.

    Operations:
    - insert: Add newly available seat
    - extract_min: Get lowest numbered available seat
    - All operations maintain O(log n) complexity
    """

    def __init__(self):
        self.heap = []

    def insert(self, seat_id):
        self.heap.append(seat_id)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None

        min_val = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()

        if self.heap:
            self._heapify_down(0)

        return min_val

    def _heapify_up(self, i):
        parent = (i - 1) // 2
        if i > 0 and self.heap[i] < self.heap[parent]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            self._heapify_up(parent)

    def _heapify_down(self, i):
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)


class SeatReservationSystem:
    """
    Main system class that coordinates all seat reservation operations.

    Components:
    - Red-Black Tree for reserved seats
    - Min-Heap for waitlist
    - Min-Heap for available seats

    Key operations:
    1. Seat Reservation
    2. Cancellation
    3. Priority Updates
    4. Waitlist Management
    5. Bulk Seat Release
    """

    def __init__(self, output_file):
        self.reserved_seats = RedBlackTree()  # Red-Black Tree for seat reservations
        self.available_seats = AvailableSeatsHeap()  # Min-heap for available seats
        self.waitlist = MinHeap()  # Min-heap for waitlist
        self.total_seats = 0
        self.timestamp_counter = 0
        self.output_file = output_file

    def write_output(self, message):
        with open(self.output_file, "a") as f:
            f.write(message + "\n")

    def initialize(self, seat_count):
        self.total_seats = seat_count
        self.reserved_seats = RedBlackTree()
        self.available_seats = AvailableSeatsHeap()
        self.waitlist = MinHeap()

        # Initialize available seats
        for seat_id in range(1, seat_count + 1):
            self.available_seats.insert(seat_id)
        self.write_output(f"{seat_count} Seats are made available for reservation")

    def available(self):
        message = f"Total Seats Available : {len(self.available_seats.heap)}, Waitlist : {len(self.waitlist.heap)}"
        print(message)
        self.write_output(message)

    def reserve(self, user_id, user_priority):
        """
        Handles seat reservation requests.

        Flow:
        1. Try to get lowest numbered available seat
        2. If seat available: Assign to user in Red-Black Tree
        3. If no seat: Add to waitlist with priority and timestamp

        """

        next_seat = self.available_seats.extract_min()

        if next_seat is not None:
            self.reserved_seats.insert(user_id, next_seat)
            message = f"User {user_id} reserved seat {next_seat}"
            print(message)
            self.write_output(message)
        else:
            # Add to waitlist - lower priority number means higher priority
            self.timestamp_counter += 1
            self.waitlist.insert(-user_priority, self.timestamp_counter, user_id)
            message = f"User {user_id} is added to the waiting list"
            print(message)
            self.write_output(message)

    def cancel(self, seat_id, user_id):
        node = self.reserved_seats.find_by_seat_id(seat_id)

        if node and node.user_id == user_id:
            self.reserved_seats.delete_node(node)
            message = f"User {user_id} canceled their reservation"
            print(message)
            self.write_output(message)

            next_user = self.waitlist.extract_min()
            if next_user:
                # Assign to highest priority waiting user
                self.reserved_seats.insert(next_user.user_id, seat_id)
                message = f"User {next_user.user_id} reserved seat {seat_id}"
                print(message)
                self.write_output(message)
            else:
                self.available_seats.insert(seat_id)
        else:
            message = f"User {user_id} has no reservation for seat {seat_id} to cancel"
            print(message)
            self.write_output(message)

    def update_priority(self, user_id, new_priority):
        """
        Updates user's priority in waitlist.

        Flow:
        1. Find user in waitlist
        2. Remove from current position
        3. Reinsert with new priority but same timestamp
        4. Maintain heap properties

        """

        if user_id in self.waitlist.position:
            idx = self.waitlist.position[user_id]
            original_timestamp = self.waitlist.heap[idx].timestamp

            # Remove and reinsert with new priority
            self.waitlist.remove_user(user_id)
            self.waitlist.insert(-new_priority, original_timestamp, user_id)

            message = f"User {user_id} priority has been updated to {new_priority}"
            print(message)
            self.write_output(message)
        else:
            message = f"User {user_id} priority is not updated"
            print(message)
            self.write_output(message)

    def add_seats(self, count):
        message = f"Additional {count} Seats are made available for reservation"
        print(message)
        self.write_output(message)

        new_seat_start = self.total_seats + 1
        self.total_seats += count

        # Create list of new seats and sort them
        new_seats = sorted(range(new_seat_start, new_seat_start + count))

        # Assign seats to waiting users in priority order
        for seat in new_seats:
            next_user = self.waitlist.extract_min()
            if next_user:
                self.reserved_seats.insert(next_user.user_id, seat)
                message = f"User {next_user.user_id} reserved seat {seat}"
                print(message)
                self.write_output(message)
            else:
                self.available_seats.insert(seat)

    def exit_waitlist(self, user_id):
        """Remove a user from the waitlist if they are present."""
        # Try to remove user from waitlist
        if self.waitlist.remove_user(user_id):
            message = f"User {user_id} is removed from the waiting list"
            print(message)
            self.write_output(message)
        else:
            message = f"User {user_id} is not in waitlist"
            print(message)
            self.write_output(message)

    def print_reservations(self):
        reservations = self.reserved_seats.get_sorted_reservations()
        if reservations:
            for seat_id, user_id in reservations:
                message = f"Seat {seat_id}, User {user_id}"
                print(message)
                self.write_output(message)

    def release_seats(self, user_id1, user_id2):
        """
        Releases all seats for users in given ID range.

        Steps:
        1. Collect all seats to be released
        2. Remove users from both reserved seats and waitlist
        3. Reassign released seats to waiting users by priority
        4. Add remaining seats to available pool

        """

        released_seats = []
        # Get all reservations and sort by seat_id
        reservations = self.reserved_seats.get_sorted_reservations()

        # Collect seats to be released
        for seat_id, user_id in reservations:
            if user_id1 <= user_id <= user_id2:
                node = self.reserved_seats.find_by_user_id(user_id)
                if node:
                    self.reserved_seats.delete_node(node)
                    released_seats.append(seat_id)

        # Remove users from waitlist
        users_to_remove = []
        for node in self.waitlist.heap:
            if user_id1 <= node.user_id <= user_id2:
                users_to_remove.append(node.user_id)

        for user_id in users_to_remove:
            self.waitlist.remove_user(user_id)

        message = f"Reservations of the Users in the range [{user_id1}, {user_id2}] are released"
        print(message)
        self.write_output(message)

        # Reassign released seats in order
        for seat_id in sorted(released_seats):
            next_user = self.waitlist.extract_min()
            if next_user:
                self.reserved_seats.insert(next_user.user_id, seat_id)
                message = f"User {next_user.user_id} reserved seat {seat_id}"
                print(message)
                self.write_output(message)
            else:
                self.available_seats.insert(seat_id)


def main():
    """
    Main program entry point.

    Functions:
    1. Parses command-line arguments
    2. Reads input file
    3. Executes commands
    4. Handles output generation
    5. Manages error conditions

    Input Format: command(arg1, arg2, ...)
    Output: Written to inputfile_output_file.txt
    """

    if len(sys.argv) != 2:
        print("Usage: python gator_ticket_master.py <input_file>")
        return

    input_file = sys.argv[1]
    output_file_name = input_file.split(".")[0] + "_output_file.txt"

    try:
        with open(input_file, "r") as file:
            system = SeatReservationSystem(output_file_name)

            for line in file:
                line = line.strip()
                if not line:
                    continue

                match = re.match(r"(\w+)\((.*)\)", line)
                if match:
                    command = match.group(1)
                    args = [
                        arg.strip() for arg in match.group(2).split(",") if arg.strip()
                    ]

                    if command == "Initialize":
                        system.initialize(int(args[0]))
                    elif command == "Reserve":
                        system.reserve(int(args[0]), int(args[1]))
                    elif command == "Cancel":
                        system.cancel(int(args[0]), int(args[1]))
                    elif command == "ExitWaitlist":
                        system.exit_waitlist(int(args[0]))
                    elif command == "UpdatePriority":
                        system.update_priority(int(args[0]), int(args[1]))
                    elif command == "AddSeats":
                        system.add_seats(int(args[0]))
                    elif command == "Available":
                        system.available()
                    elif command == "PrintReservations":
                        system.print_reservations()
                    elif command == "ReleaseSeats":
                        system.release_seats(int(args[0]), int(args[1]))
                    elif command == "Quit":
                        print("Program Terminated!!")
                        system.write_output("Program Terminated!!")
                        break

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
