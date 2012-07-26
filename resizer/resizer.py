from .image import Image, Size


class Resizer(object):
    def __init__(self, sizes=None, crop=False, precise=False,
                 default_format='png', adaption_mode='downsize'):
        self.sizes = sizes
        self.crop = crop
        self.precise = precise
        self.default_format = default_format
        self.adaption_mode = adaption_mode

    def resize_image(self, image):
        if self.sizes is None:
            raise ValueError('Sizes may not be None.')

        if not isinstance(image, Image):
            image = Image(image)
        self.image = image

        images = {}

        for (name, attrs) in self.sizes.iteritems():
            img = self._handle_size(image, *self._parse_attrs(attrs))
            if img:
                images[name] = img

        return images

    def _parse_attrs(self, attrs):
        if len(attrs) == 3:
            return Size(*attrs[:2]), attrs[2] or self.default_format
        elif len(attrs) == 2:
            return Size(*attrs), self.image.ext or self.default_format
        else:
            raise ValueError(
                'Size attributes must be a two-tuple or a three-tuple.'
            )

    def _handle_size(self, source, size, ext):
        if self._is_smaller(source, size):
            return self._handle_adaption(source, size, ext)

        if self.precise:
            return self._handle_precise(source, size, ext)

        return self._handle_common(source, size, ext)

    def _handle_common(self, source, size, ext):
        # We know the image isn't smaller than this size and that the width and
        # height of this size should be treated as "max width" and "max
        # height".
        image = Image(source)
        image.thumbnail(size)
        image.ext = ext
        return image

    def _handle_precise(self, source, size, ext):
        # Check the aspect ratio by resizing the image and checking if the
        # resulting size is the same as the required one because it's the most
        # accurate way.
        image = self._handle_common(source, size, ext)

        if image.width == size.width and image.height == size.height:
            return image

        if self.crop:
            return self._handle_crop(source, size, ext)

        raise ValueError('Image does not have the required aspect ratio.')

    def _handle_crop(self, source, size, ext):
        width, height = self._get_projected_size(size, source)
        print 'cropping to', width, height
        return self._handle_common(
            source.crop((0, 0, width, height)), size, ext
        )

    def _get_crop_size(self, source, size):
        # We know the source is at least as large as size.
        width_ratio = float(source.width) / size.width
        height_ratio = float(source.height) / size.height
        ratio = min(width_ratio, height_ratio)
        return Size(
            int(round(size.width * ratio)),
            int(round(size.height * ratio))
        )

    def _handle_adaption(self, *args):
        if self.adaption_mode == 'ignore':
            return
        elif self.adaption_mode == 'throw':
            raise ValueError(
                'Image must be at least as large as the largest size.'
            )
        elif self.adaption_mode == 'downsize':
            return self._handle_downsize_adaption(*args)
        elif self.adaption_mode == 'resize':
            return self._handle_resize_adaption(*args)
        else:
            raise ValueError('Unknown adaption mode.')

    def _handle_downsize_adaption(self, *args):
        return self._handle_common(*args)

    def _handle_resize_adaption(self, source, size, ext):
        width, height = self._get_projected_size(source, size)
        image = source.resize(width, height)
        return self._handle_common(image, size, ext)

    def _get_projected_size(self, small, large):
        width_ratio = float(large.width) / small.width
        height_ratio = float(large.height) / small.height
        ratio = min(width_ratio, height_ratio)
        return Size(
            int(round(small.width * ratio)),
            int(round(small.height * ratio))
        )

    def _is_smaller(self, a, b):
        return a.width < b.width or a.height < b.height
