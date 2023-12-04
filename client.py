#!/usr/bin/env python
import threading
from typing import Annotated, Literal
from uuid import uuid4

import confluent_kafka
import curtsies
from curtsies.fmtfuncs import bold, fmtstr
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
    print('Subscribing to ', topics)
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

    threading.Thread(target=consume).start()

    with curtsies.Input() as keypresses:
        for _ in keypresses:
            value = randomname.get_name()
            text = fmtstr(
                bold(f'[{color}]') + ' produced "' + value + '"',
                style=color)
            producer.produce(color, value)
            print(text)


if __name__ == "__main__":
    typer.run(main)
