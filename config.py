#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""configuration for jmoiron.net"""

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = "mongodb://localhost:21071/jmoiron"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

