from composable import pipeable

class Nothing(object):
    """A class representing nothing

    This class allows calling any attribute or calling like a function.
    """
    def __init__(self):
        pass

    def __getattr__(self, name):
        return Nothing()

    def __call__(self, *args, **kwargs):
        return Nothing()

    def __repr__(self):
        return "Nothing()"

    def map(self, func):
        """ Map applies a function to the underlying data, if present.
        
        When mapping a function to Nothing, we return Nothing()
        
        Args.
            - self.  Nothing()
            - func. A single argument function to be applied. If the underlying data is type
                    A, then `func` should be type `Callable[A, B]`, that is it should be designed
                    to work with the underlying data.
            
        Returns.  Nothing().
        """
        return Nothing()
    
    def and_then(self, func):
        """ Apply a function that returns Optional values.
        
        When chaining a function with `and_then` to Nothing, we return Nothing()
        
        Args.
            - self.  Nothing()
            - func. A single argument function to be applied. If the underlying data is type
                    A, then `func` should be type `Callable[A, Optional[B]`, that is it should be designed
                    to work with the underlying data.
            
        Returns.  Nothing().
        """
        return Nothing()


class Just(object):
    """A class representing a non-missing value

    Any attribute or call will be passed to the underlying object.
    """
    def __init__(self, just):
        self.just = just

    def __getattr__(self, name):
        return Just(getattr(self.just, name))

    def __call__(self, *args, **kwargs):
        return Just(self.just(*args, **kwargs))

    def __repr__(self):
        return f"Just({self.just.__repr__()})"

    def map(self, func):
        """ Map applies a function to the underlying data, if present.
        
        When mapping a function to Just(x), we return Just(func(x))
        
        Args.
            - self. Just(x)
            - func. A single argument function to be applied. If the underlying data is type
                    A, then `func` should be type `Callable[A, B]`, that is it should be designed
                    to work with the underlying data.
            
        Returns.  Just(func(x)).
        """
        return Just(func(self.just))
    
    def and_then(self, func):
        """ Apply a function that returns Optional values.
        
        When chaining a function with `and_then` to Just(x), we return Nothing() if func(x) is None,
        otherwise return Just(x).  This function is useful for clean chaining of functions with Optional return values.
        
        Args.
            - self.  Just(x)
            - func. A single argument function to be applied. If the underlying data is type
                    A, then `func` should be type `Callable[A, Optional[B]`, that is it should be designed
                    to work with the underlying data.
            
        Returns.  Just(func(x)) if func(x) is not None else Nothing().
        """
        return func(self.just)



# The maybe type, which is an alternative to Optional and 
# Can be thought of as an applicative maybe monad.
Maybe = Nothing | Just

@pipeable
def maybe(value):
    """ Wraps a value  `Just` or returns `Nothing()` in place of `None`

    Args:
        value (Optional[T]): Any value that is either None or of type T
    
    Returns (Maybe): Just(value) or Nothing()
    """
    return Nothing() if value is None else Just(value)

@pipeable
def unmaybe(value, *, default = None):
    """ Extracts the optional value from an object of type Maybe

    This function is the inverse of maybe.

    Args:
        value (Maybe): Returns value for Just(value) or None for Nothing()

    Returns:
        Optional(T): Returns the value wrapped by Just(value) or None 
    """
    return value.just if isinstance(value, Just) else default

_built_in_map = map

@pipeable
def map(func, value):
    """Maybes a functions to the value, when it exists

    Args:
        func (Callable[T, S]): A function that takes one argument of type T and returns an object of type S.
        value (Maybe[T]): An optional value

    Returns:
        Maybe[T]: Returns the result of applying `func` to the optional value, or Nothing()
    """
    return value.map(func)

# @pipeable
# def and_then(func, value):
#     """Maybes a functions to the value, when it exists

#     Args:
#         func (Callable[T, Optional[S]]): A function that takes one argument of type T and returns an object of type Optional[S].
#         value (Maybe[T]): An optional value

#     Returns:
#         Maybe[T]: Returns Nothing() if the original value is Nothing() or func(x) is None, otherwise returns Just(func(x))
#     """
#     return value.and_then(func)

@pipeable
def just_if(pred, value):
    """Apply a filter to optional objects and keep just the values that pass.

    Any value that (A) is Nothing() or (B) whose wrapped value fails the test return Nothing().

    Args:
        pred (Callable[T, bool]): A predicate functions for object of the wrapped type.
        value (Maybe[T]): A wrapped optional value (Nothing() or Just(val))

    Returns:
        Maybe[T]: returns Just(val) if pred(val) otherwise Nothing() [pred(val) is false or value is Nothing()]
    """
    if isinstance(value, Just) and pred(value.just):
        return value
    else:
        return Nothing()

@pipeable
def try_(func, value):
    """Trys to apply a function to an optional wrapped value and returns Nothing() on any exception.

    Args:
        func (Callable[T, S]): A function applied to the optional wrapped value that may through an exception.
        value (Maybe[T]): An optional wrapped value

    Returns:
        Maybe[T]: Returns Just(func(val)) when (A) the optional val exists and (B) func(val) doesn't throw an exception, returning Nothing() otherwise.
    """
    try:
        return Just(func(value.just))
    except:
        return Nothing()

@pipeable
def is_just(value):
    """Determines if an optional wrapped value exists."""
    return isinstance(value, Just)

@pipeable
def is_nothing(value):
    """Determines if an optional wrapped value is missing."""
    return isinstance(value, Nothing)

