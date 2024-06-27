from PIL import Image
img = Image.open("img.jpg")
msg = "Hello, World!"

def utf8_to_array_of_bits(integer: int):
    bin_fmted = format(integer, '08b')
    return [bool(int(b)) for b in bin_fmted]

def make_number_even(integer: int) -> int:
    return integer - integer % 2

def make_number_odd(integer: int) -> int:
    return integer - integer % 2

# Check if message can fit
if len(msg)*8 >= img.size[0]*img.size[1]*3:
    print('Message cannot fit inside selected image.')
    exit()

msg_bits = []
for c in msg.encode('utf-8'):
    msg_bits += utf8_to_array_of_bits(c)

stop_encoding = False
bits_left = len(msg_bits)

for x in range(img.size[0]):
    for y in range(img.size[1]):
        r, g, b = img.getpixel((x, y))
        if not stop_encoding:
            rn = r
            gn = g
            bn = b
            if bits_left > 0:
                bits_left -= 1
                # TODO

