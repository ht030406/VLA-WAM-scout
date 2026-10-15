# -*- coding: utf-8 -*-
"""vla-wam-scout 配置：数据源关键词、API 端点、环境变量读取。"""
import os
from pathlib import Path

# ---------- 路径 ----------
PROJECT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# ---------- 环境变量（.env 或系统环境） ----------
def _load_dotenv():
    env_file = PROJECT_DIR / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

_load_dotenv()

def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)

# ---------- LLM（OpenAI 兼容） ----------
# 默认 ModelScope 公网推理接口（GitHub Actions runner 可访问）；
# 兼容旧配置名 LINGSHU_*；如用灵枢需提供其公网网关域名（内网域名 runner 无法解析）。
LLM_BASE_URL = env("LLM_BASE_URL") or env("LINGSHU_BASE_URL") or "https://api-inference.modelscope.cn/v1/"
LLM_API_KEY = env("LLM_API_KEY") or env("LINGSHU_API_KEY") or env("DEEPSEEK_API_KEY", "")
LLM_MODEL = env("LLM_MODEL") or env("LINGSHU_MODEL") or "deepseek-ai/DeepSeek-V4.1-Flash"
# 备用模型（逗号分隔）：主模型失败/限流时依次尝试
LLM_FALLBACK_MODELS = [m.strip() for m in env("LLM_FALLBACK_MODELS", "").split(",") if m.strip()]
# 自定义 CA 证书：仅内部网关（如灵枢）需要；默认空 = 系统证书（公网端点）
CA_CERT_FILE = env("CA_CERT_FILE", "").strip()
LLM_MAX_TOKENS = int(env("LLM_MAX_TOKENS", "2000"))
LLM_TEMPERATURE = float(env("LLM_TEMPERATURE", "0.3"))

# ---------- GitHub ----------
GITHUB_TOKEN = env("GITHUB_TOKEN", "")
GITHUB_API = "https://api.github.com"

# ---------- 回看窗口（天） ----------
LOOKBACK_DAYS = int(env("LOOKBACK_DAYS", "2"))

# ---------- arXiv 查询 ----------
# 与 daily-arxiv-vla 仓库默认关键词保持一致，并扩充 world model 相关表达
ARXIV_QUERY = (
    'all:"VLA" OR all:"Vision-Language-Action" OR all:"World Action Model" '
    'OR all:"World-Action Model" OR all:"action world model" OR '
    'all:"world model" AND all:"robot" OR all:"world modeling" AND all:"action"'
)
ARXIV_MAX_RESULTS = int(env("ARXIV_MAX_RESULTS", "60"))
ARXIV_PAGE_SIZE = int(env("ARXIV_PAGE_SIZE", "20"))
ARXIV_API = "https://export.arxiv.org/api/query"
ARXIV_TIMEOUT = int(env("ARXIV_TIMEOUT", "40"))

# ---------- GitHub 仓库搜索 ----------
# 每组查询会分别搜索，随后合并去重过滤；{date} 为回看窗口起始日期
GITHUB_QUERIES = [
    # 新创建：近 LOOKBACK_DAYS 天内创建
    '"{VLA}" created:>{date}',
    '"vision language action" created:>{date}',
    '"vision-language-action" created:>{date}',
    '"world-model" created:>{date}',
    '"world model" created:>{date} robot',
    '"world action model" created:>{date}',
    # 活跃更新：近 LOOKBACK_DAYS 天内有 push（含老项目新动态）
    '"{VLA}" pushed:>{date}',
    '"vision-language-action" pushed:>{date}',
    '"world model" robot pushed:>{date}',
    '"world action model" pushed:>{date}',
]
GITHUB_SEARCH_PER_PAGE = int(env("GITHUB_SEARCH_PER_PAGE", "12"))
GITHUB_MAX_REPOS = int(env("GITHUB_MAX_REPOS", "25"))
GITHUB_TIMEOUT = int(env("GITHUB_TIMEOUT", "30"))
# 判定"有意义"的最低硬门槛（字符串关键词命中 README/描述，否则过滤）
GITHUB_MIN_STARS = int(env("GITHUB_MIN_STARS", "0"))
# 忽略的纯文档/非代码语言
GITHUB_SKIP_LANGS = {"HTML", "CSS", "TeX", "Jupyter Notebook"}
# 硬性相关词：命中则保留（README 摘录里出现）
RELEVANCE_HARD_HITS = [
    "vla", "vision-language-action", "vision language action",
    "world-action", "world action model", "world model", "action world model",
    "action-conditioned world model", "robot foundation model",
    "physical intelligence", "embodied",
]

# ---------- HuggingFace ----------
HF_API = "https://huggingface.co/api"
HF_MAX_MODELS = int(env("HF_MAX_MODELS", "25"))
HF_TIMEOUT = int(env("HF_TIMEOUT", "30"))
HF_SEARCH_TERMS = ["vla", "vision language action", "world model", "world-action", "embodied"]
