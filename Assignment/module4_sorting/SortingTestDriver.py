# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Test sorting correctness, stability and required input conditions.

import random
import numpy as np
from CollectionRequest import CollectionRequest
from FarmRecord import FarmRecord
from DataLoader import buildSystem
from module4_sorting.DSAsorts import mergeSort, quickSort, isSorted
from module4_sorting.benchmark import makeRecords, makeCondition, sameRecords, reachableFarmIDs, SEED
from module4_sorting.benchmark import benchmarkSizes, benchmarkConditions
from TestHelpers import check


def fixture(values):
    records = np.empty(len(values), dtype=object)
    for index, value in enumerate(values):
        request = CollectionRequest(f"TEST{index}", "testfarm", 10)
        request.transport_time = value
        records[index] = request
    return records


def sameFarmIDs(before, after):
    if len(before) != len(after):
        return False
    for index in range(len(before)):
        if before[index] != after[index]:
            return False
    return True


def fixtureValues(case_index):
    """The original nine edge cases, stored in fixed-size NumPy arrays."""
    if case_index == 0:
        return np.empty(0, dtype=int)
    if case_index == 1:
        values = np.empty(1, dtype=int)
        values[0] = 1
    elif case_index == 2 or case_index == 3:
        values = np.empty(2, dtype=int)
        values[0] = 2 if case_index == 2 else 1
        values[1] = 1 if case_index == 2 else 2
    elif case_index == 4:
        values = np.empty(3, dtype=int)
        values[0] = 3
        values[1] = 1
        values[2] = 2
    elif case_index == 5:
        values = np.empty(3, dtype=int)
        for index in range(3):
            values[index] = 2
    elif case_index == 6 or case_index == 7:
        values = np.empty(5, dtype=int)
        for index in range(5):
            values[index] = 5 - index if case_index == 6 else index + 1
    else:
        values = np.empty(4, dtype=float)
        values[0] = 1.5
        values[1] = 0.5
        values[2] = 1.5
        values[3] = 2.5
    return values


def runTests():
    print("=== SORTING EDGE CASES (SYNTHETIC UNIT FIXTURES) ===")
    for case_index in range(9):
        values = fixtureValues(case_index)
        original = fixture(values)
        for algorithm_index in range(2):
            working = original.copy()
            if algorithm_index == 0:
                mergeSort(working)
                name = "mergeSort"
            else:
                quickSort(working)
                name = "quickSort"
            check(f"{name} {values}", isSorted(working) and sameRecords(original, working))
    values = np.empty(6, dtype=int)
    for index in range(6):
        values[index] = 2 - index % 2
    repeated = fixture(values)
    mergeSort(repeated)
    stable = True
    for index in range(6):
        original_index = 2 * index + 1 if index < 3 else 2 * (index - 3)
        if repeated[index].request_id != f"TEST{original_index}":
            stable = False
    check("Merge Sort preserves equal-key order", stable)
    values = np.empty(1500, dtype=int)
    for index in range(1500):
        values[index] = 1
    large = fixture(values)
    quickSort(large)
    check("Quick Sort all-equal large input terminates", isSorted(large))

    print("=== REQUIRED GRAPH-DERIVED INPUT CONDITIONS ===")
    _, _, _, scheduler = buildSystem()
    for size_value in benchmarkSizes():
        size = int(size_value)
        base = makeRecords(scheduler, size, random.Random(SEED + size))
        for condition in benchmarkConditions():
            inputs = makeCondition(base, condition, random.Random(SEED))
            if condition == "nearly_sorted":
                baseline = base.copy()
                mergeSort(baseline)
                moved = 0
                for index in range(size):
                    if inputs[index] is not baseline[index]:
                        moved += 1
                check(f"{size}: exactly 10% records displaced", moved == size // 10)
            if condition == "reversed":
                descending = True
                for index in range(1, size):
                    if inputs[index - 1].transport_time < inputs[index].transport_time:
                        descending = False
                check(f"{size}: reversed descending", descending)
            for algorithm_index in range(2):
                working = inputs.copy()
                if algorithm_index == 0:
                    mergeSort(working)
                    name = "mergeSort"
                else:
                    quickSort(working)
                    name = "quickSort"
                check(f"{size} {condition} {name}",
                      isSorted(working) and sameRecords(inputs, working))
    # Synthetic fixture for a normal menu workflow: insert farm before graph node.
    before = reachableFarmIDs(scheduler.farms, scheduler.graph, scheduler.hub)
    extra = FarmRecord("new01", "Test farm without a graph location", "Pigs", -32, 116,
                       "", "", "", "WA", "", "Australia")
    scheduler.farms.insert(extra)
    after = reachableFarmIDs(scheduler.farms, scheduler.graph, scheduler.hub)
    check("benchmark ignores farms whose graph locations are not yet added",
          sameFarmIDs(before, after))
    generated = makeRecords(scheduler, 100, random.Random(SEED))
    excludes_new_farm = True
    for request in generated:
        if request.farm_id == extra.farm_id:
            excludes_new_farm = False
    check("benchmark records still generate after farm-only insertion",
          len(generated) == 100 and excludes_new_farm)
    scheduler.graph.addVertex(extra.farm_id, extra.name)
    check("benchmark also ignores newly added isolated farm locations",
          sameFarmIDs(reachableFarmIDs(scheduler.farms, scheduler.graph, scheduler.hub), before))
    scheduler.graph.addEdge(extra.farm_id, scheduler.hub, 10)
    connected = reachableFarmIDs(scheduler.farms, scheduler.graph, scheduler.hub)
    found = False
    for farm_id in connected:
        if farm_id == extra.farm_id:
            found = True
            break
    check("benchmark includes farm after it is connected to hub", found)
    print("SORTING TESTS PASSED")


if __name__ == "__main__":
    runTests()
