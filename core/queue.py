# simple mocking for decoupling things.
# this entire module should became a facade for celery.


def add(_callable, *args, **kwargs):
    # this should be executed from a celery queue.
    _callable(*args, **kwargs)

