# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Load CSV inputs, build the shared system and export collection records.

import csv
import numpy as np
from pathlib import Path
from common.DSALinkedList import DSALinkedList
from models.FarmRecord import FarmRecord
from module1_graph.DSAGraph import DSAGraph
from module2_hash.DSAHashTable import DSAHashTable
from services.CollectionScheduler import CollectionScheduler

ROOT = Path(__file__).resolve().parents[1]
HUB = "HUB"


def columnIndex(headers, name, required=True):
    if headers is not None:
        for index in range(len(headers)):
            if headers[index] == name:
                return index
    if required:
        raise ValueError("CSV is missing required column: " + name)
    return -1


def fieldValue(row, index):
    if index < 0:
        return ""
    if index >= len(row):
        raise ValueError("CSV row has missing columns")
    return row[index]


def loadFarmRecords(filename):
    records = DSALinkedList()
    names = np.empty(14, dtype=object)
    names[0] = "Id"
    names[1] = "Name"
    names[2] = "Species"
    names[3] = "Lat"
    names[4] = "Lng"
    names[5] = "Street Num"
    names[6] = "Street"
    names[7] = "Suburb"
    names[8] = "State"
    names[9] = "Postcode"
    names[10] = "Country"
    names[11] = "Map URL"
    names[12] = "Profile URL"
    names[13] = "Last Known Status"
    with open(filename, newline="", encoding="utf-8-sig") as source:
        reader = csv.reader(source)
        headers = next(reader, None)
        indices = np.empty(14, dtype=int)
        for index in range(len(names)):
            indices[index] = columnIndex(headers, names[index], index < 11)
        for row in reader:
            if len(row) == 0:
                continue
            try:
                values = np.empty(14, dtype=object)
                for index in range(len(names)):
                    values[index] = fieldValue(row, indices[index])
                record = FarmRecord(values[0], values[1], values[2], values[3], values[4],
                                    values[5], values[6], values[7], values[8], values[9],
                                    values[10], values[11], values[12], values[13])
            except (ValueError, TypeError) as error:
                raise ValueError(f"Farm CSV line {reader.line_num}: {error}") from error
            records.insertLast(record)
    return records


def loadGraph(records, edge_filename):
    graph = DSAGraph()
    graph.addVertex(HUB, "Proposed Kwinana-area biogas hub")
    for record in records:
        graph.addVertex(record.farm_id, record.name)
    with open(edge_filename, newline="", encoding="utf-8-sig") as source:
        reader = csv.reader(source)
        headers = next(reader, None)
        source_index = columnIndex(headers, "Source")
        destination_index = columnIndex(headers, "Destination")
        time_index = columnIndex(headers, "TransportTime")
        for row in reader:
            if len(row) == 0:
                continue
            try:
                graph.addEdge(fieldValue(row, source_index), fieldValue(row, destination_index),
                              fieldValue(row, time_index))
            except (ValueError, TypeError, KeyError) as error:
                raise ValueError(f"Edge CSV line {reader.line_num}: {error}") from error
    return graph


def buildSystem(trace=False):
    records = loadFarmRecords(ROOT / "data/dataset.csv")
    farms = DSAHashTable(53)
    for record in records:
        farms.insert(record, trace=trace)
    graph = loadGraph(records, ROOT / "data/transport_edges.csv")
    scheduler = CollectionScheduler(farms, graph, HUB)
    system = np.empty(4, dtype=object)
    system[0] = records
    system[1] = farms
    system[2] = graph
    system[3] = scheduler
    return system


def loadRequests(scheduler, filename):
    accepted = 0
    rejected = 0
    with open(filename, newline="", encoding="utf-8-sig") as source:
        reader = csv.reader(source)
        headers = next(reader, None)
        request_index = columnIndex(headers, "RequestID")
        farm_index = columnIndex(headers, "FarmID")
        feedstock_index = columnIndex(headers, "EstimatedFeedstock")
        for row in reader:
            if len(row) == 0:
                continue
            try:
                scheduler.insert(fieldValue(row, request_index), fieldValue(row, farm_index),
                                 fieldValue(row, feedstock_index))
                accepted += 1
            except (ValueError, KeyError, TypeError) as error:
                print(f"REJECTED request CSV line {reader.line_num}: {error}")
                rejected += 1
    counts = np.empty(2, dtype=object)
    counts[0] = accepted
    counts[1] = rejected
    return counts


def writeCollectionRecords(filename, records):
    with open(filename, "w", newline="", encoding="utf-8") as destination:
        writer = csv.writer(destination)
        fields = np.empty(6, dtype=object)
        fields[0] = "RequestID"
        fields[1] = "FarmID"
        fields[2] = "EstimatedFeedstock"
        fields[3] = "TransportTime"
        fields[4] = "Priority"
        fields[5] = "Status"
        writer.writerow(fields)
        for request in records:
            fields[0] = request.request_id
            fields[1] = request.farm_id
            fields[2] = request.feedstock
            fields[3] = request.transport_time
            fields[4] = request.priority
            fields[5] = request.status
            writer.writerow(fields)
