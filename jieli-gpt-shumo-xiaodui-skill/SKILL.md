---
name: jieli-gpt-shumo-xiaodui-skill
description: "基于多个独立 Codex Agent 的端到端数学建模竞赛工作流。用于 CUMCM、MCM、ICM 及类似赛题，按协调者、建模手、编程手、图示手、论文手和验收手分工完成拆题、建模、代码执行、科研绘图、Typst/LaTeX 论文与最终校验。"
---

# MathModelAgent

## Source Baseline

Base this integration on `jihe520/MathModelAgent` commit `be9c59c1aaa13c3dcb74452ea5cae11dada27589`.

Keep the upstream files unchanged under `components/`. Use `references/agent-roles.md` for Codex-compatible role prompts; it corrects upstream prompt defects without modifying the preserved source files.

## Required Multi-Agent Model

Run a full task with separate Codex agents. The lead agent is the orchestrator and must spawn these roles rather than impersonating them:

1. `CoordinatorAgent`: parse the unchanged problem, identify subquestions and dependencies, record user preferences, and create `plan.md`, `todo.md`, and `reports/COORDINATOR_REPORT.md`.
2. `ModelerAgent`: develop assumptions, variables, candidate models, objectives, constraints, solution methods, and validation plans. Write `reports/ANALYSIS_MODELING_REPORT.md`. Do not write implementation code or the paper.
3. `CoderAgent`: implement and execute the accepted model, save reproducible code and structured results, and generate data-driven figures. Write `code/`, `results/`, `figures/`, and `reports/RESULTS_REPORT.md`. Do not silently change the model.
4. `DiagramAgent`: create only non-data diagrams when useful, including workflows and model structures. Write `figures/*.drawio`, exported PDFs, and `reports/DRAWIO_REPORT.md`.
5. `WriterAgent`: write the requested Typst or LaTeX paper using only verified artifacts. Own `paper/`; do not invent results, citations, or figures.
6. `VerifierAgent`: independently check solver reproducibility, numerical consistency, references, compilation, PDF layout, and submission readiness. Write `reports/VERIFY_REPORT.md` and block delivery on failures.

If the Agent/sub-agent tool is unavailable, say so explicitly and preserve the same role boundaries sequentially. Never claim that multiple agents ran when they did not.

## Execution Order

1. Inspect the workspace, problem statement, attachments, data, and available runtimes.
2. Read `components/1start-mathmodel/SKILL.md` and `components/_references/math_modeling_norms.md` completely.
3. Read `references/agent-roles.md`, then spawn `CoordinatorAgent` with exclusive ownership of planning artifacts.
4. Review the coordinator artifacts. Resolve only ambiguities that materially change the model or deliverable.
5. Read `components/2analysis-modeling/SKILL.md`, then spawn `ModelerAgent`.
6. Review the model report for explicit variables, assumptions, objectives, constraints, baselines, validation, and physical feasibility.
7. Read `components/3coding-visual/SKILL.md`, then spawn `CoderAgent`. Require executed code and saved outputs before accepting numerical claims.
8. Spawn `VerifierAgent` for the coding gate. Return failures to `CoderAgent` and rerun the gate.
9. If non-data diagrams are justified, read `components/4drawio/SKILL.md` and spawn `DiagramAgent`.
10. Read `components/5writing/SKILL.md`. For Typst, also read `components/typst-author/SKILL.md`. Spawn one `WriterAgent` with exclusive ownership of `paper/`.
11. Read `components/6verity/SKILL.md`, then spawn `VerifierAgent` for final QA. Fix and recheck every blocking finding.
12. Update `todo.md` after each accepted handoff and deliver only after the final gate passes.

## Handoff Contract

Give each agent only the problem files, accepted upstream artifacts, its role prompt, exclusive output paths, and measurable acceptance criteria. Each handoff must report:

- files read and written;
- methods and assumptions used;
- commands actually executed;
- checks passed and failed;
- unresolved risks;
- the exact next acceptance criteria.

Agents communicate through workspace files, not hidden chat context. The orchestrator must inspect produced artifacts before starting a dependent role.

Parallelize only independent coding experiments or disjoint subquestions after the model report is accepted. Do not let agents concurrently edit the same report, source file, figure, or paper section.

## Non-Negotiable Gates

- Do not report unexecuted numbers as results.
- Do not let the writer infer missing metrics from prose or images.
- Do not accept optimization results without physical bounds and feasibility checks.
- Do not fabricate data, references, experiments, or performance.
- Do not start the upstream FastAPI/Redis application unless the user explicitly requests the full web application.
- Do not mark the workflow complete while `reports/VERIFY_REPORT.md` contains blocking failures.

## Resource Map

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
