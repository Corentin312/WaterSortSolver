from tools import screenshot_path, read_pixel_color, capture_screenshot
from coords import *

def get_color(nb_couleurs):
    color_coords2 = coords_dict[nb_couleurs][color_coords]
    i=0
    for tube_coords in color_coords2:
        print("Tube", i)
        j = 0
        for x, y in tube_coords:
            pixel_color = read_pixel_color(screenshot_path, x, y)
            print("Tube", i, "part", j, ":", pixel_color)
            j = j+1
        i = i+1

if __name__ == "__main__":
    nb_couleurs = int(input("How many colors ? "))
    capture_screenshot(screenshot_path)
    get_color(nb_couleurs)
    

