# Model Continuity and Numerical Validation

Use this reference when questions inherit a common physical/statistical core, introduce new regimes, use field solvers or surrogates, or report several scenario-dependent optima.

## Contents

1. Build a Shared Core Before Splitting Questions
2. Applicability-Regime Matrix
3. Parameter Provenance Ledger
4. Fidelity Ladder
5. Numerical Field-Solver Gate
6. Coupled Simulation and Optimization
7. Scenario and Result-Type Ledger
8. Dynamic-System Gate
9. Evidence-Level Language
10. Blocking Failures

## 1. Build a Shared Core Before Splitting Questions

When several questions describe the same system, first define:

- governing equations or common statistical state;
- conserved quantities, hard limits, and common objective metrics;
- bridge quantities passed between questions;
- inputs that later questions may replace;
- assumptions whose failure requires a new submodel.

Do not rebuild each question independently. For every `Qk`, record:

| question | scenario_key | inherited core | new variables | invalidated assumption | replacement submodel | outputs returned to core |
| --- | --- | --- | --- | --- | --- | --- |

The final result of each question must return to the original decision constraint. A trend in an intermediate proxy is not a complete answer unless its decision consequence is computed.

## 2. Applicability-Regime Matrix

Create `reports/MODEL_REGIME_MATRIX.md`. Define stable `regime_id` values and at least these dimensions when relevant:

- steady vs transient;
- spatially uniform vs spatially varying boundary/input;
- linear vs nonlinear;
- deterministic vs stochastic;
- laminar/empirical vs turbulent/high-fidelity physics;
- interpolation vs extrapolation range;
- training/validation population and operating envelope.

Before reusing a model, state whether the new scenario remains inside its regime. If not, extend or replace the affected submodel and preserve the unaffected shared core. Never hide a regime change inside a parameter substitution.

## 3. Parameter Provenance Ledger

Create `results/parameter_ledger.csv` with:

```text
parameter_id,symbol,value,unit,source_type,source_ref,valid_range,regime_id,uncertainty,sensitivity_status
```

Use `source_type` values such as `problem`, `attachment`, `literature`, `measured`, `fitted`, `simulated`, or `assumed`. Record page/table/URL/file references. If a literature range is collapsed to one convenient value, propagate the full credible range before accepting the conclusion.

Do not randomly map qualitative grades to numbers unless the stochastic encoding is itself part of the model, uses a fixed seed, has a defensible distribution, and is tested for rank/decision stability. Subjective weights require rationale, range analysis, and rank-reversal thresholds.

## 4. Fidelity Ladder

Classify model levels as:

- `conceptual`: causal or structural diagram;
- `analytical`: closed form, limiting case, or exact small model;
- `reduced`: simplified dimension, surrogate, response surface, or modular approximation;
- `numerical`: direct discretized solver at the declared resolution;
- `high_fidelity`: trusted multiphysics/CFD/experiment-backed simulation;
- `experimental`: measured reference data.

For each reduced or surrogate model, name the reference level and benchmark it on representative cases. Report accuracy, speed gain, valid range, and failure mode. A future suggestion to compare is not calibration, and visual resemblance is not an error metric.

Use independent corroboration only when both methods test the same claim at the same resolution. A clustering family pattern does not independently verify a multi-criteria method's exact top-ranked item. Prefer analytical limits, manufactured solutions, experiments, trusted solver comparisons, held-out cases, or exact small-instance optimization.

## 5. Numerical Field-Solver Gate

For FDM, FEM, FVM, spectral, or multiphysics field models, require:

1. governing equation, domain, source terms, constitutive parameters, and units;
2. initial and boundary conditions with physical justification;
3. method classification and discretization/stencil or weak form;
4. solver, tolerance, stopping condition, iteration cap, and failure handling;
5. residual history and convergence status;
6. conservation or balance error;
7. mesh and time-step refinement study as applicable;
8. analytical, manufactured, experimental, or trusted-solver benchmark where feasible;
9. extrema and hotspot locations checked against physical expectations;
10. exact configuration used by downstream optimization.

Do not infer method names from plot style. A colored contour can come from FDM, FEM, interpolation, or measured data. Use the method justified by equations and code.

## 6. Coupled Simulation and Optimization

Separate geometric feasibility from physical feasibility. A packing, schedule, or allocation that fits combinatorially may still violate temperature, stress, flow, or reliability limits.

For simulation-constrained optimization:

- define how every decision vector becomes a simulation configuration;
- evaluate hard constraints using the accepted solver or calibrated surrogate;
- save rejected and accepted constraint margins;
- compare heuristics against exact small instances, multiple starts, or a credible alternative;
- avoid claiming global optimality without a certificate or exhaustive bound;
- rerun the final candidate with the reference-fidelity model.

## 7. Scenario and Result-Type Ledger

Create `results/scenario_results.csv` with at least:

```text
question_id,scenario_key,regime_id,model_level,result_type,changed_factors,core_metrics,constraint_margins,evidence_path
```

Use these result types:

- `strict_feasible`: all declared real constraints verified;
- `validated_estimate`: calibrated approximation within a stated error/range;
- `scenario_result`: conditional result for a named input scenario;
- `ideal_upper_bound`: deliberately optimistic boundary or relaxed-constraint limit.

Never compare scenario values without listing what changed. Never write an ideal upper bound as “the optimum” without the qualifier. Use the same scenario key in tables, figure manifest, captions, and prose.

## 8. Dynamic-System Gate

For time-varying environments:

- justify why a steady model remains valid or why a transient replacement is needed;
- define input, output, initial state, time unit, time constant, and operating range;
- test stability, steady-state gain, lag, overshoot, peak response, and frequency/step-size range as applicable;
- propagate the dynamic response to the actual decision variable or hard constraint;
- restrict statements such as “no overshoot” to the tested model class and input conditions.

Do not call an open-loop transfer-function response a controller result unless a controller, feedback path, and closed-loop test are present.

## 9. Evidence-Level Language

Match prose strength to evidence:

- analytical identity or verified computation: “shows” or “establishes”;
- calibrated numerical agreement: “supports within ... error”;
- literature-consistent trend: “is consistent with”;
- unvalidated simplification: “suggests under the stated assumptions”;
- ideal scenario: “provides an upper bound”.

Final recommendations must cite scenario keys, thresholds, margins, and sensitivity. Convert high-sensitivity parameters into measurement, manufacturing, monitoring, or safety-margin requirements.

## 10. Blocking Failures

Block delivery when any applies:

- dependent questions silently change the shared core or consume an unfrozen bridge quantity;
- the model is reused outside its regime without a validity decision;
- a key parameter lacks source, unit, range, or uncertainty treatment;
- a fitted equation violates its declared coordinate convention, monotonicity, dimensional form, boundary behavior, or observed range;
- a numerical solver lacks convergence, balance, or refinement evidence;
- a reduced model lacks calibration against its declared reference level;
- geometric feasibility is reported as physical feasibility;
- an ideal upper bound, heuristic result, or scenario estimate is labeled as a strict/global optimum;
- purported independent validation tests a different claim or merely replots the same information;
- equations, weights, parameters, code values, result tables, and figure axes disagree.
