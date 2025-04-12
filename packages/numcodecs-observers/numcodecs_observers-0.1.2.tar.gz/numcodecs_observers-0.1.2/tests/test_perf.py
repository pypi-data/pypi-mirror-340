import numcodecs_combinators
import numcodecs_observers
import numcodecs
import numpy as np


def test_perf():
    nbytes = numcodecs_observers.bytesize.BytesizeObserver()
    timing = numcodecs_observers.walltime.WalltimeObserver()

    stack = numcodecs_combinators.stack.CodecStack(
        numcodecs.BitRound(keepbits=6), numcodecs.Zlib(level=7)
    )

    data = np.random.normal(size=(100, 100))

    with numcodecs_observers.observe(stack, [nbytes, timing]) as stack_:
        stack_.encode_decode(data)

    print(nbytes.encode_sizes)
    print(nbytes.decode_sizes)
    print(timing.encode_times)
    print(timing.decode_times)
