import logging
from threading import local

_thread_locals = local()

logger = logging.getLogger(__name__)


def get_local_thread_value(item):
    """
    Returns value of an item of this current thread.
    """
    return getattr(_thread_locals, item, None)


def list_thread_locals(attrs):
    """
    Returns a line of key:val pairs of current thread locals.
    """
    return str("Current thread locals: " + ', '.join(
        [
            f"{attr}: {str(get_local_thread_value(attr))}"
            for attr in attrs
        ]))


class ThreadLocalMiddleware():
    """
    This middleware, for every request separately, reads important values
    from Request or Session objects and adds them to local thread attributes.
    This makes the values available throughout the project - in views, etc.
    """
    def __init__(self, get_response=None):
        """
        One-time configuration and initialization.
        Called only once at server startup.
        """
        self.get_response = get_response
        self.attrs_to_remove = ['c_user', 'c_session_id', ]

    def _set_user(self, request):
        """Get username from request data and add it to thread."""
        c_user = getattr(request, 'user', None)
        logger.debug(f"_set_user to _thread_locals: {c_user}")
        setattr(_thread_locals, 'c_user', c_user)

    def _set_session_id(self, request):
        """Get session ID from session store and add it to thread."""
        c_session = getattr(request, 'session', {})
        c_session_key = getattr(c_session, 'session_key', None)
        c_session_id = c_session_key[-10:] if c_session_key else None
        logger.debug(f"_set_session_id to _thread_locals: {c_session_id}")
        setattr(_thread_locals, 'c_session_id', c_session_id)

    def _unset_local_attr(self):
        """Remove attributes provided in attr_list from local thread."""
        logger.debug(f"_unset_local_attr")
        for attr in self.attrs_to_remove:
            if hasattr(_thread_locals, attr):
                delattr(_thread_locals, attr)

    def __call__(self, request):
        """
        Called for every request.
        Fetch and store User information into local thread,
        which is then available for logging filter.
        """
        # Code to be executed for each request before
        # the view (and later middlewares) are called.

        self._set_user(request)
        self._set_session_id(request)
        logger.debug(list_thread_locals(self.attrs_to_remove) + " (request)")

        # Forward Request further the satck and wait for Response
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # Unset all local thread attributes
        # to ensure they are not kept in next request/response cycle.
        self._unset_local_attr()
        logger.debug(list_thread_locals(self.attrs_to_remove) + " (response)")

        # Let other middlewares execute their response part.
        return response

    def process_exception(self, request, exception):
        """
        In case of exception, delete the local thread attributes,
        and return None so that other middlewares can act too.
        """
        logger.debug('process_exception: exception in thread_local')
        self._unset_local_attr()
