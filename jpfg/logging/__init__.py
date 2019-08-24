from jpfg.logging.eventlogger import EventLogger

CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
NOTSET = 0

def getEventLogger(name=None, host='localhost', port=24224):
    """Returns an EventLogger for structed event logging.
    
    The optional host and port parameters are used to forward messages to the centralized fluentd
    server at the specified `$host:$port`."""
    return EventLogger(name, host, port)

def critical(name, event_or_message=None, **kwargs):
    """Emits an event log with level CRITICAL."""
    kwargs.update({"__caller_stack": 3})
    getEventLogger(name).critical(event_or_message, **kwargs)

def error(name, event_or_message=None, **kwargs):
    """Emits an event log with level ERROR."""
    kwargs.update({"__caller_stack": 3})
    getEventLogger(name).error(event_or_message, **kwargs)

def warning(name, event_or_message=None, **kwargs):
    """Emits an event log with level WARNING."""
    kwargs.update({"__caller_stack": 3})
    getEventLogger(name).warning(event_or_message, **kwargs)

def info(name, event_or_message=None, **kwargs):
    """Emits an event log with level INFO."""
    kwargs.update({"__caller_stack": 3})
    getEventLogger(name).info(event_or_message, **kwargs)

def debug(name, event_or_message=None, **kwargs):
    """Emits an event log with level DEBUG."""
    kwargs.update({"__caller_stack": 3})
    getEventLogger(name).debug(event_or_message, **kwargs)
