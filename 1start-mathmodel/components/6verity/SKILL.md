---
name: 6verity
description: "数学建模竞赛最终验证和验收阶段，支持 Typst 和 LaTeX 双引擎。用于论文写完后检查章节数量、标题顺序、图表引用、数值一致性、占位符、内部文件泄露、参考文献、代码可复现性、编译和提交就绪状态。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# 验证和验收（Typst / LaTeX）

本 skill 同时承担增量验收和最终验收。工作过程中只检查发生变化的任务、产物或论文页面；交付前仍必须执行一次完整的代码可复现性检查，以及一次全论文编译、逐页栅格化和视觉验收。它不重新建模、不生成新结果、不代替写作阶段重写论文。

## 数学建模规范参考

如需领域判断，读取 `../_references/math_modeling_norms.md` 中的"论文验收与一致性"小节。该文件只是规范知识库，不是固定执行流程；具体目录、入口文件、结果文件和图表目录由当前项目结构决定。

## 阶段边界

- 本阶段负责：结构验收、文本质量门禁、图表引用检查、结果一致性检查、Typst/LaTeX 编译检查、PDF 视觉检查、提交清单。
- 本阶段不负责：重新设计模型、重新跑大规模实验、重新组织整篇论文。
- 发现硬错误时，优先做小范围修复；如果需要回到前序阶段，写入 `reports/VERIFY_REPORT.md` 并标记为未通过。

每个失败项必须记录 `failure_scope`、`owner_task`、`artifact`、`failed_check`、`required_fix`、`rerun_command`。修复后只重跑失败检查和受影响页面；只有 accepted 输出、共享输入、单位、控制方程或导出接口变化时，才按 `workflow_edges.csv` 的 blocking 后继扩大范围。不得用“保险起见”要求全流程重跑。

## 输入

由模型先根据当前工作区判断项目布局，再把实际路径传给检查脚本。常见输入包括但不限于：

1. 论文入口文件：`main.typ`（Typst）或 `main.tex`（LaTeX）。
2. 正文章节目录或若干正文文件（`.typ` 或 `.tex`）。
3. 参考文献文件（`references.typ` 或 `references.tex`）。
4. 前序阶段的分析、建模、结果、图示报告。
5. 图表目录
6. 可复现代码目录。
7. 编译后的 PDF，或可由入口文件编译得到的输出 PDF。

不要假设论文目录一定叫 `paper/`，也不要假设结果文件一定在项目根。若项目使用不同命名，按实际结构传参并在 `reports/VERIFY_REPORT.md` 中说明。

## 工作流程


### Step 1: 运行文本质量门禁

优先运行本 skill 的脚本。脚本按入口文件扩展名自动选择检查逻辑（`.typ` → Typst 检查，`.tex` → LaTeX 检查）：

```bash
set -o pipefail
mkdir -p _tmp
SCRIPT_PATH="<按当前 skill 实际位置确定>/scripts/writing_check.sh"
bash "$SCRIPT_PATH" \
  --paper-dir "$PAPER_DIR" \
  --main "$MAIN_FILE" \
  --sections-dir "$SECTIONS_DIR" \
  --references "$REFERENCES_FILE" \
  --figures-dir "$FIGURES_DIR" \
  --results-file "$RESULTS_FILE" \
  --problem-analysis "$PROBLEM_ANALYSIS_FILE" \
  --all-results "$ALL_RESULTS_FILE" \
  | tee _tmp/writing_check.log
```

如果本 skill 被复制到其他目录，使用实际脚本路径。可以先运行 `bash <script> --help` 查看参数。不要把脚本路径、论文目录或文件名写死在验收逻辑中。

脚本只扫描文本，不生成论文，也不编译 PDF。它的 `FAIL` 属于硬错误，必须修复后重跑。

### Step 2: 章节数量和标题顺序

**Typst 引擎**检查：

- 入口 `.typ` 文件中 `#include("...")` 的数量是否与实际正文结构匹配。
- include 顺序是否符合文件名前缀顺序，例如 `1_...`, `2_...`, `3_...`。
- 每个 section 是否有明确一级标题（`= 标题`，等号后有空格）。
- 标题顺序是否符合所选论文类型。

**LaTeX 引擎**检查：

- 入口 `.tex` 文件中 `\input{...}` 或 `\include{...}` 的数量是否与实际正文结构匹配。
- 章节顺序是否符合文件名前缀顺序。
- 每个 section 是否有 `\section{}` 或对应级别标题。

通用检查（两种引擎）：

- 章节文件是否缺失、重复引用、未被引用。
- 如果题目不是三问，不强行要求三段问题章节；按 `ANALYSIS_MODELING_REPORT.md` 的子问题数量核对。
- 读取 `../../references/paper-structure-first-prize-writing.md`，并使用实际问题 ID 运行根 Skill 的结构校验器：

```bash
python <root-skill>/scripts/validate_paper_structure.py \
  --paper-dir "$PAPER_DIR" \
  --questions Q1 Q2 Q3 \
  --language zh \
  --engine auto
```

将 `Q1 Q2 Q3` 替换为题目的真实顶层问题 ID。中文论文必须同时满足：一个一级“问题分析”节且每问有独立二级分析小节；摘要中每问有独立自然段；全篇恰有一个一级“模型假设”节。共同与各问特有假设只能在该节内部编号或分组。

### Step 3: 图表和章节匹配

**Typst 引擎**检查：

- 图表目录中的 PDF 是否在正文中被引用。
- `#figure(image(...), caption: [...])` 的图片是否真实存在。图片路径必须相对于 `.typ` 文件。
- 数据图是否放在对应结果/分析章节，非数据流程图是否放在方法/总体思路章节。

**LaTeX 引擎**检查：

- `\includegraphics{}` 引用的图片文件是否真实存在。路径相对于 `.tex` 文件。
- `\caption{}` 是否存在。
- 数据图是否放在对应结果/分析章节。

通用检查（两种引擎）：

- 连续图表之间是否有足够解释文字。
- caption 是否过长、过泛或与图意不一致。
- 图表编号、正文引用和章节语义是否一致。

不要生成 `*_typst_includes.typ` 或 `*_latex_includes.tex`；图表必须直接嵌在对应 section 中。

### Step 4: 写作质量和泄露检查

检查并修复：

- `TODO`、`PLACEHOLDER`、`待补充`、`待续写`、`示例数据` 等占位符。
- 论文正文出现内部工作流文件名、临时目录名、代码目录名或结果 JSON 路径。
- 过多列表式写作（Typst 中大量 `#list`、`enum`，LaTeX 中大量 `\begin{itemize}`、`\begin{enumerate}`）。
- 段落反复以"如图""由图""图 X 展示了"开头。
- 图表后没有解释、公式后没有变量含义、结论只报数不解释。
- 问题分析是否逐问说明输入输出、任务本质、依赖、难点、备选方法、选择理由与预期证据，而非复述题面或跳到最终公式。
- 摘要是否逐问分段，并在每段给出实际方法、接受结果或结果类型、验证结论和含义。
- 模型选择是否有可信备选、适用条件、优缺点和验证方案；机械堆叠模型名称应退回写作或建模阶段。

### Step 5: 数值和结果一致性

检查：

- 论文中的关键数值必须来自当前工作流声明的结果记录或结果 JSON。
- 目标函数值、误差指标、排名、权重、阈值、灵敏度结果不得与结果记录冲突。
- 如果存在汇总结果 JSON，抽取关键指标并确认论文正文中有对应结果。
- 公式中的符号应在符号说明或正文首次出现处解释。
- 实际附件提供的材料参数、几何、字段或场景是否被忠实使用；不得以“代表值/典型范围”替代而不说明且不验证。
- 经验修正因子、权重、拟合常数是否有来源或推导、适用范围和敏感性结果。
- 同一 claim 的数值、单位、舍入、场景键、候选 ID 和结果类型是否在 CSV、registry、表格、图内标注、caption、摘要、正文、结论和建议中完全一致。
- `FAILED_DIAGNOSTIC` 是否被错误用于主图、摘要、结论或推荐。
- 推荐措辞是否超过证据等级；`PAPER_USABLE` 不得被描述为施工安全、规范认证、实验验证或普适最优。

发现数值冲突时，不要自行发明新结果；应回到结果记录或代码输出修正论文。

### Step 6: 引用和模板规范

检查：

- 参考文献文件是否存在，或模板是否采用了其他真实参考文献机制。
- 正文引用标记（Typst 的 `@label`/`#super`，LaTeX 的 `\cite{}`）是否能对应到真实参考文献。
- 中文论文 caption、表题、摘要语言保持中文；英文论文保持英文。
- 选定的模板入口是否保留所选比赛模板的必要封面、摘要、编号、页眉页脚或提交格式。
- 不要把模板结构误删成普通空白文档。


### Step 7: 编译

**Typst 编译**：

```bash
command -v typst >/dev/null 2>&1 && typst compile "$MAIN_FILE" "$OUTPUT_PDF"
```

**LaTeX 编译**：

```bash
command -v xelatex >/dev/null 2>&1 && xelatex -interaction=nonstopmode "$MAIN_FILE" && xelatex -interaction=nonstopmode "$MAIN_FILE"
```

xelatex 需跑两遍解决目录和交叉引用。

编译失败必须修复语法、路径、图片引用或模板问题后重跑。编译通过后确认输出 PDF 非空。

### Step 8: PDF 视觉检查

如果模型有视觉能力，必须把编译后的 PDF 每页导出为 PNG 并逐页查看。这个步骤用于发现纯文本扫描和编译器无法发现的版式错误。

优先使用系统已有工具导出页面 PNG；不要为了视觉检查引入沉重依赖。可选命令示例：

```bash
mkdir -p _tmp/pdf-pages
if command -v pdftoppm >/dev/null 2>&1; then
  pdftoppm -png -r 160 "$OUTPUT_PDF" _tmp/pdf-pages/page
elif command -v mutool >/dev/null 2>&1; then
  mutool draw -r 160 -o _tmp/pdf-pages/page-%03d.png "$OUTPUT_PDF"
elif command -v magick >/dev/null 2>&1; then
  magick -density 160 "$OUTPUT_PDF" _tmp/pdf-pages/page-%03d.png
else
  echo "No PDF rasterizer found; record visual check as not run."
fi
```

导出后逐页检查：

- 页面是否空白、缺页、页数异常或页面尺寸异常。
- 标题、摘要、正文、页眉页脚、页码是否被裁切或位置明显错误。
- 表格是否超出页边距，单元格文字是否重叠、溢出、被截断。
- 图片、图题、表题、公式、编号是否与正文重叠。
- 公式是否越界，长公式是否压到页边距或下一段文字。
- 列表、段落、脚注、参考文献是否出现异常大空白、重叠或孤立残行。
- 中文/英文/数学符号字体是否明显缺字、乱码或 fallback 异常。
- 图内是否出现 `####`、乱码、重复字符、标签被箭头遮挡、图例/色条/单位缺失，或在最终论文尺寸下无法阅读。
- 封面、摘要页、目录、附录等模板关键页面是否保留比赛要求的视觉结构。

如果是模板转换或已有参考 PDF 的项目，还应将不同引擎的 PDF 都逐页导出 PNG，按页对比版式差异；页数或页面尺寸不一致必须记录为硬错误或明确说明原因。

若当前执行环境确实没有任何视觉能力，最终结论必须为 `FAIL` 并明确记录阻塞原因；不得以 PDF 非空、页数或页面尺寸检查替代逐页视觉验收。局部增量检查可以只查看受影响页面，但最终交付必须查看全部页面和全部正文引用图。

### Step 9: 写验收报告

创建 `reports/VERIFY_REPORT.md`：

```markdown
# 验证和验收报告

## 结论
PASS / FAIL

## 检查项
| 检查项 | 结果 | 说明 |
| --- | --- | --- |

## 章节结构

## 图表引用

## 数值一致性

## 文本质量门禁

## 编译

## PDF 视觉检查

## 仍需处理的问题
```

只有当硬错误都修复、文本门禁通过、核心图表都引用、数值一致、编译成功、全页视觉检查通过且交付质量底线全部满足时，才写 `PASS`。编译或视觉检查无法执行时只能写 `FAIL`。

## 硬错误标准

以下问题必须判定 `FAIL`：

- 缺少选定的论文入口文件（`main.typ` 或 `main.tex`）或核心正文。
- 论文入口引用的章节文件不存在。
- Typst 入口缺少 `#include`；LaTeX 入口缺少 `\input`/`\include`。
- 正文章节缺少一级标题（Typst `= ` 后缺空格，LaTeX `\section{}` 缺失）。
- 章节顺序明显错误或重复。
- 问题分析未按真实顶层问题逐问设置独立小节。
- 中文摘要未按真实顶层问题逐问分段，或遗漏任一问题。
- 全文不存在、存在多个一级“模型假设”节，或各问假设被拆成分散的一级章节。
- 正文仍有占位符。
- 正文泄露内部工作流文件名。
- 引用的图片不存在。
- 关键数值与结果记录冲突。
- 相关附件有真实数据却使用未经说明和验证的代表值、典型范围或虚构替代。
- 经验修正因子、权重、拟合常数缺少来源/推导、适用范围或敏感性证据。
- 同一 claim 在结果、表格、图、摘要、正文、结论或建议中数值、单位、场景或舍入不一致。
- `FAILED_DIAGNOSTIC` 被用作主证据，或推荐措辞超过证据等级。
- 正文包含内部路径、文件名、Agent/工作流、重跑、门禁、调试或模板示例语言。
- 编译器可用但论文编译失败。
- 编译后的 PDF 为空、缺页、页数异常或页面尺寸异常且无法解释。
- 视觉检查发现正文、表格、图片、公式、页眉页脚、页码等关键元素重叠、裁切、越界、乱码、`####`、重复字、箭头遮字或最终尺寸不可读。

## 警告标准

以下问题可判定为 `WARN`，但应尽量修复：

- 未引用的备用图片。
- 某章节过短或明显不均衡。
- caption 偏长。
- 参考文献偏少。
- 图表后解释文字不足。
- 代码完整复现耗时过长，只做了轻量检查。
