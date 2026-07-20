---
name: 1start-mathmodel
description: "基于多个独立 Codex Agent 的端到端数学建模竞赛工作流。用于 CUMCM、MCM、ICM、MathorCup 及类似赛题，按协调、建模、MATLAB 编程与科研绘图、图示、中文 LaTeX/Typst 写作和独立验收分工，逐问形成可复现的论断证据链并完成最终交付。"
---

# MathModelAgent

## Source Baseline

Base this integration on `jihe520/MathModelAgent` commit `be9c59c1aaa13c3dcb74452ea5cae11dada27589`.

Preserve upstream provenance under `components/`, but allow explicit local stage corrections required by this Codex integration. Keep such changes narrowly scoped and synchronize them with the role contracts, reference rules, and validators so stage instructions do not conflict.

## Required Multi-Agent Model

Run a full task with separate Codex agents. The lead agent orchestrates and must spawn these roles rather than impersonating them:

1. `CoordinatorAgent`: preserve the problem statement, map question dependencies, record preferences, and own planning artifacts.
2. `ModelerAgent`: create the overall framework and implementable per-question model contracts, including a figure storyboard. Do not write code or paper prose.
3. `CoderAgent`: implement and execute accepted contracts, preferably in MATLAB when requested or appropriate, and own structured results and data-driven figures.
4. `DiagramAgent`: create only useful non-data diagrams and editable DrawIO sources.
5. `WriterAgent`: write the requested LaTeX or Typst paper from accepted evidence only.
6. `VerifierAgent`: independently test reproducibility, evidence coverage, numerical consistency, compilation, and rendered layout; block delivery on failures.

If Agent tools are unavailable, state that limitation and preserve the same role boundaries sequentially. Never claim that multiple agents ran when they did not.

## Required Reading

Before dispatching roles:

1. Read `components/1start-mathmodel/SKILL.md` and `components/_references/math_modeling_norms.md` completely.
2. Read `references/agent-roles.md` completely.
3. Read `references/evidence-chain-matlab-figures.md` completely when the task contains computational subquestions, requests MATLAB, or requires a paper with figures.
4. Read `references/model-continuity-numerical-validation.md` completely when questions inherit models, use numerical field solvers, mix steady and dynamic regimes, or compare several scenarios.
5. Read `references/decision-metrics-reproducibility.md` completely when the task uses ranking, multi-objective weighting, fitted relations, custom metrics, candidate screening, or MATLAB result generation.
6. Read `references/attachments-and-model-rendering.md` completely when the problem supplies attachments or the paper needs engineering geometry, material, mechanism, boundary-condition, mesh, or structure figures.
7. Read `references/paper-structure-first-prize-writing.md` completely before paper outlining, writing, or final verification.
8. Read each stage Skill immediately before starting that stage.

## Continuous Execution Order

1. Inspect the problem, attachments, workspace, MATLAB availability, LaTeX/Typst toolchain, and user preferences without assuming schemas or content.
2. Spawn `CoordinatorAgent`. Require `inputs/input_manifest.csv`, `reports/ATTACHMENT_INVENTORY.md`, `reports/MODELING_DECISION_LOG.md`, `plan.md`, `todo.md`, `reports/COORDINATOR_REPORT.md`, a question-dependency table, scenario keys, model-regime targets, and initial figure coverage targets.
3. Run `scripts/validate_input_manifest.py`. Do not begin model selection until every problem file and attachment is profiled, mapped to questions, and accepted or explicitly excluded with evidence.
4. Read `components/2analysis-modeling/SKILL.md`; spawn `ModelerAgent` for the shared governing model, cross-question bridge quantities, fidelity ladder, regime matrix, parameter ledger, decision-metric audit, claim registry schema, attachment-use map, and per-question contracts in `reports/ANALYSIS_MODELING_REPORT.md`.
5. Review the model report. Reject it if attachment evidence, variables, units, assumptions, equations, parameter provenance, applicability regimes, objective normalization, custom-metric validation, physical bounds, baselines, validation, downstream mappings, result-type labels, or the model-rendering storyboard are missing.
6. Process questions in dependency order. Independent questions may run in parallel only when they have disjoint files and no shared unresolved input.
7. For each question `Qk`, enforce the state sequence `INVENTORIED -> MODELED -> COMPUTED -> VISUALIZED -> VERIFIED -> FROZEN`:
   - accept the question's model contract before coding;
   - read `components/3coding-visual/SKILL.md` and dispatch `CoderAgent` to implement and execute only the accepted contract;
   - require structured scenario and claim rows, feasibility/error checks, numerical convergence where applicable, plot source data, MATLAB scripts, and updated result manifests;
   - dispatch `VerifierAgent` for the question gate;
   - write `reports/handoffs/Qk.md` and mark `FROZEN` only after every blocking check passes.
8. Do not start a dependent question from provisional prose or screenshots. It may consume only fields explicitly exported by a frozen upstream handoff. If an upstream question changes, mark dependents `STALE` and rerun them.
9. Read `components/4drawio/SKILL.md` and dispatch `DiagramAgent` for justified roadmap, logic, architecture, or algorithm diagrams. Keep parameterized engineering geometry, material maps, boundaries, discretization, layouts, and result fields with MATLAB when they depend on model values. Inspect all rendered output for text/arrow overlap.
10. Run the input, figure, and claim validators with project-appropriate options. Return failures to the owning Agent.
11. Read `components/5writing/SKILL.md` and `references/paper-structure-first-prize-writing.md`; for Typst also read `components/typst-author/SKILL.md`. Dispatch one `WriterAgent` with exclusive ownership of `paper/`. Require a per-question problem-analysis outline, a per-question paragraph plan for the Chinese abstract, and one consolidated top-level model-assumptions section before drafting prose.
12. Read `components/6verity/SKILL.md`; run `scripts/validate_paper_structure.py` with the actual question IDs, then dispatch `VerifierAgent` for final QA. Fix and recheck every blocking finding.
13. Update `todo.md` after every accepted gate and deliver only after final verification passes.

## Evidence Chain

Every material conclusion must follow:

`claim -> model/algorithm -> executed result -> validation -> figure/table -> interpretation`

Assign stable `claim_id` values in the model report. The same IDs must appear in result records and `results/figure_manifest.csv`. A prose claim without executed evidence, or a figure without a specific claim, is incomplete.

Store canonical quantitative and categorical conclusions in `results/claim_registry.csv`. Generate summary, body, tables, captions, and recommendations from those accepted claims or verify them against the registry; do not maintain conflicting hand-copied values.

Label each reported solution as `strict_feasible`, `validated_estimate`, `scenario_result`, or `ideal_upper_bound`. Never present an ideal boundary or reduced-model estimate as an implementable optimum. Use stable scenario keys across result tables, figures, captions, and prose.

Each computational question must cover three visual evidence roles:

- mechanism, geometry, input, or model structure;
- primary result or comparison;
- validation, sensitivity, robustness, or diagnostics.

A well-designed multi-panel figure may cover several roles, but each panel must be registered separately. Do not add decorative or duplicate views merely to meet a count. For a typical four-computation-question paper, plan at least 12 core evidence units, with at least 8 generated by MATLAB when MATLAB is the chosen runtime; adapt the target to the actual problem and document the reason.

## MATLAB Policy

When the user requests MATLAB, or the task is engineering, optimization, dynamic simulation, numerical analysis, or geometry-heavy, use MATLAB as the primary computation and data-figure runtime unless it is unavailable. Do not silently substitute Python.

Require reproducible `.m` entry scripts, fixed random seeds where applicable, saved source data (`.mat` or `.csv`), structured result exports, vector PDF figures, 300 dpi PNG previews, explicit Chinese fonts for Chinese papers, complete units/legends/colorbars, and a run command. Generate geometry, response surfaces, fields, convergence, constraints, residuals, sensitivity, or time-series plots from actual model parameters and outputs, not hand-drawn approximations.

For engineering tasks, MATLAB must visualize the model itself where meaningful: coordinate system and dimensions, candidate structures or material-property space, heat sources/loads, initial and boundary conditions, mesh/stencil or computational domain, final layout, field extrema, and validation. Data-summary plots alone do not satisfy model visualization.

## Handoff Contract

Each handoff must report:

- files read and written;
- problem/attachment IDs used, extracted fields/pages/sheets, and explicit exclusions;
- model and data version, inputs, units, assumptions, and methods;
- scenario key, applicability regime, model fidelity, parameter provenance, and result type;
- commands actually executed;
- structured result rows and their source files;
- canonical claim rows, candidate IDs, metric definitions, normalization rules, and source keys;
- constraint, error, baseline, robustness, and sensitivity checks;
- figures, claim IDs, source data, generation scripts, and intended paper sections;
- exact downstream fields with names, units, and paths;
- passed checks, failed checks, unresolved risks, and next acceptance criteria.

Agents communicate through workspace artifacts, not hidden chat context. The orchestrator inspects artifacts before starting dependent work. Never let agents concurrently edit the same report, source file, manifest rows, figure, or paper section.

## Non-Negotiable Gates

- Do not report unexecuted numbers as results.
- Do not begin modeling while a supplied problem file or attachment is unprofiled, silently ignored, or unmapped to a question.
- Do not let the writer infer missing metrics from prose or images.
- Do not accept optimization results without physical bounds, feasibility, and active-constraint checks.
- Do not accept a reduced or surrogate model until it is benchmarked against a higher-fidelity, analytical, experimental, or small-instance reference on the claim it supports.
- Do not accept numerical field results without governing equations, boundary/initial conditions, residual convergence, conservation or balance checks, and mesh/time-step sensitivity as applicable.
- Do not accept unseeded random quantification of qualitative attributes, untraced empirical parameters, or subjective weights without range/robustness analysis.
- Do not combine objectives or indicators with incompatible units or scales before direction unification and explicit normalization. Require weight sweeps, contribution shares, and Pareto or rank-switch evidence as applicable.
- Do not accept a custom metric until its units, direction, invariances, simple test cases, and relationship to the actual physical or decision target are validated.
- Do not accept hard-coded MATLAB drawings or snippets as implementation of search, fitting, ranking, or optimization. One driver must regenerate every core claim, table, and figure from declared inputs with assertions.
- Do not accept an engineering paper whose MATLAB output consists only of generic data charts when parameterized geometry, materials, boundaries, discretization, layouts, or physical fields are central to the model.
- Do not accept a modeling decision that jumps from attachment or formula to a chosen method without recording alternatives, evidence, rationale, risks, validation, and downstream effect in the decision log.
- Do not reuse a model outside its declared steady/dynamic, spatial, linearity, or boundary-condition regime without an explicit validity decision and replacement model.
- Do not accept a computational question without its three visual evidence roles, unless the model report gives a specific and verified reason.
- Do not accept MATLAB figures without their `.m` generator, source data, PDF, PNG preview, and manifest row.
- Do not accept figures with clipped labels, unreadable Chinese, misleading axes, arrow/text overlap, or unexplained visual encodings.
- Do not accept a problem-analysis section that merges all questions into generic prose; every top-level question must have its own analysis subsection covering inputs/outputs, task essence, dependencies, difficulty, credible alternatives, selection rationale, and expected evidence.
- Do not accept a Chinese abstract unless it has an opening overview and a separate prose paragraph for every top-level question, with the actual method, accepted result or result type, validation, and meaning.
- Do not accept zero, duplicate, or scattered top-level model-assumptions sections. All shared and question-specific assumptions must live inside one coherent `模型假设` section and state basis, scope, effect, and failure treatment.
- Do not select or combine named models merely to signal sophistication. Require evidence-based alternatives, applicability, limitations, rejection reasons, and a validation plan.
- Do not fabricate data, references, experiments, performance, or citations.
- Do not start the upstream FastAPI/Redis application unless the user explicitly requests it.
- Do not mark the workflow complete while any question is not `FROZEN` or `reports/VERIFY_REPORT.md` contains blocking failures.

## Resource Map

- Role contracts: `references/agent-roles.md`
- Evidence, MATLAB, and figure rules: `references/evidence-chain-matlab-figures.md`
- Model continuity and numerical validation: `references/model-continuity-numerical-validation.md`
- Decision metrics and reproducibility: `references/decision-metrics-reproducibility.md`
- Attachments and MATLAB model rendering: `references/attachments-and-model-rendering.md`
- First-prize paper structure and writing contract: `references/paper-structure-first-prize-writing.md`
- Input manifest validator: `scripts/validate_input_manifest.py`
- Figure manifest validator: `scripts/validate_figure_manifest.py`
- Claim registry validator: `scripts/validate_claim_registry.py`
- Paper structure validator: `scripts/validate_paper_structure.py`
- Original entry: `components/1start-mathmodel/SKILL.md`
- Analysis/modeling: `components/2analysis-modeling/SKILL.md`
- Coding/data figures: `components/3coding-visual/SKILL.md`
- DrawIO diagrams: `components/4drawio/SKILL.md`
- Paper writing: `components/5writing/SKILL.md`
- Verification: `components/6verity/SKILL.md`
- Environment diagnostics: `components/doctor/SKILL.md`
- Scientific plot templates: `components/mathmodel-figure-templates/SKILL.md`
- Typst reference: `components/typst-author/SKILL.md`
- Modeling norms: `components/_references/math_modeling_norms.md`
- Preserved upstream role code: `components/agent-protocol/`
