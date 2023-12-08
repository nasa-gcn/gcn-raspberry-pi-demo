#!/usr/bin/env python
import threading
from typing import Annotated, Literal
from uuid import uuid4

import confluent_kafka
import curtsies
from curtsies.fmtfuncs import bold, fmtstr
import randomname
import typer
import RPi.GPIO as GPIO

COLORS = {'red', 'green', 'blue'}

# GPIO pins for the push button
BUTTON_PIN = 40

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel, producer, color):
    if GPIO.input(channel) == GPIO.HIGH:
        #print(f"Button on GPIO {channel} pressed.")
        produce_message(producer, color)

def keypress_callback(e, producer, color):
    if isinstance(e, str) and len(e) == 1:
        #print(f"Key '{e}' pressed. Displaying message.")
        produce_message(producer, color)

def produce_message(producer, color):
    value = randomname.get_name()
    text = fmtstr(
        bold(f'[{color}]') + f' produced "{value}"',
        style=color)
    producer.produce(color, value)
    print(text)

def consume_messages(consumer):
    while True:
        for message in consumer.consume():
            topic = message.topic()
            text = fmtstr(
                bold(f'[{topic}]') + ' consumed "'
                + (message.error() or message.value().decode()) + '"',
                style=topic)
            print(text)

def main(
        bootstrap_server: Annotated[str, typer.Option()],
        color: Annotated[str, typer.Option()],
        input_method: str = typer.Option(default="keypress", help="Choose 'keypress' or 'button'"),
        bouncetime: int = typer.Option(default=300, help="Bounce time for the button in milliseconds"), # bouncetime: Duration (in ms) during which button's state is ignored
):
    if input_method not in ['keypress', 'button']:
        raise typer.BadParameter("Input method must be either 'keypress' or 'button'.")
    
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

    threading.Thread(target=lambda: consume_messages(consumer)).start()

    if input_method == "button":
        setup_gpio()
        GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=lambda ch: button_callback(ch, producer, color), bouncetime=bouncetime)
        print(f"Monitoring buttons on GPIO {BUTTON_PIN}.")

    elif input_method == "keypress":
        with curtsies.Input() as keypresses:
            for key_event in keypresses:
                keypress_callback(key_event, producer, color)
                    

if __name__ == "__main__":
    typer.run(main)

