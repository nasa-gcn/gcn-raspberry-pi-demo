#!/usr/bin/env python
import datetime
import json
import sys
import termios
import threading
import tty
from contextlib import contextmanager

import confluent_kafka
import numpy as np
import typer
from rich.console import Console

COLORS = {"red", "green", "blue"}


@contextmanager
def terminal_raw_input(fd: int):
    old = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    try:
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def main(
    bootstrap_server: str,
    color: str,
):
    console = Console()
    console.clear()
    console.show_cursor(False)
    console.print("Starting client", end=None)

    states = dict()

    def stats(data):
        for broker in json.loads(data)["brokers"].values():
            nodeid = broker["nodeid"]
            if broker["source"] != "configured" or nodeid < 1:
                continue
            old_state = states.get(nodeid, False)
            new_state = broker["state"] == "UP"
            if old_state != new_state:
                console.print(
                    "\nBroker", nodeid, "UP" if new_state else "DOWN", end=None
                )
                states[nodeid] = new_state

    def consume():
        while True:
            for message in consumer.consume():
                topic = message.topic()
                if error := message.error():
                    print(error, file=sys.stderr)
                else:
                    console.print(
                        f"\n[{topic} bold]RECV[not bold] {message.value().decode()}",
                        end=None,
                    )

    consumer = confluent_kafka.Consumer(
        {
            "bootstrap.servers": bootstrap_server,
            "group.id": color,
            "enable.auto.commit": False,
            "socket.timeout.ms": 1500,
            "stats_cb": stats,
            "statistics.interval.ms": 250,
            "reconnect.backoff.max.ms": 2000,
        }
    )
    producer = confluent_kafka.Producer(
        {
            "bootstrap.servers": bootstrap_server,
            "socket.timeout.ms": 1500,
            "reconnect.backoff.max.ms": 2000,
        }
    )
    consumer.subscribe(list(COLORS - {color}))

    threading.Thread(target=consume, daemon=True).start()

    def produce():
        date = datetime.datetime.now(datetime.UTC).strftime("%m/%d/%y %H:%M:%S.%f")[:-3]
        ra = np.random.uniform(0, 360)
        dec = 90 - np.rad2deg(np.arccos(np.random.uniform(-1, 1)))
        ra_str = np.format_float_positional(ra, min_digits=3, precision=3, pad_left=3)
        dec_str = np.format_float_positional(
            dec, min_digits=3, precision=3, pad_left=3, sign=True
        )
        value = f"{ra_str}°{dec_str}°\n{date}"
        console.print(f"\n[{color} bold]SEND[not bold] {value}", end=None)
        producer.produce(color, value)

    with terminal_raw_input(sys.stdin.fileno()):
        while sys.stdin.read(1) != "q":
            produce()


if __name__ == "__main__":
    typer.run(main)
