#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import io
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {
            section: {
                option_name: option
                for option_name, option in self.items(section)
            }
            for section in self.sections()
        }


def read_configuration_file(configuration_file):
    try:
        with io.open(
            configuration_file,
            encoding=CONFIGURATION_ENCODING_FORMAT
        ) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error):
        return dict()


def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def integeriser(nombre):
    if str(nombre)[-2:] == ".0":
        nombre = int(nombre)
    return nombre


def action_wrapper(hermes, intentMessage, conf):
    firstTerm = integeriser(intentMessage.slots.firstTerm.first().value)
    secondTerm = integeriser(intentMessage.slots.secondTerm.first().value)
    somme = firstTerm + secondTerm
    result = "{} et {} font {}".format(firstTerm, secondTerm, somme)
    hermes.publish_end_session(intentMessage.session_id, result)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent(
            "abienvenu:getAddition",
            subscribe_intent_callback
        ).start()
