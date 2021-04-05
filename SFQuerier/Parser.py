##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : Parser.py

import json
from types import SimpleNamespace

def parse(orderedDict):
    if 'records' in orderedDict:
        json_object = json.dumps(orderedDict['records'], indent=2)
    else:
        json_object = json.dumps(orderedDict, indent=2)
    parsed_object = json.loads(json_object, object_hook=lambda d: SimpleNamespace(**d))
    return parsed_object
