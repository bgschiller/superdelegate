import pytest
from . import delegate_to, SuperDelegate, BadDelegateSetup

def test_missing_metaclass_causes_explanatory_error():
    class IncorrectUsage:
        x = delegate_to('child')
    iu = IncorrectUsage()
    with pytest.raises(BadDelegateSetup):
        iu.x('any args', even='keywords')

def test_delegated_method_arrives_at_child():
    class ImmutableList(SuperDelegate):
        def __init__(self, lst):
            self._lst = lst

        __getitem__ = __len__ = __iter__ = delegate_to('_lst')

    fruits = ImmutableList(['apple', 'banana', 'pineapple'])
    assert len(fruits) == 3
    # we should be able to iterate over the ImmutableList
    for f in fruits:
        pass
    assert fruits[1] == 'banana'

def test_property_access_can_also_be_delegated():
    class DefinesProps:
        def __init__(self):
            self._name = 'Logan'
            self._age = 12

        @property
        def name(self):
            return self._name

        @property
        def age(self):
            return self._age
        @age.setter
        def age(self, age):
            self._age = age

    class Container(SuperDelegate):
        def __init__(self):
            self._prop_holder = DefinesProps()

        name = delegate_to('_prop_holder')
        age = delegate_to('_prop_holder')

    example = Container()
    assert example.name == 'Logan'
    assert example.age == 12
    example.age = 14
    assert example.age == 14
    assert example._prop_holder.age == 14

    # name has no setter
    with pytest.raises(AttributeError):
        example.name = 'Allan'


def test_multiple_delegates_do_not_conflict():
    class SandwichMaker:
        def choose_cheese(self):
            return 'swiss'
    class NavyEngineer:
        def lift_periscope(self):
            return 'done'
    class SubmarineTechnician(SuperDelegate):
        def __init__(self):
            self.sm = SandwichMaker()
            self.ne = NavyEngineer()

        choose_cheese = delegate_to('sm')
        lift_periscope = delegate_to('ne')

    st = SubmarineTechnician()
    assert st.choose_cheese() == 'swiss'
    assert st.lift_periscope() == 'done'

def test_sorted_list_example():
    import bisect

    class SortedList(SuperDelegate):
        def __init__(self, *args, **kwargs):
            self._lst = list(*args, **kwargs)

        def insert(self, elem):
            bisect.insort(self._lst, elem)

        def __contains__(self, elem):
            ix = bisect.bisect(self._lst, elem)
            return ix != len(self._lst) and self._lst[ix] == elem

        __getitem__ = __reversed__ = __len__ = __iter__ = delegate_to('_lst')

    lst = SortedList()

    for x in (4, 5, 2, 12, 9):
        lst.insert(x)

    for x in lst:
        pass

    assert len(lst) == len(lst._lst)
    assert lst[0] == 2
    with pytest.raises(TypeError):
        lst[0] = 10  # pylint: disable=unsupported-assignment-operation
