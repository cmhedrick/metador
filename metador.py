import exifread

# images need to be opened in binary
f = open('image.jpg', 'rb')

# Return Exif tags
tags = exifread.process_file(f)

# get just GPS coords
print(
    'Lat: {0}|Long: {1}'.format(
        tags['GPS GPSLatitude'],
        tags['GPS GPSLongitude']
    )
)