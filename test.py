import tone_player
import tone_generators
import note_math

if __name__ == '__main__':
    with tone_player.TonePlayer() as player:
        sound = (tone_generators.sin_wave(note_math.note_freq(i), 0.5)
                for i in range(15, -1, -3))
        player.play(*sound)
