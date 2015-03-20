#!/usr/bin/env python

import numpy as np
import pyaudio

from music_base import *

if __name__ == '__main__':
    root = Note('G', 3)
    scale = Scale(root, [2, 2, 1, 2, 2, 2, 1])

    sa_note = scale.get(0)
    ri_note = scale.get(1)
    ga_note = scale.get(2)
    ma_note = scale.get(3)
    pa_note = scale.get(4)
    da_note = scale.get(5)
    ni_note = scale.get(6)
    usa_note = scale.get(7)
    uri_note = scale.get(8)
    uga_note = scale.get(9)

    sa = rise_flat_fall(sa_note)
    ri = rise_flat_fall(ri_note)
    ga = rise_flat_fall(ga_note)
    ma = rise_flat_fall(ma_note)
    pa = rise_flat_fall(pa_note)
    da = rise_flat_fall(da_note)
    ni = rise_flat_fall(ni_note)
    usa = rise_flat_fall(usa_note)
    uri = rise_flat_fall(uri_note)
    uga = rise_flat_fall(uga_note)

    rig = from_next(ri_note, ga_note, 1)
    dag = from_next(da_note, usa_note, 1)
    urig = from_next(uri_note, uga_note, 1)

    chunks = []

    # Mohanam: Aarohanam and avarohanam
    chunks.append(sa)
    chunks.append(rig)
    chunks.append(ga)
    chunks.append(pa)
    chunks.append(dag)
    chunks.append(usa)

    chunks.append(usa)
    chunks.append(dag)
    chunks.append(pa)
    chunks.append(ga)
    chunks.append(rig)
    chunks.append(sa)

    chunk = np.concatenate(chunks) * 0.25

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    stream.write(chunk.astype(np.float32).tostring())
    stream.close()
    p.terminate()
