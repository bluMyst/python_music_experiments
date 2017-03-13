import math
import string

NOTE_DISTANCE = 2 ** (1/12)

NOTE_LETTERS = {
    'A':  0,
    'B':  2,
    'C':  3,
    'D':  5,
    'E':  7,
    'F':  8,
    'G': 10,
}

NOTE_LETTERS_BACKWARDS = {
    v: k for k, v in NOTE_LETTERS.items()
}

def note_freq(hsteps):
    """ Return the frequency in hertz of the given note in the equal tempered
    scale.

    hsteps: Half steps from A4.
    """

    if hsteps == 0: return 440

    return note_freq(0) * NOTE_DISTANCE ** hsteps

def notestr_to_hsteps(notestr):
    """
    notestr: a <note>

    In BNF:
    <note>       ::= [<octave>] <letter> [<accidental>]
    <octave>     ::= "1" | "2" | "3" | ...
    <accidental> ::= "#" | "b"
    <letter>     ::= <lowercase> | <uppercase>
    <lowercase>  ::= "a" | "b" | ... | "g"
    <uppercase>  ::= "A" | "B" | ... | "G"

    Octave defaults to 4.
    """
    notestr = notestr.strip()

    if notestr[0] in string.digits:
        octave = int(notestr[0])
        notestr = notestr[1:]
    else:
        octave = 4

    if notestr[0] not in string.ascii_letters:
        raise ValueError("Weird notestr.")

    note = (octave - 4) * 12
    note += NOTE_LETTERS[notestr[0].upper()]

    if len(notestr) == 2:
        if notestr[1] == '#':
            note += 1
        elif notestr[1] == 'b':
            note -= 1
        else:
            raise ValueError("Invalid accidental:", notestr[1])

    return note

def hsteps_to_notestr(hsteps):
    """
    hsteps: halfsteps to 4A
    """
    # TODO: Wrong. So wrong.
    octave = math.floor(hsteps / 12) + 4
    note = str(octave)

    hsteps = hsteps % 12

    if hsteps in NOTE_LETTERS_BACKWARDS:
        note += NOTE_LETTERS_BACKWARDS[hsteps]
        return note
    elif hsteps+1 in NOTE_LETTERS_BACKWARDS:
        note += NOTE_LETTERS_BACKWARDS[hsteps+1]
        note += "#"
        return note
    elif hsteps-1 in NOTE_LETTERS_BACKWARDS:
        note += NOTE_LETTERS_BACKWARDS[hsteps-1]
        note += "b"
        return note
    else:
        assert False, "NOTE_LETTERS is wrong somehow"

def nrange(*args):
    """
    It's range() but for notestrings.
    step should still be an int, though.

    range(stop)
    range(start, stop[, step])
    """
    # Default values to be overridden.
    start, step = "4A", 1

    if len(args) == 1:
        stop = args[0]
    elif len(args) == 2:
        start, stop = args
    elif len(args) == 3:
        start, stop, step = args
    else:
        raise TypeError("nrange() takes 1-3 positional arguments but "
            "{nargs} was given".format(nargs=len(args)))

    start = notestr_to_hsteps(start)
    stop  = notestr_to_hsteps(stop)
    for i in range(start, stop, step):
        yield hsteps_to_notestr(i)
