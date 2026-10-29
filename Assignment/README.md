# Biogas Feedstock Collection Network

F.M. Ashfaq, 23472297

COMP5008 Data Structures and Algorithms

This program manages farm records and feedstock collection requests. It uses a
graph to find transport routes, a hash table to look up farms, a max heap to choose
the next collection, and Merge Sort or Quick Sort to prepare collection reports.

## Setup and run

From this folder, create and activate a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 interactive_menu.py
```

You can also run `python3 main.py`. It starts the same menu.

NumPy is used for array storage, following the practicals. The graph algorithms,
hash probing, heap operations and sorting algorithms are implemented in the code.
CSV files are read and written with `csv.reader` and `csv.writer`. Header columns
are found using a manual loop.

## Using the program

The program loads 70 farm records and a transport graph with 71 locations and
98 undirected connections. The collection heap starts empty.

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

## Tests and benchmarks

With the virtual environment active:

```sh
python3 -m tests.run_tests
```

This runs the four module drivers, input tests, integration tests and sorting
benchmarks. It saves the results in `sample_output/`.

You can run a module separately:

```sh
python3 -m module1_graph.GraphTestDriver
python3 -m module2_hash.HashTestDriver
python3 -m module3_heap.HeapTestDriver
python3 -m module4_sorting.SortingTestDriver
python3 -m module4_sorting.benchmark
```

The benchmark tests both sorting algorithms with 100, 500 and 1,000 records under
random, nearly sorted and reversed input. It uses seed 5008, one warm-up and seven
measured repetitions. Running it again will replace the saved timing results.

## Data and model

`data/dataset.csv` contains 70 selected WA records from the Blackboard-provided
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

## Contents

```text
COMP5008_assignment_23472297/
  README.md                      this file
  requirements.txt               Python dependency (NumPy)
  technical_report.pdf           technical report
  main.py                        starts the menu
  interactive_menu.py            menu and user input
  common/
    DSALinkedList.py             doubly linked list
    DSAQueue.py                  queue built on the linked list
    DSAStack.py                  stack built on the linked list
  models/
    FarmRecord.py                farm record with validation
    CollectionRequest.py         collection request with validation
  services/
    DataLoader.py                loads CSV files and writes exports
    CollectionScheduler.py       farm lookup, routing, priority and history
  module1_graph/
    DSAGraph.py                  graph, BFS, DFS and Dijkstra
    DSAGraphNode.py              graph vertex and weighted edge
    GraphTestDriver.py           graph tests
  module2_hash/
    DSAHashTable.py              double-hashed farm table
    DSAHashEntry.py              hash table slot
    HashTestDriver.py            hash tests
  module3_heap/
    DSAHeap.py                   max heap
    DSAHeapEntry.py              heap entry with priority and sequence
    HeapTestDriver.py            heap and scheduling tests
  module4_sorting/
    DSAsorts.py                  Merge Sort and Quick Sort
    SortingTestDriver.py         sorting tests
    benchmark.py                 sorting benchmark
  tests/
    run_tests.py                 runs every test and saves the logs
    InputTestDriver.py           CSV input and menu tests
    TestHelpers.py               shared check functions
  data/
    dataset.csv                  70 selected farm records
    transport_edges.csv          98 transport connections
    collection_requests.csv      12 valid and 7 invalid requests
  data_preparation/
    prepare_data.py              recreates the three files in data/
    farm_dataset_sample.csv      original Blackboard CSV (229 rows)
  sample_output/
    graph_tests.txt              graph test log
    hash_tests.txt               hash test log
    heap_tests.txt               heap test log
    sorting_tests.txt            sorting test log
    input_tests.txt              input and menu test log
    integration_tests.txt        integration test log
    benchmark_run.txt            benchmark log
    benchmark_results.csv        benchmark timings
    benchmark_environment.json   benchmark settings and versions
    sorting_input_1000.csv       1,000-record benchmark input
    merge_sorted_1000.csv        Merge Sort output
    quick_sorted_1000.csv        Quick Sort output
    collection_records_sorted.csv  accepted requests sorted by transport time
```

Each folder with Python code also has an `__init__.py` package file.
