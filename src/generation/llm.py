"""One small LLM client for generation, the support check and the eval judge.

It uses the OpenAI-compatible Chat Completions API, which most providers
(OpenRouter, Groq, Gemini's OpenAI-compatible endpoint, Together, a local
Ollama server) accept. Switching provider = changing .env, not code.

Several API keys (key pool)
---------------------------
Put them comma-separated in .env:  LLM_API_KEYS=key1,key2,key3
Each call uses the next key in turn (round robin). If a key is rate-limited (429)
or out of credit (402) it rests for a minute; if it is invalid (401/403) it is
skipped for the rest of the run. The SAME messages are re-sent with the next key,
so no context is lost: every call carries its full context, and the disk cache is
shared by all keys.
LLM_KEY_STRATEGY=failover makes every call start from the first key instead
(use the later keys only as backups).

Responses are cached on disk so re-running the eval does not burn quota.
"""

import hashlib
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

CACHE_DIR = Path(os.getenv("LLM_CACHE_DIR", "artifacts/llm_cache"))
REST_SECONDS = 60          # how long a rate-limited / out-of-credit key rests
MAX_WAIT_SECONDS = 60      # longest single wait when every key is resting

_next_key = 0                       # round-robin pointer, shared by all calls in this run
_rest_until: dict[str, float] = {}  # key -> time it can be used again (inf = invalid key)


def mask(key: str) -> str:
    """Never print a whole key: show only its last 4 characters."""
    return f"...{key[-4:]}" if len(key) > 8 else "***"


def api_keys() -> list[str]:
    raw = os.getenv("LLM_API_KEYS") or os.getenv("LLM_API_KEY", "")
    return [k.strip() for k in raw.split(",") if k.strip()]


def _settings() -> tuple[str, list[str], str | None]:
    model = os.getenv("LLM_MODEL", "")
    keys = api_keys()
    base_url = os.getenv("LLM_BASE_URL") or None
    if not model or model == "choose-with-team" or not keys:
        raise RuntimeError(
            "LLM is not configured. Set LLM_MODEL and LLM_API_KEYS (or LLM_API_KEY), "
            "plus LLM_BASE_URL if your provider needs it, in .env. "
            "To work without a key, set LLM_PROVIDER=fake."
        )
    return model, keys, base_url


def _make_client(key: str, base_url: str | None):
    from openai import OpenAI  # imported here so tests can run without a key
    return OpenAI(api_key=key, base_url=base_url)


def _cache_path(model: str, messages: list[dict], json_mode: bool, temperature: float) -> Path:
    # The key is NOT part of the cache name, so all keys share one cache.
    raw = json.dumps([model, messages, json_mode, temperature], ensure_ascii=False, sort_keys=True)
    return CACHE_DIR / (hashlib.sha256(raw.encode("utf-8")).hexdigest() + ".json")


def _call_with_keys(kwargs: dict, keys: list[str], base_url: str | None, max_rounds: int) -> str:
    """Try the keys in turn until one answers. Raises if every key fails."""
    global _next_key
    if os.getenv("LLM_KEY_STRATEGY", "round_robin").lower() == "failover":
        _next_key = 0
    last_error = "no key was tried"
    for round_no in range(max_rounds):
        for _ in range(len(keys)):
            key = keys[_next_key % len(keys)]
            _next_key += 1
            if _rest_until.get(key, 0) > time.time():
                continue  # this key is resting or invalid
            try:
                reply = _make_client(key, base_url).chat.completions.create(**kwargs)
                return reply.choices[0].message.content or ""
            except Exception as err:  # rate limit, no credit, bad key, timeout, no JSON mode
                status = getattr(err, "status_code", None)
                last_error = f"{type(err).__name__} (status {status}) on key {mask(key)}"
                if "response_format" in kwargs and "response_format" in str(err):
                    kwargs.pop("response_format")  # provider has no JSON mode; rely on the prompt
                    _next_key -= 1                 # retry the same key without it
                elif status in (401, 403):
                    _rest_until[key] = float("inf")  # invalid key: skip for this run
                elif status in (402, 429):
                    _rest_until[key] = time.time() + REST_SECONDS
                # other errors (timeouts, 5xx): just move on to the next key
        usable = [t for k, t in _rest_until.items() if k in keys and t != float("inf")]
        if all(_rest_until.get(k) == float("inf") for k in keys):
            break  # every key is invalid; waiting will not help
        soonest = min(usable, default=0) - time.time()
        time.sleep(min(MAX_WAIT_SECONDS, max(2 ** round_no, soonest)))
    raise RuntimeError(f"LLM call failed on all {len(keys)} key(s). Last error: {last_error}")


def complete(
    messages: list[dict],
    json_mode: bool = True,
    temperature: float = 0.0,
    use_cache: bool = True,
    max_rounds: int = 4,
) -> str:
    """Send chat messages and return the model's text reply."""
    if os.getenv("LLM_PROVIDER", "").lower() == "fake":
        from .fake_llm import fake_complete
        return fake_complete(messages)

    model, keys, base_url = _settings()

    path = _cache_path(model, messages, json_mode, temperature)
    if use_cache and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["text"]

    kwargs = {"model": model, "messages": messages, "temperature": temperature}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    text = _call_with_keys(kwargs, keys, base_url, max_rounds)

    if use_cache:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"text": text}, ensure_ascii=False), encoding="utf-8")
    return text
