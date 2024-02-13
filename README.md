<h1>AutoPlayer</h1>

This project is intended to simplify repetitive computer tasks - often game related.

It uses Image Processing - specifically google's pytesseract ocr - to read text on the screen in configurable locations,
process it, and control the user's keyboard in various ways based on a json entry supplied by the user.

Use cases include:
- Auto Fishing in Minecraft (using audio subtitles)
- Auto Running in 7 Days to Die (using the stamina bar)
- (Soon) Auto skip ads on Youtube
- (Soon) Other actions in other games

<h2>Installation</h2>

1. Clone the git repo
    - Open a terminal
    - Navigate to the desired parent directory
    - Run `git clone "https://github.com/SeanDuffie/Auto-Player.git"`
2. Install Dependencies
    - Run `pip install -r requirements.txt` to install required dependencies
3. Download and install Tesseract OCR for text reading
    - View documentation here: https://tesseract-ocr.github.io/tessdoc
    - Download Tesseract OCR installer from here: https://github.com/UB-Mannheim/tesseract/wiki
    - Run the installer and either set the location to "C:/Program Files/Tesseract-OCR"
        or update the path located on line 21 for `pytesseract.pytesseract.tesseract_cmd`

<h2>Usage</h2>

Once all installation instructions have been complete, the usage should be as simple as launching "main.py" in a terminal. This can be done using the following commands:

```
cd {insert_proj_path}\Auto-Player\
python .\main.py
```

NOTE: If you run into issues with this, make sure
- Your python environment is correct, and matches with the one you `pip install`'d to
- You installed the correct Tesseract OCR, to the correct place, and gave python the correct path
- Your pathing is correct. The program is fairly rugged when it comes to pathing issues

<h2>Future Features</h2>

- [ ] Autoskip YouTube Ads
- [ ] Export program to binaries for easier distribution and easier usage.
- [ ] Use JSONs to custom wrap all configurations
- [ ] Change the "resize" function to generate the above JSON configurations
- [ ] Wrap the actual functions so that new games require as minimal code and recycle as much of the framework as possible
