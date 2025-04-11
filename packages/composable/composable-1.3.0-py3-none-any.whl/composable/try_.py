
from composable import pipeable

class Error(object):
    """A class an exception caused when applying a function. 

    This class is a data structure meant to hold information about an exception, allowing 
    the computation to proceed without halting.  In particular, it is designed for exceptions 
    that are caused by applying either functions or method calls.


    """
    def __init__(self, offending_value, error):
        self.offending_value = offending_value
        self.error = error

    def __getattr__(self, name):
        return Error(self.offending_value, self.error)

    def __call__(self, *args, **kwargs):
        return Error(self.offending_value, self.error)

    def __repr__(self):
        return f"Error({self.offending_value}, {self.error})"

    def map(self, func):
        """ Map applies a function to the underlying data, if present and captures any exception.
        
        When mapping a function to an Error, we return the Error [e.g., no additional effect]
        
        Args.
            - self.  Error(val, err)
            - func. A single argument function to be applied. If the underlying data is type
                    A, then `func` should be type `Callable[A, B]`, that is it should be designed
                    to work with the underlying data.
            
        Returns.  Error(val, err)
        """
        return Error(self.offending_value, self.error)
    
    def and_then(self, func):
        """ Apply a function that returns values if type Result[T]|Error[T, Exception].
        
        When chaining a function with `and_then` to an Error, we return an Error
        
        Args.
            - self.  Error(val, err)
            - func. A single argument function to be applied. If the underlying data is type
                    A, then `func` should be type `Callable[A, Result[B]|Error[A, Exception]`, 
                    that is it should be designed to work with the underlying data and possible 
                    return an Error.
            
        Returns.  Error(val, err)
        """
        return Error(self.offending_value, self.error)


class Result(object):
    """A class representing a non-missing value

    Any attribute or call will be passed to the underlying object.
    """
    def __init__(self, value):
        self.value = value

    def __getattr__(self, name):
        """ Result passes method/attribute access along to the underlying value."""
        try:
            if hasattr(self.value, '__getattr__'):
                return Result(self.value.__getattr__(name))
            else:
                return Result(self.value.__getattribute__(name))

        except Exception as e:
            return Error(self.value, e)

    def __call__(self, *args, **kwargs):
        """ Result passes method/function-like calls along to the underlying value."""
        try:
            return Result(self.value(*args, **kwargs))
        except Exception as e:
            return Error(self.value, e)

    def __repr__(self):
        return f"Result({self.value})"

    def map(self, func):
        """ Map applies a function to the underlying data, if present.
        
        When mapping a function to Just(x), we return Just(func(x))
        
        Args.
            - self. Just(x)
            - func. A single argument function to be applied. If the underlying data is type
                    A, then `func` should be type `Callable[A, B]`, that is it should be designed
                    to work with the underlying data.
            
        Returns.  Error(x, err) when func(x) throws an exception err, otherwise returns Result(func(x)).
        """
        try:
            return Result(func(self.value))
        except Exception as err:
            return Error(self.value, err)
    
    def and_then(self, func):
        """ Apply a function that returns values of type Result[B]| Error[A, Exception]
        
        When chaining a function with `and_then` to Result(x), we return an Error if an exception is thrown or if func(x) 
        returns an Error, otherwise return Result(func(x)).  This function is capturing complex logic with potential errors,
        and in particular allows the user to tailor the Error output.
        
        Args.
            - self.  Result(x)
            - func. A single argument function to be applied. If the underlying data is type
                    A, then `func` should be type `Callable[A, Result[B]|Error[A, E]`, that is it should be designed
                    to work with the underlying data and return either the Result or an Error.
            
        Returns.  The output of func(x) or Error(x, err) if func(x) throws an exception.
        """
        try:
            output = func(self.value)
            assert isinstance(output, Result) or isinstance(output, Error), "and_then should return a value of type Result|Error"
            return output
        except Exception as err:
            return Error(self.value, err)



# The Try type, which is an data-centric alternative try-except statement. 
# Can be thought of as an applicative maybe monad.
Try = Error | Result

@pipeable
def wrap_result(value):
    """ Wraps a value  in `Result`

    Put your data in a box that will capture any subsequent errors as data instead of halting execution.

    Args:
        value: Any value of type T
    
    Returns: Result(value).
    """
    return Result(value)

@pipeable
def get_results(value, *, error_handler = lambda x: None):
    """ Extracts the successful resulting values from an object of type Try, or applies an error handler to any errors.

    Use this to extract results from a computation captured by Try, and handle any resulting exceptions.

    Args:
        value (Try): Returns value for Result(value) or error_handler(err) for any error.
        error_handler: A function for handling any Error results [Default returns None] 

    Returns:  The value wrapped by Result(value) or the output of the error_handler (default None)
    """
    return value.value if isinstance(value, Result) else error_handler(value)

_built_in_map = map

@pipeable
def map(func, value):
    """Map a functions to the underlying value, and capture any error as type Error

    Args:
        func (Callable[T, S]): A function that takes one argument of type T and returns an object of type S.
        value (Try[T, E]): An optional value

    Returns:
        Try[T, E]: Returns the result of applying `func` to the underlying value, or an Error object containing
        information about any current or previous exception.
    """
    return value.map(func)

@pipeable
def and_then(func, value):
    """Chain a function to the underlying value, or capture/pass-along data on any exception.

    This function is useful when chaining together functions tailored to capture any exception returned 
    as a user-defined Error object.

    Args:
        func (Callable[T, Try[S, E]]): A function that takes one argument of type T and returns an object of type Optional[S].
        value (Try[T, E]): The incoming resulting value or information about a incoming exception.

    Returns:
        Try[S, E]: The outgoing resulting value or information about a current/previous exception.
    """
    return value.and_then(func)