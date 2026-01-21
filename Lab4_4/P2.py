# P2 Lab 4-4
from abc import ABC, abstractmethod

class Vehicle(ABC):
    """
    Abstract Base Class representing a generic vehicle.
    
    Attributes:
        make (str): Manufacturer of the vehicle.
        model (str): Model of the vehicle.
        year (int): Year of manufacture.
        is_running (bool): Engine status, default False.
    """

    def __init__(self, make: str, model: str, year: int, is_running = False):
      self.make = make
      self.model = model
      self.year = year
      self.is_running = is_running
    
    @abstractmethod
    def start_engine():
      "Returns Start the vehicle's engine."
      pass

    @abstractmethod
    def stop_engine():
      "Returns Stop the vehicle's engine."
      pass

    def get_info(self):
      "Return vehicle information."
      return f"{self.year}, {self.make}, {self.model}"

class CommercialVehicle():
    """
    Superclass for commercial vehicles.
    
    Attributes:
        license_number (str): Vehicle license plate.
        max_load (float): Maximum cargo capacity.
        current_load (float): Current cargo weight.
    """

    def __init__(self, license_number, max_load: float, current_load = 0):
        if not isinstance(license_number, str):
            raise ValueError("License number must be a string.")
        if max_load <= 0:
            raise ValueError("Max load must be positive.")
        if current_load < 0:
            raise ValueError("Current load can not be negative.")
        self.license_number = license_number
        self.max = max_load
        self.current_load = current_load

    def load_cargo(self, weight):
        """
        Load cargo if within capacity.
        To check if new weight not >= max_load 
        then plus new weight into current_load
        
        Args:
            weight (float): Cargo weight to load.
        Returns:
            bool: True if cargo loaded successfully, False otherwise.
        """
        if weight <= 0:
            raise ValueError("Weight must be positive.")
        if self.current_load + weight <= self.max:
          self.current_load += weight
          return True
        return False
    
    def unload_cargo(self, weight):
        """
        Unload cargo safely.
        To check if new weight >= current_load == reset current_load to 0
        
        Args:
            weight (float): Cargo weight to unload.
        Returns:
            float: Current load after unloading.
        """
        if weight <= 0:
            raise ValueError("Weight must be positive.")
        if weight >= self.current_load:
            self.current_load = 0
        else:
            self.current_load -= weight
        return self.current_load

class Car(Vehicle):
    """
    Car class inheriting from Vehicle.
    
    Attributes:
        num_doors (int): Number of doors.
    """

    def __init__(self, make: str, model: str, year: int, num_doors: int):
        super().__init__(make, model, year)
        if num_doors <= 0:
            raise ValueError("Number of doors must be positive.")
        self.num_doors = num_doors

    def start_engine(self):
        self.is_running = True
        return "Car engine started."

    def stop_engine(self):
        self.is_running = False
        return "Car engine stopped."


class Trailer(CommercialVehicle):
    """
    Trailer class inheriting from CommercialVehicle.
    
    Attributes:
        num_axles (int): Number of axles, default 2.
    """

    def __init__(self, license_number: str, max_load: float, num_axles: int = 2):
        super().__init__(license_number, max_load)
        if num_axles <= 0:
            raise ValueError("Number of axles must be positive.")
        self.num_axles = num_axles

    def get_weight_per_axle(self):
        """
        Return load per axle.
        
        Returns:
            float: Current load divided by number of axles.
        """
        if self.num_axles == 0:
            return 0
        return self.current_load / self.num_axles


class DeliveryVan(Car, CommercialVehicle):
    """
    DeliveryVan using multiple inheritance from Car and CommercialVehicle.
    
    Attributes:
        delivery_mode (bool): Delivery mode status.
    """
    def __init__(self, make: str, model: str, year: int, num_doors: int,
                 license_number: str, max_load: float):
        Car.__init__(self, make, model, year, num_doors)
        CommercialVehicle.__init__(self, license_number, max_load)
        self.delivery_mode = False

    def toggle_delivery_mode(self) -> str:
        "Switch delivery mode ON/OFF."
        self.delivery_mode = not self.delivery_mode
        return f"Delivery mode {'ON' if self.delivery_mode else 'OFF'}."

    def begin_service(self, cargo_weight: float):
        """
        Simulate a delivery service routine.
        
        Args:
            cargo_weight (float): Cargo weight to deliver.
        Returns:
            dict: Service routine results.
        """
        info = self.get_info()
        cargo_loaded = self.load_cargo(cargo_weight)
        start_msg = self.start_engine()
        mode_on = self.toggle_delivery_mode()
        stop_msg = self.stop_engine()
        self.unload_cargo(cargo_weight)
        mode_off = self.toggle_delivery_mode()

        return {
            "info": info,
            "cargo_loaded": cargo_loaded,
            "start": start_msg,
            "mode_on": mode_on,
            "stop": stop_msg,
            "mode_off": mode_off,
            "final_load": self.current_load
        }

if __name__ == "__main__":
    # Test Car
    car = Car("Toyota", "Corolla", 2020, 4)
    print(car.get_info())
    print(car.start_engine())
    print(car.stop_engine())
    print()

    # Test Trailer
    trailer = Trailer("ABC1221", 1000, 3)

    trailer.load_cargo(600)
    print("load cargo +600")
    print("Current load:", trailer.current_load)
    trailer.unload_cargo(200)
    print("unload cargo -200")
    print("Current load:", trailer.current_load)
    print("Weight per axle:", trailer.get_weight_per_axle())
    print(f"Axles: {trailer.num_axles}")

    # Test DeliveryVan
    van = DeliveryVan("Ford", "Transit", 2022, 4, "XYZ789", 2000)
    print()
    result = van.begin_service(500)
    for key, value in result.items():
        print(f"{key}: {value}")

    print(f"Doors: {van.num_doors}")
    print(f"License plate: {van.license_number}")
    print(f"Max load: {van.max}")
