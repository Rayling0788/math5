# First-Prize Paper Structure Contract

Use this contract for Chinese mathematical modeling papers unless the contest template explicitly requires another top-level order. Template constraints may change file names or placement, but they do not remove the per-question analysis, segmented abstract, or consolidated assumptions requirements.

## Problem Analysis

Create one top-level section named `问题分析` (or a contest-template equivalent). Under it, create one distinct subsection for every top-level question in the problem statement, in the original question order unless a dependency-based order is clearly explained:

- `问题一分析`
- `问题二分析`
- `问题三分析`
- continue for the actual number of questions

Each question-analysis subsection must explain, in connected prose:

1. the inputs, known conditions, attachment evidence, and required outputs;
2. the mathematical or physical essence of the task;
3. dependencies on earlier questions and quantities passed downstream;
4. the main modeling difficulty, uncertainty, or identifiability issue;
5. at least one credible alternative method when a real choice exists;
6. why the selected method matches the data volume, mechanism, accuracy target, and available validation;
7. what executed result, figure, table, or diagnostic will constitute evidence.

Do not copy the problem statement, pre-empt the full derivation, or insert final numerical conclusions into this section. The purpose is to make the reasoning path continuous before formulas and computation begin.

## Chinese Abstract

Write the abstract after all claims are frozen. Use continuous paragraphs rather than bullets, tables, equations, citations, or internal artifact names.

Required paragraph structure:

1. a short opening paragraph stating the overall task, shared framework, and central modeling idea;
2. one separate paragraph for every top-level question, preferably beginning with `针对问题一`、`针对问题二` and so on;
3. an optional short closing paragraph summarizing the principal conclusion, robustness, limitation, or practical recommendation.

Each question paragraph must contain:

- the immediate task and the actual mathematical structure or transformation used;
- the executed action sequence, including the numerical method where it matters;
- one direct answer group, with unit and answer-changing scenario when quantitative.

Add the objective or decisive constraints only when they govern the answer. Normally choose one validation, comparison, interpretation, limitation, or practical meaning for closure; an alternative interpretation that changes the answer may be stated separately.

These requirements define paragraph roles, not a checklist to compress into one sentence. The hard closure is the question, executed actions, direct answer group, and conditions that change that answer. Normally use two to four sentences; mention objectives or constraints only when they govern the decision, and choose one validation, interpretation, or limitation for closure. An answer-changing alternative interpretation may be added separately. Pair model and algorithm names with what they compute. Shared conditions may remain in the opening; keep one answer group per question and move residual lists and secondary tolerances to the body. Respect the official abstract limit by compressing shared methods and diagnostics before merging or deleting problem answers.

Avoid empty phrases such as `效果较好`、`具有一定意义` or `本文将研究`. Do not invent a number merely to satisfy the structure: for a qualitative question, state the accepted categorical result and its evidence type. Reject a paragraph if a reader cannot recover the task, model action, execution order, answer, and applicability without consulting the body.

## Adaptive Model Summary

Classify the question before choosing a summary. A sequential derivation, single-layer estimate, or recurrence should preserve its natural calculation order and may use a generalized equation without a separate `模型汇总`. A coupled system needs a compact summary only when several variable, constraint, and objective or solution-criterion families must be viewed together to reconstruct the numerical problem. A layered model that exports one explicit quantity upstream should summarize only the downstream layer that is actually coupled.

When a summary is needed, place it after representative derivations and before numerical solution. Explain variables, constraints, and the objective or actual criterion separately first, then group only governing relations consumed by the implementation. Follow the block by stating unknowns, known inputs, index ranges, interfaces, and solver order. The summary is not a second derivation, cannot introduce new symbols, and must not exist merely to satisfy four fixed headings.

## Consolidated Model Assumptions

Use exactly one top-level section named `模型假设` (or an unambiguous equivalent) in the entire paper. Place all assumptions in this section as one coherent block before the main model derivations, unless the official template requires a different location.

The section may contain `共同假设` and question-specific groups such as `问题三特有假设`, but those groups must remain subsections or numbered items inside the same top-level section. Do not create separate top-level `问题一假设`、`问题二假设` sections and do not scatter undeclared assumptions through later chapters.

Each material assumption must state:

- the assumption itself;
- its basis in the problem, attachment, literature, data, or engineering scale;
- the questions or model components to which it applies;
- its expected effect and a failure condition or sensitivity treatment.

Later derivations must cite the applicable assumption number when it matters. Do not add generic statements that neither simplify a model nor delimit its validity. Present the section as normal academic text, a compact numbered list, or a restrained table when useful; do not fragment it into decorative cards or unrelated text boxes.

## Model Choice Discipline

For each question, compare only credible alternatives. Selection must be driven by task structure, attachment evidence, data sufficiency, mechanism fidelity, interpretability, computation, and validation capacity. Do not stack CRITIC, AHP, TOPSIS, PSO, BP, LSTM, or other named techniques merely to appear advanced. A simpler model with a verified evidence chain is preferable to an unidentifiable hybrid.

Every selected model must record its applicability conditions, main advantage, main limitation, alternative considered, rejection reason, and validation plan in the modeling decision log before paper drafting.

## Interpretation And Scenario Discipline

Do not treat every possible reading as a full parallel model. First identify exactly which semantic choice changes the mathematics: the comparison object, included path or cost components, fixed endpoints, movable entry/exit locations, parameter freedom, time origin, or feasible region. Select one primary reading when the statement, figures, attachments, contest convention, dependencies, or a quick derivation clearly support it, and record why the other reading is not adopted.

If two readings remain comparably defensible and can reverse the main qualitative answer or materially change a recommendation, both must be disclosed. The primary reading receives the complete executed solution. The alternative may use another executed scenario, but a concise analytical proof, invariance argument, or counterexample is sufficient when it fully determines the alternative conclusion. Only separately executed numerical branches require separate scenario keys. Any downstream result that consumes a changed path, geometry, objective, or constraint must remain within the same scenario.

For a route-optimization ambiguity, a good disclosure states, for example: under the reading that entry and exit positions may move inside the turning region while the radius ratio remains fixed and “route length” means only the connecting arcs, the arc length can be shortened; under the reading that turning starts at fixed boundary points while the radius ratio may vary, changing the ratio may leave total arc length invariant, so the claimed optimization disappears. This is a pattern for exposing assumptions, not a license to reuse either conclusion without derivation.

In the paper, introduce the primary reading before its formulas. Put a consequential alternative in a short note, interpretation-sensitivity paragraph, or dedicated subsection using the form `在口径 A 下……；若按口径 B 理解，则……`. Never combine objective values from different definitions in one ranking or recommendation.

## Chinese Narrative Style

Write each substantive subsection as a connected argument:

1. state the immediate purpose and the physical, geometric, statistical, or decision picture;
2. explain why the chosen relation or model represents that picture;
3. introduce the mathematical expression and define its variables where they first matter;
4. describe the executed solution method at the level needed for reproducibility;
5. report the result with unit, scenario, and applicability;
6. interpret the result and close with validation, sensitivity, or a limitation.

Introduce a formula with its modeling purpose, and follow it with its physical meaning rather than leaving equations as isolated derivations. Introduce a figure by the question it helps answer, then explain the evidence it provides. Use transitions based on cause, condition, contrast, and consequence; avoid a mechanical chain of `首先`、`其次`、`最后` or repeated openings such as `如图所示`.

Translate internal evidence records into ordinary academic Chinese. Do not expose `claim`, `accepted`, `scenario_key`, `PAPER_USABLE`, `FAILED_DIAGNOSTIC`, file paths, Agent ownership, workflow state, freezing, gates, retries, or debugging. Avoid unsupported self-evaluation such as `利用数学知识`、`理论基础扎实`、`结果合理`、`符合客观事实`、`效果较好` or `具有一定意义`; name the actual residual, comparison, constraint, sensitivity, or observed mechanism instead.

For rewrite-only work, freeze accepted results rather than the old exposition. Reconstruct a reader-facing local derivation from the accepted model before presenting solver-facing vectors, unified indices, piecewise functions, objectives, or constraint sets. Equivalent symbolic steps and explanatory schematics are allowed without numerical recomputation; changing assumptions, model meaning, scenarios, or values is not. If the source artifacts cannot justify a concrete derivation, return the gap to modeling instead of preserving or polishing a formula wall.

In a Chinese abstract, retain one principal answer and one decisive validation item per question. Move secondary residuals, tolerances, intermediate optima, and full-precision diagnostics to the body or appendix. If interpretations lead to different conclusions, name their conditions explicitly rather than stacking unexplained numbers.

## Blocking Acceptance Rules

Final verification must fail when any of the following holds:

- the problem-analysis section does not contain a distinct subsection for every top-level question;
- a Chinese abstract compresses several questions into one undifferentiated paragraph or omits a question;
- the paper has zero or more than one top-level model-assumptions section;
- question-specific assumptions appear as separate top-level sections or material assumptions are introduced later without registration;
- model choice is asserted without alternatives, evidence, rationale, applicability, and validation;
- abstract results conflict with the accepted claim registry or omit required units/scenarios.
- an abstract question paragraph fails to name the actual model and executed solution method, or omits an objective/constraint that genuinely governs its answer;
- a rewrite-only chapter preserves an opaque solver-first structure, or a mechanism-heavy question presents the generalized computational model before any trustworthy local object, construction, or representative derivation;
- a mechanism-heavy question contains several equation families but lacks a readable model-summary subsection before numerical solution;
- a selected interpretation silently changes the comparison object, fixed endpoints, movable boundary, parameter freedom, or cost scope;
- comparably defensible interpretations can reverse the main answer, but the alternative is neither disclosed nor resolved by an executed scenario or sufficient analytical argument;
- downstream values combine incompatible interpretation scenarios;
- submission prose exposes internal evidence/workflow vocabulary or relies on unsupported self-evaluation instead of named evidence.
