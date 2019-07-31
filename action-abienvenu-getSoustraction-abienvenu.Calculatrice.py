#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib import listen_mqtt, get_terms


def subscribe_intent_callback(hermes, intentMessage):
    (a, b) = get_terms(intentMessage)
    difference = a - b
    result = "{} moins {} font {}".format(a, b, difference)
    hermes.publish_end_session(intentMessage.session_id, result)


if __name__ == "__main__":
    listen_mqtt("abienvenu:getSoustraction", subscribe_intent_callback)
