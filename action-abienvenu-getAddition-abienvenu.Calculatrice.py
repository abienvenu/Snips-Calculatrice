#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib import read_configuration_file, integeriser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions

CONFIG_INI = "config.ini"


def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


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
