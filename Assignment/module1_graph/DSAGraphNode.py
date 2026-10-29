# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Represent graph vertices, adjacency entries and weighted edges.

# Graph-node design adapted from COMP5008 Practical 6; weighted edges added here.
from common.DSALinkedList import DSALinkedList


class DSAGraphEdge:
    def __init__(self, destination, weight):
        self.destination = destination
        self.weight = weight


class DSAGraphNode:
    def __init__(self, label, value, index):
        self.label = label
        self.value = value
        self.index = index
        self.adjacent = DSALinkedList()

    def hasEdge(self, other):
        current_node = self.adjacent.head
        found = False
        while current_node is not None and not found:
            if current_node.getValue().destination is other:
                found = True
            else:
                current_node = current_node.getNext()
        return found
