#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib import listen_mqtt, get_terms, humaniser


def subscribe_intent_callback(hermes, intentMessage):
    (a, b) = get_terms(intentMessage)
    if b != 0:
        resultat = humaniser(a / b)
        result = "{} divisé par {} égal {}".format(a, b, resultat)
    else:
        result = "Diviser par zéro n'est pas possible"
    hermes.publish_end_session(intentMessage.session_id, result)


if __name__ == "__main__":
    listen_mqtt("abienvenu:getDivision", subscribe_intent_callback)
