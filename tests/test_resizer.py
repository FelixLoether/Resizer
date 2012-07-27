from flexmock import flexmock
from PIL.Image import ANTIALIAS
from resizer import Resizer, Image
from resizer.image import Size

fake_image_stack = []


class FakeImage(Image):
    def __init__(self, source, copy=True):
        fake_image_stack.append(self)
        self.source = source


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
        import resizer.resizer
        resizer.resizer.Image = FakeImage
        self.resizer.resize_image(source)
        resizer.resizer.Image = Image
        assert len(fake_image_stack) == 1
        assert fake_image_stack.pop().source == source

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
        import resizer.resizer
        resizer.resizer.Image = FakeImage
        self.resizer.resize_image(im)
        resizer.resizer.Image = Image
        assert len(fake_image_stack) == 1
        assert fake_image_stack.pop() is im


class TestResizerInternalMethods(object):
    def setup_method(self, method):
        self.resizer = Resizer()

    def test_parse_attrs_parses_three_tuples(self):
        width, height, ext = object(), object(), object()
        attrs = self.resizer._parse_attrs(None, (width, height, ext))
        assert attrs[0].width is width
        assert attrs[0].height is height
        assert attrs[1] is ext

    def test_parse_attrs_parses_two_tuples_and_gets_ext_from_source(self):
        width, height, ext = object(), object(), object()
        self.resizer.default_format = object()
        attrs = self.resizer._parse_attrs(
            flexmock(ext=ext), (width, height)
        )
        assert attrs[0].width is width
        assert attrs[0].height is height
        assert attrs[1] is ext

    def test_parse_attrs_gets_ext_from_default_format(self):
        width, height, ext = 0, 0, object()
        self.resizer.default_format = ext
        attrs = self.resizer._parse_attrs(
            flexmock(ext=None), (width, height)
        )
        assert attrs[1] is ext

    def test_parse_attrs_raises_value_error_for_one_tuples(self):
        try:
            self.resizer._parse_attrs(None, (0,))
        except ValueError:
            return
        assert False

    def test_parse_attrs_raises_value_error_for_four_tuples(self):
        try:
            self.resizer._parse_attrs(None, (0, 1, 2, 3))
        except ValueError:
            return
        assert False

    def test_is_smaller_returns_false_for_larger_size(self):
        assert self.resizer._is_smaller(Size(500, 500), Size(50, 50)) is False

    def test_is_smaller_returns_false_for_equal_sizes(self):
        assert self.resizer._is_smaller(Size(50, 50), Size(50, 50)) is False

    def test_is_smaller_returns_true_for_smaller_size(self):
        assert self.resizer._is_smaller(Size(50, 50), Size(500, 500))

    def test_is_smaller_returns_true_for_smaller_width(self):
        assert self.resizer._is_smaller(Size(50, 500), Size(500, 50))

    def test_is_smaller_returns_true_for_smaller_height(self):
        assert self.resizer._is_smaller(Size(500, 50), Size(50, 500))

    def _test_projected_size(self, a, b, result, smallest=True):
        size = self.resizer._get_projected_size(Size(*a), Size(*b), smallest)
        assert size == result

    def test_get_projected_size_50x50_to_200x200_is_200x200(self):
        self._test_projected_size((50, 50), (200, 200), (200, 200))

    def test_get_projected_size_50x50_to_100x150_is_100x100(self):
        self._test_projected_size((50, 50), (100, 150), (100, 100))

    def test_get_projected_size_50x100_to_200x200_is_100x200(self):
        self._test_projected_size((50, 100), (200, 200), (100, 200))

    def test_get_projected_size_50x100_to_100x100_is_50x100(self):
        self._test_projected_size((50, 100), (100, 100), (50, 100))

    def test_get_largest_projected_size_50x50_to_200x200_is_200x200(self):
        self._test_projected_size((50, 50), (200, 200), (200, 200), False)

    def test_get_largest_projected_size_50x50_to_100x150_is_150x150(self):
        self._test_projected_size((50, 50), (100, 150), (150, 150), False)

    def test_get_largest_projected_size_50x100_to_200x200_is_200x400(self):
        self._test_projected_size((50, 100), (200, 200), (200, 400), False)

    def test_get_largest_projected_size_50x100_to_100x100_is_100x200(self):
        self._test_projected_size((50, 100), (100, 100), (100, 200), False)

    def test_handle_downsize_adaption_calls_handle_common(self):
        source, size, ext = object(), object(), object()
        called = (
            flexmock(self.resizer)
            .should_receive('_handle_common')
            .once()
            .with_args(source, size, ext)
            .and_return(None)
        )
        self.resizer._handle_downsize_adaption(source, size, ext)
        called.verify()

    def test_handle_adaption_throws_value_error_when_mode_is_throw(self):
        self.resizer.adaption_mode = 'throw'
        try:
            self.resizer._handle_adaption()
        except ValueError:
            return
        assert False

    def test_handle_adaption_throws_value_error_for_unknown_mode(self):
        self.resizer.adaption_mode = 'uusipaavalniemi'
        try:
            self.resizer._handle_adaption()
        except ValueError:
            return
        assert False
