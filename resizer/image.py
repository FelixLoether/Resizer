import urllib2
from StringIO import StringIO
from PIL import Image as pil_image


class Image(object):
    def __init__(self, source):
        if isinstance(source, str) or isinstance(source, unicode):
            if source.startswith('https://') or source.startswith('http://'):
                self._load_from_url(source)
            else:
                self._load_from_file_path(source)
        elif isinstance(source, pil_image.Image):
            self._load_from_pil_image(source)
        else:
            self._load_from_file_object(source)

        format = self.pil_image.format
        self.ext = format.lower() if format else None
        self.size = self.pil_image.size

    def _load_from_pil_image(self, source):
        self.pil_image = source.copy()

    def _load_from_file_path(self, source):
        self.pil_image = pil_image.open(source)

    def _load_from_url(self, source):
        self._load_from_file_object(StringIO(urllib2.urlopen(source).read()))

    def _load_from_file_object(self, source):
        self.pil_image = pil_image.open(source)
