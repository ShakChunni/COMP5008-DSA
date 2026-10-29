# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Measure both custom sorts on reproducible graph-derived datasets.

import csv
import json
import platform
import random
import time
import numpy as np
from services.DataLoader import ROOT, buildSystem, writeCollectionRecords
from module4_sorting.DSAsorts import mergeSort, quickSort, isSorted

SEED = 5008
REPETITIONS = 7


def benchmarkSizes():
    sizes = np.empty(3, dtype=int)
    sizes[0] = 100
    sizes[1] = 500
    sizes[2] = 1000
    return sizes


def benchmarkConditions():
    conditions = np.empty(3, dtype=object)
    conditions[0] = "random"
    conditions[1] = "nearly_sorted"
    conditions[2] = "reversed"
    return conditions


def reachableFarmIDs(farms, graph, hub):
    identifiers = np.empty(farms.getCount(), dtype=object)
    count = 0
    for farm in farms.records():
        # A farm may be added to the lookup table before its graph location.
        if graph.hasVertex(farm.farm_id):
            minutes, _ = graph.dijkstra(farm.farm_id, hub)
            if minutes != float("inf") and minutes > 0:
                identifiers[count] = farm.farm_id
                count += 1
    return identifiers[:count]


def makeRecords(scheduler, size, generator):
    identifiers = reachableFarmIDs(scheduler.farms, scheduler.graph, scheduler.hub)
    if len(identifiers) == 0:
        raise ValueError("No reachable farms available for sorting records")
    records = np.empty(size, dtype=object)
    for index in range(size):
        farm_id = identifiers[generator.randrange(len(identifiers))]
        records[index] = scheduler.calculateRequest(f"B{size}_{index:04}", farm_id,
                                                   generator.randint(5, 50))
    return records


def shuffleArray(array, generator):
    # Fisher-Yates shuffle; reproducible without using a built-in sort.
    for index in range(len(array) - 1, 0, -1):
        other = generator.randrange(index + 1)
        temporary = array[index]
        array[index] = array[other]
        array[other] = temporary


def makeCondition(base, condition, generator):
    records = base.copy()
    if condition == "random":
        shuffleArray(records, generator)
    elif condition == "nearly_sorted" or condition == "reversed":
        mergeSort(records)
        if condition == "reversed":
            for index in range(len(records) // 2):
                other = len(records) - index - 1
                temporary = records[index]
                records[index] = records[other]
                records[other] = temporary
        else:
            # Select 10% distinct positions, then swap in disjoint pairs.
            count = len(records) // 10
            if count % 2 != 0:
                raise ValueError("Nearly-sorted generation requires an even displacement count")
            positions = np.empty(len(records), dtype=int)
            for index in range(len(records)):
                positions[index] = index
            shuffleArray(positions, generator)
            for index in range(0, count, 2):
                first = positions[index]
                second = positions[index + 1]
                temporary = records[first]
                records[first] = records[second]
                records[second] = temporary
    else:
        raise ValueError("Unknown input condition")
    return records


def sameRecords(before, after):
    """Check identity preservation independently of the sorting implementations."""
    same = len(before) == len(after)
    for original in before:
        matches = 0
        for candidate in after:
            if candidate is original:
                matches += 1
        if matches != 1:
            same = False
    return same


def runBenchmarks(scheduler=None):
    if scheduler is None:
        _, _, _, scheduler = buildSystem()
    output = ROOT / "sample_output"
    output.mkdir(exist_ok=True)
    rows = np.empty(18, dtype=object)
    row_index = 0
    for size_value in benchmarkSizes():
        size = int(size_value)
        base = makeRecords(scheduler, size, random.Random(SEED + size))
        conditions = benchmarkConditions()
        for condition_index in range(len(conditions)):
            condition = conditions[condition_index]
            inputs = makeCondition(base, condition, random.Random(SEED + size + condition_index + 1))
            totals = np.empty(2, dtype=float)
            totals[0] = 0.0
            totals[1] = 0.0
            # Warm-up outside the measured repetitions.
            mergeSort(inputs.copy())
            quickSort(inputs.copy())
            for repetition in range(REPETITIONS):
                # Alternate first algorithm to reduce ordering effects.
                for position in range(2):
                    algorithm_index = position if repetition % 2 == 0 else 1 - position
                    working = inputs.copy()  # Fresh copy, made outside timing.
                    start = time.perf_counter_ns()
                    if algorithm_index == 0:
                        mergeSort(working)
                    else:
                        quickSort(working)
                    elapsed = time.perf_counter_ns() - start
                    totals[algorithm_index] += elapsed / 1_000_000
                    if not isSorted(working) or not sameRecords(inputs, working):
                        raise AssertionError("Sorting correctness/permutation check failed")
            for algorithm_index in range(2):
                name = "Merge Sort" if algorithm_index == 0 else "Quick Sort"
                mean = totals[algorithm_index] / REPETITIONS
                row = np.empty(5, dtype=object)
                row[0] = size
                row[1] = condition
                row[2] = name
                row[3] = REPETITIONS
                row[4] = mean
                rows[row_index] = row
                row_index += 1
                print(f"{size:4} {condition:14} {name:10} mean={mean:.6f} ms")
            if size == 1000 and condition == "random":
                writeCollectionRecords(output / "sorting_input_1000.csv", inputs)
                working = inputs.copy()
                mergeSort(working)
                writeCollectionRecords(output / "merge_sorted_1000.csv", working)
                working = inputs.copy()
                quickSort(working)
                writeCollectionRecords(output / "quick_sorted_1000.csv", working)

    with (output / "benchmark_results.csv").open("w", newline="", encoding="utf-8") as destination:
        writer = csv.writer(destination, lineterminator="\n")
        header = np.empty(5, dtype=object)
        header[0] = "Records"
        header[1] = "Condition"
        header[2] = "Algorithm"
        header[3] = "Repetitions"
        header[4] = "MeanMilliseconds"
        writer.writerow(header)
        writer.writerows(rows)
    with (output / "benchmark_environment.json").open("w", encoding="utf-8") as destination:
        destination.write("{\n")
        destination.write('  "seed": ' + json.dumps(SEED) + ",\n")
        destination.write('  "repetitions": ' + json.dumps(REPETITIONS) + ",\n")
        destination.write('  "python": ' + json.dumps(platform.python_version()) + ",\n")
        destination.write('  "numpy": ' + json.dumps(np.__version__) + ",\n")
        destination.write('  "platform": ' + json.dumps(platform.platform()) + ",\n")
        destination.write('  "processor": ' + json.dumps(platform.processor()) + ",\n")
        destination.write('  "timer": "time.perf_counter_ns",\n')
        destination.write('  "farm_records": ' + json.dumps(scheduler.farms.getCount()) + ",\n")
        destination.write('  "vertices": ' + json.dumps(scheduler.graph.getVertexCount()) + ",\n")
        destination.write('  "edges": ' + json.dumps(scheduler.graph.getEdgeCount()) + ",\n")
        destination.write('  "dataset_generation_timed": false,\n')
        destination.write('  "input_copy_timed": false,\n')
        destination.write('  "verification_timed": false\n')
        destination.write("}\n")
    return rows


if __name__ == "__main__":
    runBenchmarks()
