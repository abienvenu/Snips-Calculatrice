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


def humaniser(nombre):
    nombre = round(nombre, 4)
    if str(nombre)[-2:] == ".0":
        nombre = int(nombre)
    return nombre


def get_terms(slots):
    firstTerm = humaniser(slots.firstTerm.first().value)
    secondTerm = humaniser(slots.secondTerm.first().value)
    return (firstTerm, secondTerm)


def addition(a, b):
    if a == 0 and b == 0:
        return "zéro plus zéro égal la tête à Toto!"
    else:
        somme = a + b
        return "{} et {} font {}".format(a, b, somme)


def soustraction(a, b):
    difference = a - b
    return "{} moins {} font {}".format(a, b, difference)


def multiplication(a, b):
    produit = a * b
    return "{} fois {} font {}".format(a, b, produit)


def division(a, b):
    if b == 0:
        return "Diviser par zéro n'est pas possible"
    else:
        resultat = humaniser(a / b)
        return "{} divisé par {} égal {}".format(a, b, resultat)


def intent_callback(hermes, intentMessage):
    functions = {
        "getAddition": addition,
        "getSoustraction": soustraction,
        "getMultiplication": multiplication,
        "getDivision": division
    }

    f = functions.get(
        intentMessage.intent.intent_name.replace("abienvenu:", "")
    )
    if f:
        (a, b) = get_terms(intentMessage.slots)
        result = f(a, b)
        hermes.publish_end_session(intentMessage.session_id, result)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intents(intent_callback).start()
