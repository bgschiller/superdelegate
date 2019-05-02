superdelegate
=============

**Delegate methods and properties to child objects in a terse, explicit style**

Consider the motivating example of a sorted list. In order to encapsulate the list and prevent clients from breaking the sorted order, we want to only allow certain methods through to the underlying list:

```python
import bisect

class SortedList:
    def __init__(self, *args, **kwargs):
        self._lst = list(*args, **kwargs)

    def insert(self, elem):
        bisect.insort(self._lst, elem)

    def __contains__(self, elem):
        ix = bisect.bisect(self._lst, elem)
        return ix != len(self._lst) and self._lst[ix] == elem

    def __getitem__(self, key):
        return self._lst.__getitem__(key)

    def __reversed__(self):
        return self._lst.__reversed__()

    def __len__(self):
        return self._lst.__len__()

    def __iter__(self):
        return self._lst.__iter__()
```

Much of that code is pretty repetitive. Can we do better? Yes! with superdelegate!

```python
import bisect
from superdelegate import SuperDelegate, delegate_to

class SortedList(SuperDelegate):
    def __init__(self, *args, **kwargs):
        self._lst = list(*args, **kwargs)

    def insert(self, elem):
        bisect.insort(self._lst, elem)

    def __contains__(self, elem):
        ix = bisect.bisect(self._lst, elem)
        return ix != len(self._lst) and self._lst[ix] == elem

    __getitem__ = __reversed__ = __len__ = __iter__ = delegate_to('_lst')
```

### FAQs

**Does it work for properties?** It _does_ work for properties!

```python
class OnlyGrowsOlder:
    def __init__(self):
        self._age

    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, new_age):
        if new_age > self._age:
            self._age = new_age
        else:
            raise ValueError('Time is like a boy band. It only flows in one direction')

class OlderWrapper(SuperDelegate):
    def __init__(self):
        self._ager

    age = delegate_to('_ager')
```

**Can you have multiple delgatees?** You can!

```python
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
```

### Inspiration

This library was inspired by Ruby ActiveSupport's `Module#delegate` extension.