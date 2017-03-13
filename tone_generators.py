def sin_wave(frequency, duration, volume=0.5):
    """
    frequency in hertz(?)
    duration in seconds
    volume from 0 to 1
    returns a percent.
    """

    factor = frequency * (math.pi * 2) / tone_player.SAMPLE_RATE

    for x in range(math.ceil(duration * tone_player.SAMPLE_RATE)):
        y = math.sin(x * factor) * volume

        # convert from -1 <= y <= 1 to 0 <= y <= 1
        y = (y + 1) / 2

        yield y


