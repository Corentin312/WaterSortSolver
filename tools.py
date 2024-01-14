import subprocess
import cv2
import numpy as np
import time
from color import colors_dict
from coords import *

screenshot_path = "files/screenshot.png"
handle_screenshot_path = "files/handle_screenshot.png"
solution_path = "files/solution.txt"

TUBE_SIZE = 4

def capture_screenshot(output_path):
    try:
        subprocess.run(["adb", "shell", "screencap", "/sdcard/screenshot.png"])
        subprocess.run(["adb", "pull", "/sdcard/screenshot.png", output_path])
    except Exception as e:
        print(f"Erreur lors de la capture d'écran : {e}")


def read_pixel_color(image_path, x, y):
    image = cv2.imread(image_path)
    if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
        color_bgr = image[y, x]
        return color_bgr
    else:
        print("Coordonnées en dehors des dimensions de l'image.")
        return None

def get_closest_color(rgb_value, known_colors, tolerance=50):
    target_color = np.array(rgb_value)
    color_distances = [np.linalg.norm(target_color - np.array(known_colors[key])) for key in known_colors]
    closest_color_key = min(known_colors, key=lambda key: color_distances[key - 1])

    if color_distances[closest_color_key - 1] > tolerance:
        return None

    return closest_color_key

def read_color(coordinates_list, empty_tube, nb_couleurs):
    position = []
    color_tube = [-1] * TUBE_SIZE
    for tube in coordinates_list:     
        for i in range(TUBE_SIZE):
            x, y = tube[i]
            pixel_color = read_pixel_color(screenshot_path, x, y)
            color_number = get_closest_color(pixel_color, colors_dict)
            if color_number is None or color_number > nb_couleurs:
                color_number = -1
            color_tube[i] = color_number
        position.append(tuple(color_tube))
    position = position + ([(0, 0, 0, 0)] * empty_tube)
    return position

def adb_click(x, y):
    try:
        adb_command = f"adb shell input tap {x} {y}"
        subprocess.run(adb_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during the execution of the ADB command : {e}")

def solving_path(path, tube_coords):
    for input, output in path:
        x_i, y_i = tube_coords[input]
        adb_click(x_i, y_i)
        time.sleep(0.5)
        x_o, y_o = tube_coords[output]
        adb_click(x_o, y_o)
        time.sleep(0.5)

def handle_exception(initial_position, nb_couleurs, error_path, tube_number, unknown_position, tolerance = 50):
    position = initial_position.copy()
    solving_path(error_path, coords_dict[nb_couleurs][tube_coords])
    time.sleep(2.5)
    capture_screenshot(handle_screenshot_path)
    x, y = coords_dict[nb_couleurs][color_coords][tube_number][unknown_position]
    color_rgb = read_pixel_color(handle_screenshot_path, x, y)
    color_number = get_closest_color(color_rgb, colors_dict)
    if color_number is None or color_number > nb_couleurs:
        print("Color", color_rgb, "still not known, check file", handle_screenshot_path, "tube", tube_number)
        exit(0)
    else:
        tube_i = list(position[tube_number])
        continuing = True
        k = unknown_position + 1
        tube_i[unknown_position] = color_number
        while continuing and k < TUBE_SIZE:
            x2, y2 = coords_dict[nb_couleurs][color_coords][tube_number][k]
            color_rgb2 = read_pixel_color(handle_screenshot_path, x2, y2)
            if np.linalg.norm(np.array(color_rgb) - np.array(color_rgb2)) <= tolerance:
                tube_i[k] = color_number
                k = k+1
            else:
                continuing = False
        
        position[tube_number] = tuple(tube_i)
        print("Initial position updated")
    return position

def reset():
    x, y = restart_button_coordinates
    adb_click(x, y)
    time.sleep(3)