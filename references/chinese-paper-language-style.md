# Chinese Mathematical Modeling Paper Language Style

Use this reference when writing a Chinese mathematical modeling paper, especially when the user provides a reference paper or asks for a similar academic style. Learn its transferable rhetoric and section rhythm; never copy its problem-specific wording, numbers, formulas, unsupported claims, or modeling errors.

## 1. Calibrate Before Drafting

Read representative passages from the supplied paper before writing the body:

1. abstract;
2. problem analysis;
3. one complete model-building subsection;
4. one algorithm or solution subsection;
5. one result-analysis subsection;
6. model evaluation or conclusion.

Record a compact style profile in the Writer handoff or modeling decision log. Cover:

- narrative subject: how often the paper uses `本文`、`本节` or subjectless statements;
- section granularity: how it separates model construction, solution, results, verification, and analysis;
- sentence length and paragraph density;
- transition pattern: causal, conditional, progressive, contrastive, or enumerative;
- formula framing: how formulas are introduced and interpreted;
- representative-example pattern: whether one component is derived first and then generalized;
- result reporting: headline value, example value, trend, and validation order;
- evaluation tone: whether strengths and limitations name concrete evidence.

Before drafting prose, turn that profile into a section-role map. For every substantive
question, list where the draft will place `model construction`, `representative
derivation`, `general model`, `solution procedure`, `requested result`, and `result
analysis or verification`. This map is an internal writing aid, not part of the submitted
paper. It prevents a writer from recognizing the reference style correctly but still
compressing all roles into one technical-report paragraph.

Do not reduce style matching to vocabulary substitution. Match the organization of reasoning at paragraph and subsection scale.

## 2. Put The Reader On A Visible Path

Treat accessibility as part of mathematical rigor. A reader should never have to infer
simultaneously what object is being studied, why an equation is valid, and what the
solver does next. For every technical subsection, expose the reasoning in this order:

```text
本节要求求什么
-> 先观察哪个具体对象或局部构型
-> 已知量从哪里来，未知量是什么
-> 根据哪条几何、物理或统计关系列式
-> 公式中的量分别表示什么
-> 该式把原问题转化成了什么待求量
-> 按什么顺序计算
-> 得到什么结果，结果说明什么
```

This is a reader path, not eight mandatory sentences. Short sections may combine
adjacent steps, but may not skip the identity of the current object, the source of the
relation, or the meaning of the output.

### One paragraph, one step

Let one paragraph cross one main reasoning boundary. Typical boundaries are
`题意 -> 对象`、`对象 -> 方程`、`方程 -> 待求量`、`待求量 -> 算法`、
`算法 -> 结果` and `结果 -> 解释`. Do not ask one paragraph to define the state,
derive the recurrence, describe the optimizer, report the optimum, and validate it.
Splitting a dense paragraph is useful only when each new paragraph receives a clear
local purpose; do not turn prose into disconnected one-sentence fragments.

### Formula handshake

Every important displayed formula needs a three-part handshake:

1. before it, name the concrete reason for writing it and the object to which it applies;
2. in or immediately around it, keep symbols traceable to the figure, data, or previous relation;
3. after it, state what is known, what is solved, and what the calculation enables next.

Do not present several new equations as a wall and postpone all interpretation until the
end. A short algebraic chain may remain together when every line transforms the same
quantity, but introduce the chain with its purpose and close it with its computational
meaning.

### Concrete before general

For recurrences, collisions, piecewise paths, and speed propagation, first explain one
complete local case: one board, one adjacent handle pair, one candidate collision pair,
one path junction, or one time step. State the known quantity and solve the next one.
Only then replace the concrete labels with a uniform index and extend the relation to
the whole chain or search domain. A model-summary block is a map after this explanation,
not the reader's first encounter with the model.

Use the actual object name as often as needed. Repeating `龙头前把手`、`后一把手` or
`当前板凳` is clearer than alternating among `该对象`、`该状态`、`该变量` and
`其`. Prefer visible actions such as `计算`、`比较`、`判断`、`代入`、`联立`、
`沿路径向后寻找`、`退回上一步`、`缩小步长` and `得到`. Replace stacked abstract
nouns with the object, action, condition, and consequence they conceal.

### Explain an algorithm as actions first

Before formal pseudocode or a flowchart, give one compact natural-language pass through
the actual execution order: choose the initial value; calculate the current candidate;
test the condition; if it fails, return to the previous feasible value; reduce the step;
repeat; stop when the tolerance is met. Include only actions implemented by the code.
The reader should be able to understand the algorithm after skipping the code appendix.

### Reader-blockage check

After each complex subsection, read it without relying on internal reports or source
code and answer:

- Who or what is being solved at this point?
- Where did every known quantity come from?
- Why is the displayed relation valid for this object?
- What new quantity does the relation produce?
- Why does the next calculation follow?
- Do the points, lines, directions, and symbols in the figure match the prose exactly?
- Can the algorithm still be followed if the pseudocode or MATLAB listing is skipped?

If any answer is missing, repair the local passage before polishing vocabulary. This
check takes priority over making the prose shorter.

## 3. Preserve The Reference Paper's Useful Rhythm

For a mechanism-heavy modeling question, normally separate the following roles:

1. `模型建立`: establish coordinates, objects, variables, physical relations, and constraints;
2. `递推或分类讨论`: derive one representative component or path segment, then generalize;
3. `模型汇总`: collect the equations, unknowns, objective, and constraints actually sent to computation;
4. `模型求解`: state bounds, initialization, search or numerical procedure, stopping rule, and MATLAB implementation;
5. `求解结果`: report the requested table, figure, event, optimum, or recommendation;
6. `结果分析与检验`: explain the trend, active mechanism, error, sensitivity, and applicability.

Merge roles only when the question is genuinely short. Do not compress model construction, algorithm, result, and validation into one dense paragraph merely to reduce page count.

### Model-summary block

After deriving one representative object and generalizing the notation, collect the final computational model in a visible `模型汇总` subsection. Use a brace, aligned equations, or a compact grouped display to separate semantic families such as `路径/几何`、`状态`、`位置递推`、`速度递推`、`目标函数` and `约束条件`. The display should let a reader see the complete solver input at a glance. Introduce the block with one sentence explaining what is being collected, then state the unknowns, known inputs, index range, and evaluation order below it.

Do not imitate a reference page by copying its formulas or by forcing every equation into one oversized brace. Keep only governing relations used by the code, split the block when it would exceed one page, and retain the earlier derivation that explains why each family is valid.

### Granularity lock

When rewriting an existing chapter, preserve or increase the number of meaningful
subsections until the roles above are visible. Do not replace several existing
subsections with one polished subsection. For a mechanism-heavy question, use at least
the following visible progression unless the supplied reference clearly uses a finer
one:

```text
模型建立（对象、坐标与局部关系）
模型汇总或一般递推（统一下标、目标与约束）
模型求解（可执行算法、边界与停止准则）
求解结果（先直接回答题问）
结果分析与检验（解释机理、误差和适用范围）
```

A subsection title alone does not satisfy a role. Each role must contain the material
named by the title. Figures and tables belong to the role whose inference they support;
do not gather all figures at the end of a chapter.

## 4. Build Paragraphs As Reasoning Units

Each paragraph should complete one local inference. Use the following sentence-group patterns flexibly.

As a practical rhythm, most modeling paragraphs should contain a short setup, one local
relation or displayed formula, and a sentence explaining what the relation makes
solvable. A result paragraph should first state the answer, then interpret one visible
trend, and only then give validation. Avoid a paragraph that simultaneously introduces
the model, describes the search, reports the optimum, and lists several residuals.

### Geometric or physical setup

```text
为刻画……，在……基础上建立……坐标系，并设……为……。
由于……始终满足……，故……之间存在如下关系：
[formula]
其中，……表示……；该式把……转化为……。
```

### Representative derivation and generalization

```text
以下以前一连接单元为例推导……。已知……，由……可得……。
[formula]
将……代入上式并求解……，即可得到……。其余单元的几何关系相同，因此统一写为……。
```

### Piecewise path or state classification

```text
把手可能位于……、……或……。三种情形的判别量分别为……。
当……时采用……关系；当……时改用……关系。这样可保证……在连接点处连续。
```

When a local geometric schematic makes the derivation easier to see, place it beside or immediately below the relevant setup and then derive the relation it exposes. Each panel should retain the actual body or segment outline, indexed points, relevant path branch, circle center or local coordinate basis, direction arrow, and dashed construction lines used by the following cosine-law, projection, tangency, distance, or contact equation. Keep symbols identical between prose, figure, and formula. The transferable feature is the diagram's analytical content, not its monochrome scan style.

Do not draw every trivial variation. Use coordinated panels for configurations whose geometry genuinely changes, and merge symmetric or algebraically identical views after showing one representative construction. The purpose is to make the derivation inspectable, not to inflate the figure count.

### Algorithm and computation

```text
由前述约束可先将搜索范围缩小为……。在该区间内，先以……定位候选区间，再以……进行加密，直至……小于给定容差。
将上述递推关系编写为 MATLAB 程序，按……顺序更新……，最终得到……。
```

### Result and interpretation

```text
计算得到……为……。其中，……时……达到……，说明……主要由……引起。
与……相比，……变化……；进一步将……加密或扰动后，结论保持不变，因此……。
```

These are compositional patterns, not fixed templates. Vary wording to fit the actual mechanism.

### Compression failure and corrected organization

The following pattern is too compressed even if every sentence is correct:

```text
对约束求导得到统一递推式。随后进行全域扫描和局部优化，得到最优值，
并通过网格加密、残差和灵敏度验证结果可靠。
```

Rewrite it by restoring the reference paper's reasoning order:

```text
先说明一个相邻单元为何满足投影相等，并推导该单元的速度关系；
再把相同几何关系推广为统一下标递推式，说明待求量和已知量；
另设“模型求解”，依次交代扫描区间、候选区间、局部加密和停止条件；
另设“求解结果”，先报告题目所求值及其发生位置；
最后在“结果分析与检验”中解释峰值形成原因，并分别给出加密、残差和敏感性证据。
```

The correction is structural, not a request to make every sentence longer.

## 5. Frame Formulas Naturally

Before a displayed formula, state the immediate modeling purpose or the relation from which it follows. Prefer concrete leads such as:

- `由定距约束可知`;
- `对弧长关系关于时间求导`;
- `在该三角形中应用余弦定理`;
- `为保证两段路径切向连续`;
- `将实体碰撞转化为分离轴上的投影比较`.

After the formula, do at least one useful thing:

- define a new symbol;
- explain its physical or geometric meaning;
- state which variable is known and which is solved;
- show the substitution that produces the next equation;
- explain how MATLAB evaluates it.

Do not repeatedly write `由数学知识可知`、`容易得到` or `显然`. Name the actual theorem, constraint, geometry, or derivative. Do not explain trivial algebra line by line when it adds no modeling meaning.

## 6. Use Transitions With Real Dependency

Words such as `首先`、`其次`、`接着`、`最后` are acceptable when they correspond to an actual dependency chain, especially in the abstract or algorithm overview. Avoid using them as empty numbering devices in every paragraph.

Prefer transitions that expose logic:

- cause: `由于`、`因此`、`由此`;
- condition: `当……时`、`在……条件下`;
- progression: `进一步`、`在此基础上`、`进而`;
- contrast: `与……不同`、`但在……处`;
- closure: `综上`、`至此`、`由上述递推关系`.

Use `本文` when stating a modeling choice, interpretation, or algorithm design. Use subjectless statements for direct mathematical consequences. Do not begin several consecutive paragraphs with `本文` or `如图所示`.

### Match the reference's lexical register

The target register is a direct Chinese contest paper, not a compressed audit report.
Prefer concrete modeling verbs such as `设`、`建立`、`由……可知`、`代入`、`联立`、
`递推`、`求解`、`得到` and `说明`. Repeat the actual object when that makes the
dependency clearer; do not replace every repeated noun with an abstract label.

Use technical terms when they carry necessary mathematical meaning, but unpack dense
noun phrases. In submission prose, avoid unexplained report-style expressions such as
`规范源`、`证据共同支持`、`控制峰值`、`执行裕量`、`保持良定`、`风险包络`
or `锁定高值区域`. For example:

```text
Too compressed: 三类证据共同支持该控制峰值，且递推保持良定。
Preferred: 网格加密后最大值的变化小于……，速度递推中的分母始终大于……，
因此没有出现运动学奇异，所得最大值在给定精度下保持不变。
```

Prefer one main clause for one mathematical action. A longer sentence is acceptable
when it expresses a single cause-and-effect relation, but do not stack the model,
algorithm, result, and verification as four comma-separated clauses. The reference may
repeat `本文`、`因此` or the modeled object more often than polished journal prose; retain
that explicitness when it improves the derivation, while avoiding mechanical repetition.

## 7. Match Chapter-Specific Density

### Abstract

Treat the abstract as a miniature solution narrative, not a compressed registry or a shortened introduction. Calibrate it separately from the body. From each supplied reference abstract, record: what the opening paragraph does; how many sentences each question receives; which sentence states the task, model transformation, execution order, result, and validation; where the principal number appears; and how the paragraph closes. Learn this role sequence, not the reference's numerical claims or possible modeling errors.

Use one compact opening of roughly one or two sentences. Name the actual research object, overall task, and shared modeling thread that connects the questions. Do not spend this paragraph on historical background, generic significance, a list of software, or a preview of every numerical answer.

Give every top-level question its own paragraph, normally beginning with `针对问题一`、`针对问题二` or an equivalent phrase. A useful paragraph usually contains two to four sentences with distinct roles:

1. state what this question must determine and name the mathematical structure used;
2. mirror the real calculation with a short action chain such as `先……，再……，进而……`, explaining what the model or algorithm actually computes;
3. introduce the objective or decisive hard constraints at the point where they govern a search or decision;
4. report the direct answer group with units and necessary scenario, then normally close with one decisive validation, trend, interpretation, or applicability statement.

These are sentence roles, not fields to force into one sentence. Split the paragraph when model, algorithm, constraints, result, and validation would otherwise become a long comma chain. Pair each model or method name with its function: say which physical, geometric, statistical, or decision relation it turns into a computable quantity. Avoid the empty substitute `建立模型并用 MATLAB 求解` and avoid algorithm-name stacks that never reveal the calculation order.

Prefer the concrete relation to an unexplained proof label. Phrases such as `由某不变量可知`、`受上述约束控制` or `根据几何性质` are too opaque in an abstract unless the same sentence names what is fixed or compared and what follows from it. Replace them with the shortest answer-bearing relation, for example `起、终点固定时，两弧总长与半径比无关，因此仅改变半径比不能缩短路线`. Keep the full derivation in the body, but do not make the abstract reader guess what the omitted argument proves.

Keep result density selective. Retain one direct answer group for each question: several positions, velocities, design values, or categories may stay together when the problem explicitly asks for them and they form one conclusion. Add one representative time, candidate, state, or trend only when it makes the requested output concrete. Include units, rounding, scenario, and boundary-versus-recommendation wording exactly as used in the body. Move full-precision residuals, several tolerances, intermediate extrema, and diagnostic lists to the results or verification section. Normally choose one validation, interpretation, or limitation for closure unless uncertainty itself is the question.

Shared geometry, data scope, or assumptions may be stated once in the opening; a question paragraph repeats only conditions that change that question's numerical answer or qualitative conclusion. When an interpretation changes the answer, name the primary interpretation before its result and dispose of the alternative in one concise conditional sentence when possible: `在……口径下……；若按……理解，则……`. This answer-changing note may accompany one ordinary feasibility check; do not merge values produced under different objectives or path definitions.

After drafting, test each paragraph together with the opening, but without consulting the body: can a reader state what was sought, how the model transformed it, what sequence was executed, what answer was obtained, and which conditions change it? If any part must be guessed, revise only that paragraph. Also test the whole abstract for rhythm: the opening should not repeat the first question, consecutive paragraphs should not all use identical sentence templates, and validation should not overwhelm the answer. Treat these as human or LLM semantic-review items; automated structure checks can verify paragraph coverage and numeric consistency but cannot reliably judge action order or list-like prose.

Respect the official word or page limit. When space is tight, compress shared methods in the opening and remove secondary diagnostics before deleting the task, action chain, direct answer, or necessary scenario from a question paragraph. Do not merge answers from different top-level questions merely to save space.

End a Chinese abstract with one keyword line. Bold both the `关键词：` label and every keyword, using the selected contest template's separator. Do not bold arbitrary result phrases throughout the abstract merely to imitate the keyword line.

### Problem analysis

Keep it shorter than the derivation. State what must be found, what earlier result it depends on, the central mathematical difficulty, and the chosen route. Do not write final formulas or stack diagnostic values here.

### Model construction

This is the most explanatory part. Introduce objects and relations in the order needed for derivation. Derive a representative component before writing a compact general recurrence. Use figures to support a geometric relation, not merely to decorate the subsection.

### Model solution

Describe the executable procedure rather than repeating the formulas. State variable bounds, branch selection, traversal order, refinement rule, optimizer, stopping rule, and failure handling as applicable.

### Result analysis

Separate `what was obtained` from `why it behaves that way`. Report the requested result first; then explain the mechanism, compare scenarios, and give validation or sensitivity. Keep full-precision diagnostics in a compact verification paragraph or appendix.

### Model evaluation

Name a specific strength with its evidence, for example analytic velocity recursion avoiding integer-time differencing. Name a specific limitation with its consequence, for example neglecting vertical tilt makes the conclusion valid only for planar motion. Do not write `理论基础扎实`、`考虑范围广` or `具有推广价值` without an object and evidence.

## 8. Figures, Tables, And Equations Must Belong To The Prose

Before a figure or table, tell the reader what relation or comparison to inspect. After it, state the conclusion supported by the visible geometry or data. Avoid consecutive figures with only captions between them.

For a geometry subsection, verify the local order `对象与条件 -> 局部构型图 -> 关系推导 -> 一般化或下一构型`. A distant overview figure does not satisfy this role when the reader must distinguish which points lie on which curve segment or which auxiliary triangle produces the equation.

For a long result table, introduce its extraction rule and units, then discuss one or two representative rows or trends. Do not narrate every cell.

## 9. Style Acceptance Checklist

When the user explicitly asks to follow a reference paper, compare the draft against the style profile on these dimensions:

1. section roles are separated at similar granularity;
2. paragraphs advance one local inference at a time;
3. representative derivations are generalized rather than skipped;
4. formulas have concrete leads and useful follow-up sentences;
5. algorithm prose mirrors the actual execution order;
6. results are followed by mechanism and validation;
7. transitions reflect real causal or conditional relations;
8. the tone is academic but not filled with unsupported self-evaluation.

Also compare the final draft directly with the recorded reference profile:

- no required section role disappeared during polishing;
- no paragraph carries more than one major evidence-chain transition;
- a recurrence is not presented before at least one representative local relation is
  explained, unless the relation is genuinely immediate;
- the algorithm order in prose matches the executed order;
- the requested answer appears before diagnostic detail;
- validation is interpreted instead of being appended as a list of small residuals.
- each complex subsection passes the reader-blockage check in Section 2;
- a model-summary block does not replace the first concrete derivation;
- no unexplained wall of formulas or chain of abstract report nouns remains.

If two or more of these checks fail, rewrite the chapter before compilation. Do not
classify a clear structural mismatch as a cosmetic warning.

## 10. Two-Pass Style Transformation

Use two passes when the user explicitly asks to match a reference paper.

**Pass 1: structural rewrite.** Build the section-role map, preserve the evidence and
numbers, split compressed paragraphs, add the representative derivation, and put
algorithm, result, and verification in their proper subsections. Do not spend time on
synonym choice yet.

**Pass 2: sentence and rhythm calibration.** Adjust formula lead-ins, causal and
conditional transitions, subject use, and paragraph length to match the reference
profile. Then compare one complete rewritten question with one complete reference
question at subsection and paragraph scale. If they only share vocabulary, repeat Pass
1; if they share organization but wording is stiff, repeat Pass 2.

During Pass 2, perform a lexical-register scan. Replace project-management or audit-like
abstractions with the concrete object, equation, numerical operation, or verification
criterion used in the model. Keep established mathematical terms such as `齐次性`、
`分离轴定理` or `运动学奇异` when they are defined and needed; the aim is clarity, not
deliberate simplification of the mathematics.

A draft that matches only vocabulary but not these reasoning structures has not matched the reference style. Correctness, evidence, and contest requirements always take precedence over stylistic imitation.
