import gpxpy
import gpxpy.gpx
import glob

path = './GPXData/*'
files = glob.glob(path)
for f in files:
    gpx_file = open(f, 'r')
    print(f)
    csv_file_name = f.split('/')[2].split('.')[0] + ".csv"
    csv_file = open("./CSVData/"+csv_file_name,'w')
    gpx = gpxpy.parse(gpx_file)
    gpx_file.close()
    for waypoint in gpx.waypoints:
        csv_file.write(waypoint.name+','+str(waypoint.latitude)+','+str(waypoint.longitude)+'\n')
    csv_file.close()