import json

class Reading_json:
    __json_file = "data.json"
    __data = None

    @staticmethod
    def __read_json():
        """
        Reads JSON data from the file specified by __json_file and loads it into __data.
        """
        with open(Reading_json.__json_file, 'r') as file:
            Reading_json.__data = json.load(file)

    @staticmethod
    def initialize():
        """
        Initializes the Reading_json class by loading data from the JSON file into __data.
        """
        Reading_json.__read_json()

    @staticmethod
    def get_game_manager():
        """
        Retrieves game manager data from __data.

        Returns:
            dict: Dictionary containing game manager data.
        """
        return Reading_json.__data.get("Game_manager", {})

    @staticmethod
    def get_street():
        """
        Retrieves street data from __data.

        Returns:
            dict: Dictionary containing street data.
        """
        return Reading_json.__data.get("Street", {})

    @staticmethod
    def get_building():
        """
        Retrieves building data from __data.

        Returns:
            dict: Dictionary containing building data.
        """
        return Reading_json.__data.get("Building", {})

    @staticmethod
    def get_floor():
        """
        Retrieves floor data from __data.

        Returns:
            dict: Dictionary containing floor data.
        """
        return Reading_json.__data.get("Floor", {})

    @staticmethod
    def get_elevator():
        """
        Retrieves elevator data from __data.

        Returns:
            dict: Dictionary containing elevator data.
        """
        return Reading_json.__data.get("Elevator", {})
    
    @staticmethod
    def get_color(color_name):
        """
        Retrieves a specific color from the Colors data in __data.

        Args:
            color_name (str): The name of the color to retrieve.

        Returns:
            str: Hexadecimal color string or color name if not found.
        """
        colors = Reading_json.__data.get("Colors", {})
        return colors.get(color_name, color_name)
    
    @staticmethod
    def get_colors():
        """
        Retrieves all colors from the Colors data in __data.

        Returns:
            dict: Dictionary containing all colors.
        """
        return Reading_json.__data.get("Colors", {})

    @staticmethod
    def get_global_variables():
        """
        Retrieves all global variables from the Global_variables data in __data.

        Returns:
            dict: Dictionary containing all global variables.
        """
        return Reading_json.__data.get("Global_variables", {})
    
    @staticmethod
    def get_global_variable(var):
        """
        Retrieves a specific global variable from the Global_variables data in __data.

        Args:
            var (str): The name of the global variable to retrieve.

        Returns:
            str: Value of the global variable or variable name if not found.
        """
        variables = Reading_json.__data.get("Global_variables", {})
        return variables.get(var, var)

# Initialize Reading_json to load data from data.json
Reading_json.initialize()
