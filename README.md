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
cp .env.example .env      # 填入 LLM_API_KEY（ModelScope 令牌）等
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
| `LLM_API_KEY` | ✅ | – | LLM 端点令牌（默认 ModelScope 令牌；兼容旧名 `LINGSHU_API_KEY`） |
| `LLM_BASE_URL` | – | `https://api-inference.modelscope.cn/v1/` | OpenAI 兼容端点（兼容旧名 `LINGSHU_BASE_URL`） |
| `LLM_MODEL` | – | `deepseek-ai/DeepSeek-V4.1-Flash` | 主模型（兼容旧名 `LINGSHU_MODEL`） |
| `LLM_FALLBACK_MODELS` | – | `ZhipuAI/GLM-5.3-Flash,moonshotai/Kimi-K3` | 备用模型，主模型失败/限流时依次尝试 |
| `CA_CERT_FILE` | – | 空 | 自定义 CA 证书路径；仅内部网关（灵枢）需要，公网端点留空 |
| `GITHUB_TOKEN` | – | – | GitHub PAT（提升搜索限额；无 token 也能跑） |
| `LOOKBACK_DAYS` | – | `2` | 采集回看天数（论文窗口为空时自动扩大） |
| `ARXIV_MAX_RESULTS` | – | `60` | 论文条数上限 |
| `GITHUB_MAX_REPOS` | – | `25` | 日报仓库条数上限 |
| `HF_MAX_MODELS` | – | `25` | HF 模型条数上限 |
| `DEDUP_DAYS_PAPER` | – | `14` | 论文去重窗口（天） |
| `DEDUP_DAYS_REPO` | – | `7` | 仓库去重窗口（天） |
| `DEDUP_DAYS_MODEL` | – | `30` | 模型去重窗口（天） |
| `STAR_SURGE_REL` / `STAR_SURGE_ABS` | – | `0.5` / `200` | 仓库 star 飙升重报阈值（相对/绝对） |

## 跨日去重（防止日报重复）

采集窗口有迭代重叠（今天 `[T-2, T]`，明天 `[T-1, T+1]`），活跃 GitHub 仓库还
会天天 push。为避免日报重复，工具维护 `reports/state.json`：

- 论文 14 天内不重复报道；仓库 7 天内不重复报道；模型 30 天内不重复报道；
- 例外：仓库 star 在去重窗口内飙升（相对 ≥50% 或绝对 ≥200）会以
  `🔥人气飙升` 标记重新报道；
- 日报头部显示本次忽略的重复数量（`🗂 去重：…`）；
- LLM 只总结**新增**部分，顺带节省 API token。

> `state.json` 会被 Git 提交跟踪，因此 GitHub Actions 每日运行同样具有跨日记忆。

## 每日自动运行（GitHub Actions）

本项目自带 `.github/workflows/daily-vla-wam.yml`，
每日 **UTC 4:00（北京时间 12:00）** 自动采集并把报告提交回仓库。

### 接入步骤

1. 将本项目代码推送（**连同 `certs/lingshu_chain.pem` 一起提交**）到你的 GitHub 仓库（可复制进 `Infinity4B/daily-arxiv-vla` 或独立仓库）；
2. 在 `Settings → Secrets and variables → Actions` 添加：
   - **Secret**：`MODELSCOPE_ACCESS_TOKEN`（必填，与 daily-arxiv-vla 同一个 ModelScope 令牌）
   - **Secret**（可选）：`GITHUB_TOKEN`（GitHub PAT，提高搜索限额）
   - **Variables**（可选）：`LLM_BASE_URL` / `LLM_MODEL` / `LLM_FALLBACK_MODELS` / `LOOKBACK_DAYS` 等
3. 推送后可在 `Actions` 页面点 **Run workflow** 手动触发一次验证；
4. 之后每天自动运行（cron UTC 4:00，GitHub 可能延迟数小时），报告提交到 `reports/` 目录。

### 关于 LLM 端点与证书（重要）

- 默认使用 **ModelScope 公网推理接口**（`api-inference.modelscope.cn`），GitHub Actions runner 可直接访问，证书用系统 CA，无需任何配置；
- ⚠️ 灵枢（`computing.huawei.com`）**没有公网 DNS 记录**（公网查询 NXDOMAIN），GitHub runner 无法解析，之前所有「AI 摘要生成失败」的根因都在这里（日志报 `NameResolutionError`），与证书无关；
- 如需切回灵枢：必须提供其**公网网关域名**，然后设仓库 Variables：`LLM_BASE_URL`、`LLM_MODEL`、`CA_CERT_FILE`（指向仓库内 `certs/lingshu_chain.pem`）；
- 代码兼容旧配置名（`LINGSHU_API_KEY` / `LINGSHU_BASE_URL` / `LINGSHU_MODEL`），本地用灵枢内网时直接设这些或 `LLM_*` 均可；
- 若 `LLM_API_KEY` 缺失，报告顶部会内联 `⚠️ AI 摘要异常：RuntimeError: LLM_API_KEY 未配置…`；若调用失败也会内联具体原因（如 `429 限流`、`NameResolutionError`），无需翻日志。

> 若你的 LLM 端点需要私有网络访问，可在仓库变量里把 `LLM_BASE_URL` 指向公网可达的镜像端点。

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
  LLM 批量总结（4 条/批，多模型容错切换，JSON 输出，字段容错解析）
      │
      ▼
 日报 Markdown + repos.md 数据表（reports/）
```

### 健壮性设计

- 任一数据源失败不影响其余来源（各自 try/except 降级）；
- LLM 调用失败时报告以"结构化信息 + 原文链接"降级输出；
- LLM JSON 解析做字段名/格式容错，解析失败自动重试；
- arXiv 窗口为空时自动扩大回看天数，保证每日有产出。
