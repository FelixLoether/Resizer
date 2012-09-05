Resizer Module
==============

.. image:: https://secure.travis-ci.org/FelixLoether/Resizer.png?branch=master

Resizer helps you resize images to a set of given sizes (and load images from
various sources such as URLs).

.. toctree::
   :maxdepth: 2

------
Sample
------
::

    from resizer import Resizer

    resizer = Resizer(
        precise=True,
        sizes={
            'thumbnail': (50, 50),
            'small': (100, 100, 'png'),
            'original': []
        }
    )

    images = resizer.resize_image('http://placekitten.com/300/200')

    for (k, im) in images.iteritems():
        print '{0}.{1}: {2}'.format(k, im.ext, im.size)
        im.save('%s.%s' % (k, im.ext))

The above code creates three versions of the image loaded from the URL (two
cropped and resized ones and one that's a duplicate of the original image)
and outputs the following::

    small.png: Size(width=100, height=100)
    thumbnail.jpeg: Size(width=50, height=50)
    original.jpeg: Size(width=300, height=200)

------------
Installation
------------
::

    pip install -e "git://github.com/FelixLoether/resizer#egg=Resizer"

-------------
API Reference
-------------

.. module:: resizer
.. class:: Image(source, copy=True)

    Image is a slight abstraction on top of PIL's Image class that abstracts
    loading images from various sources such as URLs. The Image class has all
    attributes and methods you would find on a PIL Image, which return PIL
    Images instead of an instance of the Image object.

    :param source: One of the following:

        - URL of an image.
        - Path to an image in the local file syste.
        - A PIL Image object.
        - An :class:`Image` object.
        - A readable file-like object.

    :param copy:
        If the source is a PIL Image or an Image object, copy dictates whether the
        source image will be copied instead of used directly. With Image objects
        the Image object itself is always copied, the copy argument specifies
        whether the underlying PIL Image should be copied or not.

    .. attribute:: ext

        The extension of the image.

.. class:: Resizer(sizes=None, crop=True, precise=False, default_format='png', adaption_mode='downsize', resize_mode=ANTIALIAS)

    Resizer is a utility class that helps resizing images to a set of given sizes.

    .. attribute:: default_format

        Format used when no other format is specified.

    .. attribute:: resize_mode

        Which mode should be used for resizing. One of ``PIL.Image.ANTIALIAS``
        (default), ``PIL.Image.NEAREST``, ``PIL.Image.BICUBIC``,
        ``PIL.Image.BILINEAR``.

    .. attribute:: sizes

        A dict containing lists or tuples with 0 to 3 items for each of the sizes
        (keys):

        - zero items: ``[]``
        - one item: ``[format]``
        - two items: ``[width, height]``
        - three items: ``[width, height, format]``

        If format is specified for a size, the result image will always be in that
        format. Otherwise, it remains in the original image's format (or uses the
        default_format if the original has no format).

    .. attribute:: adaption_mode

        A string dictating what to do with images that are smaller than some of the
        sizes.

        ``"ignore"``
            Don't generate an image for the sizes that are larger than the source
            image.

        ``"resize"``
            Resize the image to be as large as the larger sizes before applying the
            other operations on it.

        ``"downsize"``
            Let the images for the larger sizes be smaller than the size.

        ``"throw"``
            Throw a ``ValueError`` if the image is smaller than at least one of the
            sizes.

    .. attribute:: precise

        A boolean indicating what to do with images of different aspect ratios than
        the given sizes.

        ``False``
            The given size's width and height are treated as "max width" and "max
            height".

        ``True``
            Throw a ``ValueError`` or crop the image depending on the value of the
            crop attribute.

    .. attribute:: crop

        A boolean dictating whether the images should be automatically cropped to
        fit the given aspect ratio or not when precise is True. If True, images of
        a different aspect ratio are cropped to the closest possible width and
        height that fit the aspect ratio of the size.

        Has no effect if precise is False.

    Example::

        r = Resizer(precise=True, crop=True, sizes={'small': (50, 50)})
        imgs = r.resize_image('http://placekitten.com/300/200')
        # imgs is now {'small': Image(...)} where the image was obtained by
        # cropping the source image to (200, 200) and then resizing it to (50, 50).

        r.precise = r.crop = False
        imgs = r.resize_image('http://placekitten.com/300/200')
        # imgs is now {'small': Image(...)} where the image was obtained by
        # resizing the image to (50, 33).

        r.precise = True
        r.crop = False
        imgs = r.resize_image('http://placekitten.com/300/200')
        # Previous line threw a ValueError, so this line is not reached.

    .. method:: resize_image(image)

        Resizes ``image`` to each of the sizes.

        :param image: The image to resize.
        :type image: :class:`Image` or something its constructor can take as its ``source`` argument
        :return:
            A dict similar to the resizer's ``sizes`` attribute with the only differences
            being that the tuples have been replaced with Image objects (the results of the
            resizing) and some keys might be missing because of the image being smaller
            than the sizes (see :attr:`adaption_mode`).
