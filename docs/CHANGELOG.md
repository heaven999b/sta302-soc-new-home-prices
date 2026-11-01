# 变更记录

## 2026-11-02

- Added a complete repository-home navigation table for cloud documents, code, data, figures and outputs.
- Synced Haiwen Yi’s first three task assignments into all English proposal formats.
- Updated OneDrive submission link and removed stale submission-status claims.

- Synced the revised English proposal in Markdown, HTML, PDF and Word.
- Added English analysis/data supplements and the verified course checklist.
- Preserved member/contribution/owner blanks and documented submission prerequisites.
- Archived the successful Part 1/2 rerun logs and byte-identical cleaned-data checks.
- No model, dataset, split or test-evaluation policy was changed.


## 2026-09-30

- **探针**：组 1 用 Python（statsmodels）在 SOC 2025 微观数据上探测“面积 × Census division”。在任何建模之前用 `default_rng(302)` 固定 70/30 划分，只保存测试集 ID；所有拟合只用训练集。脚本和结果见 `probe/`。
- **判定合格**：Part 1 原始尺度 R² = 0.713，交互 HC3 p = 7.5e-24；Part 2 log–log 仍显著（HC3 p = 1.6e-10）；通过替代交互检查、抽样权重和去顶码检查；在 2024 年独立样本上复现。列为三个合格方案之一（方案一）。
- **R 化**：
  - 用 Python 按原划分生成 `data/split_ids.csv`，核对测试集 ID 与探针完全一致。
  - 写出 `Part1_Code.Rmd`（base R + car）：从原始 CSV 逐步清洗到 6,185 行，与探针的分析数据逐行一致；变量汇总、交互图、初步模型、完整残差分析。
  - 写出 `Part2_Analysis.Rmd`（MASS、car、sandwich、lmtest）：Box-Cox、变换比较、GVIF、影响点、partial F、AIC/BIC 后向选择、最终模型、HC3 与聚类 SE、混杂与敏感性、中西部对比、2024 复现、封存的测试集验证块。
  - R 与 Python 逐项核对 281 项（`verification/R_vs_Python.md`）；更正探针中的若干描述（变量个数、ICC 的解读、ENC 稳健性的边界、Condition 1 相关系数、Box-Cox CI）。
  - 英文 proposal 草稿及逐段中文对照；各节词数均在上限内；PDF 逐页检查。
- **仓库化**：整理为独立 git 仓库 `sta302-soc-new-home-prices`（将作为 `sta302-research-project` 的 submodule）。
  - proposal 移入 `proposal/`，图片路径改为 `../figures/...`，样式抽出为 `proposal/proposal.css`，HTML 重新生成。
  - 新增 `README.md`、`README_zh.md`、`design/research_design.md`（中文研究设计，数字为 R 核对后的版本）、`docs/`、`probe/README.md`。
  - 在新位置重新 knit `Part1_Code.Rmd`，`data/cleaned/soc_clean.csv` 与原文件逐字节一致。
