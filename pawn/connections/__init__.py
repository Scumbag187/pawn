from .. import concurrency
from ..messages import to_bytes, to_unicode
from ..handlers.web import http_render

import ujson as json
from uuid import uuid4
import cgi
import re
import logging
import Cookie



###
### Connection Classes
###

class Connection(object):
    """This class is an abstraction for how Brubeck sends and receives
    messages. The idea is that Brubeck waits to receive messages for some work
    and then it responds. Therefore each connection should essentially be a
    mechanism for reading a message and a mechanism for responding, if a
    response is necessary.
    """

    def __init__(self, incoming=None, outgoing=None):
        """The base `__init__()` function configures a unique ID and assigns
        the incoming and outgoing mechanisms to a name.

        `in_sock` and `out_sock` feel like misnomers at this time but they are
        preserved for a transition period.
        """
        self.sender_id = uuid4().hex
        self.in_sock = incoming
        self.out_sock = outgoing

    def _unsupported(self, name):
        """Simple function that raises an exception.
        """
        error_msg = 'Subclass of Connection has not implemented `%s()`' % name
        raise NotImplementedError(error_msg)

    def recv(self):
        """Receives a raw mongrel2.handler.Request object that you
        can then work with.
        """
        self._unsupported('recv')

    def _recv_forever_ever(self, fun_forever):
        """Calls a handler function that runs forever. The handler can be
        interrupted with a ctrl-c, though.
        """
        try:
            fun_forever()
        except KeyboardInterrupt, ki:
            # Put a newline after ^C
            print '\nBrubeck going down...'

    def send(self, uuid, conn_id, msg):
        """Function for sending a single message.
        """
        self._unsupported('send')

    def reply(self, req, msg):
        """Does a reply based on the given Request object and message.
        """
        self.send(req.sender, req.conn_id, msg)

    def reply_bulk(self, uuid, idents, data):
        """This lets you send a single message to many currently
        connected clients.  There's a MAX_IDENTS that you should
        not exceed, so chunk your targets as needed.  Each target
        will receive the message once by Mongrel2, but you don't have
        to loop which cuts down on reply volume.
        """
        self._unsupported('reply_bulk')
        self.send(uuid, ' '.join(idents), data)

    def close(self):
        """Close the connection.
        """
        self._unsupported('close')

    def close_bulk(self, uuid, idents):
        """Same as close but does it to a whole bunch of idents at a time.
        """
        self._unsupported('close_bulk')
        self.reply_bulk(uuid, idents, "")

