# Biogas Feedstock Collection Network

F.M. Ashfaq — 23472297

COMP5008 Data Structures and Algorithms

This program manages farm records and feedstock collection requests. It uses a
graph to find transport routes, a hash table to look up farms, a max heap to choose
the next collection, and Merge Sort or Quick Sort to prepare collection reports.

## Setup and run

From this folder, create and activate a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python interactive_menu.py
```

You can also run `python main.py`. It starts the same menu.

NumPy is used for array storage, following the practicals. The graph algorithms,
hash probing, heap operations and sorting algorithms are implemented in the code.
CSV files are read and written with `csv.reader` and `csv.writer`. Header columns
are found using a manual loop.

## Using the program

The program loads 40 farm records and a transport graph with 41 locations and
55 undirected connections. The collection heap starts empty.

Use the menu to display the network, run BFS or DFS, find a shortest route,
search or update farm records, and add collection requests. Option 13 loads the
supplied request data: 12 valid requests and 7 deliberate invalid cases.

Collection priority is `P = F / T`, where `F` is the estimated feedstock and `T` is
the shortest transport time to the hub. The request with the highest priority is
collected first. Equal priorities follow arrival order.

Option 14 sorts all accepted requests by transport time and exports them to
`sample_output/collection_records_sorted.csv`. The records keep their pending,
collected or cancelled status.

Farm and network changes stay in memory for the current session. A new farm needs
a graph location and transport connections before it can be scheduled.

## Files

| File or folder | What it does |
|---|---|
| `interactive_menu.py` | Menu and user input |
| `main.py` | Starts the menu |
| `models/` | FarmRecord and CollectionRequest data objects with validation |
| `services/DataLoader.py` | Loads CSV files and writes collection exports |
| `services/CollectionScheduler.py` | Connects farm lookup, routing, priority and request history |
| `common/` | Custom linked list, queue and stack |
| `module1_graph/` | Graph, BFS, DFS, Dijkstra and graph tests |
| `module2_hash/` | Double-hashed farm table and hash tests |
| `module3_heap/` | Max heap and scheduling tests |
| `module4_sorting/` | Merge Sort, Quick Sort, sorting tests and benchmarks |
| `data/` | Farm, transport-connection and collection-request CSV files |
| `sample_output/` | Test logs, sorted records and benchmark results |
| `report/figure_data/` | Saved graph, BFS, priority and heap-state values |
| `tests/` | Test runner, shared test helpers and input/menu tests |
| `data_preparation/` | Original Blackboard CSV and script for preparing model inputs |
| `report/generate_report_evidence.py` | Optional local tool for report results and figure data |
| `requirements.txt` | Python dependency |

## Tests and benchmarks

With the virtual environment active:

```sh
python3 -m tests.run_tests
```

This runs the four module drivers, input tests, integration tests and sorting
benchmarks. It saves the results in `sample_output/`. Report and figure generation
are separate from the tests.

You can run a module separately:

```sh
python -m module1_graph.GraphTestDriver
python -m module2_hash.HashTestDriver
python -m module3_heap.HeapTestDriver
python -m module4_sorting.SortingTestDriver
python -m module4_sorting.benchmark
```

The benchmark tests both sorting algorithms with 100, 500 and 1,000 records under
random, nearly sorted and reversed input. It uses seed 5008, one warm-up and seven
measured repetitions. Running it again will replace the saved timing results.

## Data and model

`data/dataset.csv` contains 40 selected WA records from the Blackboard-provided
`data_preparation/farm_dataset_sample.csv`.
The original farm IDs and source fields are retained.

The hub is a model Kwinana-area location. Connections, feedstock amounts and
transportation times are educational estimates. Edge times use coordinate distance,
a factor of 1.3 and an assumed speed of 60 km/h. One farm is deliberately isolated
to test unreachable routes.

To recreate the input CSV files:

```sh
python3 -m data_preparation.prepare_data
```

This resets the three files in `data/` to the supplied model inputs.

## Submission contents

Use the following structure inside `COMP5008_assignment_23472297.zip`:

```text
COMP5008_assignment_23472297/
  README.md
  requirements.txt
  main.py
  interactive_menu.py
  models/
  services/
  data/
  data_preparation/
  common/
  module1_graph/
  module2_hash/
  module3_heap/
  module4_sorting/
  tests/
  sample_output/
  technical_report.pdf
```

Include the module test drivers, shared tests, benchmark code, and input CSV files.
`sample_output/` contains example execution logs, measured timings and exported
records; the folder name follows the assignment specification and does not mean
that the farm identities are invented.

The farm records are source data. The proposed hub, transport network, estimated
travel times and feedstock quantities are educational modelling assumptions.

Do not include `.venv/`, `__pycache__/`, `.DS_Store`, the assignment question PDF,
or the local `report/` working folder. The final report PDF contains the required
diagrams; the figure-generation scripts and draft/audit notes are local tools.

Optional local report-evidence refresh, after running the tests:

```sh
python3 -m report.generate_report_evidence
```

The test runner does not depend on this optional tool.
