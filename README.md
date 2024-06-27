# Image Cipher Script
Hide text in images.

## How does this work?
To store data red, green and blue color channels are used. To store 1 even value is stored, to store 0 odd is stored. This way each pixel can store 3 bits of data without losing almost any visual quality.

## Usage
To encode message use: `main.py --source image.png --text "Hello, World!" --output output.png`.

To decode you use the following command: `main.py --decode --input image.png`.

### Note that this won't work with:
- Characters that can't be encoded in utf-8
- Lossy image formats
- Transparent images (transparency is removed)