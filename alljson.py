#!/usr/bin/env python3
import json
import abc
import inspect
import six
from operator import attrgetter


_encoders = {}


@six.add_metaclass(abc.ABCMeta)
class JSONEncodable(object):
    pass


class CustomizableEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(CustomizableEncoder, self).default(obj)
        except TypeError:
            klass = type(obj)
            if not issubclass(klass, JSONEncodable):
                raise
            encoder = _encoders.get(klass)
            if encoder is not None:
                return encoder(obj)
            for base in inspect.getmro(klass):
                encoder = _encoders.get(base)
                if encoder is not None:
                    return encoder(obj)
            raise


json._default_encoder = CustomizableEncoder(
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    default=None
)


def register_encoder(klass, func):
    JSONEncodable.register(klass)
    _encoders[klass] = func


def _register_common_types():
    from types import GeneratorType
    from uuid import UUID
    from decimal import Decimal
    import datetime

    register_encoder(GeneratorType, list)
    register_encoder(type(reversed([])), list)
    register_encoder(set, list)
    register_encoder(frozenset, list)
    register_encoder(type(six.iteritems({})), list)
    register_encoder(type(six.iterkeys({})), list)
    register_encoder(type(six.itervalues({})), list)
    register_encoder(type(six.viewitems({})), list)
    register_encoder(type(six.viewkeys({})), list)
    register_encoder(type(six.viewvalues({})), list)
    register_encoder(UUID, str)
    # note that decimals are represented as strings, not floats in
    # order to preserve precision
    register_encoder(Decimal, str)
    register_encoder(datetime.date, datetime.date.isoformat)
    register_encoder(datetime.datetime, datetime.datetime.isoformat)

    if six.PY3:
        import enum
        from types import MappingProxyType
        from collections.abc import Mapping, Sequence
        from pathlib import Path

        register_encoder(type(reversed(range(1))), list)
        register_encoder(map, list)
        register_encoder(filter, list)
        register_encoder(range, list)
        register_encoder(Sequence, list)
        register_encoder(Mapping, dict)
        register_encoder(MappingProxyType, dict)
        register_encoder(enum.Enum, attrgetter('value'))
        register_encoder(Path, str)


_register_common_types()
