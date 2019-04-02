#!/usr/bin/env python

__author__      = "Mario Carrillo/Victor Rodriguez"

import random
import time
import argparse
import json
import os

from influxdb import InfluxDBClient

INFLUX_SERVER = ""
INFLUX_PORT = ""
INFLUX_PASS = ""
INFLUX_USER = ""

def send_data(json_file):

    if INFLUX_SERVER and INFLUX_PORT and INFLUX_PASS and INFLUX_USER:
        client = InfluxDBClient(INFLUX_SERVER, INFLUX_PORT,
                                    INFLUX_USER, INFLUX_PASS, 'starlingx')
        if client.write_points(json_file):
            print("Data inserted successfully")
        else:
            print("Error during data insertion")
        return client
    else:
        print("Error the server is not configured yet: server.conf")
        return None

def check_data(client,table):

    query = "select value from %s;" % (table)
    result = client.query(query)
    print("%s contains:" % table)
    print(result)

def get_server_data():

    global INFLUX_SERVER
    global INFLUX_PORT
    global INFLUX_PASS
    global INFLUX_USER

    config_file = "server.conf"

    if os.path.isfile(config_file):
        FILE = open(config_file, "r")
        for line in FILE:
            if "#" in line:
                pass
            if "INFLUX_SERVER" in line:
                INFLUX_SERVER = line.split("=")[1].strip()
            if "INFLUX_PORT" in line:
                INFLUX_PORT = line.split("=")[1].strip()
            if "INFLUX_PASS" in line:
                INFLUX_PASS = line.split("=")[1].strip()
            if "INFLUX_USER" in line:
                INFLUX_USER = line.split("=")[1].strip()
    else:
        print("Error server.conf missing")

    # Table information
    table = "vm_metrics"
    test_name = "vm_boottime"
    test_units = "ms"
    # Data to be inserted
    current_date = time.strftime("%c")
    value = round(random.uniform(0.1, 10),2)
    json_file = [
        {
            "measurement": table,
            "time": current_date,
            "fields": {
                "test" : test_name,
                "unit": test_units,
                "value": value
            }
        }
    ]

    send_data(json_file)

def main():
    get_server_data()
    print(INFLUX_SERVER)
    print(INFLUX_PORT)
    print(INFLUX_PASS)
    print(INFLUX_USER)


if __name__ == '__main__':
    main()
