import subprocess
filenameTxt = 'coordinates.csv'
filenameKml = 'images.kml'
header = "Failinimi;Laiuskraad;Pikkuskraad;Kõrgus"
cmd_csv = "exiftool -n -f -q -q -p '$filepath;$gpslatitude;$gpslongitude;$gpslatitude;$gpsdatetime' Images > " + filenameTxt
cmd_kml = 'exiftool -n -q -q -p kml.fmt Images >' + filenameKml

print('Create', filenameTxt, 'file')
subprocess.run(cmd_csv, shell=True)
print('Create', filenameKml, 'file')
subprocess.run(cmd_kml, shell=True)
with open(filenameTxt, 'r', encoding='utf-8') as f:
    data = f.read()
    with open(filenameTxt, 'w', encoding='utf-8')as w:
        w.write(header + '\n' + data)