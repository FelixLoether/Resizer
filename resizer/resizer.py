from .image import Image


class Resizer(object):
    def resize_image(self, image):
        if not isinstance(image, Image):
            image = Image(image)
        self.image = image
