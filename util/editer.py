from PIL import Image


if __name__ == "__main__":
    images_dir = "./imagesimg_{}.png"
    image_max = 8590

    for i in range(3700, image_max+1, 5):
        dir_ = images_dir.format(str(i).zfill(6))
        image = Image.open(dir_)
        image = image.rotate(90, expand=True)
        image.save("./images/image{}.png".format(i), "PNG", quality=100, optimize=True)
        print("Saved", i)
