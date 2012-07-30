from __future__ import with_statement
from contextlib import contextmanager
from flexmock import flexmock
from PIL.Image import ANTIALIAS, Image as PILImage
from resizer import Resizer, Image


class FakeImage(Image):
    stack = []

    def __init__(self, source, copy=True):
        self.ext = None
        self.source = source
        FakeImage.stack.append(self)

    @staticmethod
    @contextmanager
    def context(full_cleanup=False):
        import resizer.resizer
        resizer.resizer.Image = FakeImage
        yield
        resizer.resizer.Image = Image
        if full_cleanup:
            FakeImage.stack = []


class TestResizer(object):
    def setup_method(self, method):
        self.sizes = {
            'small': (50, 50),
        }
        self.resizer = Resizer(
            sizes=self.sizes, crop=False, precise=False, default_format='jpeg',
            adaption_mode='throw', resize_mode=ANTIALIAS
        )

    def test_init_sets_up_attributes(self):
        assert self.resizer.sizes is self.sizes
        assert self.resizer.crop is False
        assert self.resizer.precise is False
        assert self.resizer.default_format == 'jpeg'
        assert self.resizer.adaption_mode == 'throw'
        assert self.resizer.resize_mode == ANTIALIAS

    def _test_image_creation(self, source):
        self.sizes.pop('small')
        with FakeImage.context():
            self.resizer.resize_image(source)
        assert len(FakeImage.stack) == 1
        assert FakeImage.stack.pop().source == source

    def test_resize_image_creates_image_from_url(self):
        self._test_image_creation('http://nonexistent/image.jpeg')

    def test_resize_image_creates_image_from_path(self):
        self._test_image_creation('/path/to/image')

    def test_resize_image_creates_image_from_file(self):
        with open('tests/image.jpg') as f:
            self._test_image_creation(f)

    def test_resize_image_does_not_create_image_from_image(self):
        im = FakeImage(None)
        self.sizes.pop('small')
        with FakeImage.context():
            self.resizer.resize_image(im)
        assert len(FakeImage.stack) == 1
        assert FakeImage.stack.pop() is im

    def test_resize_image_resizes_to_sizes(self):
        resized_image = PILImage()
        resized_image.format = 'JPEG'
        resized_image.size = (50, 50)
        image = PILImage()
        image.format = 'JPEG'
        image.size = (500, 500)

        (flexmock(PILImage)
            .should_receive('resize')
            .and_return(resized_image))
        (flexmock(PILImage)
            .should_receive('copy')
            .and_return(image))

        images = self.resizer.resize_image(image)

        assert 'small' in images
        assert images['small']._pil_image is resized_image
        assert images['small'].size == (50, 50)

    def test_resize_image_raises_value_error_if_sizes_is_none(self):
        self.resizer.sizes = None
        try:
            self.resizer.resize_image('http://placekitten.com/100/100')
        except ValueError:
            return
        assert False
