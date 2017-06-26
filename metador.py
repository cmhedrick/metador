import piexif

exif_dict = piexif.load("IMG.JPG")
for tag_type in ("0th", "Exif", "GPS", "1st"):
    for tag in exif_dict[tag_type]:
        print(piexif.TAGS[tag_type][tag]["name"], exif_dict[tag_type][tag])

piexif.remove("IMG.JPG")
print('\nREMOVED?\n')
for tag_type in ("0th", "Exif", "GPS", "1st"):
    for tag in exif_dict[tag_type]:
        print(piexif.TAGS[tag_type][tag]["name"], exif_dict[tag_type][tag])
