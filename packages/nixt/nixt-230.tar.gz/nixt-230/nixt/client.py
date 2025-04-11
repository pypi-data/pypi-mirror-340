# This file is placed in the Public Domain.


"clients"


from .fleet   import Fleet
from .object  import Default
from .reactor import Reactor


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        self.state = Default()
        Fleet.add(self)

    def announce(self, txt) -> None:
        pass

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def say(self, channel, txt) -> None:
        self.raw(txt)


def __dir__():
    return (
        'STARTTIME',
        'Client',
    )
