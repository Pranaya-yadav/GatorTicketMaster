# GatorTicketMaster

## Overview
GatorTicketMaster is a Python-based seat reservation system with a priority waitlist. It enables users to reserve, cancel, and update their seat reservations while managing a priority queue for waitlisted users. If no seats are available, users are added to a waitlist and assigned seats based on their priority as they become available.

## Features
- **Initialize Seats**: Set up an initial number of available seats.
- **Reserve Seats**: Reserve a seat for a user, considering their priority level.
- **Cancel Reservations**: Cancel a user's reservation and reassign the seat to the next waitlisted user if available.
- **Priority Update**: Adjust the priority of a user in the waitlist.
- **Add Seats**: Increase the number of available seats and assign them to waitlisted users if needed.
- **Release Seats**: Release seats within a specified user ID range.
- **Print Reservations**: Display the current seat allocations and the waitlist status.

## Project Structure
- `gatorTicketMaster.py`: Main script that runs the seat reservation system, handling commands like initialization, reservation, cancellation, and waitlist management.
- `Reservation_controller.py`: Manages reservations and waitlists, ensuring users are assigned seats based on priority.
- `Binary_Min_Heap.py`: Implements a priority queue using a binary min-heap to manage waitlisted users.
- `Red_Black_Tree.py`: Implements a Red-Black Tree for efficiently storing and sorting reservations by user ID.
- `seat_allocation_manager.py`: Interface for managing seat reservations, cancellations, and updates.
- `seats.py`: Defines the `Seat` class, representing each seat with attributes like seat number and reservation status.
- `users.py`: Defines the `User` class with user ID and priority level, allowing updates and comparisons based on priority.

## Setup and Execution
### Running the System
To initialize and run the system with an input file, use the following command:
```sh
python3 gatorTicketMaster.py <input_file>
```

### Command Guide
- `Initialize(<seat_count>)`: Sets up the initial number of seats.
- `Reserve(<user_id>, <priority>)`: Attempts to reserve a seat for the user with the specified priority.
- `Cancel(<seat_id>, <user_id>)`: Cancels the reservation for the specified seat and user.
- `UpdatePriority(<user_id>, <new_priority>)`: Updates the waitlist priority for the specified user.
- `AddSeats()`: Adds more seats and assigns them to waitlisted users if available.
- `PrintReservations()`: Outputs the list of current reservations.
- `ReleaseSeats(<user_id_start>, <user_id_end>)`: Releases seats for users within the given ID range.
- `Quit()`: Terminates the program.

## Example
### Input file (`test5.txt`):
```
Initialize(5)
Available()
Reserve(1, 1)
Reserve(2, 1)
Cancel(1, 1)
Reserve(3, 1)
PrintReservations()
Quit()
```

### Expected Output (`test5_output_file.txt`):
```
5 Seats are made available for reservation
Total Seats Available : 5, Waitlist : 0
User 1 reserved seat 1
User 2 reserved seat 2
User 1 canceled their reservation
User 3 reserved seat 1
Seat 1, User 3
Seat 2, User 2
Program Terminated!!
```
