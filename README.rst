alljson
=======

.. image:: https://travis-ci.org/mbachry/alljson.svg?branch=master
    :alt: Build status
    :target: https://travis-ci.org/mbachry/alljson

Make any type JSON-serializable.

A Python module which makes ``json.dumps`` work with several builtin
and stdlib types. A hook for registering any custom type is also
provided.

Installing
----------

Simply install ``alljson`` with pip or add it to your project dependencies::

    pip install alljson

Supported types
---------------

After installing, the following types are JSON-serializable:

* generators

* ``set`` and ``frozenset``

* ``dict`` item/key/value iterators and views

* ``datetime.date`` and ``datetime.datetime`` (as strings in ISO format)

* ``uuid.UUID``

* ``decimal.Decimal`` (serialized as string in order to preserve precision)

* ``reversed`` results

In addition to these, the following Python 3 types are supported:

* ``map``, ``filter``, ``range`` iterators

* ``enum.Enum``

* ``pathlib.Path``

* ``types.MappingProxyType``

* classes implementing ``Sequence`` and ``Mapping`` abc interfaces

Registering custom types
------------------------

In order to register a new type, use ``alljson.register_encoder(type,
encoder_function)``. ``encoder_function`` should take object of given
type as the only parameter and return a simple JSON-serializable
Python value (such as ``dict`` or ``str``).

For example::

    import arrow
    import alljson

    alljson.register_encoder(arrow.Arrow, arrow.Arrow.isoformat)

Acknowledgements
----------------

* pth trick was stolen from delightful `future-fstrings`_ project

.. _future-fstrings: https://github.com/asottile/future-fstrings
