#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"


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


def integeriser(nombre):
    if str(nombre)[-2:] == ".0":
        nombre = int(nombre)
    return nombre
