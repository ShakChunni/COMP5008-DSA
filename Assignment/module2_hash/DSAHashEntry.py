# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Represent hash slots and their free, used and deleted states.

# Entry states adapted from COMP5008 Practical 7 (DSAHashEntry).
class DSAHashEntry:
    FREE = 0
    USED = 1
    DELETED = 2

    def __init__(self):
        self.key = None
        self.value = None
        self.state = self.FREE
