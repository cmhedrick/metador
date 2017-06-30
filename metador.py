#!/usr/bin/python3
import piexif

if __name__ == "__main__":
    print('welcome:')
    in_file = input('File Path==> ')
    cmd = input('command==> ')

    if cmd.lower() == 'remove':
        print('REMOVING DATA')
        piexif.remove(in_file)

    elif cmd.lower() == 'read':
        print('READING...')
        exif_dict = piexif.load(in_file)
        for tag_type in ("0th", "Exif", "GPS", "1st"):
            for tag in exif_dict[tag_type]:
                print(piexif.TAGS[tag_type][tag]["name"],
                      exif_dict[tag_type][tag])
