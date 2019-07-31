#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib import listen_mqtt, get_terms


def subscribe_intent_callback(hermes, intentMessage):
    (a, b) = get_terms(intentMessage)
    produit = a * b
    result = "{} fois {} font {}".format(a, b, produit)
    hermes.publish_end_session(intentMessage.session_id, result)


if __name__ == "__main__":
    listen_mqtt("abienvenu:getMultiplication", subscribe_intent_callback)
