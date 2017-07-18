#!/usr/bin/python3
import io
import datetime
import random
import piexif
from PIL import Image

zeroth_ifd = {
    piexif.ImageIFD.XResolution: (72, 1),
    piexif.ImageIFD.YResolution: (72, 1),
    piexif.ImageIFD.Software: u"Camera"
}
exif_ifd = {
    piexif.ExifIFD.ColorSpace: 1,
    piexif.ExifIFD.Sharpness: 65535,
    piexif.ExifIFD.LensSpecification: (
        (1, 1), (1, 1), (1, 1), (1, 1)
    ),
}
gps_ifd = {
    piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
    piexif.GPSIFD.GPSAltitudeRef: 1,
}
first_ifd = {
    piexif.ImageIFD.Compression: 1,
    piexif.ImageIFD.XResolution: (72, 1),
    piexif.ImageIFD.YResolution: (72, 1),
    piexif.ImageIFD.Software: u"Camera"
}

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
    return [ref, abs(lat)]

def random_long():
    '''
    pseudorandomly generate Longitude along with Reference
    :return: [reference, long]
    '''
    long = int(random.uniform(-180,180) * 1000000)
    if long >= 0:
        ref = 'E'
    else:
        ref = 'W'
    return [ref, abs(long)]

def random_device():
    '''
    pseudorandomly chooses a device from device list
    :return: string
    '''
    devices = [
        'Android', 'Canon', 'GoPro', 'iPhone', 'iPhone 5', 'iPhone 5c',
        'iPhone 5s', 'iPhone SE', 'iPhone 6', 'iPhone 7', 'Sony'
    ]
    return devices[random.randrange(0, len(devices))]

def spoof_data(in_image):
    '''
    takes path to image and creates a copy with spoofed exif data
    :param in_image: string path to image
    :return: None
    '''
    lat = random_lat()
    long = random_long()
    date_stamp = random_datetime()
    device = random_device()

    zeroth_ifd[piexif.ImageIFD.Make] = device

    exif_ifd[piexif.ExifIFD.DateTimeOriginal] = date_stamp
    exif_ifd[piexif.ExifIFD.LensMake] = device

    gps_ifd[piexif.GPSIFD.GPSLatitudeRef] = lat[0]
    gps_ifd[piexif.GPSIFD.GPSLatitude] = [lat[1], 1000000]
    gps_ifd[piexif.GPSIFD.GPSLongitudeRef] = long[0]
    gps_ifd[piexif.GPSIFD.GPSLongitude] = [long[1], 1000000]
    gps_ifd[piexif.GPSIFD.GPSDateStamp] = date_stamp

    first_ifd[piexif.ImageIFD.Make] = device

    o = io.BytesIO()
    thumb_im = Image.open(in_image)
    thumb_im.thumbnail((50, 50), Image.ANTIALIAS)
    thumb_im.save(o, "jpeg")
    thumbnail = o.getvalue()
    exif_dict = {
        "0th": zeroth_ifd, "Exif": exif_ifd, "GPS": gps_ifd,
        "1st": first_ifd, "thumbnail": thumbnail
    }
    exif_bytes = piexif.dump(exif_dict)
    im = Image.open(in_image)
    im.save("out.jpg", exif=exif_bytes)

def man_spoof(lat, long, date_stamp, device, in_image):
    if lat[0].strip() == '' or lat[1].strip() == '':
        lat = random_lat()
    else:
        lat[1] = int(float(lat[1]) * 1000000)
    if long[0].strip() == '' or long[1].strip() == '':
        long = random_long()
    else:
        long[1] = int(float(long[1]) * 1000000)
    if date_stamp.strip() == '':
        date_stamp = random_datetime()
    if device.strip() == '':
        device = random_device()

    zeroth_ifd[piexif.ImageIFD.Make] = device

    exif_ifd[piexif.ExifIFD.DateTimeOriginal] = date_stamp
    exif_ifd[piexif.ExifIFD.LensMake] = device

    gps_ifd[piexif.GPSIFD.GPSLatitudeRef] = lat[0]
    gps_ifd[piexif.GPSIFD.GPSLatitude] = [lat[1], 1000000]
    gps_ifd[piexif.GPSIFD.GPSLongitudeRef] = long[0]
    gps_ifd[piexif.GPSIFD.GPSLongitude] = [long[1], 1000000]
    gps_ifd[piexif.GPSIFD.GPSDateStamp] = date_stamp

    first_ifd[piexif.ImageIFD.Make] = device

    o = io.BytesIO()
    thumb_im = Image.open(in_image)
    thumb_im.thumbnail((50, 50), Image.ANTIALIAS)
    thumb_im.save(o, "jpeg")
    thumbnail = o.getvalue()
    exif_dict = {
        "0th": zeroth_ifd, "Exif": exif_ifd, "GPS": gps_ifd,
        "1st": first_ifd, "thumbnail": thumbnail
    }
    exif_bytes = piexif.dump(exif_dict)
    im = Image.open(in_image)
    im.save("out.jpg", exif=exif_bytes)

if __name__ == "__main__":
    print('welcome! cmds include:')
    print('remove| removes data')
    print('spoof| spoof data')
    print('man-spoof| manual spoof for certain tags')
    print('read| print tags')
    in_file = input('File Path==> ')
    cmd = input('command==> ')

    if cmd.lower() == 'remove':
        print('REMOVING DATA')
        piexif.remove(in_file)

    elif cmd.lower() == 'spoof':
        print('SPOOFING DATA')
        spoof_data(in_file)

    elif cmd.lower() == 'man-spoof':
        print('All blank fields will be randomized.')
        print('Press Enter To Continue')
        lat_ref = input('Latiude Ref (N,S)==> ')
        print('Format: XX.XXX')
        lat = input('Latiude==> ')
        long_ref = input('Longitude Ref (E,W)==> ')
        print('Format: XX.XXX')
        long = input('Longitude==> ')
        print('Timestamp format: YYYY:MM:DD HH:MM:SS (24Hour Time)')
        date_stamp = input('Timestamp==> ')
        device = input('Device==> ')
        man_spoof(
            [lat_ref, lat],
            [long_ref, long],
            date_stamp,
            device,
            in_file
        )
        print('SPOOFING DATA')

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