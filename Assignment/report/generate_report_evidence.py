# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Generate measured-result notes and CSV evidence for the report.

"""Create factual Markdown results and CSV figure inputs from the running code."""

import contextlib
import csv
import io
import json
import numpy as np
from services.DataLoader import ROOT, buildSystem, loadRequests, columnIndex
from data_preparation.prepare_data import HUB_LAT, HUB_LNG
from common.DSALinkedList import DSALinkedList
from module2_hash.DSAHashTable import DSAHashTable


def environmentValue(filename, name):
    """Read one scalar from the flat JSON file written by the benchmark."""
    with filename.open(encoding="utf-8") as source:
        for line in source:
            text = line.strip()
            colon = 0
            while colon < len(text) and text[colon] != ":":
                colon += 1
            if colon == len(text):
                continue
            if json.loads(text[:colon]) == name:
                value = text[colon + 1:].strip()
                if value.endswith(","):
                    value = value[:-1]
                return json.loads(value)
    raise KeyError("Missing benchmark environment field: " + name)


def main():
    report = ROOT / "report"
    figures = report / "figure_data"
    figures.mkdir(parents=True, exist_ok=True)
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        records, farms, graph, scheduler = buildSystem()
        accepted, rejected = loadRequests(scheduler, ROOT / "data/collection_requests.csv")
        collected = np.empty(accepted, dtype=object)
        for index in range(accepted):
            collected[index] = scheduler.extract_priority()
    with (figures / "graph_vertices.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        row = np.empty(5, dtype=object)
        row[0] = "Label"
        row[1] = "Name"
        row[2] = "Latitude"
        row[3] = "Longitude"
        row[4] = "Role"
        writer.writerow(row)
        row[0] = "HUB"
        row[1] = "Proposed Kwinana-area hub"
        row[2] = HUB_LAT
        row[3] = HUB_LNG
        row[4] = "hub"
        writer.writerow(row)
        for record in records:
            row[0] = record.farm_id
            row[1] = record.name
            row[2] = record.latitude
            row[3] = record.longitude
            row[4] = "isolated_farm" if record is records.peekLast() else "farm"
            writer.writerow(row)
    with (figures / "bfs_levels.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        row = np.empty(2, dtype=object)
        row[0] = "Label"
        row[1] = "Level"
        writer.writerow(row)
        writer.writerows(graph.breadthFirstSearch("HUB"))
    with (figures / "priorities_and_collection_order.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        row = np.empty(7, dtype=object)
        row[0] = "CollectionOrder"
        row[1] = "RequestID"
        row[2] = "FarmID"
        row[3] = "FeedstockModelTonnes"
        row[4] = "ShortestMinutes"
        row[5] = "Priority"
        row[6] = "PathToHub"
        writer.writerow(row)
        for index, request in enumerate(collected):
            row[0] = index + 1
            row[1] = request.request_id
            row[2] = request.farm_id
            row[3] = request.feedstock
            row[4] = request.transport_time
            row[5] = request.priority
            row[6] = str(request.path)
            writer.writerow(row)
    with (figures / "heap_states.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        row = np.empty(3, dtype=object)
        row[0] = "OperationNumber"
        row[1] = "Operation"
        row[2] = "HeapArrayIndexOrder"
        writer.writerow(row)
        number = 0
        captured.seek(0)
        for captured_line in captured:
            line = captured_line.rstrip("\r\n")
            if line.startswith("HEAP after "):
                number += 1
                colon = 0
                while colon < len(line) and line[colon] != ":":
                    colon += 1
                if colon == len(line):
                    raise ValueError("Heap trace is missing its array separator")
                row[0] = number
                row[1] = line[:colon].removeprefix("HEAP after ")
                row[2] = line[colon + 2:]
                writer.writerow(row)

    with (ROOT / "sample_output/benchmark_results.csv").open(newline="") as source:
        benchmark_rows = DSALinkedList()
        reader = csv.reader(source)
        header = next(reader, None)
        records_column = columnIndex(header, "Records")
        condition_column = columnIndex(header, "Condition")
        mean_column = columnIndex(header, "MeanMilliseconds")
        for parsed in reader:
            if len(parsed) == 0:
                continue
            row = np.empty(len(parsed), dtype=object)
            for index in range(len(parsed)):
                row[index] = parsed[index]
            benchmark_rows.insertLast(row)
    environment_path = ROOT / "sample_output/benchmark_environment.json"
    python_version = environmentValue(environment_path, "python")
    numpy_version = environmentValue(environment_path, "numpy")
    system = environmentValue(environment_path, "platform")
    processor = environmentValue(environment_path, "processor")
    seed = environmentValue(environment_path, "seed")
    repetitions = environmentValue(environment_path, "repetitions")
    _, cycle = graph.depthFirstSearch("HUB")
    result = "# Measured results and figure inputs\n\n"
    result += ("Generated by `python3 -m report.generate_report_evidence` after `python3 -m tests.run_tests`. "
               "Re-run both after code/data changes. Timings describe this machine/run, not universal performance.\n\n")
    result += (f"Dataset: **{records.count()} farms**, all WA; graph: **{graph.getVertexCount()} vertices**, "
               f"**{graph.getEdgeCount()} undirected edges**; isolated farm: **{records.peekLast().farm_id}**.\n\n"
               f"Detected cycle: `{cycle}`. BFS reaches {graph.breadthFirstSearch('HUB').count()} locations "
               f"including the hub. DFS visits all {graph.getVertexCount()}, including the isolated farm.\n\n")
    result += "## Hash table evidence\n\n"
    result += "| Successful insertions | Live records | Capacity | Load factor |\n|---:|---:|---:|---:|\n"
    replay = DSAHashTable(53)
    resize_at = None
    with contextlib.redirect_stdout(io.StringIO()):
        for record in records:
            size_before = replay.getSize()
            replay.insert(record)
            if replay.getSize() != size_before and resize_at is None:
                resize_at = replay.getCount()
            if replay.getCount() % 10 == 0:
                result += (f"| {replay.getCount()} | {replay.getCount()} | {replay.getSize()} | "
                           f"{replay.loadFactor():.6f} |\n")
    final_count = replay.getCount()
    result += (f"\nThe {resize_at}th insertion would make {resize_at}/53 > 0.7, so the table grows "
               f"from 53 to {replay.getSize()} before inserting it. After deletion, "
               f"{final_count - 1}/{replay.getSize()} = {(final_count - 1) / replay.getSize():.6f}.\n\n"
               "Explicit collision: `qlctx` and `c1c13` both initially hash to index 45 in capacity 53. "
               "The complete probe sequence and deletion/reinsertion evidence are in "
               "`sample_output/hash_tests.txt`.\n\n")
    result += "## Scheduling results\n\n"
    result += f"The request CSV accepts **{accepted}** and rejects **{rejected}** rows.\n\n"
    result += "| Order | Request | FarmID | F (model tonnes) | T (minutes) | P=F/T |\n|---:|---|---|---:|---:|---:|\n"
    for index, request in enumerate(collected):
        result += (f"| {index + 1} | {request.request_id} | {request.farm_id} | "
                   f"{request.feedstock:.2f} | {request.transport_time:.2f} | {request.priority:.6f} |\n")
    result += "\nThe required five-extraction example is the first five rows. Equal priorities use FIFO insertion order.\n\n"
    result += "## Sorting measurements\n\n"
    result += (f"Python {python_version}; NumPy {numpy_version}; {system}; "
               f"processor `{processor}`. Base seed {seed}; "
               f"{repetitions} repetitions; one warm-up per algorithm/case. "
               "Mean time in milliseconds; `time.perf_counter_ns`. Input creation, copying, "
               "CSV writes and correctness checks are outside timing.\n\n")
    result += "| Records | Condition | Merge Sort (ms) | Quick Sort (ms) |\n|---:|---|---:|---:|\n"
    benchmark_iterator = iter(benchmark_rows)
    while True:
        merge = next(benchmark_iterator, None)
        if merge is None:
            break
        quick = next(benchmark_iterator, None)
        if quick is None:
            raise ValueError("Benchmark results are missing a matching algorithm row")
        result += (f"| {merge[records_column]} | {merge[condition_column]} | "
                   f"{float(merge[mean_column]):.6f} | {float(quick[mean_column]):.6f} |\n")
    result += ("\nDiscuss growth within each algorithm/condition and compare algorithms within each row. "
               "Short runs are sensitive to scheduler activity, caches, Python/runtime overhead and noise. "
               "The benchmarks contain repeated transport-time keys because many requests revisit the "
               f"same {graph.getVertexCount() - 2} reachable farms. Median-of-three helps on ordered data but is not a worst-case guarantee. "
               "Do not conclude that reversed data necessarily causes quadratic behavior for this implementation.\n\n")
    result += "## Figure inputs\n\n"
    result += ("- `figure_data/graph_vertices.csv`: exact node IDs/names/coordinates and isolated node.\n"
               "- `../data/transport_edges.csv`: all exact edges and estimated minute weights.\n"
               "- `figure_data/bfs_levels.csv`: exact BFS levels from HUB.\n"
               "- `figure_data/priorities_and_collection_order.csv`: computed F, T, P, order and paths.\n"
               "- `figure_data/heap_states.csv`: array positions after each insertion/extraction.\n"
               "- `../sample_output/benchmark_results.csv`: all 18 measured timing entries.\n")
    (report / "RESULTS.md").write_text(result, encoding="utf-8")
    print("Created report/RESULTS.md and four CSV figure inputs.")


if __name__ == "__main__":
    main()
