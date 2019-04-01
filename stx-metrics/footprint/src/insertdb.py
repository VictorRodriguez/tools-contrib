#!/usr/bin/env python

__author__      = "Mario Carrillo/Victor Rodriguez"

import random
import time
import argparse
import json


from influxdb import InfluxDBClient

INFLUX_SERVER = "vmrod-ubuntu-devel.zpn.intel.com"
INFLUX_PORT = "8086"
INFLUX_PASS = "root"
INFLUX_USER = "root"

def send_data(json_file):

    client = InfluxDBClient(INFLUX_SERVER, INFLUX_PORT,
                                INFLUX_USER, INFLUX_PASS, 'starlingx')
    if client.write_points(json_file):
        print("Data inserted successfully")
    else:
        print("Error during data insertion")
    return client

def check_data(client,table):

    query = "select value from %s;" % (table)
    result = client.query(query)
    print("%s contains:" % table)
    print(result)

def main():

    global INFLUX_SERVER
    global INFLUX_PORT
    global INFLUX_PASS
    global INFLUX_USER

    parser = argparse.ArgumentParser()
    parser.add_argument('--server',\
        help='addres of the influxdb server')
    parser.add_argument('--port',\
        help='port of the influxdb server')
    parser.add_argument('--user',\
        help='user of the influxdb server')
    parser.add_argument('--password',\
        help='password of the influxdb server')
    parser.add_argument('--json_file',\
        help='json file with the data to insert')

    args = parser.parse_args()

    if args.server:
        INFLUX_SERVER = args.server
    if args.port:
        INFLUX_PORT = args.port
    if args.password:
        INFLUX_PASS = args.password
    if args.user:
        INFLUX_USER = args.password
    if args.json_file:
        json_file_path = args.json_file

if __name__ == '__main__':
    main()
