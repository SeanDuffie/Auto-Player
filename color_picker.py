""" color_picker.py

    This script was initially made as a tool to help identify the RGB values of skin tones
    both in data that we collect and where they are closest to on the Monk Scale.

    For now it prompts the user to select an image, then you can select a pixel within the image
    to observe the color and where it lies on the RGB spectrum in relatin to the Monk Scale.

    If this is deemed useful enough, one day it can be used to automatically categorize images
    based on monk scale.

    NOTE: Most actual skin tone tends to have higher red values than the Monk Scale suggests.
"""
from tkinter import filedialog

import cv2
import numpy as np
from matplotlib import pyplot as plt

# RGB values for each skin tone on the Monk Scale spectrum
SKIN_RED = [0xf6, 0xf3, 0xf7, 0xea, 0xd7, 0xa0, 0x82, 0x60, 0x3a, 0x29]
SKIN_GREEN = [0xed, 0xe7, 0xea, 0xda, 0xbd, 0x7e, 0x5c, 0x41, 0x31, 0x24]
SKIN_BLUE = [0xe4, 0xdb, 0xd0, 0xba, 0x96, 0x56, 0x43, 0x34, 0x2a, 0x20]
SKIN_HEX = []
for i in range(len(SKIN_BLUE)):
    SKIN_HEX.append(f"#{SKIN_RED[i]:#x}{SKIN_GREEN[i]:#x}{SKIN_BLUE[i]:#x}".replace("0x", ""))

def mouseRGB(event,x,y,flags,param):
    """ Event handler for clicking on the image

    Args:
        event (_type_): opencv event object
        x (int): x coordinate of mouse event
        y (int): y coordinate of mouse event
        flags (_type_): event flags. Unused.
        param (tuple): tuple containing parameters passed during init
    """
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colorsB = big_image[y,x,0]
        colorsG = big_image[y,x,1]
        colorsR = big_image[y,x,2]
        colors = big_image[y,x]
        print("Red: ",colorsR)
        print("Green: ",colorsG)
        print("Blue: ",colorsB)
        print("BRG Format: ",colors)
        print(f"HEX Format: #{colorsB:02x}{colorsG:02x}{colorsR:02x}")
        new_img = np.full((500,500,3), colors, np.uint8)

        skin_graph_3d(param[0], param[1], colorsR, colorsG, colorsB)

        cv2.imshow("color", new_img)
        print("Coordinates of pixel: X: ",x,"Y: ",y)

def skin_graph_2d():
    """TODO: right now this code just generates a plot of RGB values on the monk scale
            In the future, this should work with the color picker to help identify skin tones
    """
    plt.plot(SKIN_BLUE, color="blue")
    plt.plot(SKIN_GREEN, color="green")
    plt.plot(SKIN_RED, color="red")

    plt.show()

def init_3d():
    """Generates initial 3D plot for Skin Tone spectrum on RGB spectrum
    
    TODO: Color gradient on skin tone line?

    Returns:
        tuple: a tuple pair of the newly generated figure and subplot objects
    """
    # Set up a Pyplot object for a dynamic 3D figure
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # Plot the 3D line for skin tone range
    ax.plot3D(SKIN_RED, SKIN_GREEN, SKIN_BLUE)#, color=SKIN_HEX)

    # Set Plot Labels
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')

    # Update dynamic plot for the first time
    fig.canvas.draw()
    fig.canvas.flush_events()

    return fig, ax

def skin_graph_3d(fig, ax, pr: int, pg: int, pb: int):
    """ Plots RGB value of the current color on a 3D plot, then updates the canvas

    Args:
        fig (_type_): figure to be drawn on
        ax (_type_): current subplot object
        pr (int): red pixel
        pg (int): green pixel
        pb (int): blue pixel

    Returns:
        _type_: updated subplot object
    """
    c = f"#{pr:#x}{pg:#x}{pb:#x}".replace("0x", "")
    ax.scatter(pr, pg, pb, marker="^", color=c)

    # Updates the dynamic matplotlib canvas
    fig.canvas.draw()
    fig.canvas.flush_events()

    return ax

if __name__ == "__main__":
    # Allows user to keep selecting new images until cancelled
    while True:
        # Read an image, a window and bind the function to window
        ref_name = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Images", "jpg"),
                ("Images", "JPG"),
                ("Images", "png"),
            ]
        )
        if ref_name == "":
            break

        # Read and resize image
        image = cv2.imread(ref_name)
        big_image = cv2.resize(image, (500,500))

        # Generate Callback Parameters
        FIG, AX = init_3d()
        param = [FIG, AX]

        # Display window
        cv2.namedWindow('mouseRGB')
        cv2.setMouseCallback('mouseRGB',mouseRGB, param=param)

        # Update the image until user quits with "esc"
        while True:
            cv2.imshow('mouseRGB',big_image)
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
