# 提交前待办（Part 1 截止：11 月 5 日 23:59；NQA 延期：11 月 8 日 23:59）

## 必须完成

- [ ] **组员信息**
  - [ ] `proposal/Proposal_Part1_EN.md` 标题下的组号 `[##]`
  - [ ] Contributions：每位组员的姓名和具体贡献
  - [ ] 甘特图（表 3）每项任务的负责人
  - [ ] `Part1_Code.Rmd`、`Part2_Analysis.Rmd` 开头 YAML 的 `author`
- [ ] **伦理部分换成 Module 3 术语**：目前按通用框架写（可信度、所有权与来源、隐私与去识别、合乎伦理的使用）；评分要求“可信度”和“伦理收集”各至少引用一个模块概念。`proposal/Proposal_Part1_中文对照.md` 中标了【TODO】。
- [ ] **读原文核对三篇文献**
  - [ ] Rosen (1974)：Crossref/OpenAlex 都没有摘要，目前按公认内容保守概括，必须读原文确认措辞。
  - [ ] Gyourko & Saiz (2006)、Glaeser et al. (2005)：概括依据官方摘要；确认“新增面积主要是结构”“监管严格地区斜率更陡”在文中是作为**我们的推论**出现，而不是论文原话。
- [ ] **核对数据收集目的的措辞**：Data description 中 “It produces official statistics on new residential construction and sales” 在 `socmicro_info.pdf` 中没有逐字出现，到 https://www.census.gov/construction/soc 核对。
- [ ] **甘特图日期**：对照 Quercus 上 Part 2、海报、录播的实际截止日期调整。
- [ ] **重新生成 proposal PDF** 并逐页检查（命令见 README）；每节词数重新数一遍，保持在上限内。
- [ ] **Part 0 Teamwork Agreement**：全员签字，存为 PDF。
- [ ] **OneDrive**：上传 `data/original/soc25.csv`、`data/cleaned/soc_clean.csv`、`data/split_ids.csv`（必须，Rmd 用它取训练集），建议加上 `Part1_Code.Rmd` 和 `socmicro_info.pdf`；权限设为 “Anyone in UofT with the link can access”，用无痕窗口测试。
- [ ] **Quercus**：一位组员提交 Part 0 PDF、Proposal PDF、`Part1_Code.Rmd`，并在 submission comment 中贴 OneDrive 链接。

## 可选

- [ ] 数据集引用补上 2025 年度文件的确切发布日期。
- [ ] 如需在伦理部分提 Title 13 保密条款，先在 census.gov 核对。
- [ ] 最终报告前把 `Part2_Analysis.Rmd` 的叙述改成英文。

## Part 2 之后

- [ ] 模型定稿后，运行一次 `Part2_Analysis.Rmd` 最后的测试集验证块（改为 `eval = TRUE` 或手动运行），记录结果，不再回头修改模型。
