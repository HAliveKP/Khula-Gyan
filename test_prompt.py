import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.generation.prompt import build_prompt
from src.retrieval.search import search

results = search('नागरिकता कागजात', k=5, service='citizenship')
prompt = build_prompt('नागरिकताका लागि कागजात के के चाहिन्छ?', results, lang='ne')
print('=== PROMPT ===')
for m in prompt:
    content = m['content']
    if len(content) > 500:
        content = content[:500] + '...'
    print(f'{m["role"]}: {content}')