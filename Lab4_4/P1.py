# P1.py
from room import Bedroom, Kitchen

def main():
    # Bedroom
    bedroom_1 = Bedroom(length=12, width=14, bed_size=3.5)
    print(bedroom_1.describe_room())
    print(f"Recommended lighting: {bedroom_1.get_recommended_lighting()} lumens/sq ft")
    print(f"Area: {bedroom_1.calculate_area()} sq ft\n")
    
    bedroom_2 = Bedroom(length=22, width=14, bed_size=6)
    print(bedroom_2.describe_room())
    print(f"Recommended lighting: {bedroom_2.get_recommended_lighting()} lumens/sq ft")
    print(f"Area: {bedroom_2.calculate_area()} sq ft\n")

    # Kitchen with island
    kitchen_is = Kitchen(length=20, width=12, has_island=True)
    print(kitchen_is.describe_room())
    print(f"Recommended lighting: {kitchen_is.get_recommended_lighting()} lumens/sq ft")
    print(f"Area: {kitchen_is.calculate_area()} sq ft")
    island, wall = kitchen_is.calculate_counter_space()
    print(f"Counter space (island, wall): {island:.2f}, {wall:.2f}\n")

    # Kitchen without island
    kitchen_nois = Kitchen(length=10, width=10, has_island=False)
    print(kitchen_nois.describe_room())
    print(f"Recommended lighting: { kitchen_nois.get_recommended_lighting()} lumens/sq ft")
    print(f"Area: { kitchen_nois.calculate_area()} sq ft")
    island, wall =  kitchen_nois.calculate_counter_space()
    print(f"Counter space (island, wall): {island:.2f}, {wall:.2f}")

if __name__ == "__main__":
    main()