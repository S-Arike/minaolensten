import os
import subprocess
import re


def convert_to_decimal(coordinates):
    match = re.match(r'(\d+) deg (\d+)\' ([\d.]+)" ([NSEW])', coordinates)
    if match:
        degrees = float(match.group(1))
        minutes = float(match.group(2))
        seconds = float(match.group(3))
        direction = match.group(4)
        decimal_degrees = degrees + minutes / 60 + seconds / (60 * 60)
        if direction in ['S', 'W']:
            decimal_degrees = -decimal_degrees
        return decimal_degrees
    else:
        return None


def process_media_files(folder_path, output_file):
    """
    Protsessib meediafailid (pildid) kaustas, loeb nende EXIF-andmeid kasutades ExifTooli
    ja salvestab koordinaadid tekstifaili.

    :param folder_path: Kausta tee, kus meediafailid asuvad
    :param output_file: Salvestatava tekstifaili tee
    """
    with open(output_file, 'w') as file:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                _, file_extension = os.path.splitext(file_path)

                if file_extension.lower() in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'):
                    try:
                        # Käivitab ExifTooli käsu, et lugeda EXIF-andmeid meediafailist
                        process = subprocess.Popen(
                            ['exiftool', '-gpslatitude', '-gpslongitude', '-gpsaltitude', file_path],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            universal_newlines=True)
                        output, _ = process.communicate()

                        gps_latitude = None
                        gps_longitude = None
                        gps_altitude = None

                        # Töötleb ExifTooli väljundit, et saada kätte GPS-koordinaadid
                        for line in output.splitlines():
                            if line.startswith('GPS Latitude'):
                                gps_latitude = line.split(':')[-1].strip()
                            elif line.startswith('GPS Longitude'):
                                gps_longitude = line.split(':')[-1].strip()
                            elif line.startswith('GPS Altitude'):
                                gps_altitude = line.split(':')[-1].strip()

                        # Teisendab koordinaadid kümnendsüsteemi ja salvestab tekstifaili
                        if gps_latitude and gps_longitude:
                            latitude = convert_to_decimal(gps_latitude)
                            longitude = convert_to_decimal(gps_longitude)
                            file.write(f"{file_path};{latitude};{longitude};{gps_altitude}\n")

                    except (subprocess.CalledProcessError, OSError):
                        pass


# Example usage:
folder_path = '/home/kasutaja/PycharmProjects/11-05-2023/Images'
output_file = '/home/kasutaja/Documents/geotags.txt'

process_media_files(folder_path, output_file)