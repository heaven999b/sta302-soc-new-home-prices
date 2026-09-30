# 面积 × Census division：美国新建住宅售价（SOC 2025）

STA302H1（Methods of Data Analysis I），多伦多大学，2026 秋季学期期末项目 —— 三个候选方案之一（方案一）。

> English version: [README.md](README.md)。完整的中文研究设计见 [design/research_design.md](design/research_design.md)；R 与 Python 数值核对见 [verification/R_vs_Python.md](verification/R_vs_Python.md)。

## 研究问题

在 2025 年售出的美国新建独栋住宅中，控制地块面积、卧室数、全卫和半卫数、层数、车库、地基、壁炉、外墙材料、采暖燃料、排污方式、是否属于业主协会（HOA）、是否为限龄社区、签约时的建设阶段和签约月份之后，完工面积每增加 100 平方英尺，售价增加多少？这个“面积的边际价格”在 9 个 Census division 之间是否不同？

回答问题靠的是：8 个“面积 × division”交互系数及“它们全为 0”的 partial F / HC3 Wald 检验，以及每个 division 的面积斜率和 95% 置信区间。

## 数据

- **来源**：U.S. Census Bureau, *Survey of Construction (SOC) microdata*，2025 年度文件（主分析）和 2024 年度文件（独立复现），<https://www.census.gov/construction/chars/microdata.html>，免费、免注册。变量说明：[`data/original/socmicro_info.pdf`](data/original/socmicro_info.pdf)。
- **收集方式**：全国概率抽样（约 1/50），从建筑许可中抽样，并在不需要许可的地区做实地排查；访谈建造商或业主，记录开工、出售、完工日期和 40 多项特征。特征数据的收集由 HUD 资助。
- **分析单位**：一套为出售而建、2025 年签约的新建独栋住宅。原始 25,246 行 → 清洗后 **6,185** 行 → 训练 4,330 / 测试 1,855。
- **响应变量**：售价（千美元，含地块；Census 在每个 division 内做了顶码和底码处理）。
- **预测变量（17 个）**：数值 3 个（面积、地块面积、签约月份），类别 14 个（division 加 13 个结构或市场特征）。Part 1 模型共 52 个系数。

## 主要结果（训练集，n = 4,330）

| | Part 1（原始售价，不修正） | Part 2 最终（log 售价 ~ log 面积，BIC 选择） |
|---|---:|---:|
| 系数个数 | 52 | 46 |
| R² / 调整 R² | 0.713 / 0.710 | 0.756 / 0.753 |
| 残差偏度 / 超额峰度 | 2.04 / 18.0 | 0.48 / 2.52 |
| 交互 partial F 的 p | 1.2e-57 | 2.4e-9 |
| 交互 HC3 Wald 的 p | 7.5e-24 | 1.6e-10 |
| 面积 + 交互的 ΔR² | 0.074 | 0.076 |
| 最大 Cook's D | 0.18 | 0.022 |

各 division 的面积效应：

| 地区 | n | Part 1 斜率（千美元 / 100 sqft），95% CI | Part 2 弹性，95% CI | 面积 +10% → 售价 |
|---|---:|---|---|---:|
| South Atlantic（参照） | 1,308 | 11.83 (10.60, 13.07) | 0.679 (0.630, 0.727) | +6.7% |
| New England | 39 | 19.26 (15.05, 23.47) | 0.632 (0.448, 0.815) | +6.2% |
| Middle Atlantic | 119 | 24.56 (22.32, 26.79) | 0.735 (0.633, 0.837) | +7.3% |
| East North Central | 510 | 6.85 (5.19, 8.51) | 0.525 (0.462, 0.589) | +5.1% |
| West North Central | 313 | 10.57 (8.32, 12.82) | 0.535 (0.462, 0.608) | +5.2% |
| East South Central | 344 | 13.78 (11.88, 15.68) | 0.702 (0.628, 0.775) | +6.9% |
| West South Central | 850 | 9.27 (7.71, 10.82) | 0.734 (0.677, 0.791) | +7.2% |
| Mountain | 473 | 14.60 (13.03, 16.17) | 0.584 (0.523, 0.645) | +5.7% |
| Pacific | 374 | 21.70 (19.47, 23.92) | 0.727 (0.650, 0.804) | +7.2% |

- **中西部对比（1 自由度）**：中西部（ENC + WNC）的面积弹性比其他 7 个 division 低 0.152；HC3 p = 3.2e-10；按 division 聚类、用 t(8) 参照 p = 5.9e-4。
- **稳健性**：逐个加入 7 个替代交互、7 个同时加入（HC3 p = 1.3e-7）、去掉顶码售价、用抽样权重、改用 AIC 模型，交互都显著。单个 division 的差异不够稳定（见研究设计第 8 节）。
- **独立复现**：同一最终设定用于 2024 年另一批 6,118 套房子：R² = 0.752，交互 HC3 p = 1.2e-17，格局相同（ENC、WNC、Mountain 弹性最低）。
- **数值核对**：R 结果与 Python 探针逐项核对 281 项，261 项一致（最大相对差 3.3e-10），其余差异都已查明原因。

## 文件说明

```
.
├── Part1_Code.Rmd / .html       Part 1 提交用代码（英文叙述）：读原始数据 → 逐步清洗 → 构造变量 → 写出 soc_clean.csv →
│                                只取训练集 → 变量汇总表 → 交互图 → 初步模型 → 系数表 → 完整残差分析（不修正）
├── Part2_Analysis.Rmd / .html   Part 2 工作稿（中文叙述，代码和图为英文），只用训练集：Box-Cox、log 与 log–log 比较、
│                                VIF/GVIF、影响点、partial F、AIC/BIC 后向选择、最终模型、HC3 与聚类 SE、混杂检查、
│                                敏感性、中西部对比、2024 复现；最后是 eval = FALSE 的测试集验证块
├── data/
│   ├── original/                soc25.csv（25,246 × 61）、soc24.csv（复现用）、socmicro_info.pdf（官方变量说明）
│   ├── cleaned/                 soc_clean.csv（Part 1 写出，6,185 行，含 split 和抽样权重 weight）
│   │                            soc2024_clean.csv（Part 2 写出，6,118 行）
│   └── split_ids.csv            固定的 70/30 划分（id, split）
├── figures/                     fig1_interaction、fig2_conditions、fig3_residuals、fig4_resid_by_categorical（proposal 用）；
│                                part2_*.png（Part 2 诊断图）
├── proposal/                    Proposal_Part1_EN.md / .html / .pdf（+ proposal.css）、Proposal_Part1_中文对照.md
├── design/research_design.md    中文研究设计全文（数字均为 R 核对后的版本，更正处已标出）
├── verification/R_vs_Python.md  R 与 Python 数值核对
├── probe/                       探索阶段的 Python 探针（只作溯源，已被 R 版取代）
└── docs/                        TODO.md、DECISIONS.md、CHANGELOG.md
```

说明：
- `Part1_Code.Rmd` 的叙述用英文，因为它要提交给评分者；`Part2_Analysis.Rmd` 是组内工作稿，叙述用中文。以后如果要提交 Part 2 代码，需要把叙述改成英文。
- `proposal/` 下 md 的图片路径是 `../figures/...`，在 GitHub 上和本地打开 HTML 都能显示。

## 如何运行（RStudio）

1. 克隆或下载整个仓库，保持目录结构不变（如果本地路径含中文在 Windows 上出问题，可以换成英文路径）。
2. 第一次运行前安装包（MASS 随 R 自带）：
   ```r
   install.packages(c("car", "sandwich", "lmtest", "rmarkdown", "knitr"))
   ```
3. 在 RStudio 中打开 `Part1_Code.Rmd`，点 **Knit**。它会读 `data/original/soc25.csv`，逐步打印清洗行数（25,246 → … → 6,185），写出 `data/cleaned/soc_clean.csv`，在 `figures/` 生成 4 张 proposal 图。约 5 秒。
4. **再** knit `Part2_Analysis.Rmd`（它读 Part 1 写出的 `soc_clean.csv`，所以必须先跑 Part 1）。约 10 秒。
5. 命令行（在 C locale 下 Part 2 的中文表标题会乱码，所以先设 UTF-8）：
   ```bash
   export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
   Rscript -e 'rmarkdown::render("Part1_Code.Rmd")'
   Rscript -e 'rmarkdown::render("Part2_Analysis.Rmd")'
   ```
6. 修改 proposal 后重新生成 HTML 和 PDF：
   ```bash
   cd proposal
   pandoc Proposal_Part1_EN.md -s --css proposal.css -o Proposal_Part1_EN.html
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer \
     --print-to-pdf="$PWD/Proposal_Part1_EN.pdf" "file://$PWD/Proposal_Part1_EN.html"
   ```
   改完后请逐页检查 PDF（图 4 占大半页，前后文字变多时可能换页）。

## 测试集政策

- 划分在**项目开始时一次性固定并存档**：Python 探针用 `numpy.random.default_rng(302).permutation(6185)`，前 4,330 行为训练集，存为 `data/split_ids.csv`。R 代码读这个文件，不重新抽样（R 的 `set.seed(302)` 会得到不同的划分）。1,855 个测试集 ID 与探针存档的完全相同。生成代码（只读 `soc_analysis.csv` 的 id 列）：

  ```python
  import numpy as np, pandas as pd
  df = pd.read_csv("soc_analysis.csv", usecols=["id"])
  idx = np.random.default_rng(302).permutation(len(df)); ntr = int(round(0.7 * len(df)))   # 4330
  split = np.array(["test"] * len(df), dtype=object); split[idx[:ntr]] = "train"
  pd.DataFrame({"id": df["id"], "split": split}).to_csv("split_ids.csv", index=False)
  ```
- 两个 Rmd 中的所有表、图、模型都只用训练集；Part 2 读入清洗后数据后立即丢弃测试集行。
- `Part2_Analysis.Rmd` 最后的“测试集最终验证”代码块是 `eval = FALSE`，**只在 Part 2 模型定稿后运行一次**，之后不再根据测试集结果修改模型。
- 披露：划分之前，探针曾在全部 2025 年样本上看过各 division 的价格和面积中位数（纯描述，没有拟合模型），所以测试集不是 100% 盲。

## Proposal 各节词数

统计规则：按空白分词；小节标题、图标题、表标题计入；表格单元格不计入；Contributions、Bibliography、附录不计入（课程规定）。

| 小节 | 词数 | 上限 | 余量 |
|---|---:|---:|---:|
| Introduction | 385 | 400 | 15 |
| Data description（含表 1、图 1 标题） | 278 | 300 | 22 |
| Ethics discussion | 167 | 200 | 33 |
| Preliminary results（含表 2、图 2–4 标题） | 356 | 400 | 44 |
| Plan（含表 3 标题；甘特图单元格不计） | 257 | 300 | 43 |

课程允许每节超出不多于 15 词，但目前每节都在上限以内。组员修改后请重新数一遍。

## 提交清单（Part 1，截止 11 月 5 日 23:59；NQA 延期到 11 月 8 日 23:59，两个 dropbox 不要都交）

只由**一位组员**提交全部内容：

- [ ] **Part 0 Teamwork Agreement**：全员讨论、签字，存为 PDF。
- [ ] **Proposal PDF**：填好组号、组员与分工、甘特图负责人，替换 Module 3 术语后，按上面第 6 步重新生成 `proposal/Proposal_Part1_EN.pdf`。
- [ ] **Rmd**：`Part1_Code.Rmd`（Part 1 只需要这一个；Part 2 的 Rmd 不在本次提交范围）。
- [ ] **CSV 上传到 UofT OneDrive**，保持文件夹结构，评分者才能直接 knit：
  - `data/original/soc25.csv`（原始数据）
  - `data/cleaned/soc_clean.csv`（清洗后数据）
  - `data/split_ids.csv`（Rmd 需要它来取训练集，**必须一起上传**）
  - 建议同时上传 `Part1_Code.Rmd` 和 `data/original/socmicro_info.pdf`，方便评分者对照。
- [ ] OneDrive 共享权限设为 **“Anyone in UofT with the link can access”**，用无痕窗口或组员账号测试链接能打开。
- [ ] 在 Quercus 提交页的 **submission comment** 里贴 OneDrive 链接。

## 当前状态与待办

已完成：Part 1 代码、图和清洗后数据；训练集上的 Part 2 分析；R 与 Python 数值核对；英文 proposal 草稿（各节都在词数上限内）。

待办（详见 [docs/TODO.md](docs/TODO.md)）：

1. **组员信息**：proposal 标题下的组号 `[##]`、Contributions、甘特图负责人；两个 Rmd 开头的 `author`。
2. **Module 3 术语**：伦理部分是按通用框架（可信度、所有权与来源、隐私与去识别、合乎伦理的使用）写的，需要换成 Module 3 的原词（评分要求可信度和伦理收集各至少一个模块概念）。中文对照中标了【TODO】。
3. **读原文核对文献**：Rosen（1974）在 Crossref/OpenAlex 都没有摘要，目前按公认内容保守概括，**必须读原文**；另两篇的概括依据摘要，文中“新增面积主要是结构”“监管严格地区斜率更陡”是我们的推论，读原文时确认没有被写成论文原话。
4. **“用于编制官方统计”一句**：`socmicro_info.pdf` 没有逐字出现，请在 https://www.census.gov/construction/soc 核对；如要提 Title 13 保密条款，也需先核对。
5. **甘特图日期**：目前按 Part 1 截止后的周次排，需对照 Quercus 上 Part 2、海报、录播的实际截止日期调整。
6. 数据集引用写的是 `U.S. Census Bureau. (2026)`（2025 年度文件于 2026 年 6 月发布），如能查到确切发布日期可补上。

## 需要披露的问题（写进 Part 2 / 最终报告的局限部分）

1. **测试集不是 100% 盲**：见上面“测试集政策”。
2. **顶码/底码**：Census 在每个 division 内把售价前 3%、后 1% 截到限值（训练集 7.1% 的售价被改动）；面积前后 1% 被截；地块 > 87,120 sqft 被截（训练集 93 套）。Part 1 保留这些值；Part 2 去掉被改动的售价后结论不变（HC3 p = 1.6e-10）。
3. **类别合并**：SEWER“其他”（6 套）并入 septic；FUEL“燃油”（1 套）并入 other；WAL1“混凝土砌块”并入 other。proposal 中已写成“septic or other”等。
4. **误差独立性**：公开文件没有楼盘或建造商 ID，地理只到 division，同一楼盘内的相关无法检验。加入 division 后残差 ICC ≈ 0 是机械结果，不能当作独立性的证据。
5. **稳健性的边界**：交互整体在所有设定下都显著；但 7 个替代交互全部同时加入时，ENC − SA 缩小到 −0.089（HC3 p = 0.077），Pacific − SA 在各设定下不稳。主结论放在“交互整体显著”和 1 自由度中西部对比上。
6. **只有 9 个聚类**：按 division 的聚类稳健 SE 不可靠；只对 1 自由度对比使用 t(8) 参照。
7. **研究者自由度**：Part 1 设定事先定好没有改过；Part 2 比较了 log–线性与 log–log（按 BIC 和残差曲率选，不是看交互结果选的）；混杂检查共 9 个设定。
8. **效应大小**：Part 2 中交互项自身的 ΔR² 只有 0.003；New England 训练样本只有 39 套。
9. **Part 2 已预先做过**：Part 2 的全部分析已在训练集上跑过；proposal 的 Plan 按课程要求写成计划，没有引用 Part 2 的结果。测试集验证块从未运行。
10. 结论是关联，不是因果；不加抽样权重时结论只描述样本（加权后结论不变）。

## 参考文献

- Glaeser, E. L., Gyourko, J., & Saks, R. (2005). Why is Manhattan so expensive? Regulation and the rise in housing prices. *The Journal of Law and Economics, 48*(2), 331–369. https://doi.org/10.1086/429979
- Gyourko, J., & Saiz, A. (2006). Construction costs and the supply of housing structure. *Journal of Regional Science, 46*(4), 661–680. https://doi.org/10.1111/j.1467-9787.2006.00472.x
- Rosen, S. (1974). Hedonic prices and implicit markets: Product differentiation in pure competition. *Journal of Political Economy, 82*(1), 34–55. https://doi.org/10.1086/260169
- U.S. Census Bureau. (2026). *Survey of Construction (SOC) microdata: 2025 annual file* [Data set]. https://www.census.gov/construction/chars/microdata.html
- U.S. Census Bureau. (n.d.). *Survey of Construction microdata files: General information and variable descriptions*. https://www.census.gov/construction/chars/pdf/socmicro_info.pdf
