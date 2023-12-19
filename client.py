#!/usr/bin/env python
import threading
from uuid import uuid4
import signal

import confluent_kafka
from rich.console import Console
import gpiozero
import randomname
import typer

COLORS = {"red", "green", "blue"}


def main(
    bootstrap_server: str,
    color: str,
):
    console = Console()
    console.clear()
    consumer = confluent_kafka.Consumer(
        {
            "bootstrap.servers": bootstrap_server,
            "group.id": str(uuid4()),
            "enable.auto.commit": False,
            "socket.timeout.ms": 1000,
            "log_level": 0,
        }
    )
    producer = confluent_kafka.Producer(
        {
            "bootstrap.servers": bootstrap_server,
            "socket.timeout.ms": 1000,
            "log_level": 0,
        }
    )
    consumer.subscribe(list(COLORS - {color}))

    def consume():
        while True:
            for message in consumer.consume():
                topic = message.topic()
                console.print(
                    f"[{topic} bold]RECV[not bold] {message.error() or message.value().decode()}"
                )

    threading.Thread(target=consume, daemon=True).start()

    def produce():
        value = "-" * 20
        while len(value) > 10:
            value = randomname.get_name()
        console.print(f"[{color} bold]SEND[not bold] {value}")
        producer.produce(color, value)

    button = gpiozero.Button(21, bounce_time=0.001, hold_time=0.5, hold_repeat=True)
    button.when_activated = button.when_held = produce

    signal.pause()


if __name__ == "__main__":
    typer.run(main)
