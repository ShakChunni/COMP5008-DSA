# Review of the revised technical report

Reviewed on 17 October 2026:
`/Users/ashfaq/Downloads/comp5008_report.pdf` — 15 physical PDF pages.

SHA-256: `7e1b751749c768073967e681defacdced44845fd45e2e07f72aa8875d581bf45`.

**Verdict: the substantial report issues identified yesterday have been fixed.
I found no missing substantive report section against the visible assignment
requirements and complete 40-mark rubric. Two small report corrections remain,
alongside an unresolved question about acceptance of the supplied source sample.**

This review excludes the Declaration of Originality, which you explicitly deferred.
It is a review of coverage and accuracy, not a guaranteed mark prediction.
Separate source-file headers and packaging checks still apply before submission.

The report was checked against the brief, the full rubric screenshot, current
implementation, saved evidence, yesterday's audit, and visual renders of all 15
pages. Three independent reviewers checked requirements, algorithms/complexity,
and results/evidence. Physical PDF page numbers below refer to this exact file;
the printed body page number is three less.

## 1. Two small report corrections

### 1.1 Replace the UML image with the corrected version

**Printed p.2 / PDF p.5, Figure 1.** The image still says
`calculateRequest(): P = F/T`. In UML, the text after the colon can be read as
the method's return type. The actual return value is a `CollectionRequest`, as
your revised prose on printed p.1 already correctly explains.

I corrected our reusable figure to show `calculateRequest(...)`, leaving the
priority equation in the prose. Use the updated:

`report/figures/01_system_uml.pdf`

Its PNG and the first page of `all_figures_preview.pdf` are updated too. The
generator now produces the corrected label. Upload the replacement individual
PDF to Overleaf and recompile. The reviewed report PDF itself has not been
modified; it still contains the older label until you replace the figure.

This is a precision correction. The existing figure already demonstrates the
required four-module interaction and data flow.

### 1.2 Give the environment file's complete path

**Printed p.9 / PDF p.12, Table 9, "All 18 timing means and environment" row.**

The row currently gives:

```text
sample_output/benchmark_results.csv; benchmark_environment.json
```

Use both complete paths:

```text
sample_output/benchmark_results.csv
sample_output/benchmark_environment.json
```

The environment JSON exists in `sample_output/`. This is a path clarification,
not missing evidence. Wrap the paths onto separate lines if necessary.

## 2. The substantive unresolved compliance question

**Printed p.2 / PDF p.5, Section 3.1: supplied sample versus website collection.**

Section 3.2 of the brief requires website farm data from one region and describes
`farm_dataset_sample.csv` as an example. Your implementation selects 40 original
WA rows from that supplied 229-row sample. All 40 selected rows match their source
rows exactly, and the original FarmIDs are preserved. The report truthfully says
that a sample public listing was checked and does not claim independent collection
or verification of all 40 farms.

That is accurate reporting, but it cannot establish whether the unit accepts use
of the supplied sample as fulfilling the collection requirement. Acceptance is
neither proven nor disproven by the available instructions. This remains the
largest unresolved compliance question because the brief warns that dataset
noncompliance can affect modules using it.

Close it by establishing that sample reuse is permitted, or by actually
collecting/verifying the selected records against their source listings and
recording the URLs, real access dates, checked fields and changes. Do not claim
that all 40 were checked unless that work has happened. Do not merely delete the
honest limitation from the report.

## 3. Previous findings now resolved

| Previous finding | Current location | Result |
|---|---|---|
| Hub choice lacked a reason | Section 3.1, printed p.2 | Fixed: consistent southwestern model destination, supported by 36/40 farms south of −30°; no optimal-site claim |
| Dijkstra comparison used "lower bound" incorrectly | Section 4.1, printed p.4 | Fixed: actual linear-scan bound and alternative binary-heap bound are stated correctly |
| Hash notation/space/growth analysis was incomplete | Section 9 / Table 10, printed p.10 | Fixed: q, m, m′ and C defined; storage, expected/amortized growth and worst-case probing discussed |
| Sorting discussion needed numerical input-condition comparison | Section 7.3, printed p.8 | Fixed: growth factors and within-size comparisons are correct |
| Timings were used to overstate pivot causality | Section 7.3, printed p.8 | Fixed: partition balance was not measured; observations are distinguished from complexity and causation |
| Evidence files were difficult to locate | Section 8.1 / Table 9, printed p.9 | Fixed apart from the abbreviated environment path above |
| Actual BFS groups were absent from the report | Table 3, printed p.4 | Fixed: levels 0–6 and unreachable 404a0 are shown correctly |
| Heap figure needed a link to complete operation traces | Section 6.1, printed p.6 | Fixed: complete insertion/extraction trace is explicitly referenced |
| Sorting output needed an ascending-T example | Section 7.4 / Table 7, printed pp.8–9 | Fixed: five-record excerpt and both complete 1,000-record outputs are referenced |
| Benchmark integration/displacement method was too implicit | Section 7.2, printed p.7 | Fixed: hash/Dijkstra-derived keys, repeated events, distinct disjoint swaps, copies, timing exclusions and alternating order explained |
| Hash design needed more justification | Section 5, printed p.5 | Fixed: 53/31, prime sizes, probing, tombstones and growth explained |
| Top-down Merge Sort choice needed justification | Section 7.1, printed p.7 | Fixed: traceable midpoint recursion and one reusable buffer explained |
| Distance-equation symbols needed definitions | Section 3.2, printed p.3 | Fixed: radians, coordinates, differences, kilometres and radius defined |
| 343 checks versus seven suites was ambiguous | Section 8, printed p.9 | Fixed: six drivers / 343 checks plus 18 benchmark combinations |
| Contents/list page numbering, species wording, complexity-table break | Various | Fixed; mathematical glyphs render correctly |
| Deleted/reinserted farm policy could be clearer | Section 6.2, printed p.7 | Fixed: presence rechecked and original request snapshot retained |

## 4. Complete rubric coverage

These statuses describe evidence, not marks awarded. Report changes alone do not
settle separate data-source or code-compliance questions.

| Criterion | Marks | Current coverage |
|---|---:|---|
| Graph construction and adjacency-list design | 2 | Sections 3.2/4.1: dynamic vertices/edges, two-way weighted adjacency, counts and validation; graph code/log |
| BFS | 2 | Section 4.1 and Table 3: all reachable locations grouped by level; saved trace agrees |
| DFS | 2 | Section 4.1/Table 2: explicit stack, all components, reported closed cycle and isolated vertex |
| Dijkstra | 2 | From-scratch implementation; independent cost-7 fixture and worked R005 path/time; accurate bound |
| Hash insert/search/delete | 3 | Sections 5/8 and hash log: successful/failed operations, complete records, duplicates and deletion effects |
| Hash collision handling | 1 | Figure 3 plus explicit 45→44 probe/tombstone trace in the log |
| Hash function and scalability | 2 | Modulo polynomial hash, double-hash step, primes, 40 records, load checkpoints and 53→107 growth |
| Heap insert/extract operations | 2 | Section 6: array heap, percolation, heap property, peek and FIFO ties; driver/log |
| Heap priority calculation | 2 | F/T calculated using hash lookup and graph-derived T; all 12 priority values match |
| Heap-state tracing | 2 | Explicit per-operation trace reference, required insertions/extractions and saved heap figure |
| Sorting correctness | 3 | Stable custom Merge Sort, custom Quick Sort, ascending-T excerpt and complete checked exports |
| Sorting performance analysis | 3 | All 18 means, all sizes/conditions, reproducible method, quantitative comparisons, pivot/stability/space/worst-case discussion |
| Report overview and justification | 2 | Sections 1–3: purpose, workflow, structure choices, hub/network/model rationale |
| Report UML/data flow | 2 | Figure 1 plus workflow prose; replace the minor method-label shorthand as above |
| Report complexity and reflection | 2 | Table 10 and Sections 9/10.2: time/space, implementation-specific choices and trade-offs |
| Report results, assumptions and limitations | 2 | Worked outputs, all result tables, evidence map, source/model/snapshot/scaling/timing limitations |
| Modular/readable/documented compliant code | 2 | Modular structure and comments covered; source headers remain deferred, and additional unit restrictions are not available for final verification |
| Testing and edge cases | 2 | Six drivers / 343 saved checks, complete benchmark matrix, invalid-input and integrated menu evidence |
| Error handling | 2 | Validations, controlled rejections, malformed CSV/menu recovery, empty/full/deleted/unreachable cases |
| **Total** | **40** | **Every visible criterion has identified evidence; this is not a guaranteed score.** |

The seven sorting analysis questions in Section 7.2.7 are covered: size growth,
input conditions, pivot effects, theoretical time, worst cases, space, and relevant
input characteristics such as repeated transportation-time keys.

## 5. Optional precision and presentation polish

These are small improvements, not missing substantive sections or new algorithms.

- **Printed p.10, Table 10:** the paragraph below already excludes prime-search
  work from the rehash estimate. To make the amortized-insertion row equally
  explicit, add: "The amortized estimate also excludes the prime-capacity search."
  Keep the fixed-ID and short-expected-probe assumptions. No need to introduce a
  lengthy prime-number analysis.
- **Printed p.10:** "The 0.7 growth threshold controls occupancy" is more precise as
  "controls live occupancy" because tombstones also affect probe lengths. The
  existing discussion already acknowledges the tombstone limitation.
- **Printed p.10, trace row:** if expanding the space explanation, the printed
  heap-array construction uses O(R) temporary space for its parts/text. The O(1)
  percolation workspace applies to the raw heap operation. The current table
  correctly separates raw operation time from output time.
- **Printed pp.4/9, Tables 3/9:** some main table text is about 7 pt. It is readable
  when zoomed, but wrapped columns or a short evidence list would read better than
  shrinking the whole table. No clipped rows or overlapping cells were found.
- References continue onto printed p.12. Keeping them together is cosmetic;
  no visible requirement demands that change.

No extra sorting algorithm, data structure, benchmark size, GUI, SQL service,
statistical study or additional figure is needed for the visible rubric.

## 6. What was checked this time

- All 15 PDF pages rendered and visually inspected, including tables, figures,
  arrows, parent-floor formula, theta symbols and hash-capacity primes.
- All 18 displayed timing values match the frozen CSV to six decimal places.
- Random 100→1,000 growth factors recompute to 15.2399 (Merge) and 13.1570 (Quick).
- At 1,000 records, nearly-sorted/reversed reductions versus random recompute to
  2.5539% / 11.0669% (Merge) and 7.5966% / 11.4404% (Quick), agreeing with rounding.
- Graph construction rerun in memory: 41 vertices, 55 edges; BFS group sizes
  1/4/10/9/12/2/2; actual grouped labels match Table 3.
- DFS visits 41 and returns a30b2→c6748→c1c13→a30b2.
- R005 route and 874.66-minute total agree with the graph and saved evidence.
- Request loading rerun in memory: 12 accepted, seven rejected; first five heap
  extractions agree with the report. All 12 F/T rows agree with saved results.
- All 40 dataset rows remain exact source rows; 36 are south of −30°.
- Both 1,000-row sorted exports remain ascending T and preserve the input records;
  the 12-row integrated export is also ascending T and its excerpt agrees.
- Saved PASS counts recomputed: 143 graph + 82 hash + 42 heap + 48 sorting +
  14 input + 14 integration = 343.
- All eight figure-input SHA-256 values still match the manifest.
- The corrected UML asset was regenerated, text-checked and visually inspected.

The full suite was run on a temporary package copy in yesterday's review. This
revision check revalidated current report claims and exercised the relevant
in-memory graph/request flow; it did not rerun the timing experiment or overwrite
the frozen result CSVs. Application algorithms were not changed.

## 7. Separate final-package items

These are outside this PDF's content corrections:

- Source-file author/date/purpose headers are required by brief Section 9.5 and
  remain absent following your earlier request to defer them. Restore correct
  file-specific headers before packaging.
- The menu is implemented in `main.py` as you requested. The brief's folder example
  names `interactive_menu.py`; README documents the choice, but literal filename
  enforcement cannot be established from the available material.
- The available brief omits Sections 10–11 and refers to additional unit coding
  restrictions. Those unseen instructions cannot be certified by this review.
- Include every cited evidence file in the final ZIP, including
  `report/figure_data/heap_states.csv` and `sample_output/benchmark_environment.json`.
  The final PDF and required source/data/driver/output files must be packaged too.

Your deferred declaration is deliberately not listed as a current report defect.
The Downloads PDF was left untouched; update the Overleaf source for the two small
corrections, then inspect the recompiled final PDF.
