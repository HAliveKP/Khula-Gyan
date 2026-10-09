"""One small LLM client for generation, the support check and the eval judge.

It uses the OpenAI-compatible Chat Completions API, which most providers
(Groq, OpenRouter, Gemini's OpenAI-compatible endpoint, Together, a local
Ollama server) accept. Switching provider = changing .env, not code.

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


def _settings() -> tuple[str, str, str | None]:
    model = os.getenv("LLM_MODEL", "")
    key = os.getenv("LLM_API_KEY", "")
    base_url = os.getenv("LLM_BASE_URL") or None
    if not model or model == "choose-with-team" or not key:
        raise RuntimeError(
            "LLM is not configured. Set LLM_MODEL, LLM_API_KEY (and LLM_BASE_URL "
            "if your provider needs it) in .env."
        )
    return model, key, base_url


def _cache_path(model: str, messages: list[dict], json_mode: bool, temperature: float) -> Path:
    raw = json.dumps([model, messages, json_mode, temperature], ensure_ascii=False, sort_keys=True)
    return CACHE_DIR / (hashlib.sha256(raw.encode("utf-8")).hexdigest() + ".json")


def complete(
    messages: list[dict],
    json_mode: bool = True,
    temperature: float = 0.0,
    use_cache: bool = True,
    max_retries: int = 3,
) -> str:
    """Send chat messages and return the model's text reply."""
    if os.getenv("LLM_PROVIDER", "").lower() == "fake":
        from .fake_llm import fake_complete
        return fake_complete(messages)

    model, key, base_url = _settings()

    path = _cache_path(model, messages, json_mode, temperature)
    if use_cache and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["text"]

    from openai import OpenAI  # imported here so tests can run without a key

    client = OpenAI(api_key=key, base_url=base_url)
    kwargs = {"model": model, "messages": messages, "temperature": temperature}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    last_error = None
    for attempt in range(max_retries):
        try:
            reply = client.chat.completions.create(**kwargs)
            text = reply.choices[0].message.content or ""
            break
        except Exception as err:  # rate limit, timeout, unsupported JSON mode
            last_error = err
            if "response_format" in kwargs and "response_format" in str(err):
                kwargs.pop("response_format")  # provider has no JSON mode; rely on the prompt
                continue
            time.sleep(2 ** attempt)
    else:
        raise RuntimeError(f"LLM call failed after {max_retries} tries: {last_error}")

    if use_cache:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"text": text}, ensure_ascii=False), encoding="utf-8")
    return text
