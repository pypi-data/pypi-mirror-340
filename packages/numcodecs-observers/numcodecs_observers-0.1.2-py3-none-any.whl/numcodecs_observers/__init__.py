"""
Observe encoding and decoding in the [`numcodecs`][numcodecs] buffer
compression API.

The following observers, implementing the
[`CodecObserver`][numcodecs_observers.abc.CodecObserver] class are provided:

- [`BytesizeObserver`][numcodecs_observers.bytesize.BytesizeObserver]: measure
  the byte size of the data before and after encoding / decoding
- [`WalltimeObserver`][numcodecs_observers.walltime.WalltimeObserver]: measure
  the walltime it takes to encode / decode
"""

__all__ = ["observe"]

from collections.abc import Sequence
from contextlib import contextmanager
from typing import Any, Optional, Callable
from typing_extensions import Buffer  # MSPV 3.12

import numcodecs_combinators
from numcodecs.abc import Codec
from numcodecs_combinators.abc import CodecCombinatorMixin

from . import abc as abc
from . import bytesize as bytesize
from . import walltime as walltime


@contextmanager
def observe(codec: Codec, observers: Sequence[abc.CodecObserver]):
    """
    Context manager to wrap the provided `codec` such that the `observers`
    observe every [`encode`][numcodecs.abc.Codec.encode] and
    [`decode`][numcodecs.abc.Codec.decode] call.

    Parameters
    ----------
    codec : Codec
        Codec to be observed.
    observers : Sequence[abc.CodecObserver]
        List of observers.

    Returns
    -------
    codec_ : contextlib.AbstractContextManager[Codec]
        Context manager over the observing codec, which intercepts every
        [`encode`][numcodecs.abc.Codec.encode] and
        [`decode`][numcodecs.abc.Codec.decode] call for the `observers`.
    """

    yield numcodecs_combinators.map_codec(
        codec, lambda c: _ObservingCodec(c, observers)
    )


class _ObservingCodec(Codec, CodecCombinatorMixin):
    _codec: Codec
    _observers: tuple[abc.CodecObserver, ...]

    def __init__(self, codec: Codec, observers: Sequence[abc.CodecObserver]):
        self._codec = codec
        self._observers = tuple(observers)

    def encode(self, buf: Buffer) -> Buffer:
        observers = [
            observer.observe_encode(self._codec, buf) for observer in self._observers
        ]

        encoded: Buffer = self._codec.encode(buf)  # type: ignore

        for observer in reversed(observers):
            observer(encoded)

        return encoded

    def decode(self, buf: Buffer, out: Optional[Buffer] = None) -> Buffer:
        observers = [
            observer.observe_decode(self._codec, buf, out=out)
            for observer in self._observers
        ]

        decoded: Buffer = self._codec.decode(buf, out=out)  # type: ignore

        for observer in reversed(observers):
            observer(decoded)

        return decoded

    def map(self, mapper: Callable[[Codec], Codec]) -> "_ObservingCodec":
        return _ObservingCodec(mapper(self._codec), self._observers)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._codec, name)
