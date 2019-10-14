import serial
import time
import pynmea2
import csv 
import signal 
import argparse
# import threading 

def keyBoardInterruptHandler(signal, frame):
    print("\nkeyBoardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    csvFile.close()
    exit(0)

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file_name", help="File name to save data")
args = parser.parse_args()

ser=serial.Serial("/dev/ttyAMA0", baudrate=9600)
signal.signal(signal.SIGINT, keyBoardInterruptHandler)

file_dir = "/home/pi/Desktop/"
# file_name = "data-{}".format(time.strftime("%m/%d/%Y-%H:%M:%S"))

if args.file_name is None:
	file_name = "data-{}.csv".format(time.strftime("%m%d%Y-%H%M%S"))
	print("Using default file name for logging data: {}".format(file_name))
else:
	file_name = args.file_name
	print("Using custom file name for logging data: {}".format(file_name))

file_path = file_dir + file_name
print("Starting up...")

while True:
	NMEA = ser.readline()

	if NMEA[0:6] == "$GPGLL":
		msg = pynmea2.parse(NMEA)
		saved_msg = [str(msg.latitude), str(msg.longitude)]
		print(saved_msg)

		with open(file_path, "a+") as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(saved_msg)

