""" reader.py
    This file will handle any reading of the image
    The 
"""
import sys
import logging
import cv2
import pytesseract

class ImgHandler:
    """ Tracks and reads an image """
    def __init__(self, img=None) -> None:
        # Mention the installed location of Tesseract-OCR in your system
        pytesseract.pytesseract.tesseract_cmd = r'/Program Files/Tesseract-OCR/tesseract.exe'

        # Private Variables
        if img is not None:
            self.img = img
            self.preprocess()
        self.contours = None
        self.hierarchy = None

    def update_img(self, img):
        """ Replace the current image being read """
        self.img = img
        self.preprocess()

    def show_img(self):
        """ Show the current image being processed """
        cv2.imshow("Screen Preview", self.img)

    def preprocess(self):
        """ Preprocessing the image starts
            TODO: add detail on process
        """
        # Convert the image to gray scale
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        # Specify structure shape and kernel size.
        # Kernel size increases or decreases the area
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

        # Finding contours
        self.contours, self.hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                        cv2.CHAIN_APPROX_NONE)

    def read_text(self):
        """ Read the text contained within the bounding box """
        # Check loaded image
        if self.img is None:
            logging.error("%s\t| No image loaded. Call update_Img() or init with img.", __name__)
            sys.exit(1)

        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        for cnt in self.contours:
            x, y, w, h = cv2.boundingRect(cnt)

            # Drawing a rectangle on copied image
            im2 = self.img.copy()
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]

            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)

        return text
