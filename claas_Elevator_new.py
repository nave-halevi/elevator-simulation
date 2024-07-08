import pygame


from Reading_json import Reading_json


pygame.mixer.init()

data_Elevator = Reading_json.get_elevator()

pygame.mixer.music.load(data_Elevator["sound"])

class Elevator(pygame.sprite.Sprite):
    
    def __init__(self, id_elevator, x, y):
        """
        Initialize an Elevator instance.

        Args:
            id_elevator (int): The ID of the elevator.
            x (int): The x-coordinate of the elevator's starting position.
            y (int): The y-coordinate of the elevator's starting position.
        """
        super().__init__()
        self.__id_elevator = id_elevator
        
        self.__arr = []
        self._current_floor = 0
        self.__finishing_tasks = 0
        self._current_time = 0
        self.__elevator_in_motion = False
        
        self.image = pygame.image.load(data_Elevator["img_path"])
        
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.current_task = None
        self.__time_stop = -2

    def draw_elevator(self, screen):
        """
        Draw the elevator on the provided screen.

        Args:
            screen: The screen or surface where the elevator should be drawn.
        """
        pygame.draw.rect(screen, Reading_json.get_color("white"), self.rect)
        screen.blit(self.image , self.rect)

    def get_end_time_new_task(self, floor):
        """
        Calculate the end time for a new task to reach a specific floor.

        Args:
            floor (int): The target floor.

        Returns:
            float: The calculated end time to reach the floor.
        """
        last_floor = self.__arr[-1] if self.__arr else self._current_floor
        time = max(self._current_time, self.__finishing_tasks)
        return abs(last_floor - floor) / 2 + time + data_Elevator["time_wait"]

    def update_queue_task(self, floor, time):
        """
        Update the task queue with a new task.

        Args:
            floor (int): The target floor to be added to the task queue.
            time (float): The time associated with the task.
        """
        self.__finishing_tasks = time
        self.__arr.append(floor)

    def update(self, time, ele_is_come, elevator_leaving):
        """
        Update the state of the elevator.

        Args:
            time (float): The current time or the time elapsed since the last update.
            ele_is_come (function): A callback function to indicate the elevator has arrived at a floor.
            elevator_leaving (function): A callback function to indicate the elevator is leaving a floor.
        """
        self._current_time = time

        # Case 1: Elevator is not in motion
        if not self.__elevator_in_motion:
            ele_is_come(self._current_floor)

        # Case 2: Elevator has tasks in queue and it's time to move
        if len(self.__arr) > 0 and self.__time_stop + data_Elevator["time_wait"] < time:
            if not self.__elevator_in_motion:
                elevator_leaving(self._current_floor)
            self.__elevator_in_motion = True
            target_y = Reading_json.get_global_variable("screen_height") - (self.__arr[0] * Reading_json.get_global_variable("hight_floor"))
            start_y = Reading_json.get_global_variable("screen_height") - (self._current_floor * Reading_json.get_global_variable("hight_floor"))
            total_distance = (time - self.__last_update_time) * data_Elevator["speed"]


            # Moving the elevator towards the target floor
            if self.rect.bottom < target_y:
                self.rect.bottom = min(start_y + total_distance, target_y)
            elif self.rect.bottom > target_y:
                self.rect.bottom = max(start_y - total_distance, target_y)
            else:
                # Elevator has reached the target floor
                self.handle_floor_reached(ele_is_come, time)

        # Case 3: No tasks or not yet time to move
        else:
            self.__last_update_time = time

    def handle_floor_reached(self, ele_is_cum, time):
        """
        Handle the event when the elevator reaches a target floor.

        Args:
            ele_is_cum (function): A callback function to indicate the elevator has arrived at a floor.
            time (float): The current time or the time elapsed since the last update.
        """
        self._current_floor = self.__arr[0]
        ele_is_cum(self.__arr.pop(0))
        self.__elevator_in_motion = False
        self.__time_stop = time
        self.__last_update_time = time
        pygame.mixer.music.play()
