# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Implement the NumPy-backed max heap and operation traces.

# Array-based max heap adapted from my COMP5008 Practical 8.
# Equal priorities use insertion sequence to give FIFO tie-breaking.
# Reference: Cormen et al., Introduction to Algorithms, 4th ed., 2022.

import math
import numpy as np
from module3_heap.DSAHeapEntry import DSAHeapEntry


class DSAHeap:
    def __init__(self, capacity=100):
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Heap capacity must be a positive integer")
        self._heap = np.empty(capacity, dtype=object)
        for index in range(capacity):
            self._heap[index] = None
        self._count = 0
        self._sequence = 0

    def getCount(self):
        return self._count

    def isEmpty(self):
        return self._count == 0

    def _higher(self, first, second):
        return (first.priority > second.priority
                or (first.priority == second.priority and first.sequence < second.sequence))

    def insert(self, request):
        priority = getattr(request, "priority", None)
        try:
            valid = (not isinstance(priority, bool)
                     and (isinstance(priority, int) or isinstance(priority, float))
                     and math.isfinite(priority))
        except OverflowError:
            valid = False
        if not valid:
            raise ValueError("Request needs a finite calculated priority")
        if not isinstance(getattr(request, "request_id", None), str) or not request.request_id:
            raise ValueError("Request needs a non-empty request ID")
        if self._count == len(self._heap):
            raise ValueError("Heap is full")
        self._heap[self._count] = DSAHeapEntry(priority, request, self._sequence)
        self._sequence += 1
        index = self._count
        self._count += 1
        moving = True
        while index > 0 and moving:
            parent = (index - 1) // 2
            if self._higher(self._heap[index], self._heap[parent]):
                temporary = self._heap[index]
                self._heap[index] = self._heap[parent]
                self._heap[parent] = temporary
                index = parent
            else:
                moving = False
        print("HEAP after insertion:", self.arrayString())

    def peek(self):
        if self.isEmpty():
            raise ValueError("Heap is empty")
        return self._heap[0].value

    def extract_priority(self):
        if self.isEmpty():
            raise ValueError("Heap is empty")
        result = self._heap[0].value
        self._count -= 1
        self._heap[0] = self._heap[self._count]
        self._heap[self._count] = None
        index = 0
        moving = True
        while index * 2 + 1 < self._count and moving:
            child = index * 2 + 1
            right = child + 1
            if right < self._count and self._higher(self._heap[right], self._heap[child]):
                child = right
            if self._higher(self._heap[child], self._heap[index]):
                temporary = self._heap[index]
                self._heap[index] = self._heap[child]
                self._heap[child] = temporary
                index = child
            else:
                moving = False
        print("HEAP after extraction:", self.arrayString())
        return result

    def entries(self):
        for index in range(self._count):
            yield self._heap[index].value

    def arrayString(self):
        parts = np.empty(self._count, dtype=object)
        for index in range(self._count):
            entry = self._heap[index]
            parts[index] = f"{entry.value.request_id}:{entry.priority:.6f}"
        return "[" + ", ".join(parts) + "]"

    def validateHeap(self):
        valid = True
        for index in range(1, self._count):
            if self._higher(self._heap[index], self._heap[(index - 1) // 2]):
                valid = False
        return valid
