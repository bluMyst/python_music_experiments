import numpy
import pyaudio
import itertools

SAMPLE_RATE = 44100

class TonePlayer(object):
    """
    Used to play sounds encoded as lists of 32-bit numbers. (-2147483648 to
    2147483647)

    Use as a context manager, or manually call .__enter__ and .__exit__
    """
    # TODO: For some reason, .play(sin_wave(<any>, <any>, 1)) makes a crackly
    #       noise. Lower volumes work fine, though.

    def __enter__(self):
        self.p = pyaudio.PyAudio()

        return self

    def __exit__(self, *_):
        self.p.terminate()

    def play(self, *samples):
        """
        Play iterable(s) of samples, but the samples are between 0.0 and 1.0,
        like a percentage. We don't lose any resolution like this because
        Python's floats have infinite decimal places.
        """
        samples = itertools.chain(*sounds)
        converted_samples = []

        for i, sample in enumerate(samples):
            if not 0 <= sample <= 1:
                raise ValueError(
                    ("Invalid percent at index {i}: {sample}"
                        ).format(**locals()))

            # Convert from:
            # 0 <= sample <= 1
            # to:
            # 0x7fffffff <= sample <= 0x80000000
            # Using y = mx + b where:
            # m =  0xffffffff
            # b = -0x80000000

            sample = 0xffffffff * sample - 0x80000000

            assert numpy.int32(sample) == int(sample)
            converted_samples.append(numpy.int32(sample))

        self.play_raw(converted_samples)

    def play_int32(self, samples):
        """
        Play an iterable of samples. Each sample should quack like an int32
        """
        def sample_wrapper(samples):
            for i, sample in enumerate(samples):
                sample_int32 = numpy.int32(sample)

                if sample != sample_int32:
                    raise ValueError(
                        ("Invalid int32 at index {i}: {sample} -> "
                            "{sample_int32}").format(**locals()))

                yield sample_int32

        self.play_raw(sample_wrapper(samples))

    def play_raw(self, samples):
        """
        No converting. "samples" should be an iterable of numpy.int32; anything
        else and things will break.
        """
        stream = self.p.open(
            format=pyaudio.paInt32,
            channels=1,
            rate=SAMPLE_RATE,
            output=1)

        for sample in samples:
            stream.write(sample.tostring())

        stream.close()
