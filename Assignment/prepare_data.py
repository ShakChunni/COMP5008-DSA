# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Prepare the selected farm dataset and educational transport/request data.

"""Reproduce the selected dataset and educational network from the supplied CSV."""

import csv
import math
import numpy as np
from DataLoader import ROOT, HUB, columnIndex, fieldValue

HUB_LAT = -32.23
HUB_LNG = 115.78


def estimatedMinutes(first_lat, first_lng, second_lat, second_lng):
    """Great-circle distance * 1.3 road factor / 60 km/h, expressed in minutes."""
    lat1 = math.radians(float(first_lat))
    lat2 = math.radians(float(second_lat))
    difference_lat = lat2 - lat1
    difference_lng = math.radians(float(second_lng) - float(first_lng))
    value = (math.sin(difference_lat / 2) ** 2
             + math.cos(lat1) * math.cos(lat2) * math.sin(difference_lng / 2) ** 2)
    # Clamp rounding error before square roots near antipodal coordinates.
    value = min(1.0, max(0.0, value))
    distance = 6371.0 * 2 * math.atan2(math.sqrt(value), math.sqrt(1 - value))
    return max(1.0, round(distance * 1.3, 2))


def writeThreeFields(writer, first, second, third):
    fields = np.empty(3, dtype=object)
    fields[0] = first
    fields[1] = second
    fields[2] = third
    writer.writerow(fields)


def main():
    source_path = ROOT / "farm_dataset_sample.csv"
    selected = np.empty(40, dtype=object)
    count = 0
    with source_path.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.reader(source)
        fieldnames = next(reader, None)
        state_index = columnIndex(fieldnames, "State")
        status_index = columnIndex(fieldnames, "Last Known Status")
        category_index = columnIndex(fieldnames, "Categories")
        species_index = columnIndex(fieldnames, "Species")
        name_index = columnIndex(fieldnames, "Name")
        id_index = columnIndex(fieldnames, "Id")
        lat_index = columnIndex(fieldnames, "Lat")
        lng_index = columnIndex(fieldnames, "Lng")
        for row in reader:
            if len(row) == 0:
                continue
            species_field = fieldValue(row, species_index)
            accepted_species = False
            for species in species_field.split(", "):
                if (species == "Cows/cattle" or species == "Pigs"
                        or species == "Sheep" or species == "Goats"):
                    accepted_species = True
            eligible = (fieldValue(row, state_index) == "WA"
                        and fieldValue(row, status_index) == "Open"
                        and "unconfirmed" not in fieldValue(row, category_index).lower()
                        and "unconfirmed" not in species_field.lower()
                        and "proposed" not in fieldValue(row, name_index).lower()
                        and accepted_species)
            if eligible and count < 40:
                fields = np.empty(len(row), dtype=object)
                for index in range(len(row)):
                    fields[index] = row[index]
                selected[count] = fields
                count += 1
    if count < 40:
        raise ValueError("Source does not contain 40 eligible WA records")
    (ROOT / "data").mkdir(exist_ok=True)
    with (ROOT / "data/dataset.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(fieldnames)
        for row in selected:
            writer.writerow(row)

    with (ROOT / "data/transport_edges.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writeThreeFields(writer, "Source", "Destination", "TransportTime")

        def connect(first_index, second_index):
            first = selected[first_index] if first_index >= 0 else None
            second = selected[second_index]
            minutes = estimatedMinutes(first[lat_index] if first is not None else HUB_LAT,
                                       first[lng_index] if first is not None else HUB_LNG,
                                       second[lat_index], second[lng_index])
            writeThreeFields(writer, first[id_index] if first is not None else HUB, second[id_index], minutes)

        connect(-1, 0)
        for index in range(38):
            connect(index, index + 1)
        for index in range(10, 31, 10):
            connect(-1, index)
        for index in range(0, 37, 3):
            connect(index, index + 2)
        # selected[39] is deliberately isolated for the required unreachable test.

    with (ROOT / "data/collection_requests.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writeThreeFields(writer, "RequestID", "FarmID", "EstimatedFeedstock")
        for index in range(12):
            writeThreeFields(writer, f"R{index + 1:03}", selected[index][id_index], 10 + (index * 7) % 31)
        # Intentional invalid rows demonstrate validation; these are not farm data.
        writeThreeFields(writer, "R001", selected[12][id_index], 20)
        writeThreeFields(writer, "DUPFARM", selected[0][id_index], 20)
        writeThreeFields(writer, "ISOLATED", selected[39][id_index], 20)
        writeThreeFields(writer, "MISSING", "zzzzz", 20)
        writeThreeFields(writer, "BADID", "", 20)
        writeThreeFields(writer, "NEGATIVE", selected[13][id_index], -1)
        writeThreeFields(writer, "NOTFINITE", selected[14][id_index], "nan")
    print("Prepared 40 farms, 41 vertices, 55 edges, 12 valid and 7 invalid requests.")


if __name__ == "__main__":
    main()
