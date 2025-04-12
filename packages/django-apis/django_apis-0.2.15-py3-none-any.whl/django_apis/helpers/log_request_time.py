import time
import logging
from .base import ApiviewHelperBase

__all__ = [
    "log_request_time",
]
_logger = logging.getLogger(__name__)


class log_request_time(ApiviewHelperBase):
    def __init__(self, logger=None, level=logging.WARNING):
        self.level = level
        if logger is None:
            self.logger = _logger
        elif isinstance(logger, str):
            self.logger = logging.getLogger(logger)
        else:
            self.logger = logger

    def get_response(self, view, request, **kwargs):
        stime = time.time()
        response = super().get_response(view, request, **kwargs)
        delta = time.time() - stime
        self.logger.log(self.level, f"{request.path} {delta:0.6f}")
        return response
