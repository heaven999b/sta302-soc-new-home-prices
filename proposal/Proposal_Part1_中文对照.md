# Proposal Part 1 中英对照（方案一：SOC 新房售价）

> 英文原稿：`Proposal_Part1_EN.md`（提交用 PDF：`Proposal_Part1_EN.pdf`）。本文件逐段对照翻译，供组员阅读；**提交以英文稿为准**。
> 标注说明：【需读原文核对】文献概括需要读原文确认；【TODO：换成 Module 3 术语】伦理部分待替换术语；【待办】需要组员补充的信息。

**标题**：Does Extra Floor Space Cost the Same Everywhere? Floor Area, Census Division and the Sale Price of New U.S. Homes

**中文标题**：多出来的面积在哪里都一样贵吗？——面积、Census division 与美国新建住宅售价

## 分工（Contributions，不计字数）

> Haiwen Yi — [contribution]; [Member 2] — [contribution]; [Member 3] — [contribution]; [Member 4] — [contribution].

Haiwen Yi —— [贡献]；[组员 2] —— [贡献]；[组员 3] —— [贡献]；[组员 4] —— [贡献]。

> 【待办】提交前填入每位组员的姓名和具体贡献。

## 引言（Introduction，上限 400 词）

> **Research question.** Among newly built, detached single-family homes sold in the United States in 2025, how much does an extra 100 square feet of finished floor area add to the sale price (in $1000s, including the lot), and does this marginal price of floor area differ across the nine Census divisions, holding constant lot size, bedrooms, full and half bathrooms, stories, garage, foundation, fireplaces, exterior wall material, heating fuel, sewer type, homeowners' association and age-restricted status, construction stage at sale, and month of sale?

**研究问题。** 在 2025 年售出的美国新建独栋住宅中，完工居住面积每增加 100 平方英尺，售价（千美元，含地块）增加多少？在控制地块面积、卧室数、全卫和半卫数、层数、车库、地基、壁炉、外墙材料、采暖燃料、排污方式、是否属于业主协会（HOA）、是否为限龄社区、签约时的建设阶段和签约月份之后，这个“面积的边际价格”在 9 个 Census division 之间是否不同？

> **Why a linear model.** Comparing average price per square foot across divisions is simpler, but it mixes floor area with everything that comes with bigger homes, such as extra bathrooms, garages and basements. Multiple linear regression holds these features fixed and, through a floor area × division interaction, lets the floor-area slope differ by division. The answer comes from the eight interaction coefficients and the partial F test of whether they are all zero, and from each division's floor-area slope with its 95% confidence interval.

**为什么用线性模型。** 直接比较各地区的平均每平方英尺价格更简单，但它把面积和“大房子附带的东西”（更多卫生间、更大的车库和地下室）混在一起。多元线性回归可以把这些特征固定住，并通过“面积 × division”交互项让面积斜率随地区变化。回答研究问题靠的是：8 个交互系数及“它们是否全为 0”的 partial F 检验，以及每个 division 的面积斜率和 95% 置信区间。

> **Literature.** Rosen (1974) showed that the price of a differentiated good can be written as a function of its characteristics; regressing price on characteristics recovers their implicit prices, which are market equilibrium outcomes and so may differ between markets. Our floor-area slope is the implicit price of space, and the interaction asks whether it is equal across divisions. Gyourko and Saiz (2006) found that construction costs make up most of the price of new houses in most markets and differ substantially across U.S. markets with local wages, unionization, topography and regulation. Because extra floor area is mostly extra structure, this predicts that the price of space varies by region. Glaeser, Gyourko and Saks (2005) found Manhattan prices more than twice supply costs and argued that land-use regulation also constrains supply in several other U.S. markets, where rising demand raises prices rather than the number of homes; this suggests steeper price–area slopes in tightly regulated regions. None of these three studies uses a national sample of individual new homes to compare the adjusted price of floor area across all nine divisions; that is our contribution.

**文献。** Rosen（1974）指出，差异化商品的价格可以写成其各项特征的函数；把价格对特征做回归，可以得到各特征的隐含价格，而这些隐含价格是市场均衡的结果，因此不同市场之间可以不同。我们模型中的面积斜率就是“空间的隐含价格”，交互项检验的是它在各 division 是否相同。Gyourko 和 Saiz（2006）发现，在大多数市场中建造成本占新房价格的大部分，而且美国各住房市场的建造成本差异很大，与当地工资、工会化程度、地形和监管有关。由于新增面积主要是新增的建筑结构，这预示着空间的价格会因地区而不同。Glaeser、Gyourko 和 Saks（2005）发现曼哈顿房价是供给成本的两倍以上，并认为土地使用监管在美国其他若干市场同样限制了供给，那里需求上升带来的是更高的房价而不是更多的住房；这意味着在监管严格的地区，价格对面积的斜率会更陡。这三篇研究都没有用全国性的单套新房样本，去比较 9 个 division 之间经调整后的面积价格；这正是我们要补的空白。

> 【需读原文核对】Rosen（1974）在 Crossref 和 OpenAlex 上都没有摘要，上面按该文公认的核心内容（hedonic 价格函数、隐含价格是均衡结果）做了保守概括，请读原文确认措辞。Gyourko & Saiz（2006）和 Glaeser et al.（2005）的描述依据的是 OpenAlex/Crossref 上的官方摘要；其中“新增面积主要是新增的建筑结构”“监管严格地区斜率更陡”是**我们的推论**，不是论文原话，写法上已用 this predicts / this suggests 区分。

> **Who benefits.** Home builders choosing house sizes by region, housing agencies and municipalities weighing minimum-size rules or starter-home policies, and appraisers and buyers who need a region-specific value for extra space.

**谁会受益。** 在各地区决定户型面积的建造商；权衡最小面积规定或“入门房”政策的住房机构和地方政府；需要按地区估计“多出来的面积值多少钱”的估价师和购房者。

## 数据描述（Data description，上限 300 词）

> The data are the 2025 microdata file of the U.S. Census Bureau's Survey of Construction (U.S. Census Bureau, 2026). This national survey samples about 1 in 50 new houses from building permits and canvassed areas, and interviews builders or owners about dates and over 40 characteristics. It produces official statistics on new residential construction and sales; HUD funds the collection of the characteristics (U.S. Census Bureau, n.d.).

数据来自美国人口普查局 Survey of Construction（SOC）2025 年微观数据文件（U.S. Census Bureau, 2026）。这项全国调查从建筑许可和实地排查地区中抽取约 1/50 的新房，访谈建造商或业主，记录各项日期和 40 多项特征。它用于编制新建住宅建设和销售的官方统计；这些特征数据的收集由 HUD 资助（U.S. Census Bureau, n.d.）。

> 【需核对】“1/50 抽样”“访谈建造商或业主”“40 多项特征”“HUD 资助”都出自 `data/original/socmicro_info.pdf`；“用于编制官方统计”这一句在该 PDF 中没有逐字出现，可在 https://www.census.gov/construction/soc 的调查说明页核对后保留。

> We kept homes built for sale, detached and outside condominiums, with a 2025 sales contract and all model variables reported (6,185 of 25,246 records). All summaries and models use a random 70% training set (n = 4,330).

我们保留了：为出售而建、独栋且不属于共管公寓、2025 年签约、模型所需变量全部有报告的住宅（25,246 条记录中的 6,185 条）。所有汇总和模型只用随机抽取的 70% 训练集（n = 4,330）。

> The response, sale price, is continuous (nearest $100; mean $527k, median $433k, SD $307k). It is strongly right-skewed with high outliers, and 7.1% of prices were top- or bottom-coded by the Census Bureau, so we expect non-normal, unequal-variance errors. Each row is a different house from a probability sample, so independence is plausible, although homes in the same subdivision cannot be identified.

响应变量售价是连续变量（精确到 100 美元；均值 52.7 万、中位数 43.3 万、标准差 30.7 万美元）。它明显右偏、有很高的离群值，且 7.1% 的售价被人口普查局做了顶码或底码处理，所以预计误差不服从正态、方差不齐。每一行是概率样本中的一套不同的房子，因此独立性是合理的，但同一楼盘内的房子无法识别。

（表格内容与英文稿相同，见下；表格单元格不计字数）

| Variable | Type (reference level) | Training-set summary |
|:--------------------|:----------------|:----------------------------------------|
| Sale price, $1000s (response) | Numerical | Mean 527, SD 307, min 210, median 433, max 3,300; skewness 3.04 |
| Floor area, 100 sq ft | Numerical | Mean 25.4, SD 9.9, min 7.1, median 23.0, max 85.1; skewness 1.67 |
| Lot size, 1000 sq ft | Numerical | Mean 14.1, SD 16.6, min 2.0, median 8.7, max 87.1; skewness 3.10 |
| Month of sale (1–12) | Numerical | Mean 6.3, SD 3.4, min 1, median 6, max 12; skewness 0.09 |
| Census division | 9 levels (South Atlantic) | South Atlantic 1,308; New England 39; Middle Atlantic 119; East North Central 510; West North Central 313; East South Central 344; West South Central 850; Mountain 473; Pacific 374 |
| Stories | 3 (one) | 1: 2,120; 2: 2,116; 3+: 94 |
| Bedrooms | 4 (two or fewer) | ≤2: 154; 3: 1,780; 4: 1,777; 5+: 619 |
| Full bathrooms | 4 (one or fewer) | ≤1: 46; 2: 2,664; 3: 1,203; 4+: 417 |
| Half bathrooms | 3 (none) | 0: 2,373; 1: 1,897; 2+: 60 |
| Garage | 4 (one-car) | 1-car: 158; 2-car: 3,124; 3+-car: 919; other: 129 |
| Foundation | 4 (basement) | Basement: 992; crawl space: 403; slab: 2,926; other: 9 |
| Fireplaces | 3 (none) | 0: 2,781; 1: 1,383; 2+: 166 |
| Homeowners' association | 2 (no) | No: 1,109; yes: 3,221 |
| Age-restricted community | 2 (no) | No: 4,216; yes: 114 |
| Exterior wall material | 7 (brick) | Brick 897; wood 169; stucco 906; vinyl 1,362; stone 56; fiber cement 926; other 14 |
| Heating fuel | 4 (electricity) | Electricity 2,147; natural gas 2,083; propane 52; other 48 |
| Sewer | 2 (public) | Public 3,893; septic or other 437 |
| Construction stage at sale | 3 (completed) | Completed 2,452; under construction 1,344; not started 534 |

> Table: Table 1. Training-set summary (n = 4,330). Price and lot size are strongly right-skewed with high outliers; lot size is capped at 87,120 sq ft (93 homes). Some levels are rare (New England 39 homes). Nothing is missing: homes with unreported values were removed during cleaning (130 of them for categorical codes).

表 1 标题：训练集汇总（n = 4,330）。售价和地块面积明显右偏，有很高的离群值；地块面积在 87,120 平方英尺处被截顶（93 套）。部分水平很少见（新英格兰 39 套）。没有缺失值：未报告的记录在清洗时已删除（其中 130 套是类别变量未报告）。

> **Interaction.** Following the three papers above, the price of floor area should differ by region. Figure 1 supports this: within-division slopes range from about $13k per 100 sq ft (East North Central) to $32k (Middle Atlantic).

**交互项。** 按照上面三篇文献，面积的价格应当随地区不同。图 1 支持这一点：各 division 内部的斜率从每 100 平方英尺约 1.3 万美元（东北中部）到 3.2 万美元（中大西洋）不等。

> ![Figure 1. Training set. (a) Price against floor area with one least-squares line per division; (b) within-division slopes with 95% confidence intervals.](../figures/fig1_interaction.png)

图 1 标题：训练集。(a) 售价对面积的散点，每个 division 一条最小二乘直线；(b) 各 division 内部的斜率及 95% 置信区间。

## 伦理讨论（Ethics discussion，上限 200 词）

> 【TODO：换成 Module 3 术语】课程 Module 3 的材料不在本地。下面两段先按通用框架（数据可信度、所有权与来源、隐私与去识别、合乎伦理的使用）写成；拿到 Module 3 后，请把关键词替换成课程里的术语（评分要求至少各引用一个“可信度”和“伦理收集”方面的概念）。

> **Trustworthiness.** The data come from a federal statistical agency, use a documented probability sampling design, and are released with full documentation, sampling weights and a flag on every value altered for confidentiality. Ownership and origin are clear: the Census Bureau collects the data, HUD funds the collection, and the files are free to the public. The producer discloses the main limitations (top- and bottom-coding, geography limited to nine divisions), and we report them.

**可信度。** 数据来自联邦统计机构，采用有文档说明的概率抽样设计，发布时附有完整文档、抽样权重，并对每一个为保密而修改过的值加了标记。所有权与来源清楚：人口普查局负责收集，HUD 资助收集，文件对公众免费开放。数据提供方公开说明了主要局限（顶码/底码处理，地理信息只到 9 个 division），我们在报告中如实说明。

> **Ethical collection and use.** Respondents are builders or owners reporting facts about a house, not personal attributes of occupants. The public file contains no addresses or builder names, and extreme prices and floor areas are top- and bottom-coded to prevent disclosure. We use only the public file and make no attempt to identify houses or builders. Our results describe associations among new homes sold in 2025; we will not present them as causal effects or as appraisals of individual homes, and we will note that each division contains very different local markets.

**伦理收集与使用。** 受访者是建造商或业主，他们报告的是房子的事实信息，而不是住户的个人属性。公开文件不含地址或建造商名称，极端的售价和面积做了顶码/底码处理以防泄露身份。我们只使用公开文件，不尝试识别任何房屋或建造商。我们的结果描述的是 2025 年售出新房中的关联，不会把它们说成因果效应或对单套房屋的估价，并会说明每个 division 内部包含差异很大的本地市场。

> 【说明】有资料称 SOC 受 Title 13 保密条款保护，但 `socmicro_info.pdf` 中没有写明，因此英文稿没有提 Title 13；如需加入，请先在 census.gov 核对。

## 初步结果（Preliminary results，上限 400 词，含图表标题）

> We fitted the preliminary model by least squares on the training set: sale price on floor area, division, their interaction and the other 15 predictors (17 predictors, 52 coefficients). It explains most of the variation (R² = 0.713, adjusted R² = 0.710). The eight interaction coefficients are jointly significant (partial F(8, 4278) = 37.3, p < 0.001) and add 0.020 to R².

我们在训练集上用最小二乘拟合初步模型：售价对面积、division、二者交互以及其余 15 个预测变量（共 17 个预测变量、52 个系数）。模型解释了大部分变异（R² = 0.713，调整 R² = 0.710）。8 个交互系数联合显著（partial F(8, 4278) = 37.3，p < 0.001），使 R² 增加 0.020。

（表格内容与英文稿相同，见下；表格单元格不计字数）

| Division | n | Slope | SE | 95% CI | Difference from South Atlantic (SE) |
|:----------------------|------:|------:|-----:|:---------------|:--------------------|
| South Atlantic (reference) | 1,308 | 11.83 | 0.63 | (10.60, 13.07) | — |
| New England | 39 | 19.26 | 2.15 | (15.05, 23.47) | 7.43 (2.17) |
| Middle Atlantic | 119 | 24.56 | 1.14 | (22.32, 26.79) | 12.72 (1.21) |
| East North Central | 510 | 6.85 | 0.85 | (5.19, 8.51) | −4.98 (0.91) |
| West North Central | 313 | 10.57 | 1.15 | (8.32, 12.82) | −1.26 (1.20) |
| East South Central | 344 | 13.78 | 0.97 | (11.88, 15.68) | 1.95 (1.00) |
| West South Central | 850 | 9.27 | 0.79 | (7.71, 10.82) | −2.57 (0.82) |
| Mountain | 473 | 14.60 | 0.80 | (13.03, 16.17) | 2.77 (0.87) |
| Pacific | 374 | 21.70 | 1.14 | (19.47, 23.92) | 9.86 (1.17) |

> Table: Table 2. Adjusted slope of price ($1000s) per extra 100 sq ft by division. All 52 coefficients are in Appendix A.

表 2 标题：各 division 每多 100 平方英尺售价（千美元）的调整后斜率。全部 52 个系数见附录 A。

> ![Figure 2. Condition 1 (observed against fitted price) and Condition 2 (pairs of numerical predictors), with LOWESS curves.](../figures/fig2_conditions.png)

图 2 标题：Condition 1（观测售价对拟合值）和 Condition 2（数值预测变量两两散点），附 LOWESS 曲线。

> ![Figure 3. Residuals against fitted values, scale-location and normal QQ plots (top); residuals against each numerical predictor (bottom).](../figures/fig3_residuals.png)

图 3 标题：上排为残差对拟合值、scale-location 图和正态 QQ 图；下排为残差对每个数值预测变量。

> **Assumptions.** Condition 1 holds approximately: prices scatter around one increasing curve but spread out at high fitted values (Figure 2). Condition 2 holds: numerical predictors show no curved patterns (|r| ≤ 0.22). Residual plots (Figures 3–4) then show:

**假设检查。** Condition 1 大致成立：售价围绕一条递增曲线分布，但在拟合值较高处散开（图 2）。Condition 2 成立：数值预测变量之间没有弯曲模式（|r| ≤ 0.22）。在此基础上，残差图（图 3–4）显示：

> - *Linearity:* mildly violated; residuals against fitted values and floor area bend slightly.
> - *Constant variance:* violated; residuals fan out as fitted values grow, the scale-location trend rises, and residual SDs differ five-fold across divisions.
> - *Normality:* violated; the QQ plot has a long upper tail (skewness 2.0, excess kurtosis 18; 36 standardized residuals beyond ±4), partly from top-coded prices.
> - *Uncorrelated errors:* plausible by design (one sampled house per row, no trend across sale months), but same-subdivision homes cannot be checked.

- *线性*：轻度违反；残差对拟合值、残差对面积的曲线略有弯曲。
- *方差齐性*：违反；残差随拟合值增大呈喇叭形散开，scale-location 趋势上升，各 division 的残差标准差相差约 5 倍。
- *正态性*：违反；QQ 图上尾很长（偏度 2.0，超额峰度 18；36 个标准化残差超出 ±4），部分来自售价顶码。
- *误差不相关*：从抽样设计看是合理的（每行是一套被抽中的房子，残差随签约月份没有趋势），但同一楼盘的房子无法检查。

> We do not correct these violations yet.

我们现在不修正这些违反。

> ![Figure 4. Residuals by level of each categorical predictor, and histogram of standardized residuals.](../figures/fig4_resid_by_categorical.png)

图 4 标题：按每个类别预测变量分组的残差箱线图，以及标准化残差直方图。

> **Comparison with the literature.** As Gyourko and Saiz (2006) and Glaeser et al. (2005) suggest, the price of space varies widely: 100 extra square feet add about $7k in East North Central but $22k–$25k in the Pacific and Middle Atlantic divisions. Two results are surprising. Lot size is not significant (p = 0.28) although land is part of the price, perhaps because large lots are mostly in cheaper rural areas. Holding floor area fixed, more bedrooms lower the price (5+ against ≤2: −$76k), consistent with smaller rooms. The New England and Middle Atlantic slopes rest on few homes.

**与文献对比。** 正如 Gyourko 和 Saiz（2006）以及 Glaeser 等（2005）所预示，空间的价格差异很大：多 100 平方英尺，在东北中部约加 7 千美元，而在太平洋和中大西洋约加 2.2 万至 2.5 万美元。有两点出乎意料。地块面积不显著（p = 0.28），尽管土地是价格的一部分；可能是因为大地块多在地价较低的农村地区。在面积固定时，卧室越多价格越低（5 间及以上相对 2 间及以下：−7.6 万美元），这与“房间更小”一致。新英格兰和中大西洋的斜率依据的样本很少。

## 计划（Plan，上限 300 词）

> **Predictors.** Floor area, division and their interaction must stay because they answer the research question; lot size stays because hedonic theory treats land as part of the price (Rosen, 1974). For the other 14 predictors we will use partial F tests and backward selection by AIC and BIC with the required terms fixed, and use context from the literature, such as features tied to construction cost, to settle close calls. A predictor will be dropped only if removing it lowers the chosen criterion and its partial F test is not significant at the 5% level; where AIC and BIC disagree we will prefer the simpler model if adjusted R² barely changes. We will check multicollinearity with generalized variance inflation factors.

**预测变量。** 面积、division 及其交互必须保留，因为它们直接回答研究问题；地块面积保留，因为 hedonic 理论把土地视为价格的一部分（Rosen, 1974）。其余 14 个预测变量将用 partial F 检验，以及固定必选项后的 AIC 和 BIC 后向选择来筛选，并用文献背景（例如与建造成本相关的特征）处理难以取舍的情况。只有当删除某个变量能降低所选准则、且其 partial F 检验在 5% 水平不显著时才删除；AIC 与 BIC 结论不同时，若调整 R² 变化很小，就选更简约的模型。我们用广义方差膨胀因子（GVIF）检查多重共线性。

> **Assumptions.** We will redraw the full set of residual plots after every change (after transforming, after variable selection and for the final model), and each time check leverage, standardized residuals, Cook's distance, DFFITS and DFBETAS.

**假设检查。** 每做一次改动（变换后、变量选择后、最终模型）都重新画全套残差图，并同时检查杠杆值、标准化残差、Cook 距离、DFFITS 和 DFBETAS。

> **Transformations.** Right skew, variance growing with the mean and the curved floor-area pattern point to a Box-Cox power transformation of price. We will compare the suggested power with the log, which reads as a percentage effect, and try log floor area so that the slope becomes an elasticity. If unequal variance remains, we will add heteroscedasticity-consistent (HC3) standard errors. We will also check the results without top-coded prices and with the survey's sampling weights, and evaluate the final model only once, at the end, on the 30% held-out test set.

**变换。** 右偏、方差随均值增大、面积方向的弯曲，都指向对售价做 Box-Cox 幂变换。我们会把 Box-Cox 建议的幂与 log 比较（log 可解释为百分比效应），并尝试对面积取 log，使斜率成为弹性。如果方差不齐仍然存在，会补充异方差稳健（HC3）标准误。我们还会检查去掉顶码售价、使用抽样权重后结果是否不变，并只在最后用 30% 的保留测试集评估一次最终模型。

（表格内容与英文稿相同，见下；表格单元格不计字数）

| Task | Lead | Nov 9–15 | Nov 16–22 | Nov 23–29 | Nov 30–Dec 6 | Final due date |
|:------------------------------|:-----------------|:------:|:------:|:------:|:------:|:------:|
| Transformations; re-check assumptions | Haiwen Yi, [Member 2] | ■ | | | | |
| Variable selection, VIF, influence diagnostics | [Member 3], [Member 4] | | ■ | | | |
| Final model, robustness checks, one-time test-set check | All | | | ■ | | |
| Poster (figures and text) | [Member 2], [Member 3] | | | ■ | ■ | |
| Record presentation | All | | | | ■ | |
| Final review and submission | Haiwen Yi | | | | | ■ |

> Table: Table 3. Gantt chart of the remaining work (dates are targets).

表 3 标题：剩余工作的甘特图（日期为目标日期）。

> 【待办】日期是按 Part 1 截止（11 月 5 日）之后排的目标；请对照 Quercus 上 Part 2、海报和录播的实际截止日期调整，并填入负责人。

## 参考文献（Bibliography，不计字数；保留英文 APA 格式）

Fox, J., & Weisberg, S. (2019). *An R companion to applied regression* (3rd ed.). Sage.

Glaeser, E. L., Gyourko, J., & Saks, R. (2005). Why is Manhattan so expensive? Regulation and the rise in housing prices. *The Journal of Law and Economics, 48*(2), 331–369. https://doi.org/10.1086/429979

Gyourko, J., & Saiz, A. (2006). Construction costs and the supply of housing structure. *Journal of Regional Science, 46*(4), 661–680. https://doi.org/10.1111/j.1467-9787.2006.00472.x

R Core Team. (2025). *R: A language and environment for statistical computing* (Version 4.4.3) [Computer software]. R Foundation for Statistical Computing. https://www.R-project.org/

Rosen, S. (1974). Hedonic prices and implicit markets: Product differentiation in pure competition. *Journal of Political Economy, 82*(1), 34–55. https://doi.org/10.1086/260169

U.S. Census Bureau. (2026). *Survey of Construction (SOC) microdata: 2025 annual file* [Data set]. https://www.census.gov/construction/chars/microdata.html

U.S. Census Bureau. (n.d.). *Survey of Construction microdata files: General information and variable descriptions* [Documentation]. https://www.census.gov/construction/chars/pdf/socmicro_info.pdf

## 附录 A（不计字数）

全部 52 个系数的估计、标准误和 95% 置信区间，与 `Part1_Code.html` 第 8.1 节的表格相同，见英文稿附录 A。
