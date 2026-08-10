# Evidence-Preserving Natural Prose For Modeling Papers

Use this reference when drafting, rewriting, or reviewing a mathematical modeling paper whose prose feels templated, inflated, or visibly machine-generated. Apply it after the model, claims, units, scenarios, citations, and section roles are stable. It supplements `chinese-paper-language-style.md`; it never overrides evidence, contest format, or mathematical precision.

This contract is a domain adaptation informed by `blader/humanizer` commit `523374dee72d67c7b2b5f858ea0094ffda49c3ac`. It does not import that general-purpose skill wholesale. Technical papers need neutral language, legitimate repeated terminology, standard mathematical transitions, and occasional passive or subjectless constructions. Preserve those when they make the derivation clearer.

## 1. Lock Evidence Before Editing Voice

Freeze the following before changing prose:

- every numerical value, unit, rounding rule, scenario, candidate ID, and result type;
- equations, symbol meanings, assumptions, objective functions, constraints, and model scope;
- figure and table references, caption meaning, citations, quoted text, and source attribution;
- distinctions among an ideal bound, scenario result, feasible design, and recommendation.

Humanization may reorganize paragraphs, remove filler, split or merge sentences, and replace vague language with a concrete relation already present in the evidence. It may not invent a fact, mechanism, source, validation result, causal claim, or stronger conclusion. If natural prose requires a detail that the evidence does not contain, use the plain supported statement or return the gap upstream.

For LaTeX and Typst files, leave commands, labels, citations, formula bodies, code blocks, paths, and data interfaces unchanged unless the task explicitly includes them. Edit only reader-facing prose.

## 2. Keep The Correct Academic Voice

The target is a direct competition paper, not a blog post and not a chatbot response. Neutral and plain language is the correct human voice for equations, algorithms, assumptions, and numerical verification. Do not inject first-person opinions, jokes, rhetorical questions, staged intimacy, or deliberate grammatical roughness.

When the user supplies a reference paper or personal sample, match its defensible habits: subsection granularity, sentence length, paragraph openings, punctuation, formula framing, transition density, and result-analysis rhythm. The sample may justify a construction that a generic anti-pattern list would otherwise discourage. Evidence and contest requirements still take precedence.

## 3. Diagnose Clusters, Not Isolated Words

A single `因此`、`进一步`、`本文`、passive sentence, list, or long sentence is not an AI-writing defect. Rewrite only when several patterns cluster or one pattern repeatedly hides the mathematical action.

### Unsupported elevation

Remove claims that the work is `重要`、`突破性`、`领先`、`具有广泛前景`、`奠定坚实基础` or `彰显价值` unless the sentence names the comparison, evidence, and applicable scope. End a section on the last concrete result, limitation, or decision instead of a generic positive send-off.

### Decorative analysis

Delete tails such as `从而充分体现了……`、`进一步凸显了……`、`为……提供有力支撑` when they merely repeat the preceding result. Replace them with the actual relation: which variable changed, under what condition, by how much, and what conclusion follows.

### Vague authority

Do not use `研究表明`、`专家认为`、`业内普遍认为` or `众所周知` without a named source or an adjacent citation. If no source exists, state the model assumption or observed data relation directly and limit the claim to the current study.

### Abstract-noun chains

Replace strings such as `协同机制—闭环体系—决策赋能—价值提升` and unexplained audit vocabulary with the modeled object, mathematical action, condition, and consequence. Necessary terms such as `齐次性`、`分离轴定理`、`鲁棒优化` or `运动学奇异` remain when defined and used.

### Forced symmetry

Do not force every question into the same number of subsections, every paragraph into three points, or every conclusion into a parallel slogan. Preserve the actual dependency structure. Repeating the same technical noun is often clearer than cycling through imprecise synonyms.

### Empty signposting and warm-up lines

Cut announcements such as `下面将对……进行详细分析`、`接下来让我们讨论……` or a heading followed by one sentence that restates the heading. Begin with the object, condition, equation, or action. Keep `首先—其次—最后` only when the code or derivation has that real order.

### Chat and editing residue

Submission prose must not contain `当然可以`、`希望这对你有帮助`、`如有需要可以继续`、`下面是修改后的内容`, change-log narration, prompt language, or comments addressed to the user. Describe the final model as it is, not how the draft was revised.

### Manufactured drama

Avoid runs of short fragments, rhetorical questions, aphorisms, and slogan-like contrasts. Use sentence-length variation to serve reasoning: a short sentence may state a boundary or result, while a longer sentence may carry one complete cause-and-effect relation.

## 4. Rewrite In Three Passes

### Pass 1: restore roles and evidence

Map each paragraph to one job: establish the object, derive a relation, explain the algorithm, report the requested result, interpret a mechanism, or verify robustness. Restore missing formula handshakes and reader-facing derivations before polishing vocabulary.

### Pass 2: make actions visible

Prefer `计算`、`代入`、`比较`、`判断`、`联立`、`递推`、`搜索` and `得到` over ceremonial or abstract phrasing. Use the real object as subject when a pronoun becomes ambiguous. Vary sentence length and paragraph openings naturally, but do not sacrifice symbol consistency or execution order merely to avoid repetition.

### Pass 3: run two audits

Ask:

1. Which phrases still sound templated, promotional, vague, over-balanced, or written to the user rather than the judge?
2. Did the rewrite add, remove, strengthen, weaken, or relocate any fact, number, unit, equation meaning, scenario, citation, or limitation?

Revise until the first audit finds no material cluster and the second finds no evidence drift. In a larger workflow, keep this audit internal and output only the final prose.

## 5. Chapter-Specific Priorities

- **Abstract:** preserve the task, actual action chain, direct answer, necessary scenario, and one useful closure item. Vary the rhythm across questions; do not turn four paragraphs into copies with different nouns.
- **Problem analysis:** state the real difficulty and selected route. Remove background inflation and generic claims about significance.
- **Model construction:** repeat object names when helpful, frame formulas concretely, and avoid synonym cycling that breaks symbol-to-prose mapping.
- **Model solution:** narrate implemented actions and stopping conditions, not software ceremony or an algorithm-name list.
- **Result analysis:** report the answer first, then one visible mechanism and its validation. Do not append a generic claim that the result is reasonable.
- **Model evaluation:** name a specific strength or limitation, its evidence, and its consequence. Avoid mandatory counts of advantages and disadvantages.
- **Conclusion:** end on the recommended design, applicable range, boundary result, or main limitation. Delete generic statements about a promising future or broad value.

## 6. Acceptance Standard

Accept the prose only when all three conditions hold:

1. a reader can reconstruct the model's reasoning and executed order without internal files;
2. no cluster of unsupported elevation, vague authority, decorative analysis, chatbot residue, forced symmetry, or abstract-noun chains obscures the technical content;
3. a claim-by-claim comparison finds no change to facts, numbers, units, scenarios, equations, citations, uncertainty, or recommendation strength.

Automated phrase scans are candidate generators. Treat chatbot residue and leaked editing instructions as errors, but review other hits in context. Never flatten legitimate academic prose merely to reduce a word-frequency score.
