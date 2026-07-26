---
name: 5writing
description: "数学建模竞赛论文撰写阶段，支持 Typst 和 LaTeX 双引擎及参考范文文风校准。根据建模报告、结构化结果和数据图表选择比赛模板、组织章节、撰写连贯的中文学术论证，并在正文中直接插入图表；用于新写论文、按范文重写、局部润色和结果变更后的增量修订。"
---

# 竞赛论文撰写（Typst / LaTeX）

本 skill 可在首批 claim 通过验收后提前启动，不必等待所有问题或可选高保真认证结束。它负责先建立无示例数据的可编译骨架，再按已接受证据增量写入正文；后续 claim 变化只更新受影响章节、摘要句、图表和页面。

**Typst 引擎**下可调用 typst-author skill 学习 typst 写法；**LaTeX 引擎**参考本文件末尾的"LaTeX 写作要点"小节。

## 数学建模规范参考

如需领域判断，读取 `../_references/math_modeling_norms.md` 中的“论文写作”“图表与可视化”和“非数据图工具选择”小节。该文件只作为规范知识库，论文结构仍按比赛模板和当前赛题内容决定。

## 模板族

本技能内捆绑的模板位于：

```text
templates/zh/<竞赛>/main.typ         # Typst 模板
templates/zh/<竞赛>-latex/main.tex   # LaTeX 模板
templates/en/<竞赛>/main.typ         # Typst 模板
templates/en/<竞赛>-latex/main.tex   # LaTeX 模板
```

**LaTeX 模板覆盖范围**：所有中文模板和英文模板均已提供 LaTeX 版本（`-latex` 后缀），使用 xelatex 编译。

支持的中文模板（Typst + LaTeX 双版本）：

```text
apmcm, changsanjiao, cumcm, default, diangongbei, dongsansheng,
huashubei, huaweibei, huazhongbei, mathorcup, mcm, shuweibei, stats, wuyibei
```

华为杯、华中杯、五一杯统一使用 `huaweibei`、`huazhongbei`、`wuyibei` 作为模板。

支持的英文模板（Typst + LaTeX 双版本）：

```text
apmcm, default, mcm
```

`results/claim_registry.csv` 中 accepted claim 是论文定量与定性结论的唯一规范源；`reports/RESULTS_REPORT.md`、结构化结果和 `figures/*` 只能作为同一 claim 的展开证据，发生冲突时必须退回结果阶段修正，Writer 不得自行择值。不得编造、估算或使用不同的四舍五入方式。

accepted 状态本身仍不充分。Writer 只消费同时通过根 Skill“交付质量底线”的 claim：相关附件真实字段已使用、题问完整回答、物理/量纲/基线检查通过、参数有来源与敏感性、跨产物数值一致、证据等级与措辞匹配。`FAILED_DIAGNOSTIC` 不得进入摘要、主结果图、结论或建议；若诊断反驳 claim，立即退回该 claim，不等待全局重跑。


## 工作流

### 步骤 0：确定排版引擎

**撰写论文前必须让用户选择排版引擎。** 引擎决定后续所有步骤（模板路径、章节文件扩展名、图片插入语法、编译命令），选错会导致整篇论文格式错误。

使用 AskUserQuestion 工具向用户询问："撰写论文使用哪种排版引擎？"

- 选项 1：LaTeX（xelatex 编译，数学建模竞赛主流，模板已全部就绪）— 推荐选项放第一位
- 选项 2：Typst（typst 编译，调用 typst-author skill 辅助写作）

询问前先读取 `plan.md` 的"用户偏好 → 排版引擎"字段作为预选项：
- 若 plan.md 已记录引擎选择，向用户确认："检测到之前选择的引擎是 <LaTeX/Typst>，是否沿用？"
- 若 plan.md 不存在或未记录引擎选择，直接询问用户选择。
- 若用户未明确指定或跳过，**默认使用 LaTeX**。

根据确定的引擎选择对应模板族：

- **Typst 引擎**：使用 `templates/<lang>/<竞赛>/main.typ`，调用 typst-author skill。编译命令 `typst compile main.typ`。
- **LaTeX 引擎**：使用 `templates/<lang>/<竞赛>-latex/main.tex`，xelatex 编译（中文和英文均需跑两遍解决交叉引用）。编译命令 `xelatex -interaction=nonstopmode main.tex`（执行两次）。

**后续步骤中的所有代码示例、文件扩展名、图片插入语法都必须按所选引擎选择对应版本，不要混用。**

### 步骤 1：选择语言和模板


除非用户明确要求中文，否则 MCM/ICM/COMAP 一律使用英文。所有中文竞赛名称使用中文。

模板键示例（Typst 引擎）：

```text
长三角 -> zh/changsanjiao
APMCM 英文版 -> en/apmcm
全国赛/国赛/CUMCM -> zh/cumcm
统计建模 -> zh/stats
MCM/ICM/COMAP -> en/mcm
```

模板键示例（LaTeX 引擎）：

```text
全国赛/国赛/CUMCM -> zh/cumcm-latex
MCM/ICM/COMAP -> en/mcm-latex
```

### 步骤 2：准备模板

用以下命令检查捆绑模板是否可访问（`SKILL_DIR` 为本 skill 所在目录）：

**Typst 模板**：

```bash
ls "$SKILL_DIR/templates/zh/<竞赛>/main.typ" 2>/dev/null && echo "OK" || echo "MISSING"
```

- **文件存在（OK）**：直接将 `templates/zh/<竞赛>/` 整目录复制到 `paper/`。这些模板是自包含入口文件，不依赖额外共享样式文件。
- **文件不存在（MISSING）**：说明 skill 未完整安装或在沙箱中，此时依照本 SKILL.md 步骤 3 列出的对应节文件结构，从零重建最小可编译 Typst 框架，并在 `paper/` 内注明"重建自 default 结构"。

存在匹配模板时，绝不从零开始写论文。

复制模板后立即清除所有示例题名、队伍/作者信息、示例摘要、示例数值、示例图表、占位引用和模板说明文字，再执行首次编译。未实现问题只保留真实章节标题和空结构，不得保留模板数字或虚构填充；面向匿名评审时不添加队伍名称、作者署名或说明性脚注，除非比赛模板明确要求。

**LaTeX 模板**：

```bash
ls "$SKILL_DIR/templates/zh/<竞赛>-latex/main.tex" 2>/dev/null && echo "OK" || echo "MISSING"
```

- **文件存在（OK）**：将 `templates/zh/<竞赛>-latex/` 整目录复制到 `paper/`。
- **文件不存在（MISSING）**：说明 skill 未完整安装或在沙箱中，此时依照本 SKILL.md 步骤 3 列出的对应节文件结构，从零重建最小可编译 LaTeX 框架，并在 `paper/` 内注明"重建自 default-latex 结构"。


### 步骤 3：构建图表规划

在写正文各节之前，根据 `results/claim_registry.csv`、`results/figure_manifest.csv`、`figures/*.pdf`、`reports/RESULTS_REPORT.md`，以及 `reports/DRAWIO_REPORT.md`（如果存在）构建图表规划：

进入规划的图片必须有 accepted manifest row，并已在论文最终显示尺寸下检查 PDF/PNG 渲染。阻断项包括中文缺字或 `####`、重复字符、单位/图例/色条缺失、文字或箭头遮挡、标签裁切、尺度误导，以及图内数值与 claim registry 冲突。发现图问题只退回该图生成器并在修复后复查受影响页面，不得要求重跑模型。

```text
图表规划
fig_roadmap.pdf -> 引言/问题重述
fig_algorithm_q4.pdf -> 含循环或分支的局部算法求解处
MATLAB 参数化模型示意图 -> 对应问题的代表性推导之前或之后
fig_pipeline.pdf -> 数据预处理/方法节
结果图 -> 对应的结果节
```

全篇默认只在前部安排一张总体技术路线图。局部流程图不是逐问标配；仅当算法含有真实循环、判定分支、失败回退、多初值筛选或停止条件，且读图能显著降低理解成本时才插入，并放在相应“模型求解”或算法小节。单向递推用公式和文字，数值结论用真实数据图，参数化几何示意图由 MATLAB 生成并放在首次使用局部坐标、尺寸、接触、边界或路径关系的位置；不要用 DrawIO 图替代真实模型几何。

图片路径相对于写入该图片的文件：写在 `paper/main.typ` 或 `paper/main.tex` 中通常用 `../figures/xxx.pdf`，写在 `paper/sections/*.typ` 或 `paper/sections/*.tex` 中通常用 `../../figures/xxx.pdf`。

**Typst 引擎**图片插入：

```typst
#figure(
  image("../../figures/fig_q1_error_dist.pdf", width: 85%),
  caption: [问题一预测误差分布],
)
```

**LaTeX 引擎**图片插入：

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{../../figures/fig_q1_error_dist.pdf}
  \caption{问题一预测误差分布}
  \label{fig:q1_error}
\end{figure}
```

英文论文使用英文图注。

### 步骤 3.5：参考范文文风校准

若用户提供范文或明确要求接近某种中文论文语言，撰写正文前必须读取 `../../references/chinese-paper-language-style.md`，并从范文中抽取摘要、问题分析、一个完整模型小节、求解算法、结果分析和模型评价作为校准样本。只学习其章节颗粒度、句群推进、公式衔接、代表性推导和结果解释顺序，不复制题目内容、数值、公式、错误结论或空泛自评。

在 Writer handoff 或模型决策日志中记录简洁的文风画像：叙述主语、句长、过渡方式、公式前导、公式后解释、示例到一般递推的展开方式、结果报告顺序和评价语气。先重写一个有公式、有结果分析的实质性小节作为校准稿；逐项对照文风画像修正后，再扩展到其余章节。不得只替换词语而保持原有的压缩式论证结构。

校准稿必须按 `模型建立/代表性推导 -> 一般模型或模型汇总 -> 模型求解 -> 求解结果 -> 结果分析与检验` 建立内部结构映射。改写已有论文时，不得把原有多个有效小节合并成一个“更精炼”的小节；复杂问题的角色颗粒度只能保留或细化。先完成结构改写，再做句式和连接词校准。若校准稿仍把公式、搜索、主结果和多项残差压入同一段，即使语句通顺也判为校准失败。

图一类“模型汇总”应学习其组织方式而非照抄公式：在代表性推导完成后，用一个带语义分组的方程块集中列出真正送入计算的路径/几何、状态、递推、目标、约束和边界关系。方程块前说明汇总目的，块后说明待求变量、已知量、索引范围和求解顺序。若内容超过一页或字体必须缩小才能放下，应拆成两组或移出次要恒等式。

若范文用局部构型图解释曲线、刚体和圆心之间的几何关系，应学习其“图直接服务于推导”的做法。计算姿态和真实尺寸用 MATLAB 绘制；只承担符号推导的图可用 LaTeX/TikZ 生成教材式矢量线稿。正文先指出图中要观察的对象关系，再利用图中的半径、弦、辅助三角形、投影或相切关系推导公式。图中的带下标关键点、连接点、圆心和运动方向必须与正文符号一致；不能只放整条路径总览，也不能把直观二维关系改成难以正对观察的透视图。

参考图的构型数量和面板划分不是论文配图清单。Writer 应按相邻段落的论证任务选择图型：局部公式需要正视解析构型，数值结论需要真实数据图，三变量关系才使用真实 3D 图。若一个问题同时需要机理、结果和验证，可以用多视图协同表达；若这些面板不共享同一状态或结论，则应分别放置，不得为了模仿参考图而生硬组合。

扩展到全文前，将校准稿与范文的一个完整问题章节作直接对照，并逐项回答：章节角色是否同样清楚；是否先讲一个具体对象再推广；公式后是否说明下一步求什么；算法是否按真实执行顺序展开；结果是否先回答题问再解释机理；检验是否独立成段。任意两项不满足时先返工校准稿，不进入全文改写。

句式校准时采用直接的竞赛论文语域，优先使用“设、建立、由……可知、代入、联立、递推、求解、得到、说明”等具体动作。不得把正文写成结果审计报告：将“证据共同支持、控制峰值、无执行裕量、保持良定、锁定高值区域”等高密度抽象表达，改写为具体对象、数值变化、判定阈值及其结论。保留确有必要且已解释的数学术语，不为模仿范文而降低模型严谨性。

### 步骤 4：撰写各节

撰写前先读取 `../../references/paper-structure-first-prize-writing.md`；中文论文同时读取 `../../references/chinese-paper-language-style.md`。建立以下结构合同：

1. 全文只设一个一级“问题分析”大节，按题目实际问数设置“问题一分析”“问题二分析”等独立二级小节。每问依次交代输入输出、数学或物理本质、与前问依赖、关键难点、可信备选方法、选择理由和预期证据；不得把所有问题压成一段总体思路。
2. 全文只设一个一级“模型假设”大节。共同假设与各问特有假设可在节内分组或编号，但不得拆成多个一级假设章节，也不得在后文临时引入未登记的关键假设。
3. 模型选择须与题目材料、附件、数据规模、机理和验证能力匹配。比较真实可行的备选并说明取舍，不得为了“高阶”或“创新”机械堆叠模型名称。
4. 每个经验修正因子、主观权重、拟合常数或代表参数必须给出来源/推导、适用范围和敏感性；题目附件提供真实材料、几何或场景数据时不得用代表性范围替代。
5. 推荐强度不得超过证据等级。`PAPER_USABLE` 只能写成给定场景和模型适用域内的结果，不得写成“施工安全”“已认证”“满足规范”“实验验证”或“全局最优”，除非对应强证据确已通过。
6. 对会改变核心答案的题意歧义，正文必须先说明比较对象、固定端点、可移动边界和参数自由度，再给出主解释的选择依据。若另一合理口径会得到相反结论，应以独立小段、注记或敏感性小节说明该口径及其求解或证明；不要求机械复制整套模型，但不得静默省略。不同数值场景必须使用各自的 `scenario_key`，写作时转述为自然的场景名称，不能混合结果。
7. 对含递推、分段路径、碰撞判定或连续优化的复杂问题，至少显式区分模型建立、一般模型/模型汇总、模型求解、求解结果、结果分析与检验五类角色。标题可按题意改写，但不得把这五类内容压进一个小节或一个长段。先以一个相邻单元、一个路径段、一个候选碰撞对或一个局部事件完成代表性推导，再推广到全链或全域。
8. 全文原则上只配置一张总体技术路线图，用于表达跨问题依赖。局部算法流程图按必要性配置：保留条件是存在循环、分支、回退或停止判定，并且与已有公式、几何图或数据图不重复。局部图放在对应算法小节，正文在图前说明读图目的、图后解释分支如何产生输出。

正文采用“问题目的与物理图像 → 建模理由 → 代表性对象推导 → 一般递推或分类模型 → 求解方法 → 结果解释 → 验证”的叙事顺序。机制复杂时，将“模型建立”“模型汇总”“模型求解”“求解结果”“结果分析”分开，不得把公式、算法、结果和验证压缩在同一段。公式前点明实际依据，公式后说明未知量、物理意义或下一步求解；图表前交代读图目的，图表后指出支持的结论。

可以使用“首先、其次、接着、最后”概括真实的依赖链，尤其适用于摘要和算法总述；不得把它们当作每段固定编号。优先使用“由于—因此”“当—则”“在此基础上—进而”“与……不同”等体现因果、条件和对比的连接。对递推模型，先以一个代表性板凳、节点、区域或时刻完整推导，再推广到统一下标表达，避免直接抛出总公式。

将内部证据语言转换为竞赛论文语言：`claim` 写成“结论”或“指标”，`accepted` 写成“经检验”，`scenario_key` 写成具体场景名称，`PAPER_USABLE` 写成相应模型与适用范围内的计算结果。正文不得出现“冻结”“门禁”“工作流”“重跑”“Agent”“PAPER_USABLE”“FAILED_DIAGNOSTIC”等项目过程词。避免“利用数学知识”“理论基础扎实”“结果合理”“符合客观事实”“效果较好”“具有一定意义”等没有证据对象的自我评价。

下列章节文件名只表示模板常见布局。若模板未预留独立分析文件，应新增分析文件，或在问题重述文件中另设一级“问题分析”节；不得因沿用模板而省略逐问分析结构。

**以下章节文件名按所选引擎使用 `.typ`（Typst）或 `.tex`（LaTeX）扩展名。** 例如 Typst 引擎用 `1_restatement.typ`，LaTeX 引擎用 `1_restatement.tex`。文件名主体保持一致。

中文数学建模通用模板各节文件（`changsanjiao`、`diangongbei`、`huashubei`、`mathorcup`、`wuyibei`）：

```text
1_restatement.typ  - 问题重述与分析
2_analysis.typ     - 数据理解与总体思路
3_assumptions.typ  - 模型假设
4_symbols.typ      - 符号说明
5_problem1.typ     - 问题一建模与求解
6_problem2.typ     - 问题二建模与求解
7_problem3.typ     - 问题三建模与求解
...         - 根据题目调整问题数量  
8_evaluation.typ   - 灵敏度分析、模型评价与推广
A_code.typ         - 附录代码
```

国赛/华中杯/华为杯（`cumcm`、`huazhongbei`、`huaweibei`）按以下章节结构：

```text
1_restatement.typ
2_analysis.typ
3_assumptions.typ
4_symbols.typ
5_problem1.typ
6_problem2.typ
7_problem3.typ
...        - 根据题目调整问题数量
8_sensitivity.typ
9_evaluation.typ
A_code.typ
```

东三省模板（`dongsansheng`）额外使用单独摘要文件：

```text
abstract.typ
1_restatement.typ
2_analysis.typ
3_assumptions.typ
4_symbols.typ
5_problem1.typ
6_problem2.typ
7_problem3.typ
...       - 根据题目调整问题数量
8_evaluation.typ
A_code.typ
```

数维杯模板（`shuweibei`）保留原 LaTeX 的示例入口命名：

```text
Abstract.typ
Introduction.typ
2_analysis.typ
3_assumptions.typ
4_symbols.typ
5_problem1.typ
6_problem2.typ
7_problem3.typ
...      - 根据题目调整问题数量
8_evaluation.typ
Appendices1.typ
A_code.typ
```

中文默认模板（`default`）：

```text
1_restatement.typ
2_assumptions.typ
3_symbols.typ
4_problem1.typ
5_problem2.typ
6_problem3.typ
...      - 根据题目调整问题数量
7_sensitivity.typ
8_evaluation.typ
A_code.typ
```

中文统计建模各节文件：

```text
1_introduction.typ
2_method.typ
3_data.typ
4_analysis.typ
5_results.typ
6_conclusion.typ
A_code.typ
```

英文 MCM/APMCM 各节文件（`en/mcm`、`en/apmcm`、`zh/mcm`、`zh/apmcm`）：

```text
1_introduction.typ
2_assumptions.typ
3_model_design.typ
4_solution.typ
5_sensitivity.typ
6_strengths_weaknesses.typ
7_conclusions.typ
A_code.typ
```

**LaTeX 模板章节文件**（对应 `-latex` 后缀模板，结构与 Typst 版本一一对应）：

国赛 LaTeX 模板（`zh/cumcm-latex`，对应 `cumcm` Typst 版本）：

```text
1_restatement.tex
2_analysis.tex
3_assumptions.tex
4_symbols.tex
5_problem1.tex
6_problem2.tex
7_problem3.tex
8_sensitivity.tex
9_evaluation.tex
A_code.tex
```

MCM/ICM LaTeX 模板（`en/mcm-latex`）：

```text
1_introduction.tex
2_assumptions.tex
3_model_design.tex
4_solution.tex
5_sensitivity.tex
6_strengths_weaknesses.tex
7_conclusions.tex
A_code.tex
```

其余 LaTeX 模板（`changsanjiao-latex`、`default-latex`、`huashubei-latex`、`mathorcup-latex`、`wuyibei-latex`、`huazhongbei-latex`、`huaweibei-latex`、`diangongbei-latex`、`dongsansheng-latex`、`shuweibei-latex`、`stats-latex`、`apmcm-latex`、`mcm-latex`、`en/apmcm-latex`、`en/default-latex`）的章节文件命名与上述结构类似，以 `main.tex` 中 `\input{}` 引用的文件名为准。

英文默认模板（`en/default`）：

```text
1_introduction.typ
2_assumptions.typ
3_notations.typ
4_model.typ
5_sensitivity.typ
6_evaluation.typ
7_conclusions.typ
A_code.typ
```

**正文写作应使用连贯的学术段落。最终论文不得出现任何内部路径、代码/报告文件名、Agent 或工作流术语、重跑/门禁/调试过程、模板示例或临时状态；正文只描述可复现方法与学术证据。**

### 步骤 5：参考文献

只使用真实存在的参考文献。文件名按引擎选择：Typst 用 `paper/references.typ`，LaTeX 用 `paper/references.tex`。

**Typst 引擎**：

```typst
#set enum(numbering: "[1]")
#enum[
  作者. 题名[J]. 期刊名, 年份, 卷(期): 页码.
  Author. "Title." Journal or Conference, year.
]
```

正文上标引用：`相关研究已用于物流网络优化#super("[1]")。`

**LaTeX 引擎**：

```latex
\begin{thebibliography}{99}
  \bibitem{ref1} 作者. 题名[J]. 期刊名, 年份, 卷(期): 页码.
  \bibitem{ref2} Author. "Title." Journal, year.
\end{thebibliography}
```

正文引用用 `\cite{ref1}` 或 `\cite{ref1,ref2}`。

### 步骤 6：最后撰写摘要或总结

在所有章节和 claim registry 冻结后撰写中文摘要或英文 Summary Sheet。中文摘要必须使用连贯段落，结构为：

1. 一段简短总述，说明总体任务、共享框架和核心思路；
2. 每个顶层子问题各占一个独立段落，建议以“针对问题一……”“针对问题二……”起笔；
3. 可选一段总结主要结论、鲁棒性、局限或建议。

每个问题段必须依次交代：实际使用的模型名称或数学结构、求解算法或数值方法、决定答案的目标函数或关键约束、一个最能回答题问的主要结果（定量问题含单位与必要场景）、一项关键验证或敏感性结论，以及结果含义。不得只写“建立模型并用 MATLAB 求解”，也不得在没有实际使用时堆叠算法名。其余全精度残差、搜索容差和中间指标放在正文或附录，不在摘要中堆叠。定性问题报告经验证的类别结论及证据类型，不得为满足格式捏造数值。若不同合理口径导致不同答案，使用“在……口径下……；若……则……”明确分开，不得把不同场景的数值写成同一结论。摘要不得使用项目符号、表格、复杂公式、引文、内部文件名或“效果较好”等空泛表述。

中文摘要末尾设置“关键词”行时，将“关键词：”标签和全部关键词统一加粗；关键词之间使用模板规定的空格、分号或 `\quad` 分隔，不混入正文句号。

## LaTeX 写作要点

以下要点供 **LaTeX 引擎**使用。Typst 引擎请调用 typst-author skill 获取语法帮助。

### 编译命令

```bash
# 中文模板（xelatex，跑两遍解决交叉引用）
xelatex main.tex && xelatex main.tex

# 英文模板（xelatex，同样跑两遍）
xelatex main.tex && xelatex main.tex
```

### 文档结构

```latex
\documentclass[a4paper,12pt]{article}   % 英文
\documentclass[a4paper,12pt]{ctexart}   % 中文

\usepackage{...}   % 宏包加载
\usepackage{graphicx}   % 图片支持
\usepackage{booktabs}   % 三线表
\usepackage{amsmath,amssymb}   % 数学公式
\usepackage{hyperref}   % 交叉引用（需两遍编译）
```

### 图表插入

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{../../figures/fig_q1.pdf}
  \caption{图注}
  \label{fig:q1}
\end{figure}

% 三线表
\begin{table}[htbp]
  \centering
  \caption{表注}
  \begin{tabular}{ccc}
    \toprule
    \textbf{列1} & \textbf{列2} & \textbf{列3} \\
    \midrule
    数据 & 数据 & 数据 \\
    \bottomrule
  \end{tabular}
\end{table}
```

### 交叉引用

```latex
如图~\ref{fig:q1}所示，...   % 图片引用
式~(\ref{eq:objective}) 给出...   % 公式引用
见第~\pageref{fig:q1} 页   % 页码引用
```

### 数学公式

```latex
行内公式：$f(x) = \sum_{i=1}^n \theta_i \phi_i(x)$

行间公式：
\begin{equation}
  \mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2
  \label{eq:objective}
\end{equation}
```

### 章节和强调

```latex
\section{问题重述}
\subsection{问题背景}
\textbf{问题一：} xxx   % 对应 Typst 的 #strong
```
