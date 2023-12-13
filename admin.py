#!/usr/bin/env python
from time import sleep
from typing import Annotated

from rich.live import Live
from rich.table import Table
from rich.text import Text
import confluent_kafka.admin
import typer

COLORS = ['red', 'green', 'blue']


def main(
        bootstrap_server: Annotated[str, typer.Option()],
):
    admin = confluent_kafka.admin.AdminClient({
        'bootstrap.servers': bootstrap_server,
        'socket.timeout.ms': 1000,
        'log_level': 0,
    })

    topic_collection = confluent_kafka.TopicCollection(COLORS)

    table = Table(title='In Sync Replicas')
    table.add_column('Topic')
    for i in range(1, 4):
        table.add_column(f'Broker {i}')
    cells = []
    for topic in COLORS:
        row = [Text() for _ in range(3)]
        cells.append(row)
        table.add_row(f'[{topic}]{topic}', *row)
    
    with Live(table, refresh_per_second=4):
        while True:
            for topic, row, future in zip(COLORS, cells, admin.describe_topics(topic_collection).values()):
                isr = {isr.id for isr in future.result().partitions[0].isr}
                for i, cell in enumerate(row):
                    cell.plain = 'X' if i + 1 in isr else ''
            sleep(0.1)


if __name__ == "__main__":
    typer.run(main)
