import json
import datetime
import pytest
import six
from uuid import uuid4
from decimal import Decimal


def j(v):
    return json.loads(json.dumps(v))


@pytest.mark.skipif(six.PY2, reason='py3 required')
def test_enum():
    import enum

    class E(enum.Enum):
        a = 'aa'
        b = 'bb'
        c = 'cc'

    assert j(E['a']) == 'aa'


def test_generator():
    def gen():
        for n in range(5):
            yield n
    assert j(gen()) == [0, 1, 2, 3, 4]
    assert j((int(i) for i in ('1', '2', '3'))) == [1, 2, 3]


@pytest.mark.skipif(six.PY2, reason='py3 required')
def test_mapping_proxy_type():
    from types import MappingProxyType
    assert j(MappingProxyType({'a': 1, 'b': 2})) == {'a': 1, 'b': 2}


def test_set():
    assert sorted(j({1, 2, 3})) == [1, 2, 3]


def test_frozenset():
    assert sorted(j(frozenset({1, 2, 3}))) == [1, 2, 3]


def test_reversed_iterator():
    assert j(reversed(range(5))) == [4, 3, 2, 1, 0]
    assert j(reversed(list(range(5)))) == [4, 3, 2, 1, 0]


def test_datetime():
    assert j(datetime.date(2018, 1, 28)) == '2018-01-28'
    assert j(datetime.datetime(2018, 1, 28, 17, 13, 15)) == '2018-01-28T17:13:15'


@pytest.mark.skipif(six.PY2, reason='py3 required')
def test_chainmap():
    from collections import ChainMap
    assert j(ChainMap({'a': 1, 'b': 2})) == {'a': 1, 'b': 2}


@pytest.mark.skipif(six.PY2, reason='py3 required')
def test_userdict():
    from collections import UserDict
    assert j(UserDict({'a': 1, 'b': 2})) == {'a': 1, 'b': 2}


@pytest.mark.skipif(six.PY2, reason='py3 required')
def test_userlist():
    from collections import UserList
    assert j(UserList(range(5))) == [0, 1, 2, 3, 4]


def test_map_iterator():
    assert j(map(int, ('1', '2', '3'))) == [1, 2, 3]


def test_filter_iterator():
    assert j(filter(None, ('1', '2', 0, '3'))) == ['1', '2', '3']


def test_range_iterator():
    assert j(range(5)) == [0, 1, 2, 3, 4]


def test_dict_item_iterator():
    d = {'a': 1, 'b': 2}
    assert sorted(j(six.iteritems(d))) == [['a', 1], ['b', 2]]
    assert sorted(j(six.viewitems(d))) == [['a', 1], ['b', 2]]


def test_dict_key_iterator():
    d = {'a': 1, 'b': 2}
    assert sorted(j(six.iterkeys(d))) == ['a', 'b']
    assert sorted(j(six.viewkeys(d))) == ['a', 'b']


def test_dict_value_iterator():
    d = {'a': 1, 'b': 2}
    assert sorted(j(six.itervalues(d))) == [1, 2]
    assert sorted(j(six.viewvalues(d))) == [1, 2]


def test_uuid():
    u = uuid4()
    assert j(u) == str(u)


def test_decimal():
    assert j(Decimal('15.01')) == '15.01'


@pytest.mark.skipif(six.PY2, reason='py3 required')
def test_pathlib_path():
    from pathlib import Path
    assert j(Path('/home')) == '/home'


def test_nested():
    v = (x for x in (
        datetime.datetime(2018, 1, 28, 17, 13, 15),
        Decimal('15.01'),
    ))
    assert j(v) == [
        '2018-01-28T17:13:15',
        '15.01',
    ]
