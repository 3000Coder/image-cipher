from PIL import Image

img = Image.open("new.png")
img = img.convert('RGB')
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