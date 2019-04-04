# Starling X footprint test case

## Getting Started

This test case add the capability to measure 4 basic footprint parts:

	* boot time
	* hard drive footprint
	* virtual memory footprint
	* Average CPU % utilzation

### Installing

```
python setup.py build
python setup.py install
```

### How to run test case


After installing

```
	metrics.py
```

This will get all the metrics and print the result on the screen

If we want to run an specific test case:

```
usage: metrics [-h] [--boottime] [--hd_footprint] [--memory_footprint]
               [--cpu_utilization CPU_UTILIZATION] [--send_data]

optional arguments:
  -h, --help            show this help message and exit
  --boottime            Print kernel/userspace boot time
  --hd_footprint        Print HD footprint
  --memory_footprint    Print virtual memory footprint
  --cpu_utilization CPU_UTILIZATION
                        Print cpu utilization over X seconds
  --send_data           Store data at Influx DB
```

## FluxDB DB injection

This project also has a short guide to inject metrics results in a [InfluxDB]
database, this is in order to be plotted by [Grafana] project and track
different relevant performance metrics of [StarlingX] project.


### Configuration

#### Client

In client side will be executed the scripts of this project, however they
require the next configuration.

```
$ sudo apt-get install python-influxdb
```

In the client section remember to set correctly the server.conf in the same
level where the script is running:

```
INFLUX_SERVER=<the address of the server where DB will be hosted>
INFLUX_PORT=<PORT>
INFLUX_PASS=<DB password>
INFLUX_USER=<DB user>
DB_NAME=<DB name, i.e: starlingx>
```
#### Server

Install [InfluxDB] and [Grafana] and dependencies

```
$ sudo apt-get install influxdb-client
$ sudo apt-get install grafana
```

Start systemd service

```
$ sudo systemctl start influxdb
$ sudo systemctl start grafana
```

Start interactive mode to check the data has been injected correctly:

```
$ influx
$ use starlingx
$ select * from hd_footprint (as an example)
```

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **VictorRodriguez** - *Initial work* - [VictorRodriguez](https://github.com/VictorRodriguez)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## TODO

Please feel free to add as many requests as you have:

https://etherpad.openstack.org/p/stx_performance_feedback

[Grafana]: https://grafana.com/
[InfluxDB]: https://github.com/influxdata/influxdb
[StarlingX]: http://www.starlingx.io/
