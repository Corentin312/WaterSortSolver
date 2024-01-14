import cv2
from tools import screenshot_path, capture_screenshot

def get_coordinates(image_path):
    image = cv2.imread(image_path)  
    coordinates_list = []
    scroll_position = [0]

    def on_mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            coordinates_list.append((x, y + scroll_position[0]))
            print(f"New point : {coordinates_list[-1]}")

    cv2.namedWindow('Image')
    cv2.createTrackbar('Scroll', 'Image', 0, image.shape[0], lambda x: None)
    cv2.setMouseCallback('Image', on_mouse_click)

    while True:
        scroll_position[0] = cv2.getTrackbarPos('Scroll', 'Image')
        cv2.imshow('Image', image[scroll_position[0]:, :])
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    return coordinates_list

if __name__ == "__main__":
    capture_screenshot(screenshot_path)
    print("Click on the image to get the coordinate of the point. Press q to exit")
    coordinates_list = get_coordinates(screenshot_path)
    print(f"Coordinates of selected point : {coordinates_list}")
