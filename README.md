# esp-rfid-py
Firmware for property access systems for common microcontrollers like ESP8266.

Inspired by [ESP-RFID](https://github.com/esprfid/esp-rfid), written in Micro Python ((Pycopy)[https://github.com/pfalcon/pycopy] fork).

## Status

This project is in experimental stage.

Compared to official [ESP-RFID firmware](https://github.com/esprfid/esp-rfid) lacks a lot of elementary features. Implemented features needs testing, but even at this stage should have less bugs.

## Features

- Supports multiple Wiegand readers
- Supports multiple relays with different configurations
- Master card - use "admin" tag to add new tags
- Can run on all [platforms supported by MicroPython](http://www.micropython.org/download) (theoretically, tested on ESP8266 and ESP32)
- Can be controlled and send logs over MQTT
- HTTP API
- MQTT client (access log, heartbeat, open, cards management)
- Cards import and export to JSON by REPL

Complete list of features is in [example config file](src/example.config.py).

## Goals

Scalable and reliable modular, events-based and asynchronous architecture which allows:

- enable only needed features by plugins
- code being less bug prone
- easy coding of new features (e.g. integrations to bigger systems)
- thanks to Python the code is much easier to read and maintain

## Current disadvantages

- Missing features and worse usability compared to ESP-RFID for now - it have to be configured in config files and database managed in REPL by calling Python API.
- MicroPython consumes much more RAM, so some features will be almost impossible on ESP8266 (embedded web interface).
- Will not support a many plugins enabled at one time (because of RAM).
- Missing compatibility with ESP-RFID export files (because current MicroPython Wiegand library encodes data differently).
