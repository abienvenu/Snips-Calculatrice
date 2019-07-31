#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import io
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions


class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {
            section: {
                option_name: option
                for option_name, option in self.items(section)
            }
            for section in self.sections()
        }


def read_configuration_file():
    try:
        with io.open(
            "config.ini",
            encoding="utf-8"
        ) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error):
        return dict()


def listen_mqtt(intentName, callback):
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent(
            intentName,
            callback
        ).start()


def humaniser(nombre):
    nombre = round(nombre, 4)
    if str(nombre)[-2:] == ".0":
        nombre = int(nombre)
    return nombre


def get_terms(intentMessage):
    firstTerm = humaniser(intentMessage.slots.firstTerm.first().value)
    secondTerm = humaniser(intentMessage.slots.secondTerm.first().value)
    return (firstTerm, secondTerm)
