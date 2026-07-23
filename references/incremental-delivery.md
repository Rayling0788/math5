# Incremental Delivery and Retry Standard

Use this reference for execution profile selection, token/time budgeting, local invalidation, and status reporting.

## 1. Default Budget

Treat percentages as upper bounds for the current task budget, not promises of wall-clock duration:

| Work | Delivery budget share |
| --- | ---: |
| input inventory and dependency map | 10% |
| fast model contracts and assumptions | 15% |
| runnable skeleton and smoke tests | 15% |
| fast question results and core figures | 25% |
| paper drafting and claim insertion | 20% |
| final compilation and QA | 15% |

No single solver, gate, Agent, or reference-reading phase may consume more than 20% of the total budget without explicit user approval. Stop a gate after two failed repair attempts. Preserve its logs, mark `FAILED_DIAGNOSTIC`, and continue all unaffected delivery tasks.

For token economy:

- search before reading; load only relevant sections;
- pass paths, IDs, and concise handoffs instead of pasting full reports into Agent prompts;
- cap routine handoffs at roughly 100 lines and include only changed fields;
- never ask two Agents to independently reread and summarize the same unchanged artifact;
- do not generate a new report when a row in an existing state/claim file is sufficient;
- return validators' failing rows, not their full successful logs.

## 2. Workflow State

Maintain `results/workflow_state.csv` with one row per executable task:

```text
task_id,question_id,track,status,evidence_level,input_fingerprint,output_fingerprint,attempts,owner,blocking_scope,last_command,last_error,next_action
```

Allowed `status` values:

- `READY`: inputs are available;
- `RUNNING`: task is executing;
- `ACCEPTED`: its outputs may be consumed;
- `FAILED_LOCAL`: only this task needs repair;
- `STALE`: an accepted blocking input changed;
- `SKIPPED`: outside the selected profile or not needed.

Allowed `evidence_level` values:

- `PAPER_USABLE`: satisfies the non-negotiable delivery quality floor below; it is a complete paper claim, not merely a runnable demonstration;
- `VALIDATED_ESTIMATE`: benchmark, sensitivity, refinement, holdout, or credible cross-check passed;
- `STRICT_FEASIBLE`: all declared hard engineering/physical constraints passed;
- `FAILED_DIAGNOSTIC`: not usable as a claim; retain only as a limitation or debugging record.

### Non-Negotiable Delivery Quality Floor

`delivery` reduces iteration scope and defers optional certification. It never lowers the minimum quality of evidence admitted to the paper. A claim is `PAPER_USABLE` only when all applicable items pass:

1. **Attachment fidelity:** use the actual supplied fields, tables, images, material properties, geometry, or scenarios when they are relevant. Do not replace available attachment data with representative ranges, guessed constants, or generic examples. Every used value has provenance; every excluded relevant item has a reason.
2. **Complete answer:** answer the requested quantity, decision, comparison, or recommendation for the required scenarios. A trend plot, toy case, partial mechanism, or proof-of-concept is not a complete answer.
3. **Physical and numerical sanity:** units, signs, bounds, limiting behavior, conservation or feasibility checks pass as applicable, together with at least one independent analytical, hand-calculated, literature, experimental, small-instance, or order-of-magnitude baseline.
4. **Canonical consistency:** accepted values and labels agree across structured outputs, `claim_registry.csv`, tables, figure labels, captions, abstract, body, conclusions, and recommendations. One claim has one canonical rounding rule and one scenario key.
5. **Parameter integrity:** empirical corrections, calibration factors, subjective weights, and fitted constants have a source or derivation, applicability range, and sensitivity result. An unexplained factor cannot support a paper claim.
6. **Readable evidence:** every included figure is inspected at its final paper size. Chinese and mathematical fonts render correctly; labels, units, legends, colorbars, annotations, and arrows are legible and do not overlap. Placeholder glyphs such as `####`, mojibake, duplicate characters, clipping, or misleading scales are blocking failures.
7. **Evidence hygiene:** `FAILED_DIAGNOSTIC` outputs are excluded from primary result figures, the abstract, conclusions, and recommendations. They may appear only in a clearly labeled limitation or appendix when useful.
8. **Submission prose:** no internal paths, filenames, Agent/process language, retry notes, temporary labels, template examples, or debugging text appears in the paper. The per-question problem-analysis, single assumptions block, and per-question abstract contracts pass.
9. **Claim strength:** recommendation language is capped by evidence level. `PAPER_USABLE` may support a scenario-specific modeling conclusion, but must not be called certified, construction-safe, code-compliant, experimentally verified, or universally optimal without the corresponding stronger evidence.
10. **Final artifact:** the selected template compiles, references resolve, and every final PDF page is rasterized and visually inspected once near delivery. Inability to perform this final visual audit is a delivery blocker, not a warning, when visual tooling is available to the Agent.

Optional high-fidelity work is non-blocking only if the problem can be answered responsibly without it and no diagnostic result contradicts an accepted claim. A contradiction invalidates the implicated claim and its blocking descendants; it does not restart unrelated questions.

Keep `results/workflow_edges.csv` concise:

```text
source_task,target_task,kind,exported_fields
```

Use `kind=blocking` only when the target numerically consumes the exported fields. Use `kind=advisory` for corroboration, certification, optional diagrams, or prose improvements.

## 3. Invalidation Matrix

| Change or failure | Rerun | Preserve |
| --- | --- | --- |
| local code exception before output acceptance | owner task | every accepted upstream and unrelated task |
| validation check fails but claim value is unchanged | failed validator and owner fix | solver outputs not implicated by the check |
| one figure has font, overlap, caption, or export error | figure generator and affected page QA | model solve, other figures, other pages |
| paper prose, citation, or layout error | affected section, compile, affected-page QA | all model and figure outputs |
| optional high-fidelity gate fails | certification task only | delivery-track claims at their prior evidence level |
| accepted numerical output changes | task plus blocking descendants | advisory and unrelated branches |
| shared unit, governing equation, input data, or exported interface changes | all blocking descendants | branches not reachable by blocking edges |

A verifier may widen scope only by naming the exact accepted claim or exported field that is invalidated. “For safety, rerun everything” is not an acceptable reason.

## 4. Minimum Executable Loop

Before deep optimization or high-fidelity research, run one end-to-end loop:

1. `run_all.m` or equivalent dispatcher recognizes every question.
2. At least one question executes from declared input to structured output.
3. The output creates one accepted figure or table.
4. The paper template is scrubbed of example values and compiles with that evidence.
5. Missing questions report `NOT_RUN` and do not leak example numbers.

The loop proves interfaces and file paths early. Replace fast components incrementally; do not dismantle a working loop to develop a certification solver.

## 5. Smoke-Test Gate

Before full dynamic, iterative, stochastic, optimization, or field runs, execute the cheapest meaningful tests:

- 10 iterations/steps or a short horizon;
- low, nominal, and extreme load/input;
- finite and real-valued outputs;
- sign, bounds, monotonicity, conservation, and unit checks as applicable;
- analytical, limiting, or hand-checkable baseline;
- one coarse-to-fine or step-halving comparison when the method is numerical.

Smoke failure blocks only that model task. Fix it before a full run; do not compensate by increasing iteration count or launching more Agents.

## 6. Status Update

At material milestones, or every 10--15 minutes during a long run, report only:

```text
已完成：...
真实输出：...
当前阻塞：...
论文是否可继续：是/否
下一步：...
```

Do not repeat unchanged status or dump full logs. When the user changes priority, update the execution profile immediately and cancel or isolate work outside the new profile.
