#!/usr/bin/env python
import confluent_kafka
import confluent_kafka.admin
from rich.table import box, Table
from rich.live import Live
from rich.text import Text
import typer

COLORS = ["red", "green", "blue"]
symbols = "?NY"


def main(
        bootstrap_server: str,
):
    admin = confluent_kafka.admin.AdminClient({
        'bootstrap.servers': bootstrap_server,
        'socket.timeout.ms': 1500,
        'reconnect.backoff.max.ms': 2000,
    })

    topic_collection = confluent_kafka.TopicCollection(COLORS)

    table = Table(
        width=15,
        title="Brokers",
        title_justify="right",
        caption="insync replicas",
        caption_style='gray italic',
        title_style="bold",
        show_edge=False,
        pad_edge=False,
        collapse_padding=True,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Topic")
    table.add_column("1")
    table.add_column("2")
    table.add_column("3")
    rows = [[Text() for _ in range(3)] for __ in range(3)]
    for topic, row in zip(COLORS, rows):
        table.add_row(f"[bold {topic}]{topic}", *row)

    with Live(table):
        while True:
            for topic, row, future in zip(COLORS, rows, admin.describe_topics(topic_collection).values()):
                try:
                    isr = {isr.id for isr in future.result().partitions[0].isr}
                except confluent_kafka.KafkaException:
                    for cell in row:
                        cell.plain = '?'
                else:
                    for i, cell in enumerate(row):
                        cell.plain = 'Y' if i + 1 in isr else 'N'


if __name__ == "__main__":
    typer.run(main)
