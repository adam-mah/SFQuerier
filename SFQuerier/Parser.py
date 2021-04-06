##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : Parser.py

import json
from types import SimpleNamespace


def parse(orderedDict, indent=2):
    if 'records' in orderedDict:
        json_object = json.dumps(orderedDict['records'], indent=indent)
    else:
        json_object = json.dumps(orderedDict, indent=indent)
    parsed_object = json.loads(json_object, object_hook=lambda d: SimpleNamespace(**d))
    return parsed_object
