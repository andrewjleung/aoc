"""
PART 1

A signal is a series of seemingly-random characters. 

You need to create a function to detect a "start-of-packet marker" within this
signal which is a sequence of four different characters.

Return the number of characters from the beginning of the buffer to the end of
the first instance of a marker.
"""


# Return the number of characters from the beginning of the buffer to the end of
# the first four-character marker in the given buffer.
def findMarker(buffer: str, markerLength: int) -> int:
    # Use a character frequency mapping to keep track of the number of unique
    # characters within the four-character window.
    windowFreqs = {}

    i = 0

    # Slide a window across the entire buffer of the length of the header,
    # returning as soon as it contains all unique characters.
    while i < len(buffer):
        char = buffer[i]

        windowFreqs[char] = windowFreqs.get(char, 0) + 1

        # Remove a character from the start of the window.
        if i >= markerLength:
            removeChar = buffer[i - markerLength]

            if windowFreqs[removeChar] == 1:
                del windowFreqs[removeChar]
            else:
                windowFreqs[removeChar] -= 1

        # Check if the marker has been found.
        if i >= markerLength - 1 and len(windowFreqs) >= markerLength:
            return i + 1

        i += 1

    return -1
