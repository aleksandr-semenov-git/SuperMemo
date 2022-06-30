import functools


def mocktracker(func):
    """Decorator which track some information about the testing func:

     if func was called
     save args
     save kwargs
     save result of the func (Mock obj)
     """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.has_been_called = True
        wrapper.call_args_list = args
        wrapper.call_kwargs_list = kwargs
        catch_mock = func(*args, **kwargs)
        wrapper.mock_obj = catch_mock
        return catch_mock
    wrapper.has_been_called = False
    return wrapper
