# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Implement double-hashed farm lookup, deletion and table growth.

# Adapted from my COMP5008 Practical 7: double hashing and prime-sized tables.
# Reference: Cormen et al., Introduction to Algorithms, 4th ed., 2022.

import numpy as np
from models.FarmRecord import FarmRecord, validateFarmID
from module2_hash.DSAHashEntry import DSAHashEntry


class DSAHashTable:
    def __init__(self, initial_size=53):
        if isinstance(initial_size, bool) or not isinstance(initial_size, int) or initial_size < 3:
            raise ValueError("Table size must be an integer of at least 3")
        self._size = self._nextPrime(initial_size)
        self._table = self._createArray(self._size)
        self._count = 0
        self._insertions = 0
        self._threshold = 0.7
        self._minimum_size = self._size
        self._lower_threshold = 0.2

    def _createArray(self, size):
        entries = np.empty(size, dtype=object)
        for index in range(size):
            entries[index] = DSAHashEntry()
        return entries

    def _nextPrime(self, number):
        candidate = number
        found = False
        while not found:
            prime = candidate >= 2
            divisor = 2
            while divisor * divisor <= candidate and prime:
                if candidate % divisor == 0:
                    prime = False
                divisor += 1
            if prime:
                found = True
            else:
                candidate += 1
        return candidate

    def _hashModulo(self, key, modulus):
        result = 0
        for character in key:
            result = (result * 31 + ord(character)) % modulus
        return result

    def hash(self, key):
        return self._hashModulo(validateFarmID(key), self._size)

    def _step(self, key):
        return 1 + self._hashModulo(key, self._size - 1)

    def _findIndex(self, key, inserting=False, trace=False):
        validateFarmID(key)
        start = self.hash(key)
        step = self._step(key)
        tombstone = -1
        result = -1
        searching = True
        attempt = 0
        while searching and attempt < self._size:
            index = (start + attempt * step) % self._size
            entry = self._table[index]
            if trace: #showing details printing
                state = "FREE"
                if entry.state == DSAHashEntry.USED:
                    state = "USED:" + entry.key
                elif entry.state == DSAHashEntry.DELETED:
                    state = "DELETED"
                print(f"  probe {attempt}: index {index}, {state}")
                if entry.state == DSAHashEntry.USED and entry.key != key:
                    print("  collision: occupied by a different FarmID; use next probe")


            if entry.state == DSAHashEntry.FREE:
                if inserting and tombstone != -1:
                    result = tombstone
                elif inserting:
                    result = index
                searching = False
            elif entry.state == DSAHashEntry.USED and entry.key == key:
                result = index
                searching = False
            elif entry.state == DSAHashEntry.DELETED and tombstone == -1:
                tombstone = index
            attempt += 1
        if searching and inserting:
            result = tombstone
        return result

    def insert(self, record, trace=False):
        if not isinstance(record, FarmRecord):
            raise ValueError("Insert requires a validated FarmRecord")
        key = validateFarmID(record.farm_id)
        if self._findIndex(key) != -1:
            raise ValueError("Duplicate FarmID: " + key)
        if (self._count + 1) / self._size > self._threshold: #resize if load factor exceeds threshold
            self._resize(self._size * 2, trace)
        #find inext for insertion
        index = self._findIndex(key, inserting=True, trace=trace)
        if index == -1:
            raise RuntimeError("No insertion position available")
        
        entry = self._table[index]
        entry.key = key
        entry.value = record
        entry.state = DSAHashEntry.USED
        self._count += 1
        self._insertions += 1
        if trace:
            print(f"INSERT {key}: index={index}, count={self._count}, "
                  f"size={self._size}, load={self.loadFactor():.4f}")
        if self._insertions % 10 == 0:
            print(f"After {self._insertions} successful insertions: "
                  f"load factor={self.loadFactor():.4f} "
                  f"({self._count}/{self._size})")

    def search(self, farm_id, trace=False):
        index = self._findIndex(farm_id, trace=trace)
        if index == -1:
            raise KeyError("Farm not found: " + farm_id)
        if trace:
            print(f"SEARCH {farm_id}: found at index {index}")
        return self._table[index].value

    def delete(self, farm_id, trace=False):
        index = self._findIndex(farm_id, trace=trace)
        if index == -1:
            raise KeyError("Cannot delete missing farm: " + farm_id)
        entry = self._table[index]
        entry.key = None
        entry.value = None
        entry.state = DSAHashEntry.DELETED
        self._count -= 1
        if trace:
            print(f"DELETE {farm_id}: tombstone at {index}, load={self.loadFactor():.4f}")
            
        if self._size > self._minimum_size and self.loadFactor() < self._lower_threshold:
            smaller_size = self._size // 2
            if smaller_size < self._minimum_size:
                smaller_size = self._minimum_size
            self._resize(smaller_size, trace)

    def _resize(self, requested_size, trace):
        old_table = self._table
        old_size = self._size
        self._size = self._nextPrime(requested_size)
        self._table = self._createArray(self._size)
        # Rehash directly: these are not new user insertions.
        for entry in old_table:
            if entry.state == DSAHashEntry.USED:
                index = self._findIndex(entry.key, inserting=True)
                self._table[index] = entry
        if trace:
            print(f"RESIZE {old_size} -> {self._size}; all live records rehashed")

    def records(self):
        for entry in self._table:
            if entry.state == DSAHashEntry.USED:
                yield entry.value

    def getCount(self):
        return self._count

    def getSize(self):
        return self._size

    def loadFactor(self):
        return self._count / self._size

    def display(self):
        for index in range(self._size):
            entry = self._table[index]
            state = "FREE"
            if entry.state == DSAHashEntry.USED:
                state = entry.key + " | " + entry.value.name
            elif entry.state == DSAHashEntry.DELETED:
                state = "DELETED"
            print(f"{index}: {state}")
