# 决定记录

## 已做的决定

| # | 决定 | 理由 |
|---|---|---|
| 1 | 研究问题：面积 × Census division 对新建独栋住宅售价的影响 | 三组探针约 29 个候选中合格的 3 个之一；概率抽样的微观数据，一套房一行，有 2024 年独立样本可复现 |
| 2 | 训练/测试划分沿用 Python 探针的 `default_rng(302)` 划分，存为 `data/split_ids.csv`，R 读取而不重新抽样 | R 的 `set.seed(302)` 会得到不同的划分；沿用原划分才能保证测试集是项目开始时就留出、没有被看过的那一批 |
| 3 | Part 1 用原始售价，不做任何变换或修正 | 课程要求 Part 1 只诊断不修正；原始尺度的违反（右偏、重尾、喇叭形）正好为 Part 2 的 Box-Cox 提供动机 |
| 4 | Part 1 保留 17 个预测变量；排除 LOTV、PVALU、FSLPR、FINC、ACS | LOTV/PVALU/FSLPR 与售价有机械关系或泄漏；FINC 缺失太多；ACS 几乎没有变异 |
| 5 | 类别合并：WAL1 混凝土砌块 → other；FUEL 燃油 → other；SEWER 其他 → septic 组（称为 septic or other） | 这些水平样本极少（1–14 套）；与探针保持一致以便核对 |
| 6 | Part 2 选 log 而不是 Box-Cox 给出的 λ ≈ −0.42 | log 可按百分比解释；λ = −0.5 作为对照，交互同样显著 |
| 7 | Part 2 选 log–log（对面积也取 log） | log–线性模型在面积方向仍有明显凹形（平方项 p = 2.8e-50）；log–log 的 BIC 更低；按诊断和 BIC 选，不是看交互结果选的 |
| 8 | 变量选择用 BIC 后向，AIC 作对照；强制保留面积、division、交互和地块面积 | 前三项直接回答研究问题；地块面积按 hedonic 理论是价格的一部分；BIC 模型更简约，adj R² 只比 AIC 模型低约 0.001，交互结论相同 |
| 9 | 不删除任何影响点 | 最终模型最大 Cook's D 只有 0.022，没有点超过 F(0.5) 阈值 |
| 10 | 主结论表述为“交互整体显著 + 1 自由度中西部对比”，单个 division 的差异只作描述 | 7 个替代交互全部加入时 ENC − SA 的 HC3 p = 0.077；Pacific − SA 不稳；9 个聚类只能支持 1 自由度的聚类稳健检验 |
| 11 | 聚类稳健检验同时报告 z 参照和 t(8) 参照 | statsmodels 默认 z；只有 9 个聚类时 t(G−1) 更合理 |
| 12 | 在 division × fullbath 检查中，杠杆值 = 1 的点对 HC3 meat 的贡献记为 0 | 该点残差恒为 0，标准 HC3 得到 0/0；这样处理与 Python 结果一致，其余点不受影响 |
| 13 | `Part1_Code.Rmd` 用英文叙述，`Part2_Analysis.Rmd` 用中文叙述 | Part 1 要交给评分者；Part 2 是组内工作稿 |
| 14 | Part 1 只用 base R 和 car；Part 2 另用 MASS、sandwich、lmtest；图全部用 base graphics | 课程环境要求；不依赖 tidyverse/ggplot2 |
| 15 | 数值以 R 为准 | R 与 Python 逐项核对，唯一的实质差异（聚类 SE 的 K 计数）是 statsmodels 的问题 |
| 16 | proposal 的 Plan 按课程要求写成计划，不引用已算出的 Part 2 结果 | Part 1 不应展示修正后的模型 |

## 待用户（小组）决定的事项

1. **是否选这个方案**作为最终项目（另两个候选：NTD 公交客运量、IPEDS 教师薪酬）。
2. **伦理部分是否提 Title 13**：需要先在 census.gov 核对。
3. **Part 2 最终报告是否改用 AIC 模型**：两者结论相同，AIC 模型保留了 stage（p = 0.00085）。
4. **是否在报告中报告 λ = −0.5 版本**作为主要稳健性检查。
5. **如何披露“测试集不是 100% 盲”**：建议在 Part 2 的方法部分用一句话说明。
6. **Part 2 叙述何时翻译成英文**。
