# room.py
# P1 Lab 4-4

from abc import ABC, abstractmethod

# Abstract class
class Room(ABC):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    @abstractmethod
    def get_purpose(self):
        """Returns a string describing purposes of the room"""
        pass

    @abstractmethod
    def get_recommended_lighting(self):
        """Returns recommended lighting in lumens per square foot"""
        pass
    
    # concrete method
    def calculate_area(self):
        return self.length * self.width

    def describe_room(self):
        area = self.calculate_area()
        return f"A {self.__class__.__name__} of {area} sq ft used for {self.get_purpose()}"


# Concrete class that inherits from abstract class
class Bedroom(Room):
    def __init__(self, length, width, bed_size):
        super().__init__(length, width)
        self.bed_size = bed_size

        # if bed_size < 3.5:
        #     raise ValueError("Bed size cannot less than 3.5 ft.")
        # elif bed_size != 3.5:
        #     raise ValueError("This Bed size not in choice.")
        # elif bed_size != 5:
        #     raise ValueError("This Bed size not in choice.")
        # elif bed_size != 6:
        #     raise ValueError("This Bed size not in choice.")


    def get_purpose(self):
        return f"take a rest and sleep with a cozy {self.bed_size} ft bed"

    def get_recommended_lighting(self):
        # Bedrooms typically 10-20 lumens/sq ft and color temp 3000K to 4000K. 
        return 15


class Kitchen(Room):
    def __init__(self, length, width, has_island=True):
        super().__init__(length, width)
        self.has_island = has_island

    def get_purpose(self):
        return "cooking and food preparation"

    def get_recommended_lighting(self):
        # Kitchens typically need 30-40 lumens/sq ft and color temp 3000K to 5000K
        return 35

    def calculate_counter_space(self):
    # Google style
        """Calculates the total counter space both with island and without island.

        Args:
            area (float): The represent "calculate_area()" which is calculated length * width of the room.
            has_island (bool): To store whether the kitchen has an island with the default value = True.
            island_area (float): The value of island counter area.
            wall_area (float): The value of wall counter area.

        Returns:
            float: The value of island counter area after applying the calulation formula.
            float: The value of wall counter area after applying the calulation formula.

        Examples:
            >>> calculate_counter_space(self)
            >>> New_kitchen = Kitchen(25, 20, has_island=True)
                
            (island, wall): 100.00, 125.00
        """
        area = self.calculate_area()
        if self.has_island:
            island_area = area * 0.2
            wall_area = area * 0.25
        else:
            island_area = 0
            wall_area = area * 0.5
        return island_area, wall_area