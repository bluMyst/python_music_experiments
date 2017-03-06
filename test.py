import math
import numpy
import pyaudio

class TonePlayer(object):
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
    with TonePlayer() as player:
        player.play_tone(440, 1)
        player.play_tones([
            (110, 0.5),
            (220, 0.6),
            (440, 0.7)])
