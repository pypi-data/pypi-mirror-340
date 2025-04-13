#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File    : __init__.py
from .z0scan import modulePath
import sys
import os

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
modulePath = modulePath()