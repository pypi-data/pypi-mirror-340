"""
This module defines the [`CodecObserver`][numcodecs_observers.abc.CodecObserver] base class, which allows observing a [`Codec`][numcodecs.abc.Codec]'s encode and decode calls.
"""

__all__ = ["CodecObserver"]

from typing import Optional, Callable
from typing_extensions import Buffer  # MSPV 3.12

from numcodecs.abc import Codec


class CodecObserver:
    """
    Observer base class, which allows observing a [`Codec`][numcodecs.abc.Codec]'s encode and decode calls.
    """

    def observe_encode(self, codec: Codec, buf: Buffer) -> Callable[[Buffer], None]:
        """
        Hook that is called *before* `codec.encode(buf)` is called.

        Parameters
        ----------
        codec : Codec
            Codec whose `encode` method is called.
        buf : Buffer
            Data to be encoded. May be any object supporting the new-style
            buffer protocol.

        Returns
        -------
        posthook : Callable[[Buffer], None]
            Hook that is called with the `encoded` data *after*
            `encoded = codec.encode(buf)` has returned.
        """

        return lambda encoded: None

    def observe_decode(
        self, codec: Codec, buf: Buffer, out: Optional[Buffer] = None
    ) -> Callable[[Buffer], None]:
        """
        Hook that is called *before* `codec.decode(buf, out=out)` is called.

        Parameters
        ----------
        codec : Codec
            Codec whose `decode` method is called.
        buf : Buffer
            Encoded data. May be any object supporting the new-style buffer
            protocol.
        out : Buffer, optional
            Writeable buffer to store decoded data. N.B. if provided, this buffer must
            be exactly the right size to store the decoded data.

        Returns
        -------
        posthook : Callable[[Buffer], None]
            Hook that is called with the `decoded` data *after*
            `decoded = codec.decode(buf, out=out)` has returned.
        """

        return lambda decoded: None
