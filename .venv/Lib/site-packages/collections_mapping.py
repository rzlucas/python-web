#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def load(file, serializer=json, **kwargs):
    return Mapping.load(file, serializer=serializer, **kwargs)

class Mapping(dict):

    def __init__(self, mapping=None, **kwargs):
        super().__init__(**kwargs)
        if mapping is not None:
            self.update(mapping)

    def __missing__(self, key):
        return None

    def __dict__(self):
        return dict(self)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __copy__(self):
        return self.copy()

    def copy(self):
        instance = self.__class__.__new__(self.__class__)
        instance.update(self)
        return instance

    @classmethod
    def load(cls, file, serializer=json, **kwargs):
        try:
            with open(file, 'rt') as f:
                mapping = serializer.load(f, **kwargs)
            return cls(mapping)
        except:
            raise

    def dump(self, file, serializer=json, **kwargs):
        try:
            with open(file, 'wt') as f:
                serializer.dump(self, f, **kwargs)
        except:
            raise
