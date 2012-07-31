import urllib2
from StringIO import StringIO
from PIL import Image as pil_image

try:
    from collections import namedtuple
    Size = namedtuple('Size', 'width height')
except ImportError:
    class Size(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def __getitem__(self, index):
            if index == 0:
                return self.width
            if index == 1:
                return self.height
            raise IndexError()

        def __len__(self):
            return 2

        def __eq__(self, other):
            if isinstance(other, Size):
                return (
                    self.width == other.width and
                    self.height == other.height
                )
            return (
                len(other) == 2 and
                self[0] == other[0] and
                self[1] == other[1]
            )

        def __str__(self):
            return 'Size(width=%s, height=%s)' % (self[0], self[1])

        def __repr__(self):
            return str(self)


class Image(object):
    def __init__(self, source, copy=True):
        if isinstance(source, str) or isinstance(source, unicode):
            if source.startswith('https://') or source.startswith('http://'):
                self._load_from_url(source)
            else:
                self._load_from_file_path(source)
        elif isinstance(source, pil_image.Image):
            self._load_from_pil_image(source, copy)
        elif isinstance(source, Image):
            self._load_from_image(source, copy)
        else:
            self._load_from_file_object(source)

        format = self._pil_image.format
        self.ext = format.lower() if format else None

    @property
    def size(self):
        return Size(*self._pil_image.size)

    @property
    def width(self):
        return self.size.width

    @property
    def height(self):
        return self.size.height

    def _load_from_image(self, source, copy):
        self._load_from_pil_image(source._pil_image, copy)

    def _load_from_pil_image(self, source, copy):
        if copy:
            self._pil_image = source.copy()
        else:
            self._pil_image = source

    def _load_from_file_path(self, source):
        self._pil_image = pil_image.open(source)

    def _load_from_url(self, source):
        self._load_from_file_object(StringIO(urllib2.urlopen(source).read()))

    def _load_from_file_object(self, source):
        self._pil_image = pil_image.open(source)

    def __getattr__(self, attr):
        return getattr(self._pil_image, attr)
