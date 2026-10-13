# -*- coding: utf-8 -*-
"""GitHub 仓库扫描：搜索新创建/活跃更新的 VLA/WAM 仓库，过滤出有源码、有关联意义的。"""
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import requests

import config


class GitHubSource:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/vnd.github+json"})
        if config.GITHUB_TOKEN:
            self.session.headers.update({"Authorization": f"Bearer {config.GITHUB_TOKEN}"})
        self.session.headers.update({
            "User-Agent": "vla-wam-scout/0.1",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    # ---------- 工具 ----------
    def _get(self, url: str, params: Optional[Dict] = None) -> dict:
        r = self.session.get(url, params=params, timeout=config.GITHUB_TIMEOUT)
        if r.status_code == 403 and "rate" in r.text.lower():
            print("  [github] rate limited, waiting 30s...")
            time.sleep(30)
            r = self.session.get(url, params=params, timeout=config.GITHUB_TIMEOUT)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def _date_n_days_ago(n: int) -> str:
        return (datetime.now(timezone.utc) - timedelta(days=n)).strftime("%Y-%m-%d")

    # ---------- 搜索 ----------
    def _search(self, q: str, per_page: int) -> List[dict]:
        """执行一次 GitHub 仓库搜索，返回 items。"""
        try:
            data = self._get(f"{config.GITHUB_API}/search/repositories",
                             params={"q": q, "sort": "stars", "order": "desc",
                                     "per_page": per_page})
        except requests.RequestException as e:
            print(f"  [github] search failed for q={q!r}: {e}")
            return []
        return data.get("items", [])

    def search_new_and_active(self, lookback_days: int = None) -> List[Dict]:
        """合并多组查询，去重并按 人气/新鲜度 排序。"""
        lookback_days = lookback_days or config.LOOKBACK_DAYS
        date_cutoff = self._date_n_days_ago(lookback_days)
        date_push_cutoff = self._date_n_days_ago(lookback_days)  # 活跃只看近 N 天

        candidates: Dict[str, dict] = {}
        for template in config.GITHUB_QUERIES:
            q = template.format(date=date_cutoff, VLA="VLA")
            items = self._search(q, config.GITHUB_SEARCH_PER_PAGE)
            print(f"  [github] q={q!r} -> {len(items)} results")
            for it in items:
                full_name = it.get("full_name", "")
                if not full_name or it.get("archived"):
                    continue
                cand = candidates.setdefault(full_name, it)
                # 合并时保持最高 star
                if (it.get("stargazers_count") or 0) > (cand.get("stargazers_count") or 0):
                    candidates[full_name] = it
            time.sleep(1.2)  # 搜索 API 限速（无 token 时 10 req/min）

        # 过滤硬门槛
        kept: List[dict] = []
        for it in candidates.values():
            if not self._passes_gate(it, date_push_cutoff):
                continue
            repo = self._enrich(it)
            if repo:
                kept.append(repo)

        # 排序：stars 为主，等权时新仓库靠 created/pushed 新鲜度
        kept.sort(key=lambda r: (
            r["stars"],
            r.get("created_recent", False),
        ), reverse=True)
        return kept[: config.GITHUB_MAX_REPOS]

    # ---------- 过滤 ----------
    def _passes_gate(self, it: dict, date_push_cutoff: str) -> bool:
        """是否值得进入候选：非 fork、语言合法、描述/名称含相关词或近期活跃。"""
        if it.get("fork"):
            return False
        lang = it.get("language") or ""
        if lang in config.GITHUB_SKIP_LANGS and not it.get("description"):
            return False
        return True

    def _enrich(self, it: dict) -> Optional[Dict]:
        """补充 README 摘录与相关性字段；无关仓库剔除。"""
        full_name = it["full_name"]
        readme_snippet, readme_lang = self._fetch_readme(full_name)
        hay = " ".join([
            (it.get("name") or ""),
            (it.get("description") or ""),
            " ".join(it.get("topics") or []),
            readme_snippet.lower(),
        ]).lower()

        # 相关性：名字/描述/README 命中相关词才保留
        if not any(hit in hay for hit in config.RELEVANCE_HARD_HITS):
            return None

        created_at = it.get("created_at") or ""
        pushed_at = it.get("pushed_at") or ""
        recent = lambda s: s >= self._date_n_days_ago(config.LOOKBACK_DAYS) + "T00:00:00Z"

        return {
            "full_name": full_name,
            "html_url": it.get("html_url", f"https://github.com/{full_name}"),
            "description": (it.get("description") or "").strip(),
            "language": it.get("language") or "",
            "stars": it.get("stargazers_count") or 0,
            "forks": it.get("forks_count") or 0,
            "open_issues": it.get("open_issues_count") or 0,
            "topics": it.get("topics") or [],
            "created_at": created_at,
            "pushed_at": pushed_at,
            "license": (it.get("license") or {}).get("spdx_id") or "",
            "created_recent": recent(created_at),
            "pushed_recent": recent(pushed_at),
            "readme_snippet": readme_snippet,
            "readme_lang": readme_lang,
        }

    def _fetch_readme(self, full_name: str) -> tuple:
        """返回 (README 前 1200 字符, 语言)；失败则 ('', '')。"""
        for branch in ("HEAD", "main", "master"):
            url = f"https://raw.githubusercontent.com/{full_name}/{branch}/README.md"
            try:
                r = self.session.get(url, timeout=15)
                if r.status_code == 200 and r.text.strip():
                    text = r.text.replace("\r", "")[:1200]
                    return text, "markdown"
            except requests.RequestException:
                continue
        return "", ""


def fetch_repos(lookback_days: int = None) -> List[Dict]:
    return GitHubSource().search_new_and_active(lookback_days)
