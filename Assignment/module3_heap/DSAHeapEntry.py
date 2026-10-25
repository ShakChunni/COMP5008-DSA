# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Store request priority, request reference and FIFO tie sequence.

# Priority/value entry adapted from COMP5008 Practical 8; FIFO sequence added here.
class DSAHeapEntry:
    def __init__(self, priority, value, sequence):
        self.priority = priority
        self.value = value
        self.sequence = sequence
