"""
This module defines the [`WalltimeObserver`][numcodecs_observers.walltime.WalltimeObserver] class, which measures the walltime it takes to encode / decode.
"""

__all__ = ["WalltimeObserver"]

import time
from collections import defaultdict
from collections.abc import Mapping
from typing import Callable, Optional
from typing_extensions import Buffer  # MSPV 3.12
from types import MappingProxyType

from numcodecs.abc import Codec

from .abc import CodecObserver
from .hash import HashableCodec


class WalltimeObserver(CodecObserver):
    """
    Observer that measures the walltime it takes to encode / decode.

    The list of measurements are exposed in the
    [`encode_times`][numcodecs_observers.walltime.WalltimeObserver.encode_times]
    and
    [`decode_times`][numcodecs_observers.walltime.WalltimeObserver.decode_times]
    properties.
    """

    _encode_times: defaultdict[HashableCodec, list[float]]
    _decode_times: defaultdict[HashableCodec, list[float]]

    def __init__(self):
        self._encode_times = defaultdict(list)
        self._decode_times = defaultdict(list)

    @property
    def encode_times(self) -> Mapping[HashableCodec, list[float]]:
        """
        Per-codec-instance measurements of the walltime it takes to encode.
        """

        return MappingProxyType(self._encode_times)

    @property
    def decode_times(self) -> Mapping[HashableCodec, list[float]]:
        """
        Per-codec-instance measurements of the walltime it takes to decode.
        """

        return MappingProxyType(self._decode_times)

    def observe_encode(self, codec: Codec, buf: Buffer) -> Callable[[Buffer], None]:
        encode_start = time.perf_counter()

        def post_encode(encoded: Buffer) -> None:
            self._encode_times[HashableCodec(codec)].append(
                time.perf_counter() - encode_start
            )

        return post_encode

    def observe_decode(
        self, codec: Codec, buf: Buffer, out: Optional[Buffer] = None
    ) -> Callable[[Buffer], None]:
        decode_start = time.perf_counter()

        def post_decode(decoded: Buffer) -> None:
            self._decode_times[HashableCodec(codec)].append(
                time.perf_counter() - decode_start
            )

        return post_decode
