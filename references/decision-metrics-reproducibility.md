# Decision Metrics and Reproducibility

Use this reference for multi-objective models, ranking, fitted relationships, custom indices, candidate screening, MATLAB code, and cross-document result consistency.

## 1. Candidate Identity and Screening

Assign an immutable `candidate_id` to every material, design, route, policy, or model. Join all properties by that ID, not row order or display name. Preserve source name, grade/version, units, and missing-value state.

Separate:

- domain eligibility screening;
- hard feasibility constraints;
- objective values;
- ranking or preference rules.

Test whether screening can remove a feasible Pareto or top-ranked candidate under later objectives. Do not splice properties from related grades into one synthetic candidate unless that construction is explicit and validated.

## 2. Multi-Objective and Ranking Audit

Before weighting:

1. define each objective's physical meaning, direction, unit, feasible range, and uncertainty;
2. transform all objectives to the same benefit/cost direction;
3. normalize or nondimensionalize with an explicit rule and saved reference set;
4. show raw and normalized values;
5. calculate each term's contribution at reported solutions;
6. sweep weights over their feasible range and report choice/rank-switch thresholds;
7. show a Pareto frontier or dominance table when trade-offs are material.

A stable choice under two arbitrary weights is not robustness. If one normalized contribution remains negligible, report scale dominance and revise the metric. Do not average outputs from several formulas merely because several methods exist; justify an ensemble using reference accuracy, uncertainty, or a physical/statistical combination rule.

## 3. Custom-Metric Audit

For every invented index, record:

- definition, unit, direction, and intended decision meaning;
- invariance to coordinate origin, rotation, translation, sample size, and scale as applicable;
- behavior on hand-checkable toy cases and limiting cases;
- counterexamples and failure modes;
- correlation or agreement with a direct physical/operational metric.

Reject a proxy that rewards an obviously undesirable configuration or changes under an irrelevant coordinate transformation. A distance moment is not automatically density, uniformity, airflow, heat transfer, or risk.

## 4. Fit and Formula Audit

Every fitted relation must save source samples and report method, coordinate/sign convention, domain, parameter uncertainty, residuals, `R^2` or an appropriate error metric, and validation behavior. Check dimensions, monotonicity, boundary values, signs, and order of magnitude before use.

Do not claim higher precision by averaging correlated models without a ground-truth comparison. When standards provide alternative conversions, select the applicable standard or report their spread as model uncertainty.

## 5. Statistical Learning and Validation Audit

Before fitting, define the independent evaluation unit: record, person, device, site, date, batch, route, or another cluster. If repeated observations share stable information, split by the highest leakage-relevant unit. A stratified record split is not a substitute for a grouped split.

For every predictive or classification result, save a split audit containing group IDs, fold IDs, class counts, random seed, and train/validation/test intersections. Require all preprocessing, imputation, scaling, feature selection, resampling, hyperparameter search, model stacking, calibration, and threshold selection to be fitted inside the training portion of the appropriate fold. Stacking must use out-of-fold base-model predictions; loading a model trained on the full dataset and evaluating it on nominal validation folds is leakage, not cross-validation.

Match metrics to the task and label distribution:

- report the event prevalence and a naive or domain baseline;
- for imbalanced classification, do not headline accuracy alone; include PR-AUC and recall-sensitive metrics, plus ROC-AUC when useful;
- for probabilistic predictions, include Brier score or log loss and calibration evidence;
- define every reported "accuracy", "success rate", "reliability", or "prediction precision" mathematically, including its evaluation unit and scenario;
- attach grouped Bootstrap, repeated grouped folds, or another cluster-respecting uncertainty interval to material performance claims when sample size permits.

Freeze one label contract before modeling. Record raw source field, blank handling, multi-label decomposition, mutually exclusive class mapping, class count, and the primary task. Reject a paper or code path whose prose, formulas, state dictionary, and output table disagree on the number or meaning of classes.

Match model capacity to effective independent sample size and event count. A deep, stacked, or highly tuned model must beat a credible simpler baseline under leakage-free external or nested validation. Training curves, in-sample fit, regularization, early stopping, or a high point estimate do not establish generalization by themselves. If the complex model has no stable gain, retain the simpler model and report the negative result.

Cap strong claims at the validation design. "Zero missed detections", "99% accurate", "clinical guarantee", and similar language require a clearly defined denominator and independent evidence with uncertainty; observing zero errors in a small reused sample is not a guarantee.

## 6. Canonical Claim Registry

Create UTF-8 `results/claim_registry.csv`:

```text
claim_id,question_id,scenario_key,candidate_id,metric_id,value_type,value,unit,result_type,source_file,source_key,constraint_status,status
```

Use `value_type` as `number` or `text`; use unit `1` for dimensionless numerical values. `source_key` identifies the JSON key, CSV row/key, MAT variable, or deterministic output field. Core numerical and categorical conclusions, Top-k selections, thresholds, and recommendations must have accepted rows.

The Writer must use the registry as the canonical value source. The Verifier must compare abstract, body, tables, captions, conclusion, and recommendations against it. Run `scripts/validate_claim_registry.py` before writing and final delivery.

## 7. MATLAB End-to-End Contract

Provide one documented MATLAB driver that:

1. loads declared raw/prepared inputs and parameter files;
2. validates schemas, units, candidate IDs, and missing values;
3. performs preprocessing, fitting, solving, ranking, optimization, and validation;
4. asserts dimensions, loop coverage, counts, bounds, constraints, and known small cases;
5. exports claim registry, scenario results, tables, plot data, figures, and logs;
6. exits nonzero or raises an error on failed assertions.

Hard-coded coordinates may illustrate a verified solution but cannot establish packing optimality. Plot scripts cannot substitute for the search/solver. Avoid manual transcription from MATLAB or Excel into LaTeX; export machine-readable tables and derive paper values from them. The appendix may show selected core code, but the complete runnable source must remain in `code/`.

## 8. Blocking Failures

Block delivery when any applies:

- weighted objectives retain incompatible units or unexamined scale dominance;
- no Pareto, contribution, or continuous weight/rank analysis is provided for a material trade-off;
- candidate identity or Top-k order differs across data, tables, prose, and recommendations;
- a custom metric fails invariance, toy-case, or physical-target checks;
- a fitted formula lacks source data/error diagnostics or contradicts its sign/domain convention;
- repeated entities, sites, dates, batches, or other leakage groups cross evaluation folds without a justified independent-unit argument;
- preprocessing, feature selection, resampling, tuning, stacking, calibration, or threshold selection consumes validation/test information;
- an imbalanced classification claim headlines accuracy without prevalence, baseline, recall-sensitive metrics, probability scoring, and an explicit validation unit;
- label definitions or class counts disagree across raw data mapping, formulas, code, tables, and prose;
- a complex learner lacks a leakage-free comparison with a credible simpler baseline, or a strong performance/zero-error claim lacks independent uncertainty evidence;
- appendix/code covers only drawings or derived snippets, not the core reported results;
- an executable output, registry value, table value, and recommendation disagree;
- a final recommendation violates an upstream hard bound.
