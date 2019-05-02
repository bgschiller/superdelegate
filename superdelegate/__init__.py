class BadDelegateSetup(RuntimeError):
    pass

class delegate_to:
    def __init__(self, prop):
        self.prop = prop

    def __call__(self, *args, **kwargs):
        raise BadDelegateSetup('Incorrect use of `delegate_to`. Did you forget to include `SuperDelegate` as a base class?')

def make_property(delegatee_name, key):
    def getter(self):
        delegatee = getattr(self, delegatee_name)
        delegated_attr = getattr(delegatee, key)
        return delegated_attr
    def setter(self, val):
        delegatee = getattr(self, delegatee_name)
        setattr(delegatee, key, val)
    return property(getter, setter)

class SuperDelegateMeta(type):
    def __new__(meta, name, bases, dct):
        delegates = [(k, v) for k, v in dct.items() if isinstance(v, delegate_to)]
        for k, v in delegates:
            dct[k] = make_property(v.prop, k)
        return super(SuperDelegateMeta, meta).__new__(meta, name, bases, dct)

class SuperDelegate(metaclass=SuperDelegateMeta):
    pass
