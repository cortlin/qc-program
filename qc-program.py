import csv
import RPi.GPIO as IO
import time
import sys
from termcolor import colored
import os

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(17, IO.OUT)
IO.setup(27, IO.OUT) # Scanner
IO.setup(22, IO.OUT) # Buzzer
IO.setup(23,IO.IN)   # Sensor

IO.output(17, False)
IO.output(27, True)

def SaveFile(write):

    with open('scanned-barcodes.csv', 'r+') as f:
        scannedReader = csv.DictReader(f)

        for column in scannedReader:
            if write in column['opened']:
                print(colored('ERROR: Duplicate Barcode', 'red'))
                IO.output(22, True)
                time.sleep(.2)
                IO.output(22, False)
                time.sleep(.2)
                IO.output(22, True)
                time.sleep(.2)
                IO.output(22, False)
                break
        else:
            w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            w.writerow([write])


while True:
    if (IO.input(23)==False):
        IO.output(27, False)
        barcode = input("Waiting for Scanner :")
        time.sleep(.5)
        IO.output(27, True)
        print(barcode)

        with open('barcode-list.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for column in reader:
                if (column['codes'] == barcode):
                    print(colored("Barcode Matches Master Sheet", 'green'))
                    SaveFile(barcode)
                    break

            else:
                print(colored("Error: Barcode does not match", 'red'))
                IO.output(17, True)
                IO.output(22, True)
                time.sleep(.5)
                IO.output(17, False)
                IO.output(22, False)
