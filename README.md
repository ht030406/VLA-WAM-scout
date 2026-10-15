# vla-wam-scout · VLA / World Action Model 每日情报采集器

自动搜寻 **VLA（Vision-Language-Action）** 与 **WAM（World Action Model / World Model）**
相关的最新技术动态，产出每日中文情报日报：

- 📄 **arXiv 新论文**（多关键词 + 类目过滤，LLM 提炼一句话核心贡献并标重点）
- 🐙 **GitHub 开源仓库**（新创建 + 活跃更新扫描；LLM 判断是否为真源码仓、给出中文亮点与"强烈建议关注"标记；自动剔除无关仓库）
- 🤗 **HuggingFace 新模型**（按创建时间搜索 VLA/WAM 相关模型，过滤翻译等无关模型）

> 与 [daily-arxiv-vla](https://github.com/Infinity4B/daily-arxiv-vla) 网站的关系：
> 该站负责 arXiv 论文聚合与站内展示；本工具是更广的"每日情报源"——
> 覆盖 GitHub 开源仓库与 HF 模型，补充网站缺失的开源仓库维度。
> 产物 `reports/repos.md` 采用与 `papers.md` 一致的表格风格，便于后续并入网站。

---

## 运行模式总览

| 模式 | 运行位置 | LLM 端点 | 适用场景 | 可靠性 |
|---|---|---|---|---|
| **① 本地手动** | 你的电脑 / 本服务器 | 任意（默认 ModelScope 公网；内网可用灵枢） | 随时手动跑一次、调试 | 手动触发 |
| **② 本地定时（cron）** | 本服务器（需常驻） | 同手动（本地 .env 配置） | 服务器 24h 在线时的补充定时 | 受会话驻留影响 |
| **③ GitHub Actions 远程** | GitHub 云 runner | **必须公网可达**（默认 ModelScope） | 全自动、推荐主力 | 高（GitHub 托管） |

三种模式共用同一套代码与 `reports/state.json` 去重记忆（state.json 随 git 提交，跨环境生效），
同一批条目不会被重复报道。**推荐：③ 为主 + ① 随时手动补充；② 视服务器可用性选配。**

LLM 端点规则一句话：**代码是 OpenAI 兼容的，公网端点（ModelScope）谁都能跑；
要跑华为内网灵枢只能在能访问内网的机器上跑，GitHub runner 永远不行**（详见
[LLM 端点与证书](#llm-端点与证书专题)）。

---

# 模式一：本地运行（手动 + 定时）

## 1.1 准备

- Python 3.9+（3.10 最佳），`pip` 可用
- 能出网（访问 arXiv / GitHub API / HuggingFace；本地可选华为内网）
- 可选：Git（用于定时推送；纯手动不需要）

## 1.2 安装

```bash
cd vla-wam-scout
pip install -r requirements.txt     # 仅依赖 requests（urllib3 随附）
```

## 1.3 配置环境变量（.env）

```bash
cp .env.example .env
```

编辑 `.env`，至少填 `LLM_API_KEY`。**两种常见配法：**

**配法 A：默认走 ModelScope 公网**（公司/个人电脑都行）——从 modelscope.cn 登录创建访问令牌后：

```ini
LLM_API_KEY=sk-你的ModelScope令牌
LLM_BASE_URL=https://api-inference.modelscope.cn/v1/
LLM_MODEL=deepseek-ai/DeepSeek-V4.1-Flash
LLM_FALLBACK_MODELS=ZhipuAI/GLM-5.3-Flash,moonshotai/Kimi-K3
CA_CERT_FILE=
```

**配法 B：本地在内网、想用灵枢**（本 DSH 服务器即是这种环境）：

```ini
LLM_API_KEY=你的灵枢key
LLM_BASE_URL=https://computing.huawei.com/lingshu/api/v1
LLM_MODEL=DeepSeek-V4-Flash-0731
LLM_FALLBACK_MODELS=
CA_CERT_FILE=/root/.certs/lingshu_chain.pem
```

> 兼容性：也接受旧配置名 `LINGSHU_API_KEY` / `LINGSHU_BASE_URL` / `LINGSHU_MODEL`（`LLM_*` 优先）。

## 1.4 手动运行

```bash
python run_daily.py
```

- 正常耗时 3~10 分钟（arXiv 分页 + GitHub 多组搜索 + HF + LLM 批量总结，各源带礼貌性延时）
- 屏幕进度：`[1/5] 拉取 arXiv... → [5/5] 灵枢 LLM 总结... → 完成`
- 完成后 `reports/` 下产出：

| 文件 | 说明 |
|---|---|
| `reports/daily-vla-wam-YYYY-MM-DD.md` | 当日完整日报（重点论文/全部论文/重点仓库/AI 亮点/HF 模型/今日要点） |
| `reports/latest.md` | 当日日报固定名拷贝（便于程序取用） |
| `reports/repos.md` | 开源仓库表格数据（可并入 daily-arxiv-vla 网站） |
| `reports/state.json` | 跨日去重状态（务必随 git 提交，云端/本地共享记忆） |

**怎么确认成功了？** 打开日报：
- ✅ 顶部有「📌 今日要点」的中文趋势总结；论文/仓库有 AI 亮点；有新数据
- ❌ 顶部出现 `⚠️ AI 摘要异常：...` —— 说明 LLM 失败，原因已内联在报告里，照因排查（见 FAQ）

## 1.5 定时运行（cron，可选）

> 前提：服务器**尽量 7×24 在线**；时间按 **UTC** 计算（北京 12:00 = UTC 04:00）。

**步骤 1：确保 cron 守护在跑**（Linux 容器通常无 systemd，需手动起一次）：

```bash
pgrep -x cron >/dev/null || /usr/sbin/cron     # 已装 cron 的情况下
pgrep -a cron                                   # 应能看到 /usr/sbin/cron
```

> 本项目已在 `/root/.bashrc` 加了一行自动拉起（新会话打开即保证 cron 在跑）。

**步骤 2：设定每日任务**（北京时间中午 12:00）：

```bash
crontab -e
```

加入一行：

```
0 4 * * * /workspace/vla-wam-scout/run_daily_local.sh
```

| cron 表达式 | 说明 |
|---|---|
| `0 4 * * *` | 每天 **UTC 04:00 = 北京时间 12:00**，与 daily-arxiv-vla 网站同节奏 |
| `30 4 * * *` | 想错峰换 04:30 UTC（北京 12:30），看你自己 |
| 其他 | GitHub 定时格式：`分 时 日 月 周`（全部按服务器时区，本服务器为 UTC） |

**步骤 3：了解 `run_daily_local.sh` 的行为**

- 用 `flock` **防重入**：上一次没跑完则本次自动跳过（日志会写 `!! 上次运行未结束，本次跳过`）
- 全部输出与错误写进 `logs/daily.log`，查看：`tail -f /workspace/vla-wam-scout/logs/daily.log`
- 结果只写本地 `reports/`；**推送是开关式的**（见步骤 4）

**步骤 4（可选）：跑完自动推送到 GitHub**

```bash
cd /workspace/vla-wam-scout
touch .push_enabled      # 空文件即开启"跑完自动 commit+push"
```

并在本机配好推送凭据（二选一）：
- **fine-grained PAT**：GitHub → Settings → Developer settings → Personal access tokens →
  Fine-grained → 只授权 `VLA-WAM-scout` 仓库（Contents: Read and write）→ 生成后：
  ```bash
  git remote set-url origin https://<你的名字>:<PAT>@github.com/<你的名字>/VLA-WAM-scout.git
  ```
  > 注意：PAT 不要提交进仓库，也不要写进 .env/.git-credentials 之外的地方。
- **SSH**：`ssh-keygen` 生成公钥 → GitHub → Settings → SSH keys 添加 → `git remote set-url origin git@github.com:<你的名字>/VLA-WAM-scout.git`

推送逻辑：`.push_enabled` 存在且 `reports/` 有变化时才 commit（消息
`每日VLA/WAM情报更新 - YYYY-MM-DD [local cron]`）并 push。失败会记入日志。

**步骤 5：验证**

```bash
# 手动触发一次（等同于定时行为）：
cd /workspace/vla-wam-scout && ./run_daily_local.sh
tail -20 logs/daily.log     # 应看到 采集→去重→LLM总结→完成 全流程
```

**本地模式注意三点：**
1. 会话型服务器不保证 7×24 驻留——重启新会话后 cron 会被 `.bashrc` 自动拉起，但若服务器长期停机，期间定时会断（可用模式三兜底）；
2. 服务器时钟可能有数分钟偏差（比真实时间慢、且模型活跃期间会冻结），所以"04:00 触发"实际可能晚一点，**按天粒度没问题，别要求准点**；
3. 本地若同时开了 GitHub Actions（模式三），两边共用 state.json 去重，不会重复报道同一条目。

---

# 模式二：GitHub Actions 远程（云端全自动，推荐主力）

> 核心前提：**runner 在公网，LLM 端点必须公网可达**。默认 ModelScope（`api-inference.modelscope.cn`）
> 满足此要求；华为内网灵枢在 GitHub 上**永远连不通**（无公网 DNS，见 FAQ）。

## 2.1 推送代码

```bash
cd vla-wam-scout
git add .
# 注意：reports/state.json、certs/lingshu_chain.pem 都要提交
git commit -m "部署 vla-wam-scout"
git remote add origin https://github.com/<你的名字>/VLA-WAM-scout.git   # 首次
git push -u origin main
```

## 2.2 配置 Secrets 与 Variables

仓库页面 → **Settings → Secrets and variables → Actions**：

| 类型 | 名称 | 必填 | 值/说明 |
|---|---|---|---|
| Secret | `MODELSCOPE_ACCESS_TOKEN` | ✅ | ModelScope 访问令牌（与 daily-arxiv-vla 仓库同一个；没有就去 modelscope.cn 登录→头像→访问令牌→创建） |
| Secret | `GITHUB_TOKEN` | 可选 | GitHub PAT（提升 GitHub 搜索 API 限额；不配也能跑，10 req/min） |
| Variable | `LLM_BASE_URL` | 可选 | 默认 `https://api-inference.modelscope.cn/v1/`，换端点时改 |
| Variable | `LLM_MODEL` | 可选 | 默认 `deepseek-ai/DeepSeek-V4.1-Flash` |
| Variable | `LLM_FALLBACK_MODELS` | 可选 | 默认 `ZhipuAI/GLM-5.3-Flash,moonshotai/Kimi-K3`（主模型失败自动切换） |
| Variable | `LOOKBACK_DAYS` | 可选 | 默认 `2`，采集回看天数 |

> 旧的 `LINGSHU_API_KEY` secret 已不再使用，可留可删。

## 2.3 定时时间设置

工作流内置（`.github/workflows/daily-vla-wam.yml`）：

```yaml
on:
  schedule:
    - cron: '0 4 * * *'      # 每天 UTC 04:00 = 北京时间 12:00
  workflow_dispatch: {}      # 也支持手动触发
```

- **想改时间**：直接改上面 cron 行并推送；GitHub 定时一律按 **UTC** 计算
- **⚠️ 已知现象**：GitHub 定时运行**不保证准点**，可能延迟数分钟到数小时（官方明确说明，
  属平台行为，不是配置错误）。如连续多天延迟过大，可加一个备用触发（如第二个迟到时间槽
  `30 5 * * *`，靠 state.json 去重不会重复提交）；不在意的话忽略即可。

## 2.4 手动触发与验证

1. 仓库 **Actions** → **VLA/WAM 每日情报采集** → **Run workflow**（用 main 分支）
2. 运行约 5~15 分钟（fetch 阶段含延时）
3. 完成判定：
   - 日志「运行每日采集与总结」步骤里应有：
     ```
     [llm] 端点: https://api-inference.modelscope.cn/v1/
     [llm] 模型: deepseek-ai/DeepSeek-V4.1-Flash, ZhipuAI/GLM-5.3-Flash, moonshotai/Kimi-K3
     ```
     且**没有** `[llm] ... 失败` 字样；
   - 提交的 `reports/daily-vla-wam-YYYY-MM-DD.md` 带 **今日要点 + AI 摘要**；
   - 报告顶部**没有** `⚠️ AI 摘要异常` 行。

## 2.5 失败排查速查表

| 报告/日志里看到 | 含义 | 处理 |
|---|---|---|
| `⚠️ AI 摘要异常：RuntimeError: LLM_API_KEY 未配置…` | secret 没配/名字不对 | 补 `MODELSCOPE_ACCESS_TOKEN`（见 2.2） |
| `⚠️ AI 摘要异常：401 … 服务端: Please bind your Alibaba Cloud account before use.` | ModelScope 账号**未绑定阿里云账号**，推理接口被拒（token 本身有效） | 见下方「ModelScope 绑定阿里云」步骤 |
| `⚠️ AI 摘要异常：401 …（模型 …）` 其他 401 | 令牌无效/过期 | 换新令牌 |
| `⚠️ AI 摘要异常：NameResolutionError … computing.huawei.com` | 端点域名公网不可解析（灵枢） | 换公网端点 ModelScope（改 `LLM_BASE_URL`） |
| `⚠️ AI 摘要异常：429 限流（模型 …）` | 该模型限流 | 已自动换备用模型；仍频繁则调整 `LLM_FALLBACK_MODELS` |
| 报告正常但某些条目「AI 摘要生成失败」 | LLM 解析/返回偶发 | 属容错降级，等下次或手动重跑 |
| 定时到点却没跑 | GitHub 定时延迟 | 等 30~60 分钟；仍无则手动 Run workflow |

---

## LLM 端点与证书专题

- **默认 ModelScope 公网**：`LLM_BASE_URL=https://api-inference.modelscope.cn/v1/`，
  证书用系统 CA（`CA_CERT_FILE` 留空），GitHub runner、任意电脑都可用；
- **灵枢（华为内网）**：`computing.huawei.com` **无公网 DNS 记录**（公网查询 NXDOMAIN），
  仅内网机器能访问。**GitHub Actions 永远连不上它**——这是结构性限制，不是证书问题；
- **若以后灵枢提供公网网关**：把仓库 Variables 改成 `LLM_BASE_URL=<网关>`、
  `LLM_MODEL=<模型>`、`CA_CERT_FILE=certs/lingshu_chain.pem`（自签链已在仓库内）即可切回；
- 仓库内 `certs/lingshu_chain.pem` 是灵枢链证书备份，公网场景用不到，留着无害；
- 失败原因会**内联进日报顶部**（`⚠️ AI 摘要异常：<原因>`），排查不用翻日志。

---

## 环境变量全集

| 变量 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `LLM_API_KEY` | ✅ | – | LLM 端点令牌（ModelScope 令牌 / 灵枢 key；兼容旧名 `LINGSHU_API_KEY`） |
| `LLM_BASE_URL` | – | `https://api-inference.modelscope.cn/v1/` | OpenAI 兼容端点（兼容 `LINGSHU_BASE_URL`） |
| `LLM_MODEL` | – | `deepseek-ai/DeepSeek-V4.1-Flash` | 主模型（兼容 `LINGSHU_MODEL`） |
| `LLM_FALLBACK_MODELS` | – | `ZhipuAI/GLM-5.3-Flash,moonshotai/Kimi-K3` | 备用模型，逗号分隔，主模型失败/限流时依次尝试 |
| `CA_CERT_FILE` | – | 空 | 自定义 CA 证书路径；仅内网网关（灵枢）需要 |
| `GITHUB_TOKEN` | – | – | GitHub PAT（提升搜索限额；无 token 也能跑） |
| `LOOKBACK_DAYS` | – | `2` | 采集回看天数（arXiv 窗口为空时自动扩大） |
| `ARXIV_MAX_RESULTS` | – | `60` | 论文条数上限 |
| `GITHUB_MAX_REPOS` | – | `25` | 日报仓库条数上限 |
| `HF_MAX_MODELS` | – | `25` | HF 模型条数上限 |
| `DEDUP_DAYS_PAPER` | – | `14` | 论文去重窗口（天） |
| `DEDUP_DAYS_REPO` | – | `7` | 仓库去重窗口（天） |
| `DEDUP_DAYS_MODEL` | – | `30` | 模型去重窗口（天） |
| `STAR_SURGE_REL` / `STAR_SURGE_ABS` | – | `0.5` / `200` | 仓库 star 飙升重报阈值（相对/绝对） |
| `LLM_MAX_TOKENS` | – | `2000` | 单次 LLM 响应上限 |
| `LLM_TEMPERATURE` | – | `0.3` | 采样温度 |

## 跨日去重（防止日报重复）

采集窗口有迭代重叠（今天 `[T-2, T]`，明天 `[T-1, T+1]`），活跃 GitHub 仓库还
会天天 push。为避免日报重复，工具维护 `reports/state.json`：

- 论文 14 天内不重复报道；仓库 7 天内不重复报道；模型 30 天内不重复报道；
- 例外：仓库 star 在去重窗口内飙升（相对 ≥50% 或绝对 ≥200）会以
  `🔥人气飙升` 标记重新报道；
- 日报头部显示本次忽略的重复数量（`🗂 去重：…`）；
- LLM 只总结**新增**部分，顺带节省 API token。

> `state.json` 会被 Git 提交跟踪，因此本地 cron 与 GitHub Actions 交替运行时共享同一份去重记忆。

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
- LLM 调用失败时报告以"结构化信息 + 原文链接"降级输出，且失败原因内联在报告顶部；
- LLM JSON 解析做字段名/格式容错，解析失败自动重试；多模型依次回退；
- arXiv 窗口为空时自动扩大回看天数，保证每日有产出；
- 本地定时用 flock 防重入，避免上一轮未结束导致重复采集。

## FAQ

**Q：ModelScope 报 401「Please bind your Alibaba Cloud account before use.」怎么办？**
这是 ModelScope 账号还没绑定阿里云账号，导致推理接口用不了（查看模型列表没问题，调用就 401）。
绑定步骤：
1. 登录 https://www.modelscope.cn ，点右上角头像 → **个人中心 / 账号设置**；
2. 找到 **「绑定阿里云账号」**（若没有，在模型详情页点「API 调用」tab 通常也会弹出引导）；
3. 按引导绑定或一键注册阿里云账号（手机号验证即可，免费），必要时同意「模型服务协议」；
4. 绑定后**无需更换令牌**，直接重新 Run workflow 即可。

**Q：灵枢还能用吗？**
能。在能访问华为内网的机器（如本 DSH 服务器）上照常用；只是 GitHub 云 runner 连不到它。
云端请用 ModelScope 等公网端点。

**Q：GitHub 上报告能自动提交吗？**
能。工作流跑完会自动 `git add reports/...` 并提交（`每日VLA/WAM情报更新 - 日期 [skip ci]`），
无需人工干预；state.json 也一并提交保持跨日记忆。

**Q：本地跑出来的报告和 GitHub 上的一样吗？**
内容构成一致（同一套代码）；具体条目可能不同（各自窗口、不同 LLM 端点/模型），
state.json 保证两边不会重复报道同一条目。

**Q：为什么我的 GitHub Actions 每次都"AI 摘要失败"？**
先看报告顶部的 `⚠️ AI 摘要异常` 行或 Actions 日志，绝大多数是：
secret 未配置（`LLM_API_KEY 未配置`）、端点域名公网不可达（灵枢 `NameResolutionError`）、
令牌失效（401）。对照 2.5 速查表处理。
