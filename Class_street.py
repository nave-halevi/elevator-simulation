from Class_building_new import Building
from Reading_json import Reading_json



data_street = Reading_json.get_street()

class Street():
    def __init__(self, buildings_param):
        """
        Initialize a Street instance.

        Args:
            buildings_param (list): A list of tuples where each tuple contains
                                    information about a building. Each tuple
                                    should have the format (building_type, height).
        """
        self.__buildings = []
        self.__creating_street(buildings_param)

    def __creating_street(self, buildings_param):
        """
        Private method to create a street with buildings.

        This method initializes buildings based on the parameters provided and
        positions them sequentially along the street. The position is calculated
        based on the height of each building to ensure appropriate spacing.

        Args:
            buildings_param (list): A list of tuples where each tuple contains
                                    information about a building. Each tuple
                                    should have the format (building_type, height).
        """
        pos_x = 0
        for building_param in buildings_param:
            self.__buildings.append(Building(building_param[0], building_param[1], pos_x)) 
            pos_x += Reading_json.get_global_variable("width_floor_with_line") + Reading_json.get_global_variable("width_elevator") * building_param[1] + data_street["padding_building"]

    def draw_buildings(self, screen):
        """
        Draw all buildings on the provided screen.

        Args:
            screen: The screen or surface where the buildings should be drawn.
        """
        for bul in self.__buildings:
            bul.draw(screen)

    def update_buildings(self, time):
        """
        Update the state of all buildings.

        This method should be called to update any dynamic properties of the
        buildings based on the elapsed time.

        Args:
            time: The current time or the time elapsed since the last update.
        """
        for bul in self.__buildings:
            bul.update(time)

    def mouse_pos(self, pos):
        """
        Handle mouse position interactions with buildings.

        This method is used to check and respond to the mouse position for
        interactions with the buildings.

        Args:
            pos: The current mouse position, typically a tuple (x, y).
        """
        for bul in self.__buildings:
            bul.mouse_pos(pos)
