# Attachments and MATLAB Model Rendering

Use this reference whenever the problem supplies PDFs, spreadsheets, datasets, images, diagrams, code, or other attachments, and whenever the model has geometry, materials, boundaries, discretization, layouts, or physical fields.

## 1. Inventory Before Modeling

Create `inputs/input_manifest.csv` with:

```text
input_id,source_path,file_type,sha256,size_bytes,description,questions,profile_path,usage_status,exclusion_reason,status
```

Use stable `input_id` values in reports and handoffs. Preserve originals; write extracted text, previews, cleaned tables, and profiles to separate project paths. Run `scripts/validate_input_manifest.py` before model selection.

For every input, inspect the structure rather than relying on its filename:

- PDF/document: page count, headings, tables, figures, equations, requirements, and page references;
- spreadsheet: sheet names, dimensions, headers, formulas, merged cells, units, missing/error values, and candidate IDs;
- CSV/database: encoding, delimiter, schema, row count, keys, types, units, duplicates, missingness, and ranges;
- image/diagram: dimensions, legend, labels, scale, coordinate system, and extractable measurements;
- code/archive: entry points, language, dependencies, inputs, outputs, and whether it reproduces supplied results.

Create one profile artifact per input. Map relevant pages, sheets, columns, images, or code outputs to each question. `excluded` requires a concrete reason after inspection; “not needed” is insufficient.

## 2. Attachment-Use Map

The modeling report must contain:

| input_id | page/sheet/field | question | model role | transformation | output artifact | validation |
| --- | --- | --- | --- | --- | --- | --- |

Distinguish problem-given facts from literature, assumptions, fitted parameters, and simulated outputs. If the model does not use a supplied attachment that appears relevant, stop and review before continuing.

## 3. Auditable Modeling Decisions

Maintain `reports/MODELING_DECISION_LOG.md`:

| decision_id | question | attachment/data evidence | alternatives | chosen method | rationale | risk | validation | downstream effect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Record concise, inspectable rationale rather than hidden reasoning. Update the log when an assumption, method, parameter source, or model level changes. The paper should turn accepted decisions into continuous academic prose, not expose internal Agent workflow.

## 4. MATLAB Must Render the Model

For engineering and physical tasks, plan model views before coding. Generate the applicable views from the same parameters used by the solver:

1. coordinate system, dimensions, components, and candidate geometry;
2. material regions or material-property space with stable candidate IDs;
3. sources, loads, flow directions, initial and boundary conditions;
4. computational domain, mesh, stencil, nodes, or control volumes;
5. feasible and final layouts with clear dimensions and constraint margins;
6. temperature, stress, flow, concentration, or other physical fields with extrema;
7. optimization surface/frontier, active constraints, and convergence;
8. benchmark, residual, sensitivity, uncertainty, or refinement evidence.

Use MATLAB primitives such as `patch`, `rectangle`, `plot3`, `surf`, `trisurf`, `contourf`, `imagesc`, `quiver`, and annotations when appropriate. Do not force 3D when a dimensioned 2D section communicates the model better. Do not draw geometry by eye when dimensions exist in the attachments or parameter ledger.

Every model view must save its geometry/material/field data, generator `.m`, vector PDF, PNG preview, scenario key, regime, model level, and claim. Labels must identify materials, units, boundaries, loads, and critical points at paper print size.

## 5. MATLAB and DrawIO Division

Use MATLAB for figures whose geometry, scale, materials, boundaries, layouts, or fields depend on model parameters. Use DrawIO for high-level technical routes, logical dependencies, algorithm branches, and conceptual architecture. A clean DrawIO schematic does not replace a parameterized MATLAB geometry or field plot; a MATLAB plot does not replace an algorithm flowchart when branching logic matters.

## 6. Visual Continuity Per Question

Open each question with inherited inputs and the model change, then show:

`attachment evidence -> parameterized mechanism/geometry -> equation/algorithm -> executed result -> validation -> decision`

Close with a frozen summary containing the scenario, result type, hard-constraint margins, accepted figures, and exact downstream fields. This structure prevents abrupt jumps between questions.

## 7. Blocking Failures

Block delivery when any applies:

- a supplied attachment is missing from the manifest or silently ignored;
- a relevant page, sheet, field, unit, or image is not mapped to a question;
- cleaned data cannot be traced to the original input and transformation;
- a method choice has no alternatives, evidence, rationale, or validation record;
- MATLAB supplies only generic data charts while central geometry, materials, boundaries, layouts, or fields remain unvisualized;
- a schematic uses dimensions or materials different from the solver;
- model figures are hand-drawn or hard-coded independently of accepted parameters;
- the rendered figure omits units, material identity, boundary meaning, extrema, or critical constraints.
