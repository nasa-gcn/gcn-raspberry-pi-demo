#!/usr/bin/env python
import confluent_kafka
import confluent_kafka.admin
import typer
from rich.live import Live
from rich.table import Table, box
from rich.text import Text

COLORS = ["red", "green", "blue"]


def main(
    bootstrap_server: str,
    broker_id: int,
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
        title=f"Broker {broker_id}",
        title_style="bold",
        show_edge=True,
        pad_edge=True,
        collapse_padding=True,
        box=box.DOUBLE_EDGE,
    )
    table.add_column("Topic", width=5)
    table.add_column("Status", width=12)
    labels = [Text() for _ in COLORS]
    for topic, label in zip(COLORS, labels):
        table.add_row(f"[bold {topic}]{topic}", label)

    with Live(table):
        while True:
            for topic, label, future in zip(
                COLORS, labels, admin.describe_topics(topic_collection).values()
            ):
                try:
                    result = future.result()
                except confluent_kafka.KafkaException:
                    label.plain = "unknown"
                else:
                    partition = result.partitions[0]
                    leader = None if partition.leader is None else partition.leader.id
                    isr = {isr.id for isr in partition.isr}
                    if leader == broker_id:
                        label.plain = "leader"
                    elif broker_id in isr:
                        label.plain = "in sync"
                    else:
                        label.plain = "out of sync"


if __name__ == "__main__":
    typer.run(main)
