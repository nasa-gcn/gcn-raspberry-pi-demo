#!/usr/bin/env python
import confluent_kafka
import confluent_kafka.admin
from rich.table import box, Table
from rich.live import Live
from rich.text import Text
import typer

COLORS = ["red", "green", "blue"]


def main(
    bootstrap_server: str,
):
    admin = confluent_kafka.admin.AdminClient(
        {
            "bootstrap.servers": bootstrap_server,
            "socket.timeout.ms": 500,
            "reconnect.backoff.max.ms": 1000,
            "topic.metadata.refresh.interval.ms": 500,
            "metadata.max.age.ms": 1000,
        }
    )

    topic_collection = confluent_kafka.TopicCollection(COLORS)

    table = Table(
        width=15,
        title="Brokers",
        title_justify="right",
        caption="Topic in sync:\n[bold]L[/bold]eader, [bold]Y[/bold]es, [bold]N[/bold]o",
        caption_style="gray italic",
        title_style="bold",
        show_edge=False,
        pad_edge=False,
        expand=True,
        collapse_padding=True,
        box=box.SIMPLE,
    )
    table.add_column("Topics")
    table.add_column("1")
    table.add_column("2")
    table.add_column("3")
    rows = [[Text() for _ in range(3)] for __ in range(3)]
    for topic, row in zip(COLORS, rows):
        table.add_row(f"[bold {topic}]{topic}", *row)

    with Live(table):
        while True:
            for topic, row, future in zip(
                COLORS, rows, admin.describe_topics(topic_collection).values()
            ):
                try:
                    result = future.result()
                except confluent_kafka.KafkaException:
                    for cell in row:
                        cell.plain = "?"
                else:
                    partition = result.partitions[0]
                    leader = None if partition.leader is None else partition.leader.id
                    isr = {isr.id for isr in partition.isr}
                    for i, cell in enumerate(row):
                        if i + 1 == leader:
                            cell.plain = "L"
                        elif i + 1 in isr:
                            cell.plain = "Y"
                        else:
                            cell.plain = "N"


if __name__ == "__main__":
    typer.run(main)
