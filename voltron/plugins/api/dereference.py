import logging

import voltron
from voltron.api import *

from scruffy.plugin import Plugin

log = logging.getLogger('api')

class APIDerefRequest(APIRequest):
    """
    API dereference pointer request.

    {
        "type":         "request",
        "request":      "dereference"
        "data": {
            "pointer":  0xffffff8012341234
        }
    }
    """
    _fields = {'pointer': True}

    @server_side
    def dispatch(self):
        try:
            output = voltron.debugger.dereference(self.pointer)
            log.debug('output: {}'.format(str(output)))
            res = APIDerefResponse()
            res.output = output
        except NoSuchTargetException:
            res = APINoSuchTargetErrorResponse()
        except Exception, e:
            msg = "Exception executing debugger command: {}".format(e)
            log.error(msg)
            res = APIGenericErrorResponse()
            res.message = msg

        return res


class APIDerefResponse(APISuccessResponse):
    """
    API dereference pointer response.

    {
        "type":         "response",
        "status":       "success",
        "data": {
            "output":   [0xffffff8055555555, "main + 0x123"]
        }
    }
    """
    _fields = {'output': True}

    output = None


class APIDerefPlugin(APIPlugin):
    request = "dereference"
    request_class = APIDerefRequest
    response_class = APIDerefResponse
