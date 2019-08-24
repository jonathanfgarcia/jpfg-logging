import fluent.asyncsender

import collections
import getpass
import inspect
import logging
import os
import socket
import time

class EventLogger(fluent.asyncsender.FluentSender):
    """A structured event logger for Fluentd. """
    
    def __init__(self, name, host="localhost", port=24224, nanosecond_precision=True):
        """Initializes the EventLogger."""
        fluent.asyncsender.FluentSender.__init__(
            self,
            "fluentd",
            host=host,
            port=port,
            nanosecond_precision=nanosecond_precision
        )
        self._name = name or "root"

    def __del__(self):
        """The EventLogger's destructor. Called when the instance is about to be destroyed."""
        self.close()

    def log(self, log_level, event_or_message=None, **kwargs):
        """Emits an event log with the given `log_level`."""
        # capture the current time
        now = time.time()

        # determine the caller's frame
        caller_stack = 1
        if "__caller_stack" in kwargs:
            caller_stack = kwargs.pop("__caller_stack")
        caller_frame = inspect.stack()[caller_stack]
        caller_module = inspect.getmodule(caller_frame.frame)

        # build the event structure
        event = {
            'user': {
                'uid': os.getuid(),
                'gid': os.getgid(),
                'login': getpass.getuser()
            },
            'host': {
                'name': socket.gethostname(),
                'address': socket.gethostbyname(socket.gethostname())
            },
            'log': {
                'level': log_level,
                'name': logging.getLevelName(log_level)
            },
            'where': {
                'module': caller_module and caller_module.__name__,
                'function': caller_frame.function,
                'lineNumber': caller_frame.lineno,
                'filePath': caller_frame.filename
            },
            'event': dict()
        }
        event['event'].update(kwargs)
        if isinstance(event_or_message, collections.Mapping):
            event['event'].update(event_or_message)
        else:
            event['event']["message"] = event_or_message

        # emit the event log with a timestamp
        self.emit_with_time(self._name, now, event)

    def critical(self, event_or_message=None, **kwargs):
        """Emits an event log with level CRITICAL."""
        kwargs.update({"__caller_stack": 2})
        self.log(logging.CRITICAL, event_or_message, **kwargs)

    def debug(self, event_or_message=None, **kwargs):
        """Emits an event log with level DEBUG."""
        kwargs.update({"__caller_stack": 2})
        self.log(logging.DEBUG, event_or_message, **kwargs)

    def error(self, event_or_message=None, **kwargs):
        """Emits an event log with level ERROR."""
        kwargs.update({"__caller_stack": 2})
        self.log(logging.ERROR, event_or_message, **kwargs)

    def info(self, event_or_message=None, **kwargs):
        """Emits an event log with level INFO."""
        kwargs.update({"__caller_stack": 2})
        self.log(logging.INFO, event_or_message, **kwargs)

    def warning(self, event_or_message=None, **kwargs):
        """Emits an event log with level WARNING."""
        kwargs.update({"__caller_stack": 2})
        self.log(logging.WARNING, event_or_message, **kwargs)
