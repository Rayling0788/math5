---
name: 4drawio
description: "数学建模非数据型图示阶段。根据题目、结构化方案、真实代码、运行结果和已有 figures/，生成总体/逐题技术路线图以及提出方法的模型结构或机理图；支持 DrawIO 可编辑图，也支持按数模工坊原规则输出 image2 提示词、等待用户回传并验收图片。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# 非数据图示绘制

本 skill 承接 `3coding-visual`。它只负责论文中的**非数据型图示**，例如技术路线图、求解流程图、模型结构图、数据处理流程图、变量关系图、指标体系图等。除 DrawIO 外，它还保留数模工坊原程序的 image2 图示分支。需要该分支时，完整读取 [references/image2-figure-workflow.md](references/image2-figure-workflow.md)，不得凭主观印象决定哪些图交给 image2。

## 数学建模规范参考

如需领域判断，读取 `../_references/math_modeling_norms.md` 中的“图表与可视化”和“非数据图工具选择”小节。该文件只作为规范知识库，不要求为了凑数量生成额外图示。

## 阶段边界

- 本阶段负责：DrawIO 源文件与导出图，或 image2 提示词、用户回传图及其验收记录。
- 本阶段不负责：折线图、柱状图、散点图、热力图、箱线图、雷达图等数据图。这些由 `3coding-visual` 生成。
- 本阶段不重跑模型、不修改 `code/`，不改写 `reports/RESULTS_REPORT.md` 的数值结论。
- image2 图不是数值证据，不得代替由真实数据或模型参数生成的结果图、验证图、响应面、物理场或精确参数化几何图。

## 必须产出

在当前工作目录创建或更新：

```text
figures/
  fig_roadmap.drawio
  fig_roadmap.pdf
  fig_algorithm_q4.drawio   # 仅在必要时存在
  fig_algorithm_q4.pdf
  ...
reports/DRAWIO_REPORT.md
```

采用 image2 分支时，另创建与目标图片同名的提示词文件，例如 `figures/flowchart.prompt.txt`、`figures/algo_problem1.prompt.txt`、`figures/schematic_problem2.prompt.txt`。图片尚未由用户提供时，在报告中标记 `WAITING_FOR_USER_IMAGE`，不得伪造 PNG 占位，也不得写成“已生成”。

纯 DrawIO 路线仍可按论文论证需要精简局部流程图。采用数模工坊 image2 分支时，不使用这条主观精简规则，而是严格执行原程序的固定触发集合：总体技术路线图、每个结构化子问题的技术路线图、以及仅对 `stage == proposed` 的“提出方法”任务生成模型结构/机理示意图。用户明确要求时，才额外生成机理、模型结构或场景示意图。

读取这些文件的目的不是提取数据作图，而是理解论文方法、章节结构、子问题关系和已有图表，避免重复。

## 工作流程

### Step 1: 盘点已有图表和需求

先读取以下文件（存在则读取）：`reports/ANALYSIS_MODELING_REPORT.md`、`reports/RESULTS_REPORT.md`、`figures/` 目录列表。

然后从前序文档提取非数据图需求，输出一个清单：

```text
DRAWIO PLAN CHECKLIST:
[ ] fig_roadmap      技术路线图，放在问题重述/绪论
[ ] fig_algorithm    仅在必要算法处绘制的循环/分支流程图
[ ] fig_pipeline     数据处理流程图
[ ] fig_model        模型结构/变量关系图
```

若采用 image2 分支，清单必须改按以下原程序条件生成，不得使用“复杂”“重要”“感觉适合”等无来源判断：

```text
[ ] flowchart              总体技术路线图；固定候选
[ ] algo_problemN          每个结构化子问题的技术路线图
[ ] schematic_problemN     仅当该任务 stage == proposed
[ ] schematic_custom_N     仅当用户明确提出额外机理/结构/场景图
```

总体图和逐题图先综合“结构化方案 + 真实求解代码”提炼有序模块；LLM 总结失败时才按方案启发式回退。提出方法图按“论文主题 → 当前提出方法任务 → 全局核心方法/基线/创新主张 → 真实实现代码 → 真实运行结果摘要 → 已有方法章节”的顺序构造可信上下文，代码与章节冲突时以代码为准。

清单不是固定模板，要根据题目实际删减或增补。不要为了凑图生成无意义图示。

每张局部算法流程图只覆盖与该算法直接相关的初始化、更新、判定、回退、停止和输出，不重复该问全部模型内容。节点顺序必须与 MATLAB 实际执行顺序和论文“模型求解”小节一致。简单单向递推、已有响应面或结果图能够说明的计算，不再另配流程图。

先按论证任务选择图型，不以 DrawIO 能否绘制作为选择依据：

| 论证任务 | 首选表达 | 工具 | 论文位置 |
| --- | --- | --- | --- |
| 跨问题输入、依赖和最终决策 | 总体技术路线图 | DrawIO | “问题分析”的总体思路之后 |
| 迭代、分支、回退、多初值和停止条件 | 局部算法流程图 | DrawIO | 对应“模型求解/算法”小节 |
| 单向递推或闭式计算 | 公式与连贯文字 | LaTeX/Typst | 模型建立或推导处 |
| 几何、机构、接触、尺寸、剖面和边界 | 参数化构型图 | MATLAB；纯符号关系可用 TikZ | 相关公式首次推导处 |
| 趋势、比较、响应面、可行域、物理场和验证 | 真实数据图 | MATLAB | 结果或检验小节 |

image2 不取代上表中的真实数据图和参数化几何图。它只承接数模工坊原程序明确列出的总体技术路线、逐题技术路线、`proposed` 方法结构/机理图和用户显式要求的机理/模型结构/场景示意图。

参考流程图只学习“初始化—更新—判定—循环—结束”的竖向视觉语法和清晰的回路走向，不照搬其算法节点、图数量或装饰。局部算法图不得重复总体路线，也不得承担几何示意或数值结论的角色。

### Step 2: 判定图类型

常见图示选择：

| 图类型 | 文件名建议 | 适用场景 |
| --- | --- | --- |
| 技术路线图 | `fig_roadmap` | 展示整体解题路线、章节逻辑、方法串联 |
| 局部算法流程图 | `fig_algorithm_q4` | 展示迭代、判断、回退、停止和输出 |
| 数据处理流程图 | `fig_pipeline` | 展示数据清洗、特征构造、建模输入 |
| 模型结构图 | `fig_model` | 展示模块关系、变量关系、模型层次 |
| 指标体系图 | `fig_index_system` | 展示目标层、准则层、指标层 |
| 决策树/规则图 | `fig_decision_tree` | 展示分类规则、设备选择、策略分支 |

不要用 DrawIO 画这些图：

- 结果对比柱状图
- 预测误差曲线
- 灵敏度曲线
- 相关性热力图
- 分布图和箱线图

### Step 3: 生成 DrawIO 源文件

每张图一个 `.drawio` 文件，放在 `figures/`。

DrawIO 内容要求：

- 文字语言与论文语言一致。
- 节点文字短，必要时双行，不堆长句。
- 同类节点样式统一。
- 箭头方向清晰，避免交叉。
- 图中不写大段解释，解释留给论文正文。
- 不使用装饰性阴影和过度渐变。
- 使用克制的低饱和配色区分输入、模型、约束、算法、结果和验证；同一语义在总体图和逐问图中保持同色。
- 逐问图优先采用单向主链，分支在判定点展开并及时汇合；避免回头箭头和大面积空白。

生成大 XML 时，分段写入，避免截断。示例：

```bash
mkdir -p figures
cat << 'XMLEOF' > figures/fig_roadmap.drawio
<mxfile>
  <diagram name="Page-1">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- nodes and edges -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
XMLEOF
```

### Step 3B: 生成 image2 提示词并等待回传

触发 image2 分支时，按 [references/image2-figure-workflow.md](references/image2-figure-workflow.md) 生成完整提示词，保存为 `figures/<目标文件名>.prompt.txt`，并把提示词直接交给用户。明确要求用户：使用 image2 生成后，将原始 PNG 返回或放入约定的 `figures/` 路径。

在用户返回图片前：

- 保留提示词和预期文件名；
- 在 `reports/DRAWIO_REPORT.md` 标记 `WAITING_FOR_USER_IMAGE`；
- 可继续不依赖该图的建模、计算和写作工作；
- 不得把待生成图插入论文，不得声称图示验收完成。

用户返回图片后，检查科学关系、文字/公式、标签、布局、重叠、裁切和最终版面可读性。学位论文按 8.0/10 门槛验收，最多组织两轮生成；不足 8 分时输出仅针对已发现问题的返修提示词，并再次要求用户生成后提供。

### Step 4: 导出 PDF

优先用可用的 DrawIO 命令导出 PDF：

```bash
DRAWIO_BIN="$(command -v drawio 2>/dev/null || command -v draw.io 2>/dev/null || command -v draw.io.exe 2>/dev/null || true)"
if [ -n "$DRAWIO_BIN" ]; then
  "$DRAWIO_BIN" --export --format pdf --crop --output figures/fig_roadmap.pdf figures/fig_roadmap.drawio
else
  echo "DrawIO command not found; keep .drawio source and record export failure."
fi
```

同时导出矢量 PDF 和用于验收的 PNG。若 DrawIO CLI 无法直接控制 300 dpi，先导出高分辨率 PNG 或由 PDF 栅格化为至少 300 dpi。若无法导出，保留 `.drawio`，在 `reports/DRAWIO_REPORT.md` 记录失败原因和建议命令。

### Step 5: 自检和修复

每张图必须检查：

- `.drawio` 文件非空。
- 若导出成功，`.pdf` 文件非空。
- 节点没有明显重叠。
- 箭头不穿过核心节点。
- 字号、颜色、边框风格一致。
- 文件名和图意一致。
- 没有与 `3coding-visual` 的数据图重复。
- 总体图能看出问题间依赖，逐问图能看出该问独有的模型、约束、算法和验证。
- 在论文最终显示宽度下，中文、节点、箭头和分支标签均可读且无裁切。
- image2 图的模块、数据流、分支、融合、反馈、输入、输出和验证面板均能追溯到方案、代码、结果或方法章节；不存在臆造模块、公式和结论。
- image2 图没有图号或正文式 caption；图号和 caption 由论文排版层添加。

发现问题要修 `.drawio` 并重新导出，不要只在报告里解释。

### Step 6: 写生成记录

创建 `reports/DRAWIO_REPORT.md`，至少包含：

```markdown
# DrawIO 图示生成报告

## 图示清单
| 文件 | 类型 | 来源依据 | 用途 | 状态 |
| --- | --- | --- | --- | --- |

## 未生成图示及原因

## 导出与自检记录

## 给论文阶段的嵌入建议
```

嵌入建议只说明每张图适合放入哪个章节和建议 caption，不生成 `*_typst_includes.typ`。最终的图表插入代码（Typst 的 `#figure(image(...), caption: [...])` 或 LaTeX 的 `\begin{figure}...\end{figure}`）由 `5writing` 根据论文结构和所选引擎决定。

## 质量要求

- 图示服务论文论证，不为装饰而画。
- 每张图必须能对应到`reports/ANALYSIS_MODELING_REPORT.md` 中的真实方法。
- 数据型图表不得在本阶段重复生成。
- 承担精确几何或数值证据的参数化几何、局部坐标、尺寸链、接触和边界条件图必须由 MATLAB 从真实参数生成；image2 只可表达已触发的概念性方法结构/机理关系，不能替代这类证据图。
- DrawIO 图应有 `.drawio` 源文件和 PDF；image2 图应有 `.prompt.txt`、用户提供的原始 PNG 和验收记录。缺少用户回传图时保持 `WAITING_FOR_USER_IMAGE`，不能进入论文。
