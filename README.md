# Resizer
Resizer helps you:

- generate thumbnails, palmnails, and more
- load images from various sources

## Sample

    from resizer import Resizer
    
    resizer = Resizer({
    	'thumbnail': (50, 50, 'jpeg'),
    	'small': (100, 100, 'png'),
    })
    
    images = resizer.resize_image('http://placekitten.com/300/200')
    
    for (k, im) in images.iteritems():
    	print '{0}.{1}: {2}'.format(k, im.ext, im.size)
    	with open('%s.%s' % (k, im.ext), 'wb') as f:
    		f.write(im.read())

The above code creates two cropped versions of the image loaded from the URL and outputs the following:

    thumbnail.jpeg: (50, 50)
    small.png: (100, 100)
    
## API Reference
The API consists of two classes: `Image` and `Resizer`.

### Image
Image is a read-only file-like class that abstracts loading images from various sources such as URLs.

#### Attributes
- `ext`: The extension of the image.
- `size`: A two-tuple containing the width and height of the image.
- `pil_image`: The PIL Image object for this image.

#### Image(source)
Constructs a new Image object from the given source.

##### Parameters
- `source`: One of the following:
	- URL of an image.
	- Path to an image in the local file system.
	- A PIL Image object (the image will be copied).
	- A readable file-like object.

#### *Image*.read(size=None)
Read at most `size` bytes from the image (less if EOF is hit). If `size` is omitted or negative, reads all the data. The bytes are returned as a string object.

#### *Image*.close()
Closes the image. Attempting to do further operations raises a `ValueError`.

### Resizer
Resizer is a utility class that helps resizing images to a set of given sizes.

#### Attributes
- `default_format`: Format used when no other format is specified.
- `sizes`: A dict containing two-tuples (width, height) and/or three-tuples (width, height, format) for each of the sizes (keys). If format is specified for a size, the result image will always be in that format. Otherwise, it remains in the original image's format.
- `adaption_mode`: A string indicating what to do with images that are smaller than some of the sizes.
	
	- `"ignore"`: Don't generate an image for the sizes that are larger
				  than this one.
	- `"resize"`: Resize the image to be as large as the larger sizes.
	- `"downsize"`: Let the images for the larger sizes be smaller than
				    the size.
	- `"throw"`: Throw a `ValueError` if the image is smaller than at
				 least one of the sizes.
- `precise`: A boolean indicating what to do with images of different aspect ratios than the given sizes. If False, the given sizes' width and height are treated as "max width" and "max height". If True, trying to resize images of a different aspect ratio will throw a `ValueError` or crop the images depending on the `crop` attribute.
- `crop`: A boolean indicating whether the images should be automatically cropped to fit the given dimensions or not. If True, images of a different aspect ratio are cropped to the closest possible width and height that fit the aspect ratios.

    Example:
        
        r = Resizer(precise=True, crop=True, sizes={'small': (50, 50)})
        imgs = r.resize_image('http://placekitten.com/300/200')
        # imgs is now {'small': Image(…)} where the image was obtained
        # by cropping the source image to (200, 200) and then resizing
        # it to (50, 50).
        
        r.precise = False
        r.crop = False
        imgs = r.resize_image('http://placekitten.com/300/200')
        # imgs is now {'small': Image(…)} where the image was obtained
        # by resizing the image to (50, 33).
        
        r.precise = True
        r.crop = False
        imgs = r.resize_image('http://placekitten.com/300/200')
        # Previous line threw a ValueError, so this line is not reached.

#### Resizer(sizes=None, crop=False, precise=False, default_format='png', adaption_mode='downsize')
Constructs a new resizer for the with the given sizes and configurations. See the Attributes section above for information about the arguments.

#### *Resizer*.resize_image(image)
Resizes `image` to each of the sizes.

##### Parameters
- `image`: Must be either an Image object or something the Image constructor can take as its `source` argument.

##### Return value
A dict similar to the resizer's `sizes` attribute with the only differences being that the tuples have been replaced with Image objects (the results of the resizing) and some keys might be missing because of the image being smaller than the sizes (see the `adaption_mode` attribute).