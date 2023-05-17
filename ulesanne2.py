import subprocess

filenameTxt = 'coordinates.txt'
filenameKml = 'images.kml'
header = "Failinimi;Laiuskraad;Pikkuskraad;Kõrgus"
cmd_csv = "exiftool -n -q -q -p '$filepath;$gpslatitude;$gpslongitude;$gpsdatetime' Images > " + filenameTxt
cmd_kml = 'exiftool -n -q -q -p kml.fmt Images > ' + filenameKml

print('Creating', filenameTxt, 'file')
subprocess.run(cmd_csv, shell=True, executable='/bin/bash')
print('Creating', filenameKml, 'file')
subprocess.run(cmd_kml, shell=True, executable='/bin/bash')

with open(filenameTxt, 'r', encoding='utf-8') as f:
    data = f.read()
    with open(filenameTxt, 'w', encoding='utf-8') as w:
        w.write(header + '\n' + data)
