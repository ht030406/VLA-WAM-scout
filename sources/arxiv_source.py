# -*- coding: utf-8 -*-
"""arXiv 论文拉取：按 VLA/WAM 关键词查询，返回近 LOOKBACK_DAYS 天提交的论文。"""
import html
import re
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

import requests

import config

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

# 与机器人/VLA/WM 相关的 arXiv 类目前缀；其余（天文、物理、数学等）剔除
RELEVANT_ARXIV_CATEGORY_PREFIXES = (
    "cs.RO", "cs.AI", "cs.CV", "cs.LG", "cs.NE", "cs.CL", "cs.MA",
    "eess.SY", "eess.IV", "stat.ML",
)

def _relevant_categories(categories: List[str]) -> bool:
    """类目命中任一相关前缀即认为相关（无类目信息的保留）。"""
    if not categories:
        return True
    return any(c.startswith(prefix) for c in categories for prefix in RELEVANT_ARXIV_CATEGORY_PREFIXES)


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def _parse_entry(entry: ET.Element) -> Dict[str, Any]:
    def tag(name: str) -> str:
        el = entry.find(f"atom:{name}", NS)
        return _strip_html(el.text) if el is not None and el.text else ""

    arxiv_id = re.sub(r"^http://arxiv.org/abs/|^https://arxiv.org/abs/|v\d+$", "", tag("id"))
    authors = [a.text or "" for a in entry.findall("atom:author/atom:name", NS)]
    published = tag("published")
    updated = tag("updated")

    categories = [c.get("term", "") for c in entry.findall("atom:category", NS)]

    # 提取 comment（如是否开源/项目主页）
    comment = ""
    for el in entry.findall("arxiv:comment", NS):
        if el.text:
            comment = _strip_html(el.text)
            break

    return {
        "arxiv_id": arxiv_id,
        "title": tag("title"),
        "abstract": tag("summary"),
        "authors": authors,
        "published": published,
        "updated": updated,
        "categories": categories,
        "comment": comment,
        "arxiv_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
    }


def _within_window(iso_date: str, window_days: int) -> bool:
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    except Exception:
        return False
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    return dt >= cutoff


def fetch_papers(lookback_days: int = None) -> List[Dict[str, Any]]:
    """拉取近 lookback_days 天的 VLA/WAM 论文，按提交时间倒序。

    若窗口内为空，自动扩大窗口（2x、3x、…7 天），保证每日都有产出。
    """
    lookback_days = lookback_days or config.LOOKBACK_DAYS
    attempts = [lookback_days] + [d for d in (lookback_days * 2, lookback_days * 3, 7, 14)
                                  if d != lookback_days]
    last_good = []
    for window in attempts:
        papers = _fetch_window(window)
        if papers:
            print(f"  [arxiv] window={window}d -> {len(papers)} 篇论文")
            return papers
        last_good = papers
    return last_good


def _fetch_window(lookback_days: int) -> List[Dict[str, Any]]:
    query = urllib.parse.quote(config.ARXIV_QUERY)
    papers: List[Dict[str, Any]] = []

    start = 0
    while len(papers) < config.ARXIV_MAX_RESULTS:
        url = (
            f"{config.ARXIV_API}?search_query={query}"
            f"&start={start}&max_results={config.ARXIV_PAGE_SIZE}"
            f"&sortBy=submittedDate&sortOrder=descending"
        )
        r = requests.get(url, timeout=config.ARXIV_TIMEOUT,
                         headers={"User-Agent": "vla-wam-scout/0.1"})
        r.raise_for_status()
        root = ET.fromstring(r.content)
        entries = root.findall("atom:entry", NS)
        if not entries:
            break

        # 结果按提交时间倒序：一旦某页完全落在窗口外，则停止翻页
        page_any_in_window = False
        for entry in entries:
            paper = _parse_entry(entry)
            in_window = _within_window(paper["published"], lookback_days)
            if in_window:
                page_any_in_window = True
            if in_window and _relevant_categories(paper["categories"]):
                papers.append(paper)
        if not page_any_in_window:
            break
        if len(papers) >= config.ARXIV_MAX_RESULTS:
            papers = papers[: config.ARXIV_MAX_RESULTS]
            break

        start += len(entries)
        if start >= 200:  # 防呆：最多 10 页
            break
        time.sleep(2)

    seen, dedup = set(), []
    for p in papers:
        if p["arxiv_id"] not in seen:
            seen.add(p["arxiv_id"])
            dedup.append(p)
    return dedup
