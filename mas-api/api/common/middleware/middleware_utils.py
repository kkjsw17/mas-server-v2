from fastapi import Request
from starlette.types import Message


class AsyncIteratorWrapper:
    """The following is a utility class that transforms a
    regular iterable to an asynchronous one.

    link: https://www.python.org/dev/peps/pep-0492/#example-2
    """

    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


async def set_body(request: Request):
    """
    Avails the response body to be logged within a middleware as,

    Args:
        request (Request)
    """
    receive_ = await request._receive()

    async def receive() -> Message:
        return receive_

    request._receive = receive
