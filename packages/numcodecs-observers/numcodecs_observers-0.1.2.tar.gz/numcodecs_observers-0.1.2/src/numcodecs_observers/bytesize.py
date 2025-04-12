"""
This module defines the [`BytesizeObserver`][numcodecs_observers.bytesize.BytesizeObserver] class, which measures the byte size of the data before and after encoding / decoding.
"""

__all__ = ["Bytesize", "BytesizeObserver"]

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Callable, Optional
from typing_extensions import Buffer  # MSPV 3.12
from types import MappingProxyType

import numpy as np
from numcodecs.abc import Codec

from .abc import CodecObserver
from .hash import HashableCodec


@dataclass
class Bytesize:
    """
    Stores the data size in bytes before and after encoding / decoding.
    """

    pre: int
    post: int


class BytesizeObserver(CodecObserver):
    """
    Observer that measures the byte size of the data before and after encoding / decoding.

    The list of measurements are exposed in the
    [`encode_sizes`][numcodecs_observers.bytesize.BytesizeObserver.encode_sizes]
    and
    [`decode_sizes`][numcodecs_observers.bytesize.BytesizeObserver.decode_sizes]
    properties.
    """

    _encode_sizes: defaultdict[HashableCodec, list[Bytesize]]
    _decode_sizes: defaultdict[HashableCodec, list[Bytesize]]

    def __init__(self):
        self._encode_sizes = defaultdict(list)
        self._decode_sizes = defaultdict(list)

    @property
    def encode_sizes(self) -> Mapping[HashableCodec, list[Bytesize]]:
        """
        Per-codec-instance measurements of the byte size of the data before and
        after encoding.
        """

        return MappingProxyType(self._encode_sizes)

    @property
    def decode_sizes(self) -> Mapping[HashableCodec, list[Bytesize]]:
        """
        Per-codec-instance measurements of the byte size of the data before and
        after decoding.
        """

        return MappingProxyType(self._decode_sizes)

    def observe_encode(self, codec: Codec, buf: Buffer) -> Callable[[Buffer], None]:
        def post_encode(encoded: Buffer) -> None:
            buf_, encoded_ = np.asarray(buf), np.asarray(encoded)

            self._encode_sizes[HashableCodec(codec)].append(
                Bytesize(pre=buf_.nbytes, post=encoded_.nbytes)
            )

        return post_encode

    def observe_decode(
        self, codec: Codec, buf: Buffer, out: Optional[Buffer] = None
    ) -> Callable[[Buffer], None]:
        def post_decode(decoded: Buffer) -> None:
            buf_, decoded_ = np.asarray(buf), np.asarray(decoded)

            self._decode_sizes[HashableCodec(codec)].append(
                Bytesize(pre=buf_.nbytes, post=decoded_.nbytes)
            )

        return post_decode
