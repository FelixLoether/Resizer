from flexmock import flexmock
from PIL import Image as pil_image
from PIL.Image import Image as PILImage
from resizer import Image
import urllib2


class TestImage(object):
    def setup_method(self, method):
        self.pil_image = PILImage()
        self.pil_image.size = (30, 100)
        self.pil_image.format = 'JPEG'
        self.pil_image.copy = lambda: self.pil_image
        self.image = Image(self.pil_image)
        with open('tests/image.jpg') as f:
            self.test_image_data = f.read()

    def test_size_returns_correct_size(self):
        assert self.image.size == self.pil_image.size

    def test_width_returns_correct_width(self):
        assert self.image.width == self.pil_image.size[0]

    def test_height_returns_correct_height(self):
        assert self.image.height == self.pil_image.size[1]

    def test_loading_from_url_loads_from_url(self):
        url = 'http://nonexistent/image.jpeg'
        loaded_url = (
            flexmock(urllib2)
            .should_receive('urlopen')
            .once()
            .with_args(url)
            .and_return(flexmock(read=lambda: self.test_image_data))
        )
        Image(url)
        loaded_url.verify()

    def test_loading_from_url_loads_correct_data(self):
        url = 'http://nonexistent/image.jpeg'
        (flexmock(urllib2)
            .should_receive('urlopen')
            .and_return(flexmock(read=lambda: self.test_image_data))
        )
        image = Image(url)
        assert image.size == (1, 1)
        assert image.ext == 'jpeg'

    def test_loading_from_file_path_calls_pil_open(self):
        path = 'tests/nonexistent.png'
        opened = (
            flexmock(pil_image)
            .should_receive('open')
            .once()
            .with_args(path)
            .and_return(flexmock(format='PNG'))
        )
        Image(path)
        opened.verify()

    def test_loading_from_file_path_loads_correct_data(self):
        path = 'tests/nonexistent.png'
        (flexmock(pil_image)
            .should_receive('open')
            .with_args(path)
            .and_return(flexmock(format='PNG', size=(50, 23)))
        )
        image = Image(path)
        assert image.size == (50, 23)
        assert image.ext == 'png'

    def test_loading_from_file_calls_pil_open(self):
        with open('tests/image.jpg') as f:
            opened = (
                flexmock(pil_image)
                .should_receive('open')
                .once()
                .with_args(f)
                .and_return(flexmock(format='JPEG'))
            )
            Image(f)
        opened.verify()

    def test_loading_from_file_loads_correct_data(self):
        with open('tests/image.jpg') as f:
            (flexmock(pil_image)
                .should_receive('open')
                .and_return(flexmock(format='JPEG', size=(83, 12)))
            )
            image = Image(f)
        assert image.size == (83, 12)
        assert image.ext == 'jpeg'

    def test_loading_from_image_calls_copy(self):
        def callback():
            called[0] += 1
            return flexmock(format='JPEG')

        called = [0]
        self.image._pil_image.copy = callback
        Image(self.image)
        assert called[0] == 1

    def test_loading_from_image_loads_correct_data(self):
        image = Image(self.image)
        assert image.size == self.image.size
        assert image.ext == self.image.ext
