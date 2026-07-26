---
name: 1start-mathmodel
description: "交付优先、支持增量重跑的多 Agent 数学建模竞赛工作流。用于 CUMCM、MCM、ICM、MathorCup 及类似赛题，以 MATLAB 建模计算与科研绘图、中文 LaTeX/Typst 论文、参考范文文风校准和独立验收形成可复现证据链；适合完整解题、已有项目续做、论文重写、局部修错、加速交付和可选高保真认证。"
---

# MathModelAgent

## Source Baseline

Base this integration on `jihe520/MathModelAgent` commit `be9c59c1aaa13c3dcb74452ea5cae11dada27589`.

Preserve upstream provenance under `components/`, but allow explicit local stage corrections required by this Codex integration. Keep such changes narrowly scoped and synchronize them with the role contracts, reference rules, and validators so stage instructions do not conflict.

## Execution Profile

Select one profile at the start and record it in `plan.md`:

- `delivery` (default): build a real, traceable MATLAB-to-paper loop quickly; high-fidelity certification is non-blocking.
- `balanced`: finish the delivery loop first, then spend bounded effort upgrading important claims.
- `certification`: require the declared high-fidelity, engineering, or experimental gates before final claims.

Treat requests such as “加快”“先完成论文”“继续交付” as an immediate switch to `delivery`. Do not keep pursuing a prior certification gate after that switch.

Use two independent tracks:

1. **Paper delivery track:** executed results, structured claims, figures, paper, compilation, and consistency checks.
2. **Certification track:** LBM/CFD/FEM, engineering-code checks, experiments, or other expensive corroboration.

The certification track may upgrade a claim but cannot block unrelated paper work. Label evidence honestly as `PAPER_USABLE`, `VALIDATED_ESTIMATE`, `STRICT_FEASIBLE`, or `FAILED_DIAGNOSTIC`; never promote a lower level through prose.

`PAPER_USABLE` is not a relaxed quality label. It must pass the full delivery quality floor in `references/incremental-delivery.md`: actual attachment fidelity, complete question coverage, physical/numerical baseline checks, canonical cross-artifact consistency, parameter provenance and sensitivity, readable final-size Chinese figures, clean submission prose, evidence-bounded recommendation language, successful compilation, and full final-page visual inspection. Only optional certification depth may be deferred.

## Lean Multi-Agent Model

Do not spawn every role at startup. Create an Agent only when it has an executable, bounded task and available inputs:

- the lead handles coordination and the first-pass model split;
- `CoderAgent` owns a question or disjoint question group and first produces the fast executable layer;
- `WriterAgent` starts as soon as accepted `PAPER_USABLE` claims exist;
- one independent `VerifierAgent` checks changed artifacts incrementally and performs one full final audit;
- `ModelerAgent` or `DiagramAgent` is optional and used only when model ambiguity or a justified non-data diagram needs separate ownership.

Agents must not wait for another Agent. They either consume an available handoff, work on an independent task, or finish with a precise blocked record. If Agent tools are unavailable, preserve ownership boundaries sequentially. Never claim Agents ran when they did not.

## Progressive Reading

Keep context use proportional to the current task:

1. Read this file and the current stage Skill completely.
2. Use `rg` and headings to locate only the relevant sections of references; do not load every reference in full before work starts.
3. Read `references/incremental-delivery.md` for execution profiles, retry scope, and budgets.
4. Read domain references only when their trigger applies: field solver, multi-objective metric, attachment, MATLAB model view, paper structure, or final QA.
5. Reuse accepted handoffs and hashes. Do not reread unchanged problem files, reports, code, or reference sections in every Agent turn.

## Delivery-First Execution

1. Inspect the workspace and existing artifacts before creating anything. Resume accepted work; never restart a completed question merely because a later check failed.
2. Inventory all supplied files at a metadata level, then deeply inspect only the pages, sheets, fields, and figures mapped to current questions. Run `validate_input_manifest.py` before accepting claims, not before harmless setup work.
3. Create a compact dependency graph with blocking and advisory edges. A certification output is advisory to the delivery track unless the problem explicitly requires it.
4. Define a fast executable contract and optional certification upgrade for each question. Record exact exported fields, units, evidence level, and consumers.
5. Immediately build and run a minimum loop: `run_all.m -> structured result -> one figure/table -> paper skeleton -> compile`. Unimplemented questions must emit `NOT_RUN`, never fabricated values.
6. Before any dynamic, iterative, or field solve, run bounded smoke cases: short horizon or small grid, low/nominal/high load, finite-value checks, dimensional/order-of-magnitude checks, and an analytical or limiting baseline where available.
7. Produce `PAPER_USABLE` results question by question. Independent questions and paper structure may proceed in parallel; they do not wait for high-fidelity certification.
8. Allow WriterAgent to consume only accepted claim rows, including accepted `PAPER_USABLE` rows with explicit limitations. Draft prose around available evidence and update only affected sections when claims change.
9. Run incremental verification after each changed artifact. Run full computation reproducibility, full-paper compile, and full-page visual QA once near delivery.
10. Update the compact workflow state and deliver when all claims used in the paper are accepted at their declared evidence level and final paper QA passes. Unfinished certification work remains a limitation, not a hidden blocker.

## Incremental Retry Rule

Every failure report must name `failure_scope`, `owner_task`, `artifact`, `failed_check`, `required_fix`, and `rerun_command`.

- Code or solver failure: rerun that question and its direct validators only.
- Figure failure: regenerate that figure and inspect affected paper pages only.
- Prose or citation failure: edit and recompile the paper; do not rerun models.
- Certification failure: mark `FAILED_DIAGNOSTIC` and preserve delivery results unless it disproves an accepted claim.
- Accepted upstream output change: invalidate only downstream tasks connected by a blocking edge.
- Shared input, governing equation, unit, or exported interface change: compute the downstream scope with `scripts/select_rerun_scope.py` and rerun only that scope.

Never restart the whole workflow unless the original problem, shared input data, or shared governing contract is invalidated. A gate gets at most two repair attempts in the current profile; after that, downgrade or isolate it and continue unless the user explicitly selects `certification`.

## Evidence Chain

Every material conclusion must follow:

`claim -> model/algorithm -> executed result -> validation -> figure/table -> interpretation`

Assign stable `claim_id` values in the model report. The same IDs must appear in result records and `results/figure_manifest.csv`. A prose claim without executed evidence, or a figure without a specific claim, is incomplete.

Store canonical quantitative and categorical conclusions in `results/claim_registry.csv`. Generate summary, body, tables, captions, and recommendations from those accepted claims or verify them against the registry; do not maintain conflicting hand-copied values.

Label each reported solution as `strict_feasible`, `validated_estimate`, `scenario_result`, or `ideal_upper_bound`. Never present an ideal boundary or reduced-model estimate as an implementable optimum. Use stable scenario keys across result tables, figures, captions, and prose.

### Interpretation Discipline

Before fixing an objective or feasible set, identify wording that can reasonably change the comparison object, fixed endpoints, movable boundary, parameter freedom, time origin, cost scope, or downstream path. Prefer the interpretation best supported by the literal statement, contest convention, supplied figures/attachments, and dependencies between questions; do not silently replace the stated target with a self-defined “fair”, stricter, or more engineering-like target.

A single primary interpretation is sufficient when the evidence clearly favors it or a quick derivation shows that alternatives do not materially change the answer. Record the alternative and the reason for rejecting it in the modeling decision log; a full duplicate solve is not required. If two interpretations remain comparably defensible and can reverse a qualitative answer or materially change a recommendation, disclose both. Use a full executed scenario for every interpretation needed by the final conclusion, but allow a bounded analytical proof, invariance argument, or counterexample to dispose of an alternative when that is sufficient. Give separately executed branches stable scenario keys and propagate each key to every downstream result that consumes the changed geometry, path, objective, or constraint.

Keep this reasoning in the evidence system, then translate it into ordinary academic Chinese in the paper. Internal terms such as `claim`, `PAPER_USABLE`, “冻结”, “门禁”, “工作流状态”, Agent ownership, and retry notes must not appear in submission prose.

### Reference-Paper Style Calibration

When the user supplies a reference paper or asks to match a specific Chinese writing style, inspect representative passages before WriterAgent drafts the body. Extract the reference's subsection granularity, paragraph rhythm, transition logic, formula lead-ins, representative-derivation pattern, result-analysis order, and evaluation tone. Follow `references/chinese-paper-language-style.md`; record the compact style profile in the Writer handoff or modeling decision log, and calibrate one substantive subsection before expanding the style across the paper. Treat readability as a hard requirement: expose the current object, known and unknown quantities, reason for each important equation, its output, and the next computational action; derive one concrete local case before any compact global recurrence or model-summary block.

Match reasoning structure rather than isolated phrases. Preserve factual correctness and evidence discipline: do not copy the reference's numerical results, unsupported evaluations, modeling mistakes, or unverified algorithms merely to resemble its language.

For an explicit style-matching request, use a two-pass rewrite: first restore the reference's section roles and local derivation rhythm, then calibrate sentence transitions and tone. Preserve or increase meaningful subsection granularity; never collapse model construction, solution, requested result, and verification into one polished subsection. Forward-test one complete computational question after a substantial style-rule change. A forward test that only changes vocabulary or connective words fails even when its mathematics is correct.

For a mechanism-heavy question, end the derivation with a visible `模型汇总` block before the numerical-solution subsection. Group only the equations actually consumed by the solver under semantic labels such as geometry/path, state, objective, constraints, recursion, and boundary conditions. State the unknowns and index ranges after the block. Do not replace the representative derivation with an unexplained wall of equations, and do not repeat every intermediate identity.

Each computational question used in the final paper must eventually cover three visual evidence roles:

- mechanism, geometry, input, or model structure;
- primary result or comparison;
- validation, sensitivity, robustness, or diagnostics.

A well-designed multi-panel figure may cover several roles, but each panel must be registered separately. Build these roles incrementally: first one claim-bearing result, then mechanism and validation views before final delivery. Do not delay the first runnable loop to satisfy the final figure count. For a typical four-computation-question paper, plan at least 12 core evidence units, with at least 8 generated by MATLAB when MATLAB is the chosen runtime; adapt the target to the actual problem and document the reason.

## Paper Visual Architecture

Plan the paper's visual language during modeling, not after the numerical work is finished. If the user supplies reference figures, inspect them early and extract transferable choices such as 3-D viewpoint, structural cutaway, surface mesh, field coloring, multi-panel composition, and information hierarchy. Adapt those choices to the actual model and data; do not copy labels, values, or decorative geometry from the reference.

Treat a reference figure as a source of visual grammar, not as a checklist of objects or panels to reproduce. Learn how it makes an abstract relation inspectable: choose a front or sectional view, draw the true object outline, isolate the active local relation, distinguish primary and auxiliary geometry, and coordinate annotations with the derivation. Then decide independently which paper claims need that treatment. Do not create one figure for every construction shown in the reference, and do not force the same construction style onto unrelated questions.

For each major computational question, consider whether a parameterized 3-D structure, mechanism schematic, response surface, feasible-region surface, spatial field, or coordinated multi-view figure would explain the model better than a basic line or bar chart. Prefer publication-grade MATLAB figures that expose geometry, variables, constraints, and result variation together. Every advanced visual must still be generated from the accepted model parameters or outputs and must add analytical meaning; visual complexity alone is not evidence.

Build the final visual argument by combining complementary figure types. Use an orthographic analytical construction for a local formula or contact relation, a data plot for a computed trend or numerical comparison, and a 3-D view only when its third coordinate is a real variable and reveals a relation that two dimensions cannot. These are complementary evidence roles, not mandatory panels in every question; merge them into a coordinated multi-view figure only when the panels share a common claim, scale, or state.

For curved-path, linkage, contact, or tangent geometry, first classify the figure as numerical or analytical. Use MATLAB when the body pose, clearance, field, or dimensions are computed results. When the figure only expresses a symbolic geometric relation and a MATLAB rendering would look like a simulation plot, prefer reproducible LaTeX/TikZ linework. In either case show the true relation: rigid-body outline, active path, indexed points, junction and circle center, motion direction, and dashed radii or auxiliary triangles used by the adjacent formula. Use an orthographic local frame, a tight crop, and a clear line hierarchy; do not force 3-D or global axes into a textbook-style derivation figure.

Create one overall modeling workflow diagram after the dependency graph stabilizes and place it near the start of `问题分析`. Do not assign one flowchart to every question by default. Add a local algorithm flow only when the prose contains a genuine iteration, branch, fallback, or multi-stage decision that is materially easier to read as a diagram; place it beside the corresponding algorithm subsection, not as a decorative chapter opener. Prefer equations for linear recursions, MATLAB geometry for mechanisms, and data plots for numerical conclusions. Use `4drawio` for logical routes and branching algorithms, and MATLAB for parameterized geometry or model mechanisms. Retain editable source plus PDF/PNG exports and verify arrow direction, Chinese text, spacing, and final-size readability.

## MATLAB Policy

When the user requests MATLAB, or the task is engineering, optimization, dynamic simulation, numerical analysis, or geometry-heavy, use MATLAB as the primary computation and data-figure runtime unless it is unavailable. Do not silently substitute Python.

Require reproducible `.m` entry scripts, fixed random seeds where applicable, saved source data (`.mat` or `.csv`), structured result exports, vector PDF figures, 300 dpi PNG previews, explicit Chinese fonts for Chinese papers, complete units/legends/colorbars, and a run command. Generate geometry, response surfaces, fields, convergence, constraints, residuals, sensitivity, or time-series plots from actual model parameters and outputs, not hand-drawn approximations.

For engineering tasks, MATLAB must visualize the model itself where meaningful: coordinate system and dimensions, candidate structures or material-property space, heat sources/loads, initial and boundary conditions, mesh/stencil or computational domain, final layout, field extrema, and validation. Data-summary plots alone do not satisfy model visualization.

For geometric or mechanism models, include at least one publication-style MATLAB schematic built from the same parameters as the solver. Prefer clean linework or restrained fills; show the true object outline or section, centerline/path, named key points, local tangent/normal or other basis vectors, dimension arrows with units, and the exact contact, load, boundary, or constraint relation used in the derivation. Keep labels horizontal when possible and route arrows away from text. A schematic is analytical evidence, not decoration.

## Handoff Contract

Each handoff reports only fields changed since its previous accepted version:

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

Agents communicate through workspace artifacts, not hidden chat context. Keep routine handoffs concise and reference unchanged evidence by stable path/hash rather than copying it. The orchestrator inspects only the changed contract and required evidence before starting dependent work. Never let agents concurrently edit the same report, source file, manifest rows, figure, or paper section.

## Non-Negotiable Gates

- Do not report unexecuted numbers as results.
- Do not accept `PAPER_USABLE` merely because code ran. Enforce every item in the non-negotiable delivery quality floor; a missing item blocks that claim, not unrelated tasks.
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
- Do not accept an interpretation that silently changes the stated comparison object, fixed endpoints, movable boundary, parameter freedom, or cost scope. When comparably defensible interpretations can reverse the main answer, require explicit disclosure and either separate executed scenarios or a sufficient analytical proof for the non-primary branch.
- Do not reuse a model outside its declared steady/dynamic, spatial, linearity, or boundary-condition regime without an explicit validity decision and replacement model.
- Do not accept a computational question whose mechanism, principal result, and validation evidence are absent without a specific reason. These are evidence roles, not a required count of separate figures, and they do not imply a per-question flowchart. Use the single overall roadmap for cross-question dependencies; require a local algorithm flow only when a genuine loop, branch, fallback, multi-start selection, or stopping decision is materially clearer as a diagram than as equations and prose.
- Do not accept a mechanism-heavy paper chapter that derives several equation families but never provides a compact, labeled model-summary block before numerical solution.
- Do not accept a geometry-heavy paper whose MATLAB figures omit the local construction actually used in the derivation. A generic full-path overview cannot replace a close-up showing the rigid body, named points, center or tangent reference, motion arrow, and auxiliary distance relations.
- Do not accept MATLAB figures without their `.m` generator, source data, PDF, PNG preview, and manifest row.
- Do not accept figures with clipped labels, unreadable Chinese, misleading axes, arrow/text overlap, or unexplained visual encodings.
- Do not admit figures containing `####`, mojibake, duplicate glyphs, clipped final-size labels, or failed diagnostic content into the paper.
- Do not substitute representative material ranges, geometry, fields, or scenarios when the supplied attachments contain the relevant actual data.
- Do not accept unexplained correction factors, weights, fitted constants, or calibration coefficients without provenance, applicability, and sensitivity evidence.
- Do not allow numbers, scenario keys, candidate IDs, or recommendation wording to disagree across structured outputs, registry rows, tables, figures, abstract, body, conclusions, and recommendations.
- Do not expose internal paths, code/report filenames, Agent/process language, retry notes, or template examples in the submission paper.
- Do not expose evidence-management vocabulary such as `claim`, `PAPER_USABLE`, `FAILED_DIAGNOSTIC`, “冻结”, “门禁”, or scenario-registry mechanics in the submission paper; rewrite them as model assumptions, applicability conditions, numerical verification, or sensitivity conclusions.
- Do not describe `PAPER_USABLE` evidence as certified, construction-safe, code-compliant, experimentally verified, or universally optimal.
- Do not accept a problem-analysis section that merges all questions into generic prose; every top-level question must have its own analysis subsection covering inputs/outputs, task essence, dependencies, difficulty, credible alternatives, selection rationale, and expected evidence.
- Do not accept a Chinese abstract unless it has an opening overview and a separate prose paragraph for every top-level question, explicitly naming the model, solution method, decisive objective or constraints, accepted result or result type, validation, and meaning.
- Do not accept zero, duplicate, or scattered top-level model-assumptions sections. All shared and question-specific assumptions must live inside one coherent `模型假设` section and state basis, scope, effect, and failure treatment.
- Do not select or combine named models merely to signal sophistication. Require evidence-based alternatives, applicability, limitations, rejection reasons, and a validation plan.
- Do not fabricate data, references, experiments, performance, or citations.
- Do not start the upstream FastAPI/Redis application unless the user explicitly requests it.
- Do not mark delivery complete while a claim used in the paper lacks accepted evidence at its declared level or `reports/VERIFY_REPORT.md` contains a paper-blocking failure. Unused or certification-only tasks may remain `SKIPPED` or `FAILED_DIAGNOSTIC` with an explicit limitation.

## Resource Map

- Role contracts: `references/agent-roles.md`
- Evidence, MATLAB, and figure rules: `references/evidence-chain-matlab-figures.md`
- Model continuity and numerical validation: `references/model-continuity-numerical-validation.md`
- Decision metrics and reproducibility: `references/decision-metrics-reproducibility.md`
- Attachments and MATLAB model rendering: `references/attachments-and-model-rendering.md`
- First-prize paper structure and writing contract: `references/paper-structure-first-prize-writing.md`
- Chinese paper language and reference-style calibration: `references/chinese-paper-language-style.md`
- Incremental delivery, budgets, and retry scope: `references/incremental-delivery.md`
- Input manifest validator: `scripts/validate_input_manifest.py`
- Figure manifest validator: `scripts/validate_figure_manifest.py`
- Claim registry validator: `scripts/validate_claim_registry.py`
- Paper structure validator: `scripts/validate_paper_structure.py`
- Local rerun scope selector: `scripts/select_rerun_scope.py`
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
