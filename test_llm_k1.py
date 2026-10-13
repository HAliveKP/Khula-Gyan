import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.generation.prompt import format_passages
from src.retrieval.search import search
from src.generation.llm import complete

results = search('नागरिकता कागजात', k=1, service='citizenship')

# Build passages
passages_text = format_passages(results)
print('Passages length:', len(passages_text))

# Build minimal messages
messages = [
    {"role": "system", "content": """You are Khula Gyan. Reply with JSON only:
{"status": "answered", "answer": "2-4 sentences", "checklist": {"documents": [], "fees": [], "steps": [], "where": ""}, "citations": [{"passage": 1, "quote": "exact words"}], "confidence": "high"}"""},
    {"role": "user", "content": passages_text + "\n\nQUESTION: नागरिकताका लागि कागजात के के चाहिन्छ?"}
]

print('Total prompt length:', len(messages[0]['content']) + len(messages[1]['content']))

resp = complete(messages, json_mode=True)
print('Response:', repr(resp))

if resp.strip():
    try:
        parsed = json.loads(resp)
        print('Parsed:', json.dumps(parsed, ensure_ascii=False, indent=2))
    except json.JSONDecodeError as e:
        print('JSON decode error:', e)
else:
    print('EMPTY RESPONSE')