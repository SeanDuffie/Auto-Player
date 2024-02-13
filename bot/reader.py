""" reader.py
    This file will handle any reading of the image
    
    Pytesseract Documentation - https://pypi.org/project/pytesseract/
    Google's Tesseract-OCR is used for reading text
"""
import logging
import sys
from tkinter import filedialog

import cv2
import pytesseract

# Initial Logger Settings
FMT_MAIN = "%(asctime)s\t| %(levelname)s\t| %(message)s"
logging.basicConfig(format=FMT_MAIN, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")

DEBUG = False


class ImgHandler:
    """ Tracks and reads an image """
    def __init__(self, img=None) -> None:
        # Mention the installed location of Tesseract-OCR in your system
        pytesseract.pytesseract.tesseract_cmd = r'/Program Files/Tesseract-OCR/tesseract.exe'

        self.wp = 255
        self.bp = 0

        # Private Variables
        if img is not None:
            self.img = img
        # else:
        #     print("ERROR: image is None")

    def update_img(self, img):
        """ Replace the current image being read """
        self.img = img

    def show_img(self):
        """ Show the current image being processed """
        cv2.imshow("Screen Preview", self.img)

    def read_text(self, white_text: bool = True):
        """ Read the text contained within the bounding box """
        # Check loaded image
        if self.img is None:
            logging.error("%s\t| No image loaded. Call update_img() or init with img.", __name__)
            sys.exit(1)

        # Convert the image to gray scale
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        if DEBUG:
            cv2.imshow("Grayscale", gray)

        # Performing OTSU threshold
        if white_text:
            thresh = cv2.threshold(gray, self.bp, self.wp, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)[1]
        else:
            thresh = cv2.threshold(gray, self.bp, self.wp, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]
        if DEBUG:
            cv2.imshow("Threshold", thresh)

        # TODO: Research into new values for structuring element
        # FIXME: This may need to be a passed variable per game
        # Specify structure shape and kernel size.
        # Kernel size increases or decreases the area
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect
        # each word instead of a sentence.
        # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # dilation = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, rect_kernel)

        # Apply a Gaussian Blur, this seems to work the best overall when given a white background and dark text
        dilation = cv2.GaussianBlur(thresh, (7,7), 0)
        self.img = dilation.copy()
        if DEBUG:
            cv2.imshow("Dilation", dilation)

        # Finding contours
        contours = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_NONE)[0]

        # FIXME: May be able to do this without contours
        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        text = ""
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            # Cropping the text block for giving input to OCR
            cropped = dilation[y:y + h, x:x + w]

            # Apply OCR on the cropped image
            text += pytesseract.image_to_string(cropped)

            if DEBUG:
                cv2.imshow("cropped", dilation)

        return text

if __name__ == "__main__":
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
            cv2.destroyAllWindows()
            sys.exit()

        # Read and resize image
        raw_img = cv2.imread(ref_name)
        rdr = ImgHandler(raw_img)

        print(rdr.read_text())
        cv2.waitKey()
