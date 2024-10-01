import random
import matplotlib.pyplot as plt
from pynput.mouse import Listener

def generate_frame(num_objects=3):
    # Generate random coordinates for each object
    object_coords = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(num_objects)]
    return object_coords

def on_move(x, y):
    print('Mouse moved to ({0}, {1})'.format(x, y))

def onclick(event):
    global num_clicks, object_selected
    num_clicks += 1
    if num_clicks == 1:
        user_x = event.xdata
        user_y = event.ydata
        print("First click registered. Now click on an object.")
    elif num_clicks == 2:
        user_object_x = event.xdata
        user_object_y = event.ydata
        object_selected = check_object_selection(user_object_x, user_object_y)
    else:
        plt.close()
        return

def check_object_selection(user_x, user_y):
    for i, (object_x, object_y) in enumerate(object_coords):
        if (user_x >= object_x - rect_size/2 and user_x <= object_x + rect_size/2) and \
           (user_y >= object_y - rect_size/2 and user_y <= object_y + rect_size/2):
            return i
    return None

if __name__ == "__main__":
    object_to_select = "box"
    num_objects = 3
    object_coords = generate_frame(num_objects)
    num_clicks = 0
    object_selected = None
    
    # Display the frame
    fig, ax = plt.subplots()
    ax.set_title("Select an object in the frame")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Draw rectangles around the object areas
    rect_size = 0.1  # Adjust rectangle size as needed
    rects = []
    for object_x, object_y in object_coords:
        rect = plt.Rectangle((object_x - rect_size/2, object_y - rect_size/2), rect_size, rect_size, fill=False, edgecolor='red', linewidth=2)
        rects.append(rect)
        ax.add_patch(rect)
    
    # Capture the user's click event
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    # Capture mouse movements
    with Listener(on_move=on_move) as listener:
        plt.show()

    # Check if the selected object matches with any of the object coordinates
    if num_clicks == 3:
        if object_selected is not None:
            print(f"Congratulations! You are verified!!!")
        else:
            print("Sorry! Your selection did not match any object.")
