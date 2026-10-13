# -*- coding: utf-8 -*-
"""每日报告生成：Markdown 日报 + repos.md（供网站集成）。"""
from datetime import datetime, timezone
from typing import Dict, List

import config

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def _cn_date(dt=None) -> str:
    dt = dt or datetime.now(timezone.utc)
    return f"{dt.year}-{dt.month:02d}-{dt.day:02d}"


def _cn_date_label(dt=None) -> str:
    dt = dt or datetime.now(timezone.utc)
    wd = WEEKDAYS[dt.weekday()]
    return f"{_cn_date(dt)} {wd}"


def _fallback_paper_line(p: dict) -> str:
    return "（AI 摘要生成失败，请查看原文）"


def build_markdown_report(
    papers: List[dict],
    repos: List[dict],
    models: List[dict],
    paper_summaries: Dict[str, dict],
    repo_judgements: Dict[str, dict],
    insight: str,
) -> str:
    date_label = _cn_date_label()
    n_papers, n_repos, n_models = len(papers), len(repos), len(models)

    lines = [
        f"# VLA / WAM 每日情报 · {date_label}",
        "",
        f"> 数据源：arXiv（{n_papers} 篇）/ GitHub（{n_repos} 仓）/ HuggingFace（{n_models} 模型）",
        f"> 自动生成于 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · vla-wam-scout",
        "",
        "---",
        "",
        "## 📌 今日要点",
        "",
        insight or "今日暂无可总结条目。",
        "",
        "---",
        "",
    ]

    # ---------- 论文 ----------
    lines += ["## 📄 新论文（arXiv）", ""]
    if not papers:
        lines += ["今日无新提交论文。", ""]
    else:
        key_papers = [p for p in papers if paper_summaries.get(p["arxiv_id"], {}).get("is_key")]
        lines += ["### 重点论文", ""]
        if key_papers:
            for p in key_papers:
                s = paper_summaries.get(p["arxiv_id"], {})
                highlight = s.get("highlight") or _fallback_paper_line(p)
                cat = f" `[{s.get('category') or 'VLA'}]`" if s.get("category") else ""
                lines += [
                    f"- **{p['title']}**{cat}",
                    f"  - {highlight}",
                    f"  - {_authors(p['authors'])} · [arXiv]({p['arxiv_url']}){comment_suffix(p)}",
                    "",
                ]
        else:
            lines += ["（今日无突出重点论文）", ""]

        lines += ["### 全部论文", ""]
        non_key = [p for p in papers if not paper_summaries.get(p["arxiv_id"], {}).get("is_key")]
        if non_key:
            for p in non_key:
                s = paper_summaries.get(p["arxiv_id"], {})
                highlight = s.get("highlight") or _fallback_paper_line(p)
                lines.append(
                    f"- **{p['title']}** — {highlight} · [{p['arxiv_id']}]({p['arxiv_url']})"
                )
            lines.append("")
        else:
            lines += ["（今日全部论文均列于重点）", ""]

    lines += ["---", ""]

    # ---------- 仓库 ----------
    lines += ["## 🐙 开源仓库动态", ""]
    if not repos:
        lines += ["今日未发现新相关仓库。", ""]
    else:
        # 剔除 LLM 判定为"无关"的条目，保证列表全是 VLA/WAM 相关
        kept_repos = [r for r in repos
                      if repo_judgements.get(r["full_name"], {}).get("verdict") != "noise"]
        verdict_cn = {"source": "源码仓", "docs": "文档/汇总", "noise": "无关（已标注）"}
        # 强烈关注 + 源码仓优先
        suggested = [r for r in kept_repos
                     if repo_judgements.get(r["full_name"], {}).get("verdict") == "source"
                     and repo_judgements.get(r["full_name"], {}).get("suggest")]
        lines += ["### ⭐ 强烈建议关注", ""]
        if suggested:
            for r in suggested:
                lines += [repo_line(r, repo_judgements)]
            lines += [""]
        else:
            lines += ["（今日无强烈建议项）", ""]

        lines += ["### 新仓库 / 活跃仓库", ""]
        others = [r for r in kept_repos if r not in suggested]
        if others:
            for r in others:
                lines.append("- " + repo_line_compact(r, repo_judgements))
            lines.append("")
        else:
            lines += ["（无）", ""]

    lines += ["---", ""]

    # ---------- HF 模型 ----------
    if models:
        lines += ["## 🤗 HuggingFace 新模型", ""]
        for m in models:
            created = (m.get("createdAt") or "")[:10]
            lines.append(
                f"- [{m['model_id']}]({m['url']}) · ⬇{m.get('downloads', 0)} · 创建于 {created}"
            )
        lines += [""]

    lines += [
        "---",
        "",
        "_由 vla-wam-scout 自动生成。arXiv 数据来自 [arXiv.org](https://arxiv.org)，"
        "仓库数据来自 [GitHub](https://github.com) 与 [HuggingFace](https://huggingface.co)。_",
        "",
    ]
    return "\n".join(lines)


def _authors(authors: List[str], limit: int = 4) -> str:
    if not authors:
        return ""
    shown = authors[:limit]
    suffix = " et al." if len(authors) > limit else ""
    return ", ".join(shown) + suffix


def comment_suffix(p: dict) -> str:
    c = (p.get("comment") or "").strip()
    if not c:
        return ""
    c = c.replace("\n", " ")[:120]
    return f" · 💬 {c}"


def repo_line(r: dict, judge: Dict[str, dict]) -> str:
    j = judge.get(r["full_name"], {})
    verdict_cn = {"source": "源码仓", "docs": "文档/汇总", "noise": "无关"}.get(
        j.get("verdict", ""), "候选")
    highlight = j.get("highlight") or (r.get("description") or "（暂无摘要）")
    star = r.get("stars", 0)
    recent = "🆕新仓 " if r.get("created_recent") else ("🔄活跃 " if r.get("pushed_recent") else "")
    return (
        f"- **[{r['full_name']}]({r['html_url']})** `{verdict_cn}` `{r.get('language') or '—'}` "
        f"`⭐{star}` {recent}\n"
        f"  - {highlight}"
    )


def repo_line_compact(r: dict, judge: Dict[str, dict]) -> str:
    j = judge.get(r["full_name"], {})
    verdict_cn = {"source": "源码仓", "docs": "文档/汇总", "noise": "无关"}.get(
        j.get("verdict", ""), "候选")
    highlight = j.get("highlight") or (r.get("description") or "")
    star = r.get("stars", 0)
    return (
        f"[{r['full_name']}]({r['html_url']}) `{verdict_cn}` `{r.get('language') or '—'}` "
        f"`⭐{star}` — {highlight}"
    )


# --------------------------------------------------------------------------
# repos.md（表格格式，兼容 daily-arxiv-vla 站点的 papers.md 风格，便于后续集成）
# --------------------------------------------------------------------------
def build_repos_md(repos: List[dict], judge: Dict[str, dict], date_str: str = None) -> str:
    date_str = date_str or _cn_date()
    rows = []
    for r in repos:
        if judge.get(r["full_name"], {}).get("verdict") == "noise":
            continue  # 不把无关仓库写进数据表
        j = judge.get(r["full_name"], {})
        highlight = j.get("highlight") or (r.get("description") or "")
        verdict_cn = {"source": "源码仓", "docs": "文档/汇总", "noise": "无关"}.get(
            j.get("verdict", ""), "候选")
        suggest = "⭐" if j.get("suggest") else ""
        rows.append(
            f"| {date_str} | [{r['full_name']}]({r['html_url']}) | "
            f"{r.get('language') or '—'} | ⭐{r.get('stars', 0)} | {verdict_cn}{suggest} | "
            f"{highlight} |"
        )
    header = "| 日期 | 仓库 | 语言 | Stars | 类型 | 亮点 |"
    sep = "|------|------|------|-------|------|------|"
    return "\n".join([header, sep] + rows) + "\n"
