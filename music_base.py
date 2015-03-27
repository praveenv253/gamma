"""
Credits: http://davywybiral.blogspot.com/2010/09/
                                procedural-music-with-pyaudio-and-numpy.html
"""

import numpy as np
import itertools
from scipy import interpolate
from operator import itemgetter

import matplotlib.pyplot as plt

LENGTH = 0.5
RATE = 44100

class Note(object):
    """
    Class to define a "note" - a single frequency - using its English notation
    and octave number.
    """

    NOTES = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']

    def __init__(self, note, octave=4):
        """
        Define a note using its English notation and octave number.
        note: Can be an integer, in which case it is an index into a list of
              notes starting from 'C', or it can be a string, containing the
              note name (possibly in sharp, but never in flat notation).
        octave: An integer describing which octave to place the note in.
        """
        self.octave = octave
        if isinstance(note, int):
            self.index = note
            self.note = Note.NOTES[note]
        elif isinstance(note, str):
            self.note = note.strip().lower()
            self.index = Note.NOTES.index(self.note)

    def transpose(self, halfsteps):
        """
        A function that returns a note `halfsteps' notes away from the given
        note.
        halfsteps: An integer describing how many notes to shift ahead or 
                   behind
        """
        octave_delta, note = divmod(self.index + halfsteps, 12)
        return Note(note, self.octave + octave_delta)

    def frequency(self):
        """
        Returns the frequency of the note in Hertz.
        """
        base_frequency = 16.35159783128741 * 2.0 ** (float(self.index) / 12.0)
        return base_frequency * (2.0 ** self.octave)

    def __float__(self):
        return self.frequency()


class Scale:

    def __init__(self, root, intervals):
        self.root = Note(root.index, root.octave)
        self.intervals = intervals

    def get(self, index):
        intervals = self.intervals
        if index < 0:
            index = abs(index)
            intervals = reversed(self.intervals)
        intervals = itertools.cycle(self.intervals)
        note = self.root
        for i in xrange(index):
            note = note.transpose(intervals.next())
        return note

    def index(self, note):
        intervals = itertools.cycle(self.intervals)
        index = 0
        x = self.root
        while x.octave != note.octave or x.note != note.note:
            x = x.transpose(intervals.next())
            index += 1
        return index

    def transpose(self, note, interval):
        return self.get(self.index(note) + interval)


def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (np.pi * 2) / rate
    return np.sin(np.arange(length) * factor)

def shape(data, points, kind='slinear'):
    items = points.items()
    items.sort(key=itemgetter(0))
    keys = map(itemgetter(0), items)
    vals = map(itemgetter(1), items)
    interp = interpolate.interp1d(keys, vals, kind=kind)
    factor = 1.0 / len(data)
    shape = interp(np.arange(len(data)) * factor)
    return data * shape

def shape_freq(data, points):
    """Interpolate with cosines"""
    xy_pairs = list(points)
    #print xy_pairs
    n = data.size
    modulator = np.ones(n)
    for i in range(len(xy_pairs) - 1):
        (x1, y1) = xy_pairs[i]
        (x2, y2) = xy_pairs[i+1]
        start_index = round(x1 * n)
        end_index = round(x2 * n)
        wave = 0.5 + 0.5 * np.cos(np.pi * np.linspace(0, 1,
                                                      end_index - start_index))
        wave *= (y1 - y2)
        wave += y2
        modulator[start_index:end_index] = wave
    return data * modulator

def harmonics1(freq, length):
    a = sine(freq * 1.00, length, 44100)
    b = sine(freq * 2.00, length, 44100) * 0.5
    c = sine(freq * 4.00, length, 44100) * 0.125
    return (a + b + c) * 0.2

def harmonics2(freq, length):
    a = sine(freq * 1.00, length, 44100)
    b = sine(freq * 2.00, length, 44100) * 0.5
    return (a + b) * 0.2

def pluck1(note):
    chunk = harmonics1(note.frequency(), 2)
    return shape(chunk, {0.0: 0.0, 0.005: 1.0, 0.25: 0.5, 0.9: 0.1, 1.0:0.0})

def pluck2(note):
    chunk = harmonics2(note.frequency(), 2)
    return shape(chunk, {0.0: 0.0, 0.5:0.75, 0.8:0.4, 1.0:0.1})

def chord(n, scale):
    root = scale.get(n)
    third = scale.transpose(root, 2)
    fifth = scale.transpose(root, 4)
    return pluck1(root) + pluck1(third) + pluck1(fifth)

def flat(note):
    chunk = harmonics1(note.frequency(), LENGTH)
    return shape(chunk, {0.0: 1.0, 1.0: 1.0})

def flat_fall(note):
    chunk = harmonics1(note.frequency(), LENGTH)
    return shape(chunk, {0.0: 1.0, 0.9: 1.0, 1.0: 0.0})

def rise_flat(note):
    chunk = harmonics1(note.frequency(), LENGTH)
    return shape(chunk, {0.0: 0.0, 0.1: 1.0, 1.0: 1.0})

def rise_flat_fall(note):
    chunk = harmonics1(note.frequency(), LENGTH)
    return shape(chunk, {0.0: 0.0, 0.005: 1.0, 0.9: 1.0, 1.0: 0.0})

def slow_rise_fall(note):
    chunk = harmonics1(note.frequency(), LENGTH)
    return shape(chunk, {0.0: 0.0, 0.7: 1.0, 0.9: 1.0, 1.0: 0.0})

def from_next(note1, note2, times=1, lamda_shape=None):
    n = LENGTH * RATE

    # Define the frequency over time
    # To do this, we shape the wavelength according to lamda_shape and take
    # its inverse to get frequency
    lamda1 = 1. / note1.frequency()
    lamda2 = 1. / note2.frequency()
    delta_lamda = lamda2 - lamda1
    lamdas = np.ones(n / times) * float(delta_lamda)
    # Define the shape if not given
    if lamda_shape is None:
        #lamda_shape = {0.0:1.0, 0.1:1.0, 0.2:1.0, 0.3:0.9, 0.4:0.75, 0.5:0.5,
        #               0.6:0.25, 0.7:0.10, 0.8:0.02, 0.9:0.0, 1.0:0.0}
        lamda_shape = [(0.0, 1.0), (0.2, 1.0), (0.6, 0.0), (1.0, 0.0)]
    lamdas = shape_freq(lamdas, lamda_shape)
    lamdas += lamda1
    freqs = 1. / lamdas
    freqs = np.concatenate([freqs, ] * times)
    #plt.plot(freqs)
    #plt.show()

    # Now, to integrate over the product of frequency and time
    t = np.ones(n, dtype=float) / RATE
    phase = np.cumsum(freqs * t)
    chunk = np.sin(2 * np.pi * phase)
    chunk += 0.5 * np.sin(2 * np.pi * 2 * phase) # Third harmonic
    chunk += 0.125 * np.sin(2 * np.pi * 4 * phase) # Fifth harmonic
    chunk *= 0.2
    return shape_freq(chunk, [(0.0, 0.0), (0.05, 1.0), (1.0, 1.0)])
