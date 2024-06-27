from PIL import Image

img = Image.open("img.png").convert('RGB')
msg = "Hello, World!"

def utf8_to_array_of_bits(integer: int) -> list[bool]:
    bin_fmted = format(integer, '08b')
    return [bool(int(b)) for b in bin_fmted]

def make_number_even(integer: int) -> int:
    return integer - integer % 2

def make_number_odd(integer: int) -> int:
    return integer + (integer % 2 - 1)


# Check if message can fit
if len(msg)*8 >= img.size[0]*img.size[1]*3:
    print('Message cannot fit inside selected image.')
    exit()

msg_bits = []
for c in msg.encode('utf-8'):
    msg_bits += utf8_to_array_of_bits(c)

stop_encoding = False
bits_left = len(msg_bits)


def modify_color(color: int) -> int:
    global stop_encoding, bits_left, msg_bits
    if stop_encoding:
        return make_number_odd(color)
    else:
        if bits_left <= 0:
            stop_encoding = True
            return make_number_odd(color)
        else:
            bit = msg_bits[-bits_left]
            bits_left -= 1
            if bit:
                return make_number_even(color)
            else:
                return make_number_odd(color)

for x in range(img.size[0]):
    for y in range(img.size[1]):
        r, g, b = img.getpixel((x, y))
        rn = modify_color(r)
        gn = modify_color(g)
        bn = modify_color(b)
        img.putpixel((x, y), (rn, gn, bn))
        # print(img.getpixel((x, y))[0])

img.save('new.png')