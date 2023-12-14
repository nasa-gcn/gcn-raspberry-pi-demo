#!/usr/bin/env python
import threading
from typing import Annotated
from uuid import uuid4
import signal

import confluent_kafka
from curtsies.fmtfuncs import bold, fmtstr
import gpiozero
import randomname
import typer

COLORS = {'red', 'green', 'blue'}


def main(
        bootstrap_server: Annotated[str, typer.Option()],
        color: Annotated[str, typer.Option()],
):
    consumer = confluent_kafka.Consumer({
        'bootstrap.servers': bootstrap_server,
        'group.id': str(uuid4()),
        'enable.auto.commit': False,
        'socket.timeout.ms': 1000,
        'log_level': 0,
    })
    producer = confluent_kafka.Producer({
        'bootstrap.servers': bootstrap_server,
        'socket.timeout.ms': 1000,
        'log_level': 0,
    })
    topics = list(COLORS - {color})
    consumer.subscribe(list(COLORS - {color}))

    def consume():
        while True:
            for message in consumer.consume():
                topic = message.topic()
                text = fmtstr(
                    bold(f'[{topic}]') + ' consumed "'
                    + (message.error() or message.value().decode()) + '"',
                    style=topic)
                print(text)

    threading.Thread(target=consume, daemon=True).start()

    def produce():
        value = randomname.get_name()
        text = fmtstr(
            bold(f'[{color}]') + ' produced "' + value + '"',
            style=color)
        producer.produce(color, value)
        print(text)

    button = gpiozero.Button(21, bounce_time=0.0001, hold_time=0.5, hold_repeat=True)
    button.when_activated = button.when_held = produce

    signal.pause()


if __name__ == "__main__":
    typer.run(main)
