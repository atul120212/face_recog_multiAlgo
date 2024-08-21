import sys
import mmap


def IdentifyFileRotation(filePath, rotation):
    zero = bytes([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  64])

    r90 = bytes([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 255, 255, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 64])

    r180 = bytes([255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  64])

    r270 = bytes([0, 0, 0, 0, 255, 255, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  64])

    all = [zero, r90, r180, r270]
    ii = int(rotation)

    with open(filePath, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        jj = mm.find(b'vide')
        mm.seek(jj - 160)
        jj = mm.find(bytes([64])) - 32
        mm.seek(jj)
        if jj > 0:
            a = mm.read(33)
            if a in all:
                return all.index(a)  # rotation found
                mm.seek(jj)
                mm.write(all[ii])
            else:
                return -1  # no rotation
