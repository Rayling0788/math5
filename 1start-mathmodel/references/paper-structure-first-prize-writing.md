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

- the method and named model actually used;
- the key mechanism, variable, objective, or constraint that distinguishes the approach;
- at least one exact accepted result when the question is quantitative, including unit and scenario where needed;
- the relevant validation, comparison, sensitivity, uncertainty, or feasibility conclusion;
- the practical or mathematical meaning of the result.

Avoid empty phrases such as `效果较好`、`具有一定意义` or `本文将研究`. Do not invent a number merely to satisfy the structure: for a qualitative question, state the accepted categorical result and its evidence type.

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

## Blocking Acceptance Rules

Final verification must fail when any of the following holds:

- the problem-analysis section does not contain a distinct subsection for every top-level question;
- a Chinese abstract compresses several questions into one undifferentiated paragraph or omits a question;
- the paper has zero or more than one top-level model-assumptions section;
- question-specific assumptions appear as separate top-level sections or material assumptions are introduced later without registration;
- model choice is asserted without alternatives, evidence, rationale, applicability, and validation;
- abstract results conflict with the accepted claim registry or omit required units/scenarios.
