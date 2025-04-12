import logging
import functools

__all__ = [
    "ApiviewHelperBase",
]


class ApiviewHelperBase(object):
    def __call__(self, view):
        def inner_view(request, **kwargs):
            response = self.get_response(view, request, **kwargs)
            return response

        return functools.wraps(view)(inner_view)

    def get_response(self, view, request, **kwargs):
        response = view(request, **kwargs)
        return response
