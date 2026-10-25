# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Implement the weighted graph, BFS, DFS and Dijkstra algorithms.

# Adapted from my COMP5008 Practical 6 graph and linked-list implementation.
# Algorithm reference: Cormen et al., Introduction to Algorithms, 4th ed., 2022.

import math
import numpy as np
from common.DSALinkedList import DSALinkedList
from common.DSAQueue import DSAQueue
from common.DSAStack import DSAStack
from module1_graph.DSAGraphNode import DSAGraphNode, DSAGraphEdge


def makePair(first, second):
    pair = np.empty(2, dtype=object)
    pair[0] = first
    pair[1] = second
    return pair


class DSAGraph:
    def __init__(self):
        self._vertices = DSALinkedList()
        self._count = 0
        self._edge_count = 0

    def getVertexCount(self):
        return self._count

    def getEdgeCount(self):
        return self._edge_count

    def vertices(self):
        return iter(self._vertices)

    def getVertex(self, label):
        if not isinstance(label, str) or not label.strip():
            raise ValueError("Location label must be a non-empty string")
        for vertex in self._vertices:
            if vertex.label == label:
                return vertex
        raise KeyError("Location not found: " + label)

    def hasVertex(self, label):
        try:
            self.getVertex(label)
            return True
        except KeyError:
            return False

    def addVertex(self, label, value=None):
        if not isinstance(label, str) or not label.strip():
            raise ValueError("Location label must be a non-empty string")
        if self.hasVertex(label):
            raise ValueError("Duplicate location: " + label)
        self._vertices.insertLast(DSAGraphNode(label, value, self._count))
        self._count += 1

    def addEdge(self, source, destination, weight):
        first = self.getVertex(source)
        second = self.getVertex(destination)
        if first is second:
            raise ValueError("Self-connections are not supported")
        try:
            if isinstance(weight, bool):
                raise ValueError("Invalid weight")
            weight = float(weight)
        except (TypeError, ValueError, OverflowError) as error:
            raise ValueError("Transportation time must be numerical") from error
        if not math.isfinite(weight) or weight <= 0:
            raise ValueError("Transportation time must be positive and finite")
        if first.hasEdge(second):
            raise ValueError("Duplicate undirected edge")
        first.adjacent.insertLast(DSAGraphEdge(second, weight))
        second.adjacent.insertLast(DSAGraphEdge(first, weight))
        self._edge_count += 1

    def displayAsList(self):
        output = ""
        for vertex in self._vertices:
            output += vertex.label + " -> "
            first = True
            for edge in vertex.adjacent:
                if not first:
                    output += ", "
                output += f"{edge.destination.label} ({edge.weight:.2f} min)"
                first = False
            if first:
                output += "(isolated)"
            output += "\n"
        return output

    def breadthFirstSearch(self, source):
        """Return label/level arrays in BFS order; unreachable vertices excluded."""
        start = self.getVertex(source)
        levels = np.empty(self._count, dtype=int)
        for index in range(self._count):
            levels[index] = -1
        levels[start.index] = 0
        queue = DSAQueue()
        queue.enqueue(start)
        result = DSALinkedList()
        while not queue.isEmpty():
            current = queue.dequeue()
            result.insertLast(makePair(current.label, int(levels[current.index])))
            for edge in current.adjacent:
                neighbor = edge.destination
                if levels[neighbor.index] == -1:
                    levels[neighbor.index] = levels[current.index] + 1
                    queue.enqueue(neighbor)
        return result

    def displayBFS(self, source):
        output = ""
        previous_level = -1
        for label, level in self.breadthFirstSearch(source):
            if level != previous_level:
                if previous_level != -1:
                    output += "\n"
                output += f"Level {level}: "
                previous_level = level
            else:
                output += ", "
            output += label
        return output

    def depthFirstSearch(self, source):
        """Visit source component first, then other components; return one cycle.

        Colours: 0=unvisited, 1=active stack path, 2=finished.
        In an undirected graph the edge to the parent is not a cycle.
        """
        start = self.getVertex(source)
        colours = np.empty(self._count, dtype=int)
        parents = np.empty(self._count, dtype=object)
        for index in range(self._count):
            colours[index] = 0
            parents[index] = None
        order = DSALinkedList()
        cycle = DSALinkedList()

        def visit(root):
            # Store the neighbor iterator with each vertex so we can resume it.
            # This has the same traversal order as recursive DFS without its limit.
            stack = DSAStack()
            colours[root.index] = 1
            order.insertLast(root.label)
            stack.push(makePair(root, iter(root.adjacent)))
            while not stack.isEmpty():
                current, neighbors = stack.top()
                edge = next(neighbors, None)
                if edge is None:
                    colours[current.index] = 2
                    stack.pop()
                    continue
                neighbor = edge.destination
                if colours[neighbor.index] == 0:
                    parents[neighbor.index] = current
                    colours[neighbor.index] = 1
                    order.insertLast(neighbor.label)
                    stack.push(makePair(neighbor, iter(neighbor.adjacent)))
                elif (colours[neighbor.index] == 1
                      and neighbor is not parents[current.index]
                      and cycle.isEmpty()):
                    # Reconstruct the ancestor-to-current path and closing edge.
                    cursor = current
                    cycle.insertFirst(cursor.label)
                    while cursor is not neighbor:
                        cursor = parents[cursor.index]
                        cycle.insertFirst(cursor.label)
                    cycle.insertLast(neighbor.label)

        visit(start)
        for vertex in self._vertices:
            if colours[vertex.index] == 0:
                visit(vertex)
        return makePair(order, cycle)

    def dijkstra(self, source, destination):
        """Return an array containing minutes and the linked-list path.

        Unreachable means infinite minutes and an empty path.

        Select the next vertex by a linear scan: O(V^2 + E), O(V) workspace.
        Keep direct vertex references in edges to avoid lookup during relaxation.
        """
        start = self.getVertex(source)
        target = self.getVertex(destination)
        distances = np.empty(self._count, dtype=float)
        previous = np.empty(self._count, dtype=object)
        finished = np.empty(self._count, dtype=bool)
        for index in range(self._count):
            distances[index] = math.inf
            previous[index] = None
            finished[index] = False
        distances[start.index] = 0.0
        overflow_seen = False

        for _ in range(self._count):
            current = None
            for vertex in self._vertices:
                if (not finished[vertex.index]
                        and distances[vertex.index] < math.inf
                        and (current is None
                             or distances[vertex.index] < distances[current.index])):
                    current = vertex
            if current is None:
                break
            finished[current.index] = True
            if current is target:
                break
            for edge in current.adjacent:
                neighbor = edge.destination
                if finished[neighbor.index]:
                    continue
                candidate = float(distances[current.index]) + edge.weight
                if not math.isfinite(candidate):
                    # An overflowing alternative cannot improve a finite route.
                    overflow_seen = True
                    continue
                if candidate < distances[neighbor.index]:
                    distances[neighbor.index] = candidate
                    previous[neighbor.index] = current

        path = DSALinkedList()
        if not math.isfinite(distances[target.index]) and overflow_seen:
            for label, _ in self.breadthFirstSearch(source):
                if label == destination:
                    raise ValueError("Transportation-time total exceeds the finite numerical range")
        if math.isfinite(distances[target.index]):
            cursor = target
            while cursor is not None:
                path.insertFirst(cursor.label)
                cursor = previous[cursor.index]
        return makePair(float(distances[target.index]), path)
