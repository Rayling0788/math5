# Evidence Chain and MATLAB Figure Standard

Use this reference for computational questions, MATLAB work, figure planning, paper writing, and verification.

## Contents

1. Why Figures Exist
2. Per-Question Freeze Package
3. Minimum Visual Evidence
4. Plot Selection by Model
5. MATLAB Requirements
6. Figure Manifest
7. Writing Pattern
8. Verification Blocks

## 1. Why Figures Exist

A competition figure is evidence for a specific claim. Use this chain:

`claim_id -> model/algorithm -> executed result -> validation -> figure/table -> interpretation`

Reject both failure modes:

- a conclusion whose number or trend cannot be traced to executed data;
- a decorative figure that has no precise claim, comparison, or decision attached.

The model report must contain a figure storyboard before code starts:

| claim_id | question | scenario | regime | model level | claim | evidence_role | planned figure | generator | source data | acceptance rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 2. Per-Question Freeze Package

Move each computational question through `DRAFT -> MODELED -> COMPUTED -> VISUALIZED -> VERIFIED -> FROZEN`.

Create `reports/handoffs/Qk.md` with:

- problem inputs and data version;
- assumptions, variables, equations, constraints, units, and model version;
- exact run command and runtime/toolbox versions;
- structured result rows with file paths;
- feasibility, error, baseline, stability, and sensitivity checks;
- figure manifest rows and visual inspection result;
- downstream field names, values, units, paths, and consumers;
- invalidation conditions and Agent sign-off.

Do not start a dependent question until its upstream package is frozen. If upstream data, assumptions, equations, parameters, or result fields change, mark downstream packages `STALE`.

## 3. Minimum Visual Evidence

Each computational question must cover these roles:

1. **Mechanism/input:** parameterized geometry, material space, structure, boundary/initial conditions, discretization, data distribution, feature structure, or model architecture.
2. **Primary result:** fitted response, optimal solution, predicted trajectory, field distribution, ranking, or before/after comparison.
3. **Validation:** residuals, errors, convergence, active constraints, sensitivity, robustness, uncertainty, or held-out comparison.

A panel can satisfy more than one role only when each panel has a separate manifest row and interpretation. Recoloring the same data or changing a 3D camera angle is not new evidence.

Plan an overall roadmap and model architecture when they materially clarify dependencies. For a typical four-computation-question paper, target at least 12 core evidence units and at least 8 MATLAB-generated units when MATLAB is primary. Use evidence coverage, not raw count, as the delivery gate; document any justified reduction.

When the user explicitly requires MATLAB, plan at least two MATLAB evidence units per computational question unless a non-computational question has no meaningful numerical view. Record the exception before coding; do not use it to excuse a missing validation figure.

## 4. Plot Selection by Model

| Task | Mechanism/input | Primary result | Validation/robustness |
| --- | --- | --- | --- |
| Engineering/geometry | parameterized 2D section, 3D structure, boundary conditions | field map, critical section, dimensioned optimum | mesh/step convergence, boundary perturbation, constraint margin |
| PDE/field solver | domain, mesh/stencil, source and boundary conditions | field/contour map with extrema and geometry | residual, conservation balance, mesh/time-step independence, benchmark case |
| Optimization | feasible region, objective section | response surface, Pareto frontier, optimum with bounds | convergence, active constraints, parameter sensitivity |
| Multi-objective/ranking | normalized objectives, candidate map | Pareto frontier, rank/choice vs weight, contribution shares | rank-switch thresholds, normalization and weight sensitivity |
| Dynamic/thermal/ODE | forcing, initial/boundary state, structure | state trajectory, temperature field, phase/season comparison | measured/baseline comparison, error band, step-size sensitivity |
| Regression/statistics | distribution, correlation, feature screening | fit/effect curve, prediction interval | residual, Q-Q, cross-validation, influence diagnostics |
| Machine learning | sample/feature structure, importance | prediction comparison, decision boundary | learning curve, ROC/PR, confusion matrix, calibration |
| Evaluation/ranking | index system, weight structure | score/rank comparison | weight perturbation, rank stability, uncertainty interval |
| Spatiotemporal | locations and temporal forcing | heatmap, contour, 3D surface | holdout error map, temporal/spatial residual pattern |

Use 3D plots only when the third dimension encodes an actual variable or model output. Mark optima, constraints, critical sections, or reference planes; an unannotated surface is rarely sufficient evidence.

## 5. MATLAB Requirements

When MATLAB is selected:

- use a reproducible `.m` entry script or function for each question;
- record MATLAB release, required toolboxes, seed, inputs, and command;
- export core results to `.csv`, `.json`, or `.mat` rather than leaving them only in the workspace;
- save the exact plotting data to `.csv` or `.mat`;
- export vector PDF with `exportgraphics(..., 'ContentType', 'vector')` where supported;
- export a 300 dpi PNG preview for visual QA;
- set Chinese fonts explicitly for Chinese figures, with a known CJK fallback such as Microsoft YaHei, SimHei, SimSun, or Noto Sans CJK SC;
- set axes labels, units, legends, colorbars, line widths, and marker sizes for the final paper size;
- avoid large in-plot titles; use the LaTeX/Typst caption;
- inspect the actual PDF/PNG for clipping, missing glyphs, low contrast, false perspective, overplotting, and unreadable annotations.

Do not accept a collection of `createfigure(input)` wrappers as a reproducible implementation. At least one entry point must start from the declared raw or prepared inputs, execute the model, calculate validation metrics, save structured results and plotting data, and then call the figure functions.

Recommended MATLAB setup pattern:

```matlab
rng(2026, 'twister');
set(groot, 'defaultAxesFontName', 'Microsoft YaHei');
set(groot, 'defaultTextFontName', 'Microsoft YaHei');
set(groot, 'defaultAxesFontSize', 9);
set(groot, 'defaultLineLineWidth', 1.2);
exportgraphics(gcf, pdfPath, 'ContentType', 'vector');
exportgraphics(gcf, pngPath, 'Resolution', 300);
```

If the preferred font is unavailable, detect an installed CJK font and record the fallback. Do not treat arrow/text overlap as a font problem: reroute connectors, increase spacing, shorten labels, or move annotations and re-export.

## 6. Figure Manifest

Create UTF-8 `results/figure_manifest.csv`. Use one row per evidence unit. For a multi-panel figure, share `figure_id` and use distinct `panel_id` values.

Required columns:

```text
figure_id,panel_id,question_id,scenario_key,regime_id,model_level,claim_id,claim_text,evidence_role,figure_type,generator,script_path,data_path,pdf_path,png_path,paper_section,status
```

Allowed values:

- `question_id`: `Q0` for overall material or `Q1`, `Q2`, ...;
- `scenario_key`: stable identifier shared by results, figures, captions, and prose;
- `regime_id`: identifier defined in the model-regime matrix;
- `model_level`: `conceptual`, `analytical`, `reduced`, `numerical`, `high_fidelity`, or `experimental`;
- `evidence_role`: `overview`, `architecture`, `mechanism`, `geometry`, `material`, `boundary`, `discretization`, `input`, `result`, `comparison`, `tradeoff`, `validation`, `sensitivity`, `diagnostic`;
- `generator`: `matlab`, `drawio`, `latex`, `other`;
- `status`: `planned`, `generated`, `checked`, `accepted`, `rejected`.

Optional columns may include `run_id`, `data_sha256`, `parameter_source`, `tex_label`, `caption`, `interpretation_anchor`, `reviewer`, and `review_note`.

Rules:

- `figure_id + panel_id` must be unique;
- final LaTeX/Typst labels and displayed figure numbers must be unique and sequential within the selected template convention;
- `claim_text` must state what the figure demonstrates, not “show results”;
- result figures must identify the scenario and result type in the caption or adjacent text;
- MATLAB rows require an existing `.m` script, saved data, PDF, and PNG;
- result/comparison/validation/sensitivity/diagnostic rows require saved data;
- final paper may use only `accepted` rows;
- all paths must remain inside the project;
- one data set rendered with cosmetic variants counts once unless the variants test different claims.

For field-map comparison groups, keep geometry, coordinates, units, color limits, colormap direction, and print size consistent. Include a colorbar and mark extrema or constraint-violating regions. If fixed limits would hide essential structure, use separate scales but state that direct color comparison is invalid.

Use the correct numerical-method name. Distinguish FDM, FEM, FVM, spectral methods, interpolation, and generic heatmaps from their equations, discretization, and solver; do not call every colored field plot a finite-element cloud map. Likewise, call open-loop transfer-function responses “dynamic responses” unless an actual controller and closed loop are present.

Validate before writing and before final delivery. Example for four computational questions:

```bash
python <skill-dir>/scripts/validate_figure_manifest.py \
  results/figure_manifest.csv --project-root . --questions Q1 Q2 Q3 Q4 \
  --min-core 12 --min-matlab 8 --final
```

Adjust thresholds to the real problem and record the rationale in `reports/VERIFY_REPORT.md`.

## 7. Writing Pattern

For each important result, write in this order:

1. State the claim and the model condition.
2. Cite the equation, table row, or figure.
3. Quantify the trend, optimum, error, interval, or constraint margin.
4. Explain why it occurs and what decision it supports.
5. State limitations or sensitivity when material.

Avoid long text-only modeling sections. Place figures near their claims and explain axes, units, extrema, baselines, uncertainty, and practical meaning. Do not repeat the caption as body text.

## 8. Verification Blocks

Block a question or final delivery when any applies:

- a core claim lacks executed data or validation;
- one of the three per-question visual roles is missing without a justified exception;
- a MATLAB figure lacks its `.m` generator, source data, PDF, or PNG;
- manifest paths are broken, outside the project, duplicated, or not `accepted`;
- key numbers, units, or labels disagree across data, figure, table, and prose;
- scenario keys, result types, model levels, numerical-method names, or comparison scales are missing or misleading;
- figures contain blank output, clipped content, unreadable Chinese, misleading axes, text overlap, arrow-label overlap, or unexplained encodings;
- a diagram was checked only at source/XML level and not as rendered output;
- the paper cites a figure but does not interpret the evidence it contains.

Automated checks do not replace visual inspection. Rasterize all paper pages and core figures, then inspect them at their intended printed size.
