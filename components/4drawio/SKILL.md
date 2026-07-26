---
name: 4drawio
description: "数学建模非数据型图示绘制阶段。根据 ANALYSIS_MODELING_REPORT.md、RESULTS_REPORT.md 和已有 figures/ 生成技术路线图、子问题求解流程图、模型结构图、数据处理流程图等 DrawIO 图，并导出论文可引用 PDF。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# DrawIO 非数据图示绘制

本 skill 承接 `3coding-visual`。它只负责论文中的**非数据型图示**，例如技术路线图、求解流程图、模型结构图、数据处理流程图、变量关系图、指标体系图等。

## 数学建模规范参考

如需领域判断，读取 `../_references/math_modeling_norms.md` 中的“图表与可视化”和“非数据图工具选择”小节。该文件只作为规范知识库，不要求为了凑数量生成额外图示。

## 阶段边界

- 本阶段负责：DrawIO 源文件、非数据图 PDF、图示生成记录。
- 本阶段不负责：折线图、柱状图、散点图、热力图、箱线图、雷达图等数据图。这些由 `3coding-visual` 生成。
- 本阶段不重跑模型、不修改 `code/`，不改写 `reports/RESULTS_REPORT.md` 的数值结论。

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

竞赛论文默认只生成一张 `fig_roadmap` 总体技术路线图，放在论文前部“问题分析”的总体思路处。不要按问题数量机械生成 `fig_flow_q1`、`fig_flow_q2` 等图。局部流程图保留必须同时满足两个条件：至少存在一个真实循环、判断分支、失败回退、多初值筛选或停止判定；且流程图比公式、几何图或数据图更能降低理解成本。否则不生成，也无需逐问说明“为何省略”。

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
- 参数化几何、局部坐标、尺寸链、接触或边界条件示意图必须由 MATLAB 生成，不得用 DrawIO 仿画。
- 论文阶段引用的非数据图都应有 `.drawio` 源文件和 PDF，或者在 `reports/DRAWIO_REPORT.md` 说明导出失败。
