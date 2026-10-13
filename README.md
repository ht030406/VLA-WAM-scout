# vla-wam-scout · VLA / World Action Model 每日情报采集器

自动搜寻 **VLA（Vision-Language-Action）** 与 **WAM（World Action Model / World Model）**
相关的最新技术动态，产出每日中文情报日报：

- 📄 **arXiv 新论文**（多关键词 + 类目过滤，AI 提炼一句话核心贡献并标重点）
- 🐙 **GitHub 开源仓库**（新创建 + 活跃更新扫描；LLM 判断是否为真源码仓、给出中文亮点与"强烈建议关注"标记；自动剔除无关仓库）
- 🤗 **HuggingFace 新模型**（按创建时间搜索 VLA/WAM 相关模型，过滤翻译等无关模型）

> 与 [daily-arxiv-vla](https://github.com/Infinity4B/daily-arxiv-vla) 网站的关系：
> 该站负责 arXiv 论文聚合与站内展示；本工具是更广的"每日情报源"——
> 覆盖 GitHub 开源仓库与 HF 模型，补充网站缺失的开源仓库维度。
> 产物 `reports/repos.md` 采用与 `papers.md` 一致的表格风格，便于后续并入网站。

---

## 快速开始（本地）

```bash
cd vla-wam-scout
pip install -r requirements.txt
cp .env.example .env      # 填入 LINGSHU_API_KEY（灵枢）等
python run_daily.py
```

首次运行即可在当前目录 `reports/` 生成：

| 文件 | 说明 |
|---|---|
| `reports/daily-vla-wam-YYYY-MM-DD.md` | 当日完整情报日报 |
| `reports/latest.md` | 当日日报固定名拷贝（便于程序取用） |
| `reports/repos.md` | 开源仓库数据表（可并入网站） |

## 环境变量

| 变量 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `LINGSHU_API_KEY` | ✅ | – | 灵枢 API Key（OpenAI 兼容） |
| `LINGSHU_BASE_URL` | – | `https://computing.huawei.com/lingshu/api/v1` | 灵枢端点 |
| `LINGSHU_MODEL` | – | `DeepSeek-V4-Flash-0731` | 总结用模型 |
| `CA_CERT_FILE` | – | `/root/.certs/lingshu_chain.pem` | 自签 CA 证书路径；GitHub Actions 留空 |
| `GITHUB_TOKEN` | – | – | GitHub PAT（提升搜索限额；无 token 也能跑） |
| `LOOKBACK_DAYS` | – | `2` | 采集回看天数（论文窗口为空时自动扩大） |
| `ARXIV_MAX_RESULTS` | – | `60` | 论文条数上限 |
| `GITHUB_MAX_REPOS` | – | `25` | 日报仓库条数上限 |
| `HF_MAX_MODELS` | – | `25` | HF 模型条数上限 |

## 每日自动运行（GitHub Actions）

本项目自带 `.github/workflows/daily-vla-wam.yml`，
每日 **UTC 4:00（北京时间 12:00）** 自动采集并把报告提交回仓库。

### 接入步骤

1. 将本项目代码推送到你的 GitHub 仓库（可复制进 `Infinity4B/daily-arxiv-vla` 或独立仓库）；
2. 在 `Settings → Secrets and variables → Actions` 添加：
   - **Secret**：`LINGSHU_API_KEY`（必填）
   - **Secret**（可选）：`GITHUB_TOKEN`（GitHub PAT，提高搜索限额）
   - **Variables**（可选）：`LINGSHU_BASE_URL` / `LINGSHU_MODEL` / `LOOKBACK_DAYS` 等
3. 推送后可在 `Actions` 页面点 **Run workflow** 手动触发一次验证；
4. 之后每天中午自动运行，报告提交到 `reports/` 目录。

> 注意：灵枢 API 若部署在私有网络，需确认 GitHub Actions runner 可访问；
> 若证书链不可用，可在变量里把 `LINGSHU_BASE_URL` 指向公网可达的镜像端点。

## 与 daily-arxiv-vla 网站集成（进阶）

`reports/repos.md` 是表格格式（`| 日期 | 仓库 | 语言 | Stars | 类型 | 亮点 |`），
可在 `daily-arxiv-vla` 的站点构建脚本中解析该文件，新增"开源仓库"板块：

```python
# 示意：在 build_site.py 中读取并传给前端数据
import re
rows = []
for line in open("reports/repos.md", encoding="utf-8"):
    m = re.match(r"\|\s*(\S+)\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+)\|", line)
    if m:
        rows.append({"date": m.group(1), "repo": m.group(2),
                     "url": m.group(3), "lang": m.group(4).strip()})
```

## 工作原理

```
arXiv API ──► 论文（VLA/WAM 关键词，按提交时间倒序，类目过滤）
GitHub API ─► 仓库（新创建 + 活跃更新，README 摘录，相关词过滤）
HF API    ──► 模型（createdAt 排序，跨词去重，无关 pipeline 剔除）
      │
      ▼
 灵枢 LLM 批量总结（4 条/批，JSON 输出，字段容错解析）
      │
      ▼
 日报 Markdown + repos.md 数据表（reports/）
```

### 健壮性设计

- 任一数据源失败不影响其余来源（各自 try/except 降级）；
- LLM 调用失败时报告以"结构化信息 + 原文链接"降级输出；
- LLM JSON 解析做字段名/格式容错，解析失败自动重试；
- arXiv 窗口为空时自动扩大回看天数，保证每日有产出。
