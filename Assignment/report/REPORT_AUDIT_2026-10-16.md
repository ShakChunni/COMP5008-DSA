# Hostile review of the drafted technical report

Reviewed: `/Users/ashfaq/Downloads/comp5008_report (1).pdf`, 13 physical PDF pages.
Draft SHA-256: `88723f80540b27b97ef5998ea1fa691bc671efc695aaaadb28732e0c23554195`.

Review date: 16 October 2026. Basis: the supplied assignment PDF, the complete
marking-table screenshot supplied with this request, current code, saved CSVs/logs,
and visual inspection of every report page. Three independent reviews covered
requirements, technical accuracy and presentation; their findings were cross-checked.

**Verdict: the draft has the main required technical content and correct saved
numbers, but it is not ready to submit unchanged.** The missing first-page
Declaration of Originality is a definite submission failure. Hub justification and
several technical/analysis details need tightening. Data-source acceptance and extra
unit restrictions remain questions that the available materials cannot resolve.

This is an audit, not a predicted score. A marker can assess explanation quality
differently; no review can guarantee 40/40. The written report supports module
criteria such as sorting analysis as well as the separate eight report marks.

## Page references

References below are for this exact draft, before adding a declaration:

| Physical PDF page | Printed page | Main content |
|---:|---|---|
| 1 | Unnumbered | Cover |
| 2 | i | Executive summary and contents |
| 3 | ii | Lists of figures/tables |
| 4 | 1 | Introduction, workflow, structure choices, Table 1 |
| 5 | 2 | UML, dataset and hub |
| 6 | 3 | Network, distance equations, request data |
| 7 | 4 | Graph algorithms/results and hash formula |
| 8 | 5 | Hash results, heap operations |
| 9 | 6 | Heap figure, priorities and request-state policy |
| 10 | 7 | Sorting implementation, experiment and timing table |
| 11 | 8 | Timing plot, validation and start of complexity table |
| 12 | 9 | Complexity table continued, trade-offs and limitations |
| 13 | 10 | Reflection, conclusion, references |

Adding the declaration changes physical PDF page numbers; printed body numbers can
stay as they are. Do not use the physical/printed page numbers interchangeably.

## 1. Definite corrections before submission

### A01 — Required Declaration of Originality is absent

**Priority: highest.** PDF page 1 is a cover, and the declaration is absent from all
13 pages. Assignment Section 9.1 explicitly requires it as the first report page.

Use the actual unit declaration/form, complete it truthfully, and put it before the
cover. A title page with your name is not that declaration. Do not invent a signed
statement or assume a Blackboard checkbox replaces the required PDF page.

If the official form is a separate PDF, a normal LaTeX approach is:

```tex
% Preamble:
\usepackage{pdfpages}
% First item after \begin{document}, before the cover:
\includepdf[pages=-]{declaration_of_originality.pdf}
```

Use this only with the correct completed form. Inspect the final exported PDF,
including its physical first page, rather than relying on the source order alone.

### A02 — State why the Kwinana-area hub was chosen

**Priority: high; report justification.** Printed p.2 / PDF p.5, Section 3.1 gives
coordinates and says the location is illustrative, but gives no reason for choosing
it. Section 3.3 of the assignment specifically asks for a justification.

An honest data-based rationale is available: 36 of the 40 selected records have
latitude south of -30 degrees. Do not describe this as an optimized site or a
verified processing plant. Suggested addition to adapt:

> I selected a fixed Kwinana-area model point in southwestern WA to give the case
> study one consistent processing destination. Most selected farms are in southern
> WA: 36 of the 40 records lie south of latitude -30 degrees. This makes a southern
> hub a reasonable educational reference point, while the more distant farms test
> longer routes. No site-feasibility or optimal-location claim is made.

This is a modelling justification, not proof of commercial suitability. If you add
claims about industrial infrastructure, support them with a source you actually read.

### A03 — Correct the Dijkstra complexity terminology

**Priority: technical accuracy.** Printed p.4 / PDF p.7, Section 4.1 says the linear
implementation has O(V²+E) "rather than the lower bound available from a heap-based
implementation." A faster implementation gives a different *upper bound* on its
running time; it is not a lower bound on the problem.

Replace that sentence with:

> This linear-scan implementation runs in O(V²+E) time. A binary-heap implementation
> can achieve O((V+E) log V), but the linear scan is straightforward to trace and
> sufficient for the 41-vertex test network.

Do not change the reported complexity of our actual code to the heap-based bound.

### A04 — Repair complexity notation and complete hash-space analysis

**Priority: technical accuracy/report complexity.** Printed pp.8–9 / PDF pp.11–12,
Section 9 and Table 7:

- `n` is defined as sorting records but is reused in the hash-resize row `O(m+n)`.
  That row needs the number of live hash records, not the sorting dataset size.
- `C` appears in heap storage `O(C)` but is not defined in the notation paragraph.
- Hash storage has no explicit numerical space bound. Descriptions of probing and
  arrays coexisting are useful, but add the actual space costs.
- The resize row says "normal rehash work" without clearly stating expected probing,
  fixed-length keys or the separate prime-search work.
- Insertion that triggers a resize is more expensive than an ordinary insertion;
  identify expected *amortized* O(1) rather than implying every insertion is O(1).

Suggested notation and rows:

> Let q be the number of live farm records, m the old hash capacity, m' the new
> capacity, L the ID length,
> C the heap capacity (100 here), and n the sorting-record count. V, E, R and H
> retain their existing meanings. Constant-time hash bounds assume fixed-length
> IDs and expected short probe sequences; all submitted FarmIDs have length five.

| Operation | Time | Space / qualification |
|---|---|---|
| Hash table storage | — | O(m) slots plus q stored farm records; O(m+q) total |
| Hash search/delete | Expected O(1), worst O(m), for fixed L | O(1) auxiliary workspace |
| Hash insert without resizing | Expected O(1), worst O(m), for fixed L | O(1) auxiliary workspace |
| Growing/rehashing table | Expected O(m+m'+q) rehash work for fixed L | O(m+m') table slots plus stored records; old and new tables coexist during rehash |
| Hash insertion over a growth sequence | Expected amortized O(1), for fixed L | One resizing insertion can be much more expensive |

Add the qualification:

> The rehash estimate assumes expected short probe sequences and excludes the
> additional trial-division search for a prime capacity. A pathological collision
> pattern can require O(q²) probing work while reinserting q records. The full
> worst-case rehash work is O(m+m'+q²), plus the prime-search cost.
> Tombstone-heavy workloads can also lengthen searches despite a low live load.

The expected rehash estimate is not a universal worst-case guarantee. Our ordinary
case uses q<=m and geometric growth. There is no need to turn the report into a
number-theory analysis of prime gaps; name the additional cost and its assumption.

The earlier report guide also reused `n` in its hash-resize row. That guidance has
been corrected as part of this review; this is not solely a drafting mistake.

### A05 — Make the sorting condition comparison explicit

**Priority: meaningful analysis, Module 4's three analysis marks and report reflection.**
Printed p.7 / PDF p.10, Section 7.3 states that time rises and Quick Sort wins each
row. Those statements are correct, but the assignment also asks how input condition
affects each algorithm. Add an actual within-algorithm comparison.

All numbers below are from the saved run already in Table 5; no new timings are needed:

> At 1,000 records, Merge Sort takes 0.667744 ms on random input, 0.650691 ms on
> nearly sorted input and 0.593845 ms on reversed input. Relative to random input,
> the latter means are approximately 2.6% and 11.1% lower. Quick Sort changes from
> 0.458065 ms to 0.423268 ms and 0.405661 ms, approximately 7.6% and 11.4% lower.
> Thus both algorithms are faster on the two ordered variants at this size in this
> run, although the exact ranking and magnitude vary with size and timing noise.

For a concrete growth discussion:

> Increasing random input from 100 to 1,000 records multiplies the saved Merge Sort
> mean by about 15.24 and the Quick Sort mean by about 13.16. These three dataset
> sizes illustrate observed growth; they do not establish an asymptotic bound.

These are descriptive differences between saved means. Do not call them statistically
significant or invent confidence intervals: the original experiment saves means only.

### A06 — Reduce the causal claim about the Quick Sort pivot

**Priority: precision in the same sorting discussion.** Section 7.3 says the
median-of-three strategy gives useful splits, "which is why reversed input does
not become a quadratic case here." The implementation supports the theoretical
explanation, but the experiment did not measure partition balance. Three small sizes
also do not establish a runtime class experimentally.

Safer replacement:

> Median-of-three avoids always choosing an extreme first or last value on simple
> monotonic inputs. The saved reversed-input means show no conspicuous slowdown,
> which is consistent with this design. Partition balance was not measured, so the
> experiment does not isolate the pivot rule as the cause or establish an asymptotic
> result. Adversarial arrangements can still produce quadratic worst-case time.

## 2. Resolve these compliance questions, rather than hiding them

### A07 — Supplied sample versus collection from the website

**Priority: potentially broad, but conditional.** Printed p.2 / PDF p.5, Section 3.1
truthfully says the 40 records are selected from the supplied sample and not all
re-collected/verified from the website. The brief says to collect website farm data,
describes the provided CSV as an example, and allows markers to check source records.

The 40 records are genuine source-exact rows with preserved IDs; I found no fabricated
farm records. That does not settle whether the unit accepts supplied-sample reuse as
the required collection step. Do not label the dataset automatically compliant or
automatically disallowed without that information.

To close the question, establish that sample selection is permitted, or verify/collect
the selected source records and record FarmID, profile/map URL, actual access date,
which fields were checked and any changes. Preserve original FarmIDs. Never change
the report to claim all 40 were checked unless that work was actually completed.

### A08 — Required code headers are still absent

**Priority: definite code-compliance omission; separate from the PDF.** Section 9.5
requires an author/date/purpose block. They were removed earlier at your request for
the working copy and have not been restored. A scan found no such blocks in current
Python files. The cover's author details do not satisfy source-file headers.

Before final packaging, add the correct details and specific purpose to each submitted
source file. Keep existing practical-reuse and algorithm citations. Example only:

```python
# Author: F. M. Ashfaq
# Student ID: 23472297
# Date: <actual appropriate date>
# Purpose: <what this specific file implements>
```

This omission is relevant to the two marks for modular/readable/documented compliant
code. The rubric does not specify a fixed per-header deduction, so I do not invent one.

### A09 — Missing instructions and entry-point filename

The supplied screenshot now confirms the complete **40-mark rubric**, including
Graph's **8 marks**. Those graph marks are no longer inferred. However the earlier
brief copy still omits Sections 10–11; any report instructions or extra unit coding
restrictions there remain unavailable. In particular, check whether indexed Python
lists are permitted as arrays. The visible tasks do not themselves ban that usage;
do not invent a ban, but do not ignore an actual extra unit rule either.

The packaging example names `interactive_menu.py`, while you requested a menu entirely
in `main.py`. The program works and README explains the substitution. If filenames
are enforced literally, confirm the substitution is acceptable. This is an entry-point
naming question, not a missing interactive menu. No extra wrapper was reintroduced.

## 3. Make evidence easy for the marker to locate

The following are strengthening changes, not claims that the corresponding code or
ZIP evidence is absent. The brief does not require reproducing every log in the PDF.

### A10 — Add a short evidence-location paragraph or appendix

Printed p.8 / PDF p.11 states validation coverage but does not name the exact saved
outputs. Replace vague "saved evidence" references with deliverable paths:

| Evidence | Submitted file |
|---|---|
| Graph, BFS levels, DFS cycle, shortest paths and error cases | `sample_output/graph_tests.txt` |
| Hash operations, collision probes, deletion/reinsertion, resizing | `sample_output/hash_tests.txt` |
| Every required heap insertion/extraction state and invalid request cases | `sample_output/heap_tests.txt` |
| Exact arrays for heap figure/operation traces | `report/figure_data/heap_states.csv` |
| Sorting correctness and input conditions | `sample_output/sorting_tests.txt` |
| CSV/menu validation | `sample_output/input_tests.txt` |
| Four-module integration | `sample_output/integration_tests.txt` |
| All 18 timing results and environment | `sample_output/benchmark_results.csv`, `benchmark_environment.json` |
| Correctly sorted 1,000-record outputs | `sample_output/merge_sorted_1000.csv`, `quick_sorted_1000.csv` |
| Sorted accepted request history | `sample_output/collection_records_sorted.csv` |

The exact heap-state CSV is supporting material: the required complete trace already
exists in heap_tests.txt. If you cite the CSV, include it in the ZIP too.

### A11 — Show actual BFS groups, not only the reachable count

Printed p.4 / PDF p.7 reports 40 reachable vertices and levels 0–6, but does not
show the grouped labels. Program output already does. A compact appendix listing or
the existing `04_bfs_levels.pdf` would let the marker see the requirement directly.
The exact current grouping is appended at the end of this audit.

### A12 — Link the heap figure to complete operation traces

Printed p.6 / PDF p.9 shows only the state after insertion 12. That is a valid heap
figure, but by itself it does not demonstrate state printing after every insertion
and extraction. The required trace is already in the submitted log. Add:

> The heap array is printed after every successful insertion and extraction.
> The complete 12-insertion and extraction sequence is supplied in
> sample_output/heap_tests.txt; Figure 4 shows the state after insertion 12.

A short before/after excerpt is useful, but duplicating the entire trace in the
body is unnecessary if the ZIP log is present and referenced.

### A13 — Show/report the sorting output as well as timing

Table 4 is priority order, not ascending-T reporting order. Add a short sorted-output
excerpt and point to both full benchmark outputs. A verified excerpt from the
integrated export is:

| Request | FarmID | T (minutes, shown to 2 decimals) |
|---|---|---:|
| R011 | cc5fd | 137.15 |
| R001 | v75pu | 199.07 |
| R002 | h9cp1 | 378.26 |
| R003 | qlctx | 382.70 |
| R010 | 8e64d | 411.06 |

State that Quick Sort may order equal-time records differently from stable Merge
Sort while still being correct. The full 1,000-record exports have already been
checked for ascending T and record preservation.

### A14 — Make benchmark integration and displacement reproducible in prose

Section 7.2 is broadly correct. One additional methods paragraph can close two gaps:

> Each generated benchmark record uses the same scheduler calculation as a live
> request: a hash-table FarmID lookup and Dijkstra-derived shortest transportation
> time. Farm selection and feedstock are pseudorandom; transport times are not
> unrelated random keys. Nearly sorted input is built from a stable sorted baseline
> by selecting 10% distinct positions and swapping them in disjoint pairs, so exactly
> 10, 50 and 100 record identities move. Equal-time identities may swap without
> changing the numerical order. Both algorithms receive fresh copies of the same
> input, and their measurement order alternates between repetitions.

These details come from the current benchmark code. Do not add different seeds or
new measurement claims without updating the code and evidence consistently.

### A15 — Strengthen the hash design justification briefly

Section 5 gives correct formulas and prime-size reasoning. Two short additions
would make the choices easier to defend:

> Initial capacity 53 is prime and deliberately allows the 40-record demonstration
> to trigger growth: the 38th insertion would exceed 0.7. Multiplying the running
> hash by 31 makes character order affect the result, while reducing modulo the
> capacity at every character keeps the intermediate hash bounded. Double hashing
> provides a deterministic alternative probe sequence without allocating chains.

This does not claim cryptographic security or guaranteed uniform distribution.
Also change printed p.9's "Lookup is fast in the tested workload" to "Lookup is
expected to use few probes under the stated distribution/occupancy assumptions."
The experiment measures sorting time, not aggregate farm-lookup time. No new hash
benchmark is required; avoid presenting a theoretical expectation as a measurement.

### A16 — Justify the top-down Merge Sort variant explicitly

Section 7.2.1 of the assignment asks to explain and justify the top-down/bottom-up
choice. Printed p.7 / PDF p.10 explains top-down operation and why Merge Sort is
useful, but gives little reason for choosing that variant. Add one sentence:

> I chose top-down Merge Sort because its recursive midpoint split directly mirrors
> the divide-and-merge logic, making it easy to trace. One temporary array is reused
> for all merges, and the recursion depth is logarithmic.

This is a short justification, not a request to implement bottom-up Merge Sort too.
For input characteristics, also connect the existing discussion of repeated farms
to repeated transport keys: 1,000 model events are drawn from only 39 reachable
farms, so equal T values are common and stability/duplicate handling matter.

## 4. Small technical and presentation polish

These are lower-priority than the declaration, justification, analysis and compliance.

1. **Define the distance equation symbols** after Equations 2–3 (printed p.3 /
   PDF p.6): phi is latitude, lambda is longitude, both in radians; deltas are
   differences; d is kilometres; 6371 km is the assumed spherical Earth radius.
   The code already converts degrees to radians correctly.
2. **UML operation label:** Figure 1 says `calculateRequest(): P = F/T`. The actual
   method returns a CollectionRequest, not the scalar formula. For literal UML
   return-type precision use `calculateRequest(...): CollectionRequest`, or just
   show `calculateRequest(...)` and explain P=F/T in prose. The integration arrows
   are otherwise valid. This label originates in our generated figure.
3. **Clarify 343 versus benchmark counts:** 343 PASS checks occur in six driver
   logs (143+82+42+48+14+14); the seventh suite runs 18 benchmark combinations.
   Suggested wording: "The six module/input/integration drivers record 343 passed
   checks; the benchmark suite additionally completes all 18 combinations."
4. **Table 7 page break:** move Section 9/table start to printed p.9 rather than
   leaving only the first Graph storage row at the bottom of p.8. A clean longtable
   continuation is also acceptable. No table content is clipped or missing.
5. **Contents link/page:** the contents lists List of Figures on page i, while the
   actual list is on ii. Fix its anchor/page ordering and compile twice after adding
   the declaration. Adding References to the contents is helpful, not a stated
   separate assessment requirement.
6. **Species wording:** Section 3.1 says an eligible cattle/pig/sheep/goat "category".
   The filter actually checks Species and excludes unconfirmed Categories/Species.
   Using the exact column name avoids confusion with the CSV Categories field.
7. **References:** CLRS 4e/2022 matches the official MIT Press record; the Farm
   Transparency Map URL is live. The Sinnott/haversine reference is a real work,
   but this audit did not inspect its original scan to settle its full authorship/
   page-range formatting; do not treat the shortened p.159 entry as a confirmed
   error. Use bibliographic details from the source you actually consulted.
8. **Cover date:** 14 October is not inherently wrong for a draft. If the field is
   intended as the final submission date, update it when you actually submit.
9. **Delete/reinsert policy:** Section 6.2 already says a *still-missing* farm is
   cancelled, which is correct. For complete clarity add that reinserting the same
   FarmID before its request reaches the root restores eligibility while retaining
   the old T/path/P snapshot. This is not a newly found collection bug.

The figures, tables, floor-parent formula and Greek/theta mathematical symbols
render correctly. Some symbols disappear in pdftotext extraction; this is not a
reason to rewrite correct displayed mathematics.

## 5. Complete rubric mapping — all 40 marks accounted for

Statuses describe coverage and remaining risk, not awarded scores. The screenshot
confirms four separate two-mark graph criteria.

| Criterion | Marks | Report / implementation evidence | Review status |
|---|---:|---|---|
| Graph construction and adjacency-list design | 2 | Sections 3.2/4.1; own node/edge lists, dynamic addVertex/addEdge, positive two-way storage | Functionally covered; describe model assumptions as already done |
| BFS | 2 | Section 4.1/Table 2; grouped output in graph_tests.txt | Covered in code/log; add grouped report evidence or path reference |
| DFS | 2 | Section 4.1 cycle labels and disconnected scan; graph_tests.txt | Covered; closed cycle and isolated/disconnected cases supported |
| Dijkstra | 2 | Sections 3.2/4.1/Table 2; real and independent 7-minute fixture | Correct implementation/results; fix lower-bound wording |
| Hash insert/search/delete | 3 | Sections 5/8; 40 record round trips, failures/deletions/reinsertions in hash_tests.txt | Functionally covered; point to exact log |
| Hash collision handling | 1 | Figure 3 and capacity-53 probe/tombstone trace | Covered; exact 45→44 sequence shown |
| Hash function and scalability | 2 | Equations 5–6, prime capacity, 53→107, Table 3 | Covered; strengthen 53/31 justification and expected/amortized wording |
| Heap insert/extract | 2 | Sections 6/8; percolation, heap property and operation tests | Covered |
| Heap priority calculation | 2 | Equation 1, Table 4, hash+Dijkstra integration | Covered; values all match saved results |
| Heap-state tracing | 2 | Figure 4 plus complete insertion/extraction log | Covered in deliverables; explicitly reference full log |
| Sorting correctness | 3 | Section 7.1 and both sorted 1,000-row CSVs | Covered in code/CSV; short output excerpt strengthens report proof |
| Sorting performance analysis | 3 | Sections 7.2–7.3, Table 5/Figure 5 | Full matrix correct; justify top-down variant, strengthen condition comparison and qualify pivot causality |
| Report overview and justification | 2 | Sections 1–3, structure-choice table | Mostly covered; missing hub rationale is an explicit fix |
| Report UML/data-flow diagram | 2 | Figure 1 and Section 2.1 workflow | Covered; optional literal method-return label correction |
| Report complexity/reflection | 2 | Section 9/Table 7/Section 10.2 | Good substance; correct hash notation/space/amortization and Dijkstra terminology |
| Report results/assumptions/limitations | 2 | Figures/tables, Sections 3/8/10 | Strong numerical agreement and candid limits; improve evidence locations |
| Modular/readable/documented compliant code | 2 | Separate classes/modules, main menu, README, reuse comments | Source headers still missing; extra unit restrictions/filename acceptance need checking |
| Testing and edge cases | 2 | Six drivers/343 checks, benchmark suite, isolated package run | Covered by saved and freshly rechecked evidence |
| Error handling | 2 | Validation and CSV/menu tests | Covered; controlled rejection/recovery verified |
| **Total** | **40** | | |

## 6. What was verified, without changing the saved experiment

- All 13 PDF pages were rendered and inspected; no clipped figures, overlapping
  table cells, unreadable equation glyphs or missing graphical edges were found.
- All 18 means in Table 5 match benchmark_results.csv to the displayed six decimals.
- All 12 F/T values, complete collection order and first five extractions match.
- The R005 four-edge sum is 874.66 minutes and matches the graph path.
- 41 vertices/55 undirected edges, isolated 404a0, BFS 40-reachable, DFS 41-visited,
  cycle and the A–C–B–D–E cost-7 fixture match saved/current code.
- Hash checkpoints, prime capacities and insertion-38 growth match implementation.
- The six PASS-producing logs total exactly 343 checks.
- Both 1,000-row sorted exports and the 12-row accepted-history export are ascending T.
- The figures' input hashes match the current evidence files.
- A fresh copy under a temporary directory passed the full seven-suite run,
  including all 18 benchmark cases. The original CSV timings and RESULTS.md were
  hashed before/after and remained unchanged.

Do not rerun benchmarks in the submission folder casually after finalizing the report:
new timings may differ. If you do rerun them, refresh Table 5, Figure 5 and any
numerical analysis together. This review did not change the draft PDF or core code.

## 7. Suggested edit order

1. Resolve the declaration and data-source/extra-instruction questions.
2. Add hub rationale; fix the Dijkstra phrase and complexity rows.
3. Add the numerical input-condition comparison and safer pivot explanation.
4. Add a compact evidence appendix/table of paths, BFS groups and a sorted excerpt.
5. Restore source headers before packaging, respecting your actual details/dates.
6. Fix the small contents/table-break/UML-label issues if possible.
7. Recompile twice and visually inspect the actual final PDF.
8. Confirm the first PDF page is the declaration, the benchmark table matches the
   frozen CSV/figure, and the ZIP contains all referenced logs/files.
9. Package `COMP5008_assignment_23472297.zip` with matching top-level folder,
   README, main.py and its support files, common/, data/, all four module folders,
   drivers/benchmark, sample_output/ and technical_report.pdf. Keep report/figure_data/
   too if the report cites it. Exclude caches, .git and temporary/editor files.
10. Submit the report PDF to Turnitin and the ZIP to the separate assignment link.

No extra algorithm, GUI, SQL server, live GIS service, confidence-interval study or
new plotting framework is needed to fix these findings. The draft's five selected
figures are sufficient for the visible figure requirements; adding all eight is
not compulsory. The .tex/.bib source is not in the current workspace, so precise
source edits and a recompiled corrected report still require that source.

## 8. External reference checks

- [MIT Press official CLRS 4e record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
  confirms authors, fourth edition and 2022 publication.
- [Farm Transparency Map](https://www.farmtransparency.org/map) is the cited public
  source entry point. Verifying that page exists is not verification of all 40 records.

## Appendix: actual BFS groups from the submitted evidence

```text
Level 0: HUB
Level 1: v75pu, cc5fd, 7735f, 7d2c0
Level 2: h9cp1, qlctx, 8e64d, 85yvj, b9752, 90629, 6jvno, 8bd08, df2e4, 4mw8y
Level 3: 58yzc, 735d4, v2jbu, 3d8af, 1cc85, x7jvy, 60e63, 96d4e, 1d900
Level 4: fzccd, g4q82, c81cd, gslqa, zaz9u, 24tju, ee349, c96c9, 9bc88, yd20s, 37d48, 7c9d7
Level 5: cd8b9, a30b2
Level 6: c6748, c1c13
Unreachable: 404a0
```

Use wrapping/table cells or the prepared BFS figure in LaTeX rather than placing
an overlong unwrapped line outside the page margin.
