import math
import numpy
import pyaudio

def sin_wave(frequency, duration):
    total_samples = math.ceil(length * self.rate)
    factor = frequency * (math.pi * 2) / self.rate

    return numpy.sin(
        numpy.arange(total_samples, dtype=numpy.float32) * factor)

class TonePlayerInt32(object):
    """
    Used to play sounds encoded as lists of 32-bit numbers. (-2147483648 to
    2147483647)

    Use as a context manager, or manually call .__enter__ and .__exit__
    """

    # TODO: This entire class is untested.
    def __init__(self, sample_rate=44100):
        """
        sample_rate: Number of samples per second.
        """
        self.sample_rate = sample_rate

    def __enter__(self):
        self.p = pyaudio.PyAudio()

        return self

    def __exit__(self, *_):
        self.p.terminate()

    def play_percent(self, samples):
        """
        Play an iterable of samples, but the samples are between 0.0 and 1.0,
        like a percentage. We don't lose any resolution like this because
        Python's floats have infinite decimal places.
        """
        def sample_wrapper(samples):
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
                yield numpy.int32(sample)

        self.play_raw(sample_wrapper(samples))

    def play(self, samples):
        """
        Play an iterable of samples. Each sample should be an int
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
            rate=self.sample_rate,
            output=1)

        with stream:
            for sample in samples:
                stream.write(sample.tostring())

class TonePlayerFloat32(object):
    def __init__(self, rate=44100):
        self.rate = rate

    def __enter__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paFloat32, channels=1, rate=self.rate, output=1)
        return self

    def __exit__(self, *_):
        self.stream.close()
        self.p.terminate()

    def sine(self, frequency, length):
        total_samples = math.ceil(length * self.rate)
        factor = frequency * (math.pi * 2) / self.rate

        return numpy.sin(
            numpy.arange(total_samples, dtype=numpy.float32) * factor)

    def play(self, samples):
        """
        Play a numpy.array([], dtype=numpy.float32) of samples.
        """

        if type(samples) is not numpy.ndarray:
            samples = numpy.array(list(samples), dtype=numpy.float32)
        elif samples.dtype != numpy.float32:
            samples = samples.astype(numpy.float32)

        self.stream.write(samples.tostring())

    def play_tone(self, frequency, length):
        """
        frequency in hertz
        length in seconds (?)
        """
        return self.play_tones([(frequency, length)])

    def play_tones(self, tones):
        """
        tones should be: [(frequency, length), ...]
        """
        audio_data = numpy.empty(0, dtype=numpy.float32)

        for frequency, length in tones:
            audio_data = numpy.concatenate((audio_data,
                self.sine(frequency, length)))

        self.play(audio_data)

if __name__ == '__main__':
    with TonePlayerFloat32() as player:
        player.play_tone(440, 1)
        player.play_tones([
            (110, 0.5),
            (220, 0.6),
            (440, 0.7)])
