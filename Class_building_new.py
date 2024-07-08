import pygame


from Claas_floor_new import Floor
from claas_Elevator_new import Elevator
from Reading_json import Reading_json


FIXED_Y_AXIS = 1000 - Reading_json.get_global_variable("hight_floor")

date_building = Reading_json.get_building()

class Building:
    def __init__(self, floors_num, elevators_num, pos_x):
        """
        Initialize a Building instance.

        Args:
            floors_num (int): The number of floors in the building.
            elevators_num (int): The number of elevators in the building.
            pos_x (int): The x-coordinate of the building's position.
        """
        self.__floors_group = pygame.sprite.Group()
        self.__elevators_group = pygame.sprite.Group()
        self.create_floors(floors_num, pos_x, FIXED_Y_AXIS)
        self.create_elevators(elevators_num, pos_x + date_building["ele_x_axis"], date_building["ele_y_axis"])
        self.roof_pos = [(pos_x, 1000 - (35 * floors_num)),
                        (pos_x + 130, 1000 - (35 * floors_num)),
                        (pos_x + (135 // 2), 1000 - (35 * floors_num + 75))]

    def create_floors(self, floors_num, x, y):
        """
        Create the floors for the building.

        Args:
            floors_num (int): The number of floors to create.
            x (int): The starting x-coordinate for the floors.
            y (int): The starting y-coordinate for the floors.
        """
        for floor_num in range(floors_num):
            floor = Floor(floor_num, x, y)
            self.__floors_group.add(floor)
            y -= Reading_json.get_global_variable("hight_floor")

    def create_elevators(self, elevators_num, x, y):
        """
        Create the elevators for the building.

        Args:
            elevators_num (int): The number of elevators to create.
            x1 (int): The starting x-coordinate for the elevators.
            y1 (int): The starting y-coordinate for the elevators.
        """
        for elevator_num in range(elevators_num):
            elevator = Elevator(elevator_num, x, y)
            self.__elevators_group.add(elevator)
            x += Reading_json.get_global_variable("width_elevator")


    def draw(self, screen):
        """
        Draw the building, including floors, elevators, and roof, on the provided screen.

        Args:
            screen: The screen or surface where the building should be drawn.
        """
        for floor in self.__floors_group:
            floor.draw(screen)
        self.__elevators_group.draw(screen)
        pygame.draw.polygon(screen, Reading_json.get_color("red_roof"), self.roof_pos)

    def choose_elevator(self, floor: Floor):
        """
        Choose the best elevator for the given floor.

        Args:
            floor (Floor): The floor for which to choose an elevator.
        """
        num_floor = floor.get_id_floor()
        min_timer = float("inf")
        chosen_elevator = None
        for elevator in self.__elevators_group:
            timer = elevator.get_end_time_new_task(num_floor)
            if timer < min_timer:
                min_timer = timer
                chosen_elevator = elevator
        if chosen_elevator is not None:
            chosen_elevator.update_queue_task(num_floor, min_timer)
            floor.elevator_came_time = min_timer

    def update(self, time):
        """
        Update the state of the building, including floors and elevators.

        Args:
            time (float): The current time or the time elapsed since the last update.
        """
        self.__floors_group.update(time)
        self.__elevators_group.update(time, self.elevator_came, self.elevator_left)

    def mouse_pos(self, mouse_pos):
        """
        Handle mouse position interactions with floors.

        Args:
            mouse_pos (tuple): The current mouse position, typically a tuple (x, y).
        """
        id_floor = None
        for floor in self.__floors_group:
            id_floor = floor.button_clicked(mouse_pos)
            if id_floor is not None:
                self.choose_elevator(floor)
                break

    def elevator_came(self, id_floor):
        """
        Handle the event when an elevator arrives at a floor.

        Args:
            id_floor (int): The ID of the floor where the elevator has arrived.
        """
        for floor in self.__floors_group:
            if floor.get_id_floor() == id_floor:
                floor.elevator_came()

    def elevator_left(self, id_floor):
        """
        Handle the event when an elevator leaves a floor.

        Args:
            id_floor (int): The ID of the floor where the elevator has left.
        """
        for floor in self.__floors_group:
            if floor.get_id_floor() == id_floor:
                floor.elevator_left()
