# -*- coding: utf-8 -*-
"""跨日去重状态：记录已报道条目，避免每日报告重复。

state.json 结构与示例：
{
  "papers": {"2610.13945": "2026-10-13"},
  "repos":  {"NVlabs/LongLive": {"last": "2026-10-13", "stars": 2768}},
  "models": {"org/my-embodied-ai": "2026-10-13"}
}
"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import config

STATE_FILE = config.REPORTS_DIR / "state.json"

# 去重窗口（天）：窗口内已报道的条目不再重复出现
DEDUP_DAYS_PAPER = int(config.env("DEDUP_DAYS_PAPER", "14"))
DEDUP_DAYS_REPO = int(config.env("DEDUP_DAYS_REPO", "7"))
DEDUP_DAYS_MODEL = int(config.env("DEDUP_DAYS_MODEL", "30"))
# star 飙升阈值（相对增长或绝对增长任一满足即"重新报道"）
STAR_SURGE_REL = float(config.env("STAR_SURGE_REL", "0.5"))
STAR_SURGE_ABS = int(config.env("STAR_SURGE_ABS", "200"))


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _within_cutoff(last_date: str, today: str, days: int) -> bool:
    """last_date 是否在 today 往前 days 天内（含边界）。"""
    if not last_date:
        return False
    try:
        last = datetime.strptime(last_date, "%Y-%m-%d").date()
        t = datetime.strptime(today, "%Y-%m-%d").date()
    except ValueError:
        return False
    return (t - last).days <= days


class StateStore:
    def __init__(self, path: Path = None):
        self.path = path or STATE_FILE
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"papers": {}, "repos": {}, "models": {}}

    def save(self):
        self.path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---------- 查询：区分新增 / 重复 / 飙升 ----------
    def split_papers(self, papers: List[dict], today: str = None) -> Tuple[List[dict], List[dict]]:
        today = today or _today()
        new, dup = [], []
        for p in papers:
            aid = p["arxiv_id"]
            last = self.data["papers"].get(aid)
            if last and _within_cutoff(last, today, DEDUP_DAYS_PAPER):
                dup.append(p)
            else:
                new.append(p)
        return new, dup

    def split_repos(self, repos: List[dict], today: str = None) -> Tuple[List[dict], List[dict], List[dict]]:
        """返回 (新增, 重复, 飙升重报)。飙升条目已打上 _surge 标记。"""
        today = today or _today()
        new, dup, surge = [], [], []
        for r in repos:
            name = r["full_name"]
            rec = self.data["repos"].get(name)
            stars = r.get("stars") or 0
            if not rec:
                new.append(r)
                continue
            last = rec.get("last", "")
            if _within_cutoff(last, today, DEDUP_DAYS_REPO):
                old_stars = rec.get("stars") or 0
                if stars >= old_stars + STAR_SURGE_ABS or (
                        old_stars > 0 and stars >= old_stars * (1.0 + STAR_SURGE_REL)):
                    r["_surge"] = True
                    surge.append(r)
                else:
                    dup.append(r)
            else:
                new.append(r)
        return new, dup, surge

    def split_models(self, models: List[dict], today: str = None) -> Tuple[List[dict], List[dict]]:
        today = today or _today()
        new, dup = [], []
        for m in models:
            mid = m["model_id"]
            last = self.data["models"].get(mid)
            if last and _within_cutoff(last, today, DEDUP_DAYS_MODEL):
                dup.append(m)
            else:
                new.append(m)
        return new, dup

    # ---------- 报道后登记 ----------
    def mark_papers(self, papers: List[dict], today: str = None):
        today = today or _today()
        for p in papers:
            self.data["papers"][p["arxiv_id"]] = today

    def mark_repos(self, repos: List[dict], today: str = None):
        today = today or _today()
        for r in repos:
            self.data["repos"][r["full_name"]] = {
                "last": today,
                "stars": r.get("stars") or 0,
            }

    def mark_models(self, models: List[dict], today: str = None):
        today = today or _today()
        for m in models:
            self.data["models"][m["model_id"]] = today


def summarize_dedup(state: StateStore, papers_all: List[dict], repos_all: List[dict],
                    models_all: List[dict]) -> dict:
    """统计本次运行新增/重复数量（用于日报头部展示）。"""
    today = _today()
    np_, dp_ = state.split_papers(papers_all, today)
    nr, dr, sr = state.split_repos(repos_all, today)
    nm, dm = state.split_models(models_all, today)
    return {
        "papers_all": len(papers_all), "papers_new": len(np_), "papers_dup": len(dp_),
        "repos_all": len(repos_all), "repos_new": len(nr), "repos_dup": len(dr),
        "repos_surge": len(sr), "models_all": len(models_all),
        "models_new": len(nm), "models_dup": len(dm),
    }
