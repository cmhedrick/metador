#!/usr/bin/python3
import io
import piexif
from PIL import Image

def spoof_data(in_image):
    o = io.BytesIO()
    thumb_im = Image.open(in_image)
    thumb_im.thumbnail((50, 50), Image.ANTIALIAS)
    thumb_im.save(o, "jpeg")
    thumbnail = o.getvalue()

    zeroth_ifd = {piexif.ImageIFD.Make: u"iPhone",
                  piexif.ImageIFD.XResolution: (96, 1),
                  piexif.ImageIFD.YResolution: (96, 1),
                  piexif.ImageIFD.Software: u"Camera"
                  }
    exif_ifd = {piexif.ExifIFD.DateTimeOriginal: u"2005:11:30 01:01:01",
                piexif.ExifIFD.LensMake: u"iPhone",
                piexif.ExifIFD.Sharpness: 65535,
                piexif.ExifIFD.LensSpecification: (
                (1, 1), (1, 1), (1, 1), (1, 1)),
                }
    gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
               piexif.GPSIFD.GPSAltitudeRef: 1,
               piexif.GPSIFD.GPSDateStamp: u"1999:05:05 10:10:10",
               }
    first_ifd = {piexif.ImageIFD.Make: u"iPhone",
                 piexif.ImageIFD.XResolution: (40, 1),
                 piexif.ImageIFD.YResolution: (40, 1),
                 piexif.ImageIFD.Software: u"Camera"
                 }

    exif_dict = {"0th": zeroth_ifd, "Exif": exif_ifd, "GPS": gps_ifd,
                 "1st": first_ifd, "thumbnail": thumbnail}
    exif_bytes = piexif.dump(exif_dict)
    im = Image.open(in_image)
    im.thumbnail((100, 100), Image.ANTIALIAS)
    im.save("out.jpg", exif=exif_bytes)

if __name__ == "__main__":
    print('welcome! cmds include:')
    print('remove| removes data')
    print('spoof| spoof data')
    print('read| print tags')
    in_file = input('File Path==> ')
    cmd = input('command==> ')

    if cmd.lower() == 'remove':
        print('REMOVING DATA')
        piexif.remove(in_file)

    elif cmd.lower() == 'spoof':
        print('SPOOFING DATA')
        spoof_data(in_file)

    elif cmd.lower() == 'read':
        try:
            print('READING...')
            exif_dict = piexif.load(in_file)
            for tag_type in ("0th", "Exif", "GPS", "1st"):
                for tag in exif_dict[tag_type]:
                    print(piexif.TAGS[tag_type][tag]["name"],
                          exif_dict[tag_type][tag])
        except:
            print('POSSIBLY NO TAGS!?')