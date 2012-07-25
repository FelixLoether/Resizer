# TIP (title in progress)

TIP helps you:

- generate thumbnails, palmnails, and more
- load images from various sources

## Sample

    from tip import Image, Resizer
    
    resizer = Resizer(
    	crop=True,
    	sizes={
    		'thumbnail': (50, 50, 'jpeg'),
    		'small': (100, 100, 'png'),
    	}
    )
    
    image = Image('http://placekitten.com/300/200')
    images = resizer.resize_image(image)
    
    for (k, im) in images.iteritems():
    	print '%s.%s: (%s, %s)' % (k, im.ext, *im.size)
    	with open('%s.%s' % (k, im.ext), 'wb') as f:
    		f.write(im.read())

The above code creates two cropped versions of the image loaded from the URL and outputs the following:

    thumbnail.jpeg: (50, 50)
    small.png: (100, 100)