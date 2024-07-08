import pygame
from enum import Enum


from Reading_json import Reading_json


data_floor = Reading_json.get_floor()

class Floor(pygame.sprite.Sprite):
    
    class Status_elv(Enum):
        Elevator_not_on_floor = 1
        Elevator_in_way = 2
        Elevator_on_floor = 3

    def __init__(self, id_floor, x, y):
        """
        Initialize a Floor instance.

        Args:
            id_floor (int): The ID of the floor.
            x (int): The x-coordinate of the floor's position.
            y (int): The y-coordinate of the floor's position.
        """
        super().__init__()
        self.__id_floor = id_floor
        self.image = pygame.image.load(data_floor["img_path"])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.button_rect = pygame.Rect(data_floor["button_pos"])
        
        self.__floor_status = Floor.Status_elv.Elevator_not_on_floor
        
        self.elevator_came_time = 0
        self.display_time = ""
        self.x = x

    def draw_floor(self, screen):
        """
        Draw the floor on the provided screen.

        Args:
            screen: The screen or surface where the floor should be drawn.
        """
        pygame.draw.rect(screen, Reading_json.get_color("light_blue"), self.rect)
        screen.blit(self.image, self.rect)

    def draw_button(self, screen):
        """
        Draw the button for the floor on the provided screen.

        Args:
            screen: The screen or surface where the button should be drawn.
        """
        font = pygame.font.Font(None, data_floor["text_size"])
        text_surface = font.render(str(self.__id_floor), True, Reading_json.get_color("black"))
        self.button_rect.center = self.rect.center
        text_rect = text_surface.get_rect()
        text_rect.center = self.button_rect.center
        color = Reading_json.get_color("green") if self.__floor_status == Floor.Status_elv.Elevator_not_on_floor else Reading_json.get_color("light_blue")
        pygame.draw.rect(screen, color, self.button_rect)
        screen.blit(text_surface, text_rect)

    def draw_timer(self, screen):
        """
        Draw the timer for the floor on the provided screen.

        Args:
            screen: The screen or surface where the timer should be drawn.
        """
        font = pygame.font.Font(None, 22)
        text_surface = font.render(str(self.display_time), True, Reading_json.get_color("black"))
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        text_rect[0] = data_floor["timer_pos_y"] + self.x
        screen.blit(text_surface, text_rect)

    def draw_black_line(self, screen):
        """
        Draw the black line for the floor on the provided screen.

        Args:
            screen: The screen or surface where the black line should be drawn.
        """
        line_black = pygame.Rect(self.rect.x, self.rect.y, data_floor["line_width"], data_floor["line_height"])
        pygame.draw.rect(screen, Reading_json.get_color("black"), line_black)

    def draw(self, screen):
        """
        Draw the entire floor (including floor, button, timer, and black line) on the provided screen.

        Args:
            screen: The screen or surface where the floor should be drawn.
        """
        self.draw_floor(screen)
        self.draw_button(screen)
        self.draw_timer(screen)
        self.draw_black_line(screen)

    def button_clicked(self, mouse_pos):
        """
        Handle the event when the button is clicked.

        Args:
            mouse_pos: The current mouse position, typically a tuple (x, y).

        Returns:
            self: If the button is clicked and the floor status is 1 (clear), return the floor instance.
        """
        if self.button_rect.collidepoint(mouse_pos) and self.__floor_status == Floor.Status_elv.Elevator_not_on_floor:
            self.__floor_status = Floor.Status_elv.Elevator_in_way
            return self

    def elevator_came(self):
        """
        Set the floor status to indicate that the elevator has arrived.
        """
        self.__floor_status = Floor.Status_elv.Elevator_in_way

    def elevator_left(self):
        """
        Set the floor status to indicate that the elevator has left.
        """
        self.__floor_status = Floor.Status_elv.Elevator_not_on_floor

    def update(self, current_time):
        """
        Update the display time for the floor based on the current time.

        Args:
            current_time (float): The current time or the time elapsed since the last update.
        """
        time_until_arrival = self.elevator_came_time - current_time - data_floor["wait_time"]
        self.display_time = f"{time_until_arrival:.1f}" if time_until_arrival >= 0 else ""

        # self.display_time = f"{self.elevator_came_time - current_time:.1f}" if self.elevator_came_time - current_time >= 0 else ""

    def get_id_floor(self):
        """
        Get the ID of the floor.

        Returns:
            int: The ID of the floor.
        """
        return self.__id_floor
