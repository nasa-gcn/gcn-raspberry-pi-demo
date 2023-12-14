#!/usr/bin/env python
from time import sleep
import random

from rich.table import box, Table
from rich.live import Live
from rich.text import Text


topics = ["red", "green", "blue"]
symbols = "?NY"

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
for topic, row in zip(topics, rows):
    table.add_row(f"[bold {topic}]{topic}", *row)
with Live(table):
    while True:
        for i in range(3):
            for j in range(3):
                rows[i][j].plain = symbols[random.randrange(len(symbols))]
        sleep(0.5)
