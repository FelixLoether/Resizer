from __future__ import with_statement
from flexmock import flexmock
from resizer import Resizer
from resizer.image import Size
from .test_resizer import FakeImage


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

    def test_parse_attrs_parses_one_tuples(self):
        ext = object()
        attrs = self.resizer._parse_attrs(None, [ext])
        assert attrs[0] is None
        assert attrs[1] is ext

    def test_parse_attrs_parses_zero_tuples(self):
        ext = object()
        im = flexmock(ext=ext)
        attrs = self.resizer._parse_attrs(im, [])
        assert attrs[0] is None
        assert attrs[1] is ext

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

    def test_handle_adaption_returns_none_when_mode_is_ignore(self):
        self.resizer.adaption_mode = 'ignore'
        assert self.resizer._handle_adaption() is None

    def test_handle_adaption_calls_handle_downsize_adaption_for_downsize(self):
        self.resizer.adaption_mode = 'downsize'
        args = [object(), object(), object()]
        called = (
            flexmock(self.resizer)
            .should_receive('_handle_downsize_adaption')
            .once()
            .with_args(*args)
            .and_return()
        )
        self.resizer._handle_adaption(*args)
        called.verify()

    def test_handle_adaption_calls_handle_resize_adaption_for_resize(self):
        self.resizer.adaption_mode = 'resize'
        args = [object(), object(), object()]
        called = (
            flexmock(self.resizer)
            .should_receive('_handle_resize_adaption')
            .once()
            .with_args(*args)
            .and_return()
        )
        self.resizer._handle_adaption(*args)
        called.verify()

    def _mock_handle_resize_adaption(self, get_projected_size=True,
                                     resize=True, handle_size=True, width=0,
                                     height=0):
        if get_projected_size:
            (flexmock(self.resizer)
                .should_receive('_get_projected_size')
                .and_return((width, height)))
        if handle_size:
            (flexmock(self.resizer)
                .should_receive('_handle_size')
                .and_return())

        return flexmock(resize=lambda a, b: None)

    def test_handle_resize_adaption_gets_projected_size(self):
        size = object()
        source = self._mock_handle_resize_adaption(get_projected_size=False)
        called = (
            flexmock(self.resizer)
            .should_receive('_get_projected_size')
            .once()
            .with_args(source, size, False)
            .and_return((0, 0))
        )

        with FakeImage.context(full_cleanup=True):
            self.resizer._handle_resize_adaption(source, size, None)
        called.verify()

    def test_handle_resize_adaption_resizes_image(self):
        width, height, resize_mode = object(), object(), object()
        source = self._mock_handle_resize_adaption(
            resize=False, width=width, height=height
        )
        self.resizer.resize_mode = resize_mode
        called = (
            flexmock(source)
            .should_receive('resize')
            .once()
            .with_args((width, height), resize_mode)
            .and_return()
        )

        with FakeImage.context(full_cleanup=True):
            self.resizer._handle_resize_adaption(source, None, None)
        called.verify()

    def test_handle_resize_adaption_creates_an_image(self):
        resized_source = object()
        source = flexmock(resize=lambda a, b: resized_source)
        self._mock_handle_resize_adaption()

        with FakeImage.context():
            self.resizer._handle_resize_adaption(source, None, None)

        assert FakeImage.stack.pop().source is resized_source
        assert len(FakeImage.stack) == 0

    def test_handle_resize_adaption_calls_handle_size(self):
        image, size, ext = object(), object(), object()
        source = self._mock_handle_resize_adaption(handle_size=False)
        flexmock(FakeImage).new_instances(image)

        called = (
            flexmock(self.resizer)
            .should_receive('_handle_size')
            .once()
            .with_args(image, size, ext)
        )
        with FakeImage.context():
            self.resizer._handle_resize_adaption(source, size, ext)
        called.verify()

    def _mock_handle_crop(self, get_projected_size=True, handle_common=True,
                          crop=True, width=0, height=0):
        if get_projected_size:
            (flexmock(self.resizer)
                .should_receive('_get_projected_size')
                .and_return((width, height)))
        if handle_common:
            (flexmock(self.resizer)
                .should_receive('_handle_common')
                .and_return())
        return flexmock(crop=lambda a: None)

    def test_handle_crop_gets_projected_size(self):
        source = self._mock_handle_crop(get_projected_size=False)
        size = object()
        called = (
            flexmock(self.resizer)
            .should_receive('_get_projected_size')
            .once()
            .with_args(size, source)
            .and_return((0, 0))
        )

        with FakeImage.context(full_cleanup=True):
            self.resizer._handle_crop(source, size, None)
        called.verify()

    def test_handle_crop_crops_image(self):
        width, height = object(), object()
        source = self._mock_handle_crop(crop=False, width=width, height=height)
        called = (
            source
            .should_receive('crop')
            .once()
            .with_args((0, 0, width, height))
            .and_return()
        )

        with FakeImage.context(full_cleanup=True):
            self.resizer._handle_crop(source, None, None)
        called.verify()

    def _mock_handle_precise(self, handle_common=True, handle_crop=True,
                             image=None):
        if handle_common:
            (flexmock(self.resizer)
                .should_receive('_handle_common')
                .and_return(image or Size(100, 150)))
        if handle_crop:
            (flexmock(self.resizer)
                .should_receive('_handle_crop')
                .and_return())

    def test_handle_precise_calls_handle_common(self):
        source, size, ext = object(), Size(100, 150), object()
        self._mock_handle_precise(handle_common=False)
        called = (
            flexmock(self.resizer)
            .should_receive('_handle_common')
            .once()
            .with_args(source, size, ext)
            .and_return(Size(100, 150))
        )
        self.resizer._handle_precise(source, size, ext)
        called.verify()

    def test_handle_precise_returns_handle_common_if_ratio_is_correct(self):
        image = Size(100, 150)
        self._mock_handle_precise(image=image)
        im = self.resizer._handle_precise(None, Size(100, 150), None)
        assert im is image

    def test_handle_precise_returns_handle_crop_if_ratio_is_incorrect(self):
        self.resizer.crop = True
        source, size, ext, res = object(), Size(0, 0), object(), object()
        self._mock_handle_precise(handle_crop=False)
        called = (
            flexmock(self.resizer)
            .should_receive('_handle_crop')
            .once()
            .with_args(source, size, ext)
            .and_return(res)
        )
        assert self.resizer._handle_precise(source, size, ext) is res
        called.verify()

    def test_handle_precise_raises_value_error_if_crop_is_false(self):
        self.resizer.crop = False
        self._mock_handle_precise()

        try:
            self.resizer._handle_precise(None, Size(0, 0), None)
        except ValueError:
            return
        assert False

    def _mock_handle_common(self, get_projected_size=True, resize=True,
                            size=None):
        if get_projected_size:
            (flexmock(self.resizer)
                .should_receive('_get_projected_size')
                .and_return(size))

        return flexmock(resize=lambda a, b: None)

    def test_handle_common_gets_projected_size(self):
        source = self._mock_handle_common(get_projected_size=False)
        size = object()
        called = (
            flexmock(self.resizer)
            .should_receive('_get_projected_size')
            .once()
            .with_args(source, size)
            .and_return()
        )
        with FakeImage.context(full_cleanup=True):
            self.resizer._handle_common(source, size, None)
        called.verify()

    def test_handle_common_resizes_image(self):
        size = object()
        source = self._mock_handle_common(resize=False, size=size)
        called = (
            flexmock(source)
            .should_receive('resize')
            .once()
            .with_args(size, self.resizer.resize_mode)
            .and_return()
        )
        with FakeImage.context(full_cleanup=True):
            self.resizer._handle_common(source, size, None)
        called.verify()

    def test_handle_common_creates_image(self):
        self._mock_handle_common()
        resized_source = object()
        source = flexmock(resize=lambda a, b: resized_source)
        with FakeImage.context():
            self.resizer._handle_common(source, None, None)
        assert FakeImage.stack.pop().source is resized_source
        assert len(FakeImage.stack) == 0

    def test_handle_common_returns_image(self):
        source = self._mock_handle_common()
        fake_image = flexmock()
        flexmock(FakeImage).new_instances(fake_image)
        with FakeImage.context():
            im = self.resizer._handle_common(source, None, None)
        assert im is fake_image

    def test_handle_common_sets_ext_on_image(self):
        source = self._mock_handle_common()
        ext = object()
        fake_image = flexmock()
        flexmock(FakeImage).new_instances(fake_image)
        with FakeImage.context():
            self.resizer._handle_common(source, None, ext)
        assert fake_image.ext is ext

    def _mock_handle_size(self, is_smaller_val=False, handle_adaption=True,
                          handle_precise=True, handle_common=True,
                          is_smaller=True):
        if is_smaller:
            (flexmock(self.resizer)
                .should_receive('_is_smaller')
                .and_return(is_smaller_val))
        if handle_adaption:
            (flexmock(self.resizer)
                .should_receive('_handle_adaption')
                .and_return())
        if handle_precise:
            (flexmock(self.resizer)
                .should_receive('_handle_precise')
                .and_return())
        if handle_common:
            (flexmock(self.resizer)
                .should_receive('_handle_common')
                .and_return())
        return object(), object(), object()

    def test_handle_size_calls_is_smaller(self):
        source, size, _ = self._mock_handle_size(is_smaller=False)
        called = (
            flexmock(self.resizer)
            .should_receive('_is_smaller')
            .once()
            .with_args(source, size)
            .and_return()
        )
        self.resizer._handle_size(source, size, None)
        called.verify()

    def test_handle_size_calls_handle_adaption_if_is_smaller(self):
        source, size, ext = self._mock_handle_size(True, handle_adaption=False)
        res = object()
        called = (
            flexmock(self.resizer)
            .should_receive('_handle_adaption')
            .once()
            .with_args(source, size, ext)
            .and_return(res)
        )
        return_val = self.resizer._handle_size(source, size, ext)
        called.verify()
        assert return_val is res

    def test_handle_size_doesnt_call_handle_adaption_if_isnt_smaller(self):
        source, size, ext = self._mock_handle_size(
            False, handle_adaption=False
        )
        (flexmock(self.resizer)
            .should_receive('_handle_adaption')
            .and_raise(AssertionError('Not supposed to be called')))
        self.resizer._handle_size(source, size, ext)

    def test_handle_size_calls_handle_precise_if_precise_is_true(self):
        self.resizer.precise = True
        source, size, ext = self._mock_handle_size(False, handle_precise=False)
        res = object()
        called = (
            flexmock(self.resizer)
            .should_receive('_handle_precise')
            .once()
            .with_args(source, size, ext)
            .and_return(res)
        )
        return_val = self.resizer._handle_size(source, size, ext)
        called.verify()
        assert return_val is res

    def test_handle_size_doesnt_call_precise_if_precise_is_false(self):
        self._mock_handle_size(False, handle_precise=False)
        (flexmock(self.resizer)
            .should_receive('_handle_precise')
            .and_raise(AssertionError('Not supposed to be called')))
        self.resizer._handle_size(None, object(), None)

    def test_handle_size_doesnt_call_precise_if_is_smaller(self):
        self.resizer.precise = True
        self._mock_handle_size(True, handle_precise=False)
        (flexmock(self.resizer)
            .should_receive('_handle_precise')
            .and_raise(AssertionError('Not supposed to be called')))
        self.resizer._handle_size(None, object(), None)

    def test_handle_size_calls_common_if_isnt_smaller_and_isnt_precise(self):
        source, size, ext = self._mock_handle_size(False, handle_common=False)
        res = object()
        called = (
            flexmock(self.resizer)
            .should_receive('_handle_common')
            .once()
            .with_args(source, size, ext)
            .and_return(res)
        )
        return_val = self.resizer._handle_size(source, size, ext)
        called.verify()
        assert return_val is res

    def test_handle_size_doesnt_call_common_if_is_smaller(self):
        self._mock_handle_size(True, handle_common=False)
        (flexmock(self.resizer)
            .should_receive('_handle_common')
            .and_raise(AssertionError('Not supposed to be called')))
        self.resizer._handle_size(None, object(), None)

    def test_handle_size_doesnt_call_common_if_is_precise(self):
        self.resizer.precise = True
        self._mock_handle_size(handle_common=False)
        (flexmock(self.resizer)
            .should_receive('_handle_common')
            .and_raise(AssertionError('Not supposed to be called')))
        self.resizer._handle_size(None, object(), None)

    def test_resize_image_calls_handle_size_for_all_sizes(self):
        pa_stack = []
        hs_stack = []

        def parse_attrs(image, attrs):
            pa_stack.append([image, attrs])
            return attrs

        def handle_size(*args):
            hs_stack.append(args)

        flexmock(
            self.resizer,
            _parse_attrs=parse_attrs,
            _handle_size=handle_size
        )

        self.resizer.sizes = {
            'small': (50, 50),
            'medium': (150, 200, 'png')
        }

        with FakeImage.context(full_cleanup=True):
            self.resizer.resize_image('none')

        sizes = self.resizer.sizes.values()
        assert len(pa_stack) == len(hs_stack) == 2
        assert pa_stack[0][1] in sizes
        assert pa_stack[1][1] in sizes
        assert hs_stack[0][1:] in sizes
        assert hs_stack[1][1:] in sizes
