from PIL import Image, ImageDraw, ImageFont
import argparse

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def draw_to_image(size, text: str):
    h, w = size
    image = Image.new(mode = "L", size=(w*12, h*20))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('assets/CourierPrime-Regular.ttf', 20)
    draw.text((0, 0), text, 255, font = font)
    return image.resize((w*12, h*12))


def resize_(image, new_width = 100):
    width, height = image.size
    ratio = height/width
    new_height = int(new_width*ratio)
    resized_image = image.resize((new_width, new_height))
    return (resized_image)

def grayify(image):
    grayscale_image = image.convert("L")
    return (grayscale_image)

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return characters


def save_path(image_path: str, save_extension = "txt"):
    extension = image_path.split(".")[-1]
    len_extension = len(extension)
    return image_path[:-len_extension] + save_extension


def recreate(image_path: str, use_resize = False, new_width = 100):
    try:
        image = Image.open(image_path).convert("L")
        if use_resize:
            image = resize_(image, new_width)
    except:
        print("invalid path")

    h, w = image.size

    new_image_data = pixels_to_ascii(image)
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+w)] for i in range(0, pixel_count, w))
    save_txt = save_path(image_path)
    with open(f"{save_txt}", "w") as f:
        f.write(ascii_image)
    return ascii_image, (h, w)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="assets/sample.jpg")
    parser.add_argument("--use_resize", default=False)
    parser.add_argument("--new_width", default=100)

    args = parser.parse_args()

    ascii_image, size = recreate(args.image_path, use_resize=args.use_resize, new_width=args.new_width)
    image = draw_to_image(size, ascii_image)
    image.save('test.jpg')