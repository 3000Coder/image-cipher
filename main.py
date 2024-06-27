from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Hide text in images.')
parser.add_argument('--source', type=str, required=True, help='path to source image')
parser.add_argument('--output', type=str, required=False, help='path to output image (only required when encoding)')
parser.add_argument('--text', type=str, required=False, help='text to encode (only required when encoding)')
parser.add_argument('--decode', action='store_true', help='when used, decoding mode is selected')

args = parser.parse_args()

img = Image.open(args.source).convert('RGB')

def utf8_to_array_of_bits(integer: int) -> list[bool]:
    bin_fmted = format(integer, '08b')
    return [bool(int(b)) for b in bin_fmted]

def make_number_even(integer: int) -> int:
    return integer - integer % 2

def make_number_odd(integer: int) -> int:
    if integer % 2 == 0:
        return integer + 1
    else:
        return integer

if args.decode:
    msg = ""
    bit_buff = 0
    z = 0

    def read_color(color) -> None:
        global msg, bit_buff, z
        if z >= 8:
            if bit_buff != 0:
                msg += chr(bit_buff)
            bit_buff = 0
            z = 0

        if color % 2 == 0:
            bit_buff += 1 << z
        z += 1

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r, g, b = img.getpixel((x, y))
            
            for color in img.getpixel((x, y)):
                read_color(color)
            
    print(msg[::-1])
else:
    msg = args.text
    if msg == None:
        print("Argument --text is missing. Use --help for more info.")
        exit(100)
    
    if args.output == None:
        print("Argument --output is missing. Use --help for more info.")
        exit(100)

    # Check if message can fit
    if len(msg)*8 >= img.size[0]*img.size[1]*3:
        print('Message cannot fit inside selected image.')
        exit(101)

    msg_bits = []
    for c in msg.encode('utf-8'):
        msg_bits += utf8_to_array_of_bits(c)
    msg_bits.reverse()

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

    img.save(args.output)