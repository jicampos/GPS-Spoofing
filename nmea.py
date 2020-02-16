import pynmea2
import argparse
import os
import csv
# https://docs.python.org/3/library/argparse.html  

parser = argparse.ArgumentParser(description='Options for processing nmea data.')
parser.add_argument('-l', '--label', help='include label for benign (0) or malignant (1) data', required=False)
parser.add_argument('-d', '--dir', help='source directory for nmea data', required=False, default='data')
parser.add_argument('-o', '--out', help='output directory for processed data', required=False, default='')
args = parser.parse_args()

data = []
list_snr = []
capture_data = False

headers = ['YYYY-MM-DD', 'HH:MM:SS (UTC)', 'speed over ground (Knots)', 'magnetic variation', 'latitude', 
		'lat direction', 'longitude', 'lon direction', 'sat tracked', 'horizontal dilution', 
		'altitude', 'alt units', 'height of geoid', 'geoid units', 'sat in view', 'num. nmeas', 'SNR']

if args.label != None:
	headers.append('label')

for file in os.listdir(args.dir):

	# file handler to read NMEA data
	file_read = open(os.path.join(args.dir,file), "r")

	# name of csv file to write parsed data
	file_csv = file.replace('txt', 'csv')
	with open(os.path.join(args.out,file_csv), 'w', newline='') as csvfile:
		print('Writing to ' + file_csv + '...')
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(headers)
	
		for line in file_read:

			if line[0:6] == "$GPRMC":
				nmea = pynmea2.parse(line)
				
				data.append(nmea.datestamp)
				data.append(nmea.spd_over_grnd)
				data.append(nmea.mag_variation)
				
				capture_data = True

			if line[0:6] == "$GPGGA" and capture_data:
				nmea = pynmea2.parse(line)

				data.insert(1, nmea.timestamp)
				data.append(nmea.lat)
				data.append(nmea.lat_dir)
				data.append(nmea.lon)
				data.append(nmea.lon_dir)
				data.append(nmea.num_sats)
				data.append(nmea.horizontal_dil)
				data.append(nmea.altitude)
				data.append(nmea.altitude_units)
				data.append(nmea.geo_sep)
				data.append(nmea.geo_sep_units)

			if line[0:6] == "$GPGSV" and capture_data:
				nmea = pynmea2.parse(line)

				list_snr.append(nmea.snr_1)
				list_snr.append(nmea.snr_2)
				list_snr.append(nmea.snr_3)
				list_snr.append(nmea.snr_4)

				if nmea.num_messages == nmea.msg_num:

					data.append(nmea.num_sv_in_view)
					data.append(nmea.num_messages)
					data.append(list_snr)

					if args.label != None:
						data.append(args.label)

					writer.writerow(data)

					list_snr = []
					data = []

print('Done!')

# https://github.com/Knio/pynmea2