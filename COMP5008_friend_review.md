# COMP5008 assignment ZIP: strict review

Reviewed on 29 October 2026.

**Verdict: not submission-ready yet.** The main algorithms work in the checks performed, but there are restriction risks, a missing live request-history/reporting connection, an identifier collision, and unfinished report/submission requirements. Passing the supplied tests does not resolve those issues.

## Scope and evidence

- Reviewed archive: `COMP5008_assignment-latest.zip`.
- Internal project folder: `COMP5008_assignment_STUDENTID/`.
- Requirements: `COMP5008_Final_Assignment_Biogas_Feedstock_Collection_Network.pdf`, including Appendix 1, plus the semester restrictions supplied for this review.
- ZIP SHA-256: `66396d38c41abfa9eee69483cd4d88fe75d0f58a8dbc709d273e96b556cfb5d5`.
- Reviewed source, tests, CSVs, README, saved outputs, benchmark results, report source and all five rendered PDF pages. The PDF, not the editable DOCX, is the assessed report considered here.
- Tests ran in an extracted temporary copy. No implementation fixes were made. Running the benchmark regenerated results only inside that temporary copy; the original archived results were separately inspected.

Paths and line numbers below refer to files inside the ZIP's project folder. PDF page numbers refer to the current PDF, before adding the required cover page.

This is diagnostic feedback, not replacement assignment code or report text to submit. No conclusion about code authorship can be drawn from coding style or placeholders.

## What passed

| Check | Result |
|---|---|
| Submitted unit suite | All 81 tests passed on rerun |
| All demos through `interactive_menu.py --demo all` | Completed with exit code 0 |
| Additional graph checks | 150 generated graphs: BFS levels, whole-graph cycle detection and all-source shortest distances matched independent checks |
| Additional hash checks | 5,000 mixed insert/search/delete operations matched independent state |
| Additional heap checks | 1,000 insertions and 1,000 extractions; ordering, equal-priority FIFO and heap property passed |
| Additional sorting checks | Both sorts passed 300 random inputs and preserved the input arrays |
| Required benchmark matrix | All 18 algorithm/size/condition combinations passed sorted-order and permutation checks; Merge Sort retained stability |
| Nearly sorted inputs | Exactly 10% of record positions displaced at 100, 500 and 1,000 records |
| Farm CSV | 229 records, 229 unique IDs, all WA; required fields present and all records loaded |
| Modelled graph | 229 vertices, 451 edges, six isolated vertices and 219 reachable farm records |
| Saved benchmark evidence | Archived CSV has 18 rows; report values agree with the archived timing output at the displayed precision |

The additional reviewer diagnostics were outside the submitted project. They are not proposed assessment test files. These checks give useful evidence, not a guarantee that every possible input passes.

## Fix order

1. Resolve the prohibited-container uses in F01.
2. Connect actual session requests to retained, sorted reporting records in F02.
3. Complete identity, cover and required report sections in F03-F04.
4. Fix heap trace coverage, complexity explanations and the `HUB` collision in F05-F07.
5. Finish citations and PDF presentation in F08-F09.
6. Address the smaller robustness/documentation items in F10-F13.

## F01 - High: restricted containers remain in implementation code

**Requirements:** Section 9.4 and the additional semester rules prohibiting built-in lists in data-structure implementations and tuples. Section 9.4 states that a 100% penalty applies to an affected module when a prohibited built-in replaces the required implementation. The marker decides how that provision applies; this review is not a penalty prediction.

The outer `DynArray` uses NumPy, but some objects stored inside it are ordinary Python lists or tuples. A NumPy-backed outer container does not make its inner Python lists into NumPy arrays.

### Highest-risk occurrences

| Location | What is actually stored | What to change |
|---|---|---|
| `module1_graph/graph.py:107-108` | `[v, weight]` and `[u, weight]`: built-in lists forming adjacency entries | Use an allowed, explicitly defined edge representation, not Python list pairs |
| `module1_graph/algorithms.py:108,119` | `[vertex, neighbour_index]`: built-in lists used as DFS stack frames | Use an allowed frame object or manually managed arrays |
| `module1_graph/priority_queue.py:45` | `(distance, counter, vertex)`: tuples stored as Dijkstra heap entries | Use an allowed heap-entry representation |
| `module1_graph/network.py:119,128,181` | Coordinate tuples and a candidate-edge tuple | Replace these stored tuples under the supplied blanket tuple restriction |
| `module1_graph/graph.py:186` | Tuple edge records | Replace the stored tuple representation |
| `module4_sorting/records.py:78,132-134` | Farm/time tuples and a Python list of condition tuples | Use allowed records/containers for generated sorting data |
| `module4_sorting/demo_module4.py:40-44` | The collection log is accumulated using a list and `.append()` | Retain records in an allowed container |
| `module4_sorting/benchmark.py:93,96,115` | Python lists for position tracking, seen flags and a mutable counter | Use allowed storage; these are not NumPy arrays |

### Additional occurrences to resolve or clarify with the tutor

- `module2_hash/farm_record.py:104-118,122-125`: lists and `.append()` for validation messages and addresses.
- `module2_hash/hash_table.py:95,260`: list-of-tuples statistics output and tuple load-history records. Its bucket chains themselves are manually implemented, which is good.
- `module2_hash/csv_loader.py:16,33-39`: list headers and `csv.DictReader`, which produces dictionaries. Header membership checks also use automatic sequence searching.
- `module3_heap/scheduler.py:161-173`: request CSV rows are collected in a Python list of tuples using `.append()`; it also uses `csv.DictReader`.
- `module3_heap/heap.py:36,163-170`: a default list route and lists for tree formatting. The actual heap array is the custom NumPy-backed container.
- `interactive_menu.py:144-149,242-246`: list accumulation and a built-in dictionary mapping demo names to functions. Menu option lists/tuples occur throughout the file.
- `module3_heap/demo_module3.py:58-59,87-113`: list comprehensions and `.append()` for selected farms, accepted requests and extraction order.
- `module4_sorting/benchmark.py:41,47,227-236,280-286`: list constants, lists of tuples, supplementary input lists and plotting lists.
- `data/generate_requests.py:41-66`, `data/check_dataset.py:33-37`, and several submitted test files also use lists and `.append()`.

Core graph/heap storage is the clearest compliance problem. Parsing, menu formatting, plotting and test fixtures are different contexts: confirm whether the tutor permits limited use there rather than pretending that Section 9.4 alone settles every occurrence. Under the strict no-list/no-tuple instructions supplied for this review, those uses still need attention or explicit approval.

**Documentation also needs correction:** `README.md:67-74` and `docs/technical_report.md:33-38` claim a level of built-in avoidance that the files do not support. For example, `run_demo()` uses a dictionary. Fix the implementation and then describe it accurately; do not just remove the claim and leave restricted core storage unchanged.

**What is not the problem:** `DynArray.pop()`, `MinPriorityQueue.pop()`, `NameIndex` and `VertexMap` are project-defined implementations, not Python's list/dictionary operations. `try`, `except` and `raise` are language constructs, not automatic sorting/searching functions. Scalar helpers such as `ord()`, `len()` and `float()` do not replace the required algorithms. Do not remove legitimate exception handling because it looks like a built-in.

No direct use of built-in sorting, `heapq`, a graph library or NumPy sort/search routines was found in the reviewed implementation. That does not clear the separate container violations above.

**Verification:** inspect actual stored entry/frame types, not just the outer array type. Rerun the full suite and demos after changing representations. Recheck all submitted helper/test files against the tutor's exact restriction scope.

## F02 - High: Module 4 does not report the user's actual session requests

**Requirements:** Section 7.1 requires complete stored collection-request records in sorted order for reporting; Section 8 requires integrated modules.

**Where:**

- `interactive_menu.py:224-235`: `menu_sorting(_s)` ignores the supplied session.
- `module4_sorting/demo_module4.py:32-44`: builds a new system, loads the original CSV again and creates a separate temporary collection log.
- `module3_heap/scheduler.py:65-71,127-128,136-152`: there is no retained request-history collection. Processing removes a request from the heap and returns a result; the menu does not save that result.
- `docs/technical_report.md:48-50`: describes records coming from the scheduler's log, but no such retained log exists in the scheduler.

**Reproduced:** submitting and serving a request for `c4ffa` with feedstock `987.6` succeeds. Selecting Module 4's small sorting example then prints the fixed 14-record demo; the custom request is absent. Inspecting scheduler state confirms it has no request-history field.

There is also no persistent sorted collection-record store/export. The written benchmark CSV contains timing measurements, not collection-request history. Captured console output is not the same as maintaining that history.

**How to address:** retain accepted requests and their relevant status/history in an allowed structure shared with the session. Have the real reporting action sort that retained data by T, rather than silently rebuilding the demo. Implement an agreed persistent record store/export. The brief says “database” but does not prescribe SQL or a database library; clarify acceptable storage with the tutor rather than adding an unnecessary database dependency. Keep the synthetic benchmark as a separate experiment.

**Verification:** submit a distinctive request, process it, open reporting and confirm the same record appears exactly once with its actual T. Confirm pending/completed records are not silently lost, exported records are ascending by T, and saved history survives whatever persistence boundary the chosen design promises. Add an end-to-end integration test: the existing tests do not cover this menu-to-report path.

## F03 - High: identity, naming and required front cover are unfinished

**Requirements:** Sections 9.1, 9.2 and 9.5.

**Where:**

- Outer filename: `COMP5008_assignment-latest.zip`, not the required student-ID filename.
- Inner folder: `COMP5008_assignment_STUDENTID/`.
- Source headers, for example `interactive_menu.py:3`: `YOUR NAME (YOUR STUDENT ID)`.
- PDF page 1 and `docs/technical_report.md:4`: the same identity placeholder.
- PDF page 1 starts with the technical report; the required Declaration of Originality is not its first page.
- `README.md:12-18` itself lists these unfinished submission steps.

**How to address:** enter the real author/student ID, rename the ZIP and its top-level folder to the exact required forms, and include the required completed Declaration of Originality as report page 1. Regenerate/check the actual PDF: changing a Python header or Markdown source does not automatically update an already-built PDF.

**Verification:** open the final ZIP and final PDF, not only the working folder. Search submitted text/source for remaining identity placeholders. Submit the PDF to Turnitin and the ZIP to the assignment link; the brief requires both.

## F04 - Medium: the report does not follow the required Appendix 1 structure

**Requirements:** Section 10 and Appendix 1 explicitly require the supplied section structure.

**Where:** `docs/technical_report.md:8-249`; PDF pages 1-4.

The report contains much of the technical content, but uses eight differently organised sections instead of the required structure. Dataset preparation is embedded in other sections, reflection is a short sorting-choice paragraph, and no Generative AI Declaration section is present.

**How to address:** organise the existing material under the required headings:

1. System Overview
2. Dataset and Data Preparation
3. Data-Structure Justification
4. Module Integration
5. Algorithm Complexity
6. Experimental Results
7. Reflection and Design Trade-Offs
8. Limitations and Assumptions
9. Generative AI Declaration
10. References

The reflection should explain actual learning and important choices across the system, not just which sort is preferred. The declaration must truthfully describe permitted AI use; this review cannot establish authorship or certify a declaration. Do not submit this review as your own report text.

**Verification:** map each Appendix 1 bullet to a specific final-report paragraph. Check the regenerated PDF stays within the 20-page limit, excluding references/appendix.

## F05 - Medium: the main heap run stops tracing before it stops extracting

**Requirements:** Sections 6.3.2 and 6.3.4 require the heap array after every insertion and every extraction.

**Where:** `module3_heap/demo_module3.py:99-113`; report explanation at `docs/technical_report.md:123-125`.

The run inserts 14 requests, traces six extractions, then explicitly sets `heap.trace = False` and removes the remaining eight. It exceeds the minimum five extractions, but does not show the state after every extraction actually performed in that demonstration.

**How to address:** either keep tracing through the full drain, or demonstrate the required traced extractions and do not silently perform further untraced extractions as part of that run. Update the saved trace and report to match the final behaviour. The trace facility itself exists and works.

**Verification:** in the main 14-request run, if all 14 are removed, there should be 14 corresponding post-extraction heap states, including the final empty state. Do not count unrelated edge-case traces to hide omissions in this run.

## F06 - Medium: complexity claims need to match these implementations

**Requirements:** Section 7.2.7 and Appendix 1 Section 5; complexity/reflection marks.

### A. Optimised Merge Sort has a linear best case

**Where:** `module4_sorting/sorting.py:20-23,85-88`; `docs/technical_report.md:201,228`; PDF page 4.

The code skips merging when both sorted halves are already in order. On fully ascending input, every internal call returns after its boundary check. There are linearly many calls, not n log n merge work.

Independent counts: 512 elements caused 1,022 key evaluations; 1,024 caused 2,046. That is `2(n-1)`.

**Correct explanation:** this version has a tight best case of Theta(n), with average/worst Theta(n log n). Calling O(n log n) an upper bound is not mathematically false, but presenting it as the best-case classification/“always” cost misses this implementation's optimisation. All-equal input also benefits from the shortcut, so the statement that Merge Sort cannot exploit duplicates is too broad (`docs/technical_report.md:210`).

### B. Public Quick Sort allocates a full output copy

**Where:** `module4_sorting/sorting.py:51-57,113-119`; `docs/technical_report.md:150,205,229`.

The partitioning routine works in place on its working array and uses O(log n) stack because it recurses on the smaller side. However, `quick_sort()` first allocates an O(n) copy. The complete callable is not simply an O(log n)-extra-memory, in-place API on the caller's input.

**Correct explanation:** distinguish the O(log n) recursion stack from the O(n) new output/working array. If excluding returned-output space, explicitly say so. Do not recommend this public API as if it avoided allocating another full array.

### C. Lazy Dijkstra can retain O(E) heap entries

**Where:** `module1_graph/algorithms.py:16,201-217`; `module1_graph/priority_queue.py:45`; `docs/technical_report.md:77`.

Every successful improvement pushes a new queue entry; older entries remain until popped. This is not a one-entry-per-vertex decrease-key heap.

Independent positive-weight graph checks observed 238 live entries for 30 vertices/435 edges, and 928 for 60 vertices/1,770 edges. The queue is not bounded to V entries.

**Correct explanation:** account for O(V + E) auxiliary storage in the worst case for this lazy-duplicate implementation. O((V + E) log V) time remains a conventional bound for this simple graph setting; explain the queue strategy rather than claiming O(V) queue/workspace.

### D. Whole-network DFS repeats full-size map allocation

**Where:** `module1_graph/algorithms.py:103,151-158`; `common/containers.py:196-200`; `docs/technical_report.md:76`.

Each disconnected component creates a new parent `VertexMap` sized to every vertex. With V isolated vertices this costs Theta(V²) initialisation work, despite the stated O(V + E) DFS time.

Independent instrumentation: 100 isolated vertices created 101 maps totalling 10,100 slots; 200 created 201 maps totalling 40,200 slots. Each map also allocates its presence flags.

**How to address:** reuse appropriately scoped traversal storage across components, or accurately document the implemented whole-network worst case. Confirm cycle detection remains correct for disconnected components.

### E. Separate algorithm work from allocation/tracing costs

`MaxHeap.insert()` uses `DynArray.push()`, which occasionally copies the whole capacity while growing. Percolation is O(log n), but an individual growth-triggering insertion can cost O(n); distinguish amortised insertion from strict per-operation worst case. With tracing enabled, printing a full heap state is itself linear in heap size, so measured traced operations are not just O(log n).

## F07 - Medium: a farm ID can collide with the internal hub name

**Requirements:** Sections 4.2.1, 5.2.5, 6.3.1 and 9.5: valid locations, important input validation and correct routing integration.

**Where:** `module2_hash/farm_record.py:16-30`; `system_builder.py:37`; `module1_graph/network.py:118-128,78-82`; `interactive_menu.py:143-160`.

**Reproduced through the same public operations used by the menu:** insert a valid-format farm ID `HUB` at `(-33.5, 117.5)`, rebuild the network and submit a request. Insertion and submission succeed, but T is `0` and the path is just `HUB`, despite those coordinates being far from the configured hub.

**Why:** the farm table allows that ID. The graph already contains the hub vertex with the same name, so adding the farm vertex fails as a duplicate. Later lookup mistakes the farm ID for the processing hub.

**How to address:** keep hub identity separate from farm-ID identity, or explicitly reject reserved collisions before inserting the farm. Do not rewrite actual source FarmIDs to conceal the issue. Rejection should leave the table/network consistent.

**Verification:** test the reserved label at distant coordinates and ensure it is either rejected clearly or routed as a distinct farm. Keep the legitimate co-located `c4ffa` zero-time case working.

## F08 - Medium: dataset references and in-text citations are missing

**Requirements:** Sections 3.2 and 9.3; Appendix 1 Sections 2 and 10 require dataset provenance, algorithm references and IEEE referencing.

**Where:** `docs/technical_report.md:20-25,54-57,245-249`; PDF pages 1, 2 and 4.

The references list contains two books, but no Farm Transparency dataset/website reference. The numbered references are not linked to the relevant claims by in-text citations. Naming a teacher-supplied file does not fully document its public source or how the submitted regional dataset was obtained/prepared.

**How to address:** add the exact public dataset/map source, relevant filters/region and truthful collection/export/access information, and use IEEE in-text citations where algorithm and external-data claims occur. Cite the actual source of the geographic distance method if one was used. Do not invent an access date or pretend you personally exported a teacher-provided CSV. Retain valid algorithm references; removing references is not a compliance fix.

### Dataset findings: do not replace a valid dataset unnecessarily

The CSV has 229 unique WA records, not fewer than the required 40. A separate download is not automatically required just because this copy was provided by the teacher: what matters is satisfying the stated public-source and region requirements and honestly documenting provenance. The ZIP alone cannot establish every step of its original collection history.

Five records were spot-checked against public source listings; this was not an independent verification of all 229 locations or their current operations:

| ID | CSV name | Public source result |
|---|---|---|
| `c4ffa` | Treeby Egg Farm | Matching listing; source says open and operating. [Source](https://www.farmtransparency.org/facilities/c4ffa-treeby-egg-farm) |
| `7096a` | Masons Family Farm | Matching indexed source listing; source says open and operating. [Source](https://www.farmtransparency.org/facilities/7096a-masons-family-farm) |
| `f4386` | Peel Pork Piggery | Matching listing; source says open and operating. [Source](https://www.farmtransparency.org/facilities/f4386-peel-pork-piggery) |
| `7d2c0` | Louisa Downs Station | Matching listing; source says open and operating. [Source](https://www.farmtransparency.org/facilities/7d2c0-louisa-downs-station) |
| `f458e` | Former piggery | Matching listing; source says closed, consistent with the CSV. [Source](https://www.farmtransparency.org/facilities/f458e-former-piggery) |

The CSV itself labels 224 records Open and five Closed. The brief does not explicitly ban retaining closed facilities as source records. Do not claim every record is an operating feedstock supplier, and document whether closed/proposed/unconfirmed sites are only lookup/test records or eligible scheduling locations. Public listing status is not independent proof of present operation.

Invented feedstock amounts and modelled travel times are explicitly permitted by Section 3.5. The report correctly distinguishes them from real measurements. They are not evidence that the underlying farm locations were fabricated.

## F09 - Medium: the final PDF needs layout fixes

**Requirements:** Section 10 requires page numbers and consistent formatting; the UML must communicate module interaction clearly.

**Visually confirmed:**

- No page numbers on the current PDF.
- Page 5 is completely blank.
- The benchmark table splits a row across pages 3 and 4; page 4 starts with a cut continuation and no repeated table header.
- The architecture heading is left alone at the bottom of page 1.
- The UML on page 2 is very dense, with small labels at normal A4 reading size. Separate SVG/PNG files exist, but the assessed PDF should also be readable.

**Where to adjust the build:** `docs/report.css:1-8` and `docs/build_report.sh:4-6`, or the final document export workflow.

**How to address:** add page numbering, prevent table-row splitting/repeat headers, remove the blank trailing page and keep headings with following content. Enlarge/simplify the main module data-flow diagram; detailed class information can be supplementary. Re-render the final PDF after adding the originality cover and inspect every page again. Recheck pagination after any report edits.

## F10 - Low: extreme numeric input can escape validation

**Requirements:** Sections 5.2.5 and 9.5: invalid values should not terminate the program unexpectedly.

**Where:** `module2_hash/farm_record.py:44-47`; `module3_heap/priority.py:40-43`; additionally `module1_graph/graph.py:69-71` assumes numeric values are float-convertible by `math` helpers.

**Reproduced:** both `to_number(10 ** 400)` and `parse_feedstock(10 ** 400)` raise `OverflowError`; they do not return their normal invalid-input result. Their exception handlers only include `TypeError` and `ValueError`.

This is a direct Python-API edge case, not a demonstrated crash from ordinary menu text or the submitted CSV, so it is lower priority than the confirmed integration issues.

**How to address:** make numeric conversion failure handling consistent, including overflow, and add focused tests. Do not catch every exception indiscriminately and hide unrelated programming errors.

## F11 - Low: benchmark-method descriptions overstate what is excluded/measured

**Requirements:** Section 7.2.6-7 and meaningful performance analysis.

**Where:** `module4_sorting/benchmark.py:13-19,125-144,195`; `module4_sorting/sorting.py:71,117`.

The benchmark prepares one copy outside timing, but each public sorting function creates another full copy inside the timed call. Therefore the recorded time includes that internal input copy. This is not inherently unfair because both APIs do it, but the explanation should say what is actually measured.

Also, “about two key evaluations per comparison” is not a universal conversion for both algorithms. Quick Sort retrieves a key and may compare it twice, while pivot selection does additional comparisons. Key-call counts are useful, but are not interchangeable with comparison counts across these implementations.

**How to address:** describe measurements as end-to-end public sort-call time, including the internal copy, and label key evaluations as key evaluations. Only claim comparison counts if comparisons themselves are counted. Do not discard otherwise valid benchmark results just because absolute times differ on another machine.

## F12 - Low: fresh-environment instructions could be more complete

**Where:** `README.md:3,20-30`.

NumPy is named, but the README has no installation steps and uses `python`, which is not necessarily available under that name on macOS. A `requirements.txt` is not explicitly required, but reproducible setup is useful.

**How to address:** document a minimal `python3` setup and commands, for example:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install numpy
python3 interactive_menu.py
python3 -m unittest discover -s . -p 'test_*.py' -t . -v
python3 interactive_menu.py --demo all
```

Matplotlib is optional for the plot; the program handled its absence/availability separately from core sorting. Report-building dependencies are not runtime dependencies of the submitted menu. Do not package a virtual environment in the ZIP.

## F13 - Low: the optional dataset checker can report false reassurance

**Where:** `data/check_dataset.py:64-82`.

This helper does not apply the main loader's full ID/coordinate validation. For example, converting `nan`/`inf` to float succeeds, coordinate ranges are not checked, and multiple states produce a note rather than a failing result. It also searches accumulated ID/state strings using membership operations, which needs checking against the supplied automatic-search restrictions.

**How to address:** reuse the project's permitted validation logic or explicitly narrow the helper's claimed checks. Clearly fail relevant dataset-rule violations. Keep the main loader as the actual validation authority; the submitted CSV passed that loader in this review.

## Marking-criteria cross-check

This is a coverage assessment, not an estimated mark or a guarantee of a pass.

| Criterion | Evidence present | Remaining concern |
|---|---|---|
| Module 1: graph, BFS, DFS, Dijkstra - 8 marks | Manual graph/algorithms; required 12-vertex/12-edge example; cycles, isolated/disconnected cases, invalid/unreachable output | F01 core representation restrictions; F06 complexity; F07 hub namespace collision |
| Module 2: operations, collisions, scalability - 6 marks | Own linked-node chains; 229 records; prime growth; successful/failed operations; before/after collision chains; every-ten-insert load reports | F01 auxiliary container/CSV scope; F07 reserved-ID integration; F10 extreme numeric handling |
| Module 3: heap, formula, traces - 6 marks | Manual max-heap; graph-derived T and hash lookup; sensible calculated formula; 14 requests; required edge cases | F01 request containers; F05 untraced final extractions; F02 no retained history |
| Module 4: correctness/performance - 6 marks | Correct manual Merge/Quick sorts; ascending T; fixed seed; all required sizes/conditions; timing tables and seven analysis topics | F02 actual-session reporting/storage missing; F01 containers; F06/F11 analysis accuracy |
| Technical report - 8 marks | Overview, structure justification, UML, results, assumptions and limitations present | F04 required structure/reflection/declaration; F06 complexity; F08 citations/provenance; F09 layout |
| Code quality/compliance/testing/error handling - 6 marks | Modular folders, useful comments, headers, 81 tests and normal invalid-input handling | F01 restrictions; F03 identity placeholders; missing regression tests for F02/F07; smaller robustness gaps |

## Things that do not need an unnecessary rewrite

- The four core algorithms/modules are implemented; this is not a missing-module problem.
- The chosen chained hash strategy is explicitly allowed. It does not need to be changed to double hashing.
- The priority `P = 60F / (2T + 30)` has the required direction: more F increases priority and larger T reduces it; it also handles T = 0.
- Three-way median-of-three Quick Sort is a valid design choice. It need not match an earlier practical's exact partition implementation.
- The dataset exceeds 40 records. The brief does not impose a 60-farm minimum.
- The integrated benchmark's T values really come from the graph, not unrelated random travel times.
- Additional build files, diagrams and editable report sources are permitted by Section 9.2. Their presence is not itself a submission violation.
- Unit-test success and sample timings are real evidence here, but do not establish that all restrictions and report requirements are satisfied.

## Final verification checklist

- [ ] Resolve restricted core lists/tuples and clarify the scope for parsing/UI/tests.
- [ ] Make the README/report describe actual built-in use accurately.
- [ ] Retain actual session request history and sort/store that history for reporting.
- [ ] Add regression checks for the custom-request reporting path and reserved hub ID.
- [ ] Show heap states after every extraction performed in the main demonstration.
- [ ] Correct implementation-specific complexity and benchmark-method claims.
- [ ] Follow the Appendix 1 report structure, with truthful declarations and useful reflection.
- [ ] Add dataset references and relevant IEEE in-text citations.
- [ ] Fill author/ID fields and rename both archive and top-level folder correctly.
- [ ] Put the required Declaration of Originality first in the final report.
- [ ] Fix page numbers, split table rows, diagram readability and the blank page; inspect the final PDF.
- [ ] Rerun tests/demos from a clean extraction with documented dependencies.
- [ ] Regenerate saved outputs/results after code changes and keep report numbers consistent with them.
- [ ] Upload PDF and ZIP through both required links; prepare to explain/modify the implementation during the compulsory demonstration.

**Bottom line:** the core algorithm checks are encouraging. Submit only after the compliance, live reporting/integration and unfinished report/package issues are resolved. The present ZIP is not something I would certify as fully compliant or submission-ready.
