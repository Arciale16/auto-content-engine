from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance


INPUT_FOLDER = Path("assets/input")
OUTPUT_FOLDER = Path("assets/processed")

WIDTH = 1080
HEIGHT = 1920


def find_image():

    extensions = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.webp"
    ]

    for ext in extensions:
        files = list(INPUT_FOLDER.glob(ext))

        if files:
            return files[0]

    raise FileNotFoundError(
        "No image found in assets/input"
    )


def create_background(img):

    background = img.copy()

    background = background.resize(
        (WIDTH, HEIGHT)
    )

    background = background.filter(
        ImageFilter.GaussianBlur(45)
    )

    background = ImageEnhance.Brightness(
        background
    ).enhance(0.45)

    return background


def resize_subject(img):

    subject = img.copy()

    subject.thumbnail(
        (850, 1200)
    )

    return subject


def compose_image(img):

    background = create_background(img)

    subject = resize_subject(img)

    x = (
        WIDTH - subject.width
    ) // 2

    y = (
        HEIGHT - subject.height
    ) // 2


    background.paste(
        subject,
        (x, y)
    )


    return background


def main():

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )


    image_path = find_image()

    print(
        "Input image:",
        image_path
    )


    img = Image.open(
        image_path
    ).convert("RGB")


    result = compose_image(
        img
    )


    output = (
        OUTPUT_FOLDER
        /
        "processed.png"
    )


    result.save(
        output,
        quality=95
    )


    print(
        "Created:",
        output
    )


if __name__ == "__main__":
    main()