import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.generation.prompt import build_messages
from src.retrieval.search import search
from src.generation.llm import complete

results = search('नागरिकता कागजात', k=5, service='citizenship')
messages = build_messages('नागरिकताका लागि कागजात के के चाहिन्छ?', results, 'ne')

print('=== MESSAGES TO LLM ===')
for m in messages:
    content = m['content']
    if len(content) > 800:
        content = content[:800] + '...'
    print(f'{m["role"]}: {content}')

print('\n=== CALLING LLM ===')
resp = complete(messages)
print('Raw response:', repr(resp))
print('Parsed:', json.loads(resp) if resp.strip() else 'EMPTY')