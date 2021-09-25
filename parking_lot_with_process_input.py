#import fileinput to get input as file
import fileinput
import sys
# it provide the data structure as priority queue return minimum value always.
import heapq
from collections import defaultdict, OrderedDict

#Creating the class car with parameteric constructor
class Car:
    def __init__(self, registration_number, driver_age):
        self.registration_number = registration_number
        self.driver_age = driver_age

#This the class that describe the all those facilty that available in car parking
class Parking_slot_facility:
    #constuctor 
    def __init__(self):
        self.regno_slot_map = dict()
        self.driver_age_registration_mapping = defaultdict(list)
        self.slot_car_mapping = OrderedDict()
        self.available_parking_lots = []

    #method for creating parking slot with given size in input
    def create_parking_lot(self, total_slots):
        print("Created a parking lot with {} slots".format(total_slots))
        for k in range(1, total_slots + 1):
            heapq.heappush(self.available_parking_lots, k)
        return True

    #methos to get nearest free slot for car parking
    def get_nearest_slot(self):
        return heapq.heappop(self.available_parking_lots) if self.available_parking_lots else None

    #Method call after any car leave the slot
    def leave(self, slot_to_be_freed):
        found = None
        for registration_no, slot in self.regno_slot_map.items():
            if slot == slot_to_be_freed:
                found = registration_no

         #Cleaning of all cache if any car leave the slot
        if found:
            heapq.heappush(self.available_parking_lots, slot_to_be_freed)
            del self.regno_slot_map[found]
            car_to_leave = self.slot_car_mapping[slot_to_be_freed]
            self.driver_age_registration_mapping[car_to_leave.driver_age].remove(found)
            del self.slot_car_mapping[slot_to_be_freed]
            print("Slot number "+str(slot_to_be_freed)+" vacated, the car with vehicle registration number "+'"'+registration_no+'"'+" left the space, the driver of the car was of age "+str(car_to_leave.driver_age))
            return True

        else:
            print("The slot is not in use")
            return False
    #method caal when new car came to parked assign the slot number to car
    def park(self, car):
        slot_no = self.get_nearest_slot()
        if slot_no is None:
            print("Parking has no enough space!, it is full")
            return

        self.slot_car_mapping[slot_no] = car
        self.regno_slot_map[car.registration_number] = slot_no
        self.driver_age_registration_mapping[car.driver_age].append(car.registration_number)
        print("Car with vehicle registration number "+'"'+car.registration_number+'"'+" has been parked at slot number "+str(slot_no))
        return slot_no

    #Method for geeting the regisraton numer of car accrding to age of driver
    def registration_numbers_for_cars_with_driver_age(self, driver_age):
        registration_numbers = self.driver_age_registration_mapping[driver_age]
        slots = [self.regno_slot_map[reg_no] for reg_no in registration_numbers]
        if(slots):
            print("Car with vehicle registration number "+'"'+''.join(registration_numbers)+'"'+''+" has been parked at slot number"+''.join((map(str,slots))))
        return self.driver_age_registration_mapping[driver_age]

    #Method to get the slot number with driver age
    def slot_numbers_for_cars_with_driver_age(self, driver_age):
        registration_numbers = self.driver_age_registration_mapping[driver_age]
        slots = [self.regno_slot_map[reg_no] for reg_no in registration_numbers]
        print(",".join(map(str,slots)))
        return slots

    #Method to get slot number of car according to regigration number
    def slot_number_for_registration_number(self, registration_number):
        slot_number = None
        if registration_number in self.regno_slot_map:
            slot_number = self.regno_slot_map[registration_number]
            print(slot_number)
            return slot_number
        else:
            print("Not found")
            return slot_number

#creating the instance of class Parking_slot_facilit
parking_lot = Parking_slot_facility()

# Define the method to process the command params
def process(command_params):
    c_with_param = command_params.strip().split(' ')
    command = c_with_param[0]
    #print(command)

    if command == 'Create_parking_lot':
        assert len(c_with_param) == 2, "create parking slot for car needs no of slots"
        assert c_with_param[1].isdigit() is True, "param should be 'integer type'"
        parking_lot.create_parking_lot(int(c_with_param[1]))

    elif command == 'Park':
        assert len(c_with_param) == 4, "park needs registration number and driver_age"
        assert c_with_param[3].isdigit() is True, "param should be 'integer type'"
        car = Car(c_with_param[1], int(c_with_param[3]))
        parking_lot.park(car)

    elif command == 'Leave':
        assert len(c_with_param) == 2, "leave needs slot number"
        assert c_with_param[1].isdigit() is True, "slot number should be 'integer type'"
        parking_lot.leave(int(c_with_param[1]))

    elif command == 'Vehicle_registration_number_for_driver_of_age':
        assert len(c_with_param) == 2, "registration_numbers_for_cars_with_driver_age"
        assert c_with_param[1].isdigit() is True, "param should be 'integer type'"
        parking_lot.registration_numbers_for_cars_with_driver_age(int(c_with_param[1]))

    elif command == 'Slot_numbers_for_driver_of_age':
        assert len(c_with_param) == 2, "Slote no whre car parked and driver age"
        assert c_with_param[1].isdigit() is True, "param should be 'integer type'"
        parking_lot.slot_numbers_for_cars_with_driver_age(int(c_with_param[1]))

    elif command == 'Slot_number_for_car_with_number':
        assert len(c_with_param) == 2, "Slot_number_for_car_wit_number need car reg number"
        parking_lot.slot_number_for_registration_number(c_with_param[1])

    elif command == 'exit':
        exit(0)
    else:
        raise Exception("Wrong command please try with another valid command")


if len(sys.argv) == 1:
    while True:
        line = input()
        process(line)

else:
    for line in fileinput.input():
        process(line)