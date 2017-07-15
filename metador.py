#!/usr/bin/python3
import io
import datetime
import random
import piexif
from PIL import Image


def random_datetime(
        start_date=datetime.datetime(1970, 1, 1),
        date_format='%Y:%m:%d %X'
    ):
    '''
    pseudorandomly generates datetime stamp in given format based on start date
    provided. default format '%Y:%m:%d %X' (e.g: '2008:08:09 04:17:19')
    :param start_date: datetime object | default: datetime.datetime(1970, 1, 1)
    :param date_format: string | default: '%Y:%m:%d %X'
    :return:
    '''
    diff_time = (datetime.datetime.now() - start_date)
    day_delta = random.randrange(-diff_time.days, diff_time.days)
    if day_delta < 0:
        return (
            datetime.datetime.now() + datetime.timedelta(
                days=day_delta,
                hours=random.randrange(-23,23),
                minutes=random.randrange(-59,59),
                seconds=random.randrange(-59,59),
                milliseconds=random.randrange(-999,999),
                microseconds=random.randrange(-999,999)
            )
        ).strftime(date_format)
    else:
        return (
            datetime.datetime(1970, 1, 1) + datetime.timedelta(
                days=day_delta,
                hours=random.randrange(-23, 23),
                minutes=random.randrange(-59, 59),
                seconds=random.randrange(-59, 59),
                milliseconds=random.randrange(-999, 999),
                microseconds=random.randrange(-999, 999)
            )
        ).strftime(date_format)

def random_lat():
    '''
    pseudorandomly generate Latitude along with Reference
    :return: list | [reference, lat]
    '''
    lat = int(random.uniform(-90,90) * 1000000)
    if lat >= 0:
        ref = 'N'
    else:
        ref = 'S'
    return [ref, lat]

def random_lat():
    '''
    pseudorandomly generate Longitude along with Reference
    :return: [reference, long]
    '''
    long = int(random.uniform(-180,180) * 1000000)
    if long >= 0:
        ref = 'E'
    else:
        ref = 'W'
    return [ref, long]

def spoof_data(in_image):
    '''
    takes path to image and creates a copy with spoofed exif data
    :param in_image: string path to image
    :return: None
    '''
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
               piexif.GPSIFD.GPSLatitude: [86399607, 1000000],
               piexif.GPSIFD.GPSLongitude: [56119658, 1000000],
               piexif.GPSIFD.GPSDateStamp: random_datetime(),
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