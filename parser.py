def parse(song_text):
    """
    Parses the text of a song that is using a precise notation for notes and
    gamakams.

    Returns the string corresponding to the note, along with a list of
    (note_fraction, wavelength_fraction) tuples, indicating the exact gamakam
    for that note.

    Examples:
    s     Sa, flat note
    .n    Ni, flat, lower octave
    'r    Ri, flat, higher octave
    r'-   Ri, from Ga (in Mohanam, for instance), with equal emphasis on both
    .d''- Da, lower octave, coming from the next note (Sa in Mohanam, Ni in
          Shankarabharanam), with a longer duration of presence in the next
          note. Roughly 67% of the note is Sa, and 33% is Da.
    m.-.- Ma, coming from the previous note. This is like the Shankarabharanam
          Ma, with equal emphasis on Ga as well as Ma, as in 'Ga-Ma-Ga-Ma'
    m..'. Again, a Shankarabharanam Ma, but with a slower and heavier gamakam.
          It stays at Ga for some time, then goes to Pa, and returns to Ga,
          as in 'Ga-,-Pa-Ga'.
    """
    swaras = song_text.split()
    for swara in swaras:

