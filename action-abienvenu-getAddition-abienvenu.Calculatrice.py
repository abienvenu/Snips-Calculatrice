#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib import listen_mqtt, get_terms


def subscribe_intent_callback(hermes, intentMessage):
    (a, b) = get_terms(intentMessage)
    if a == 0 and b == 0:
        result = "zéro plus zéro égal la tête à Toto!"
    else:
        somme = a + b
        result = "{} et {} font {}".format(a, b, somme)
    hermes.publish_end_session(intentMessage.session_id, result)


if __name__ == "__main__":
    listen_mqtt("abienvenu:getAddition", subscribe_intent_callback)
