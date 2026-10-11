import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.generation.prompt import build_messages
from src.retrieval.search import search
from src.generation.llm import complete

results = search('नागरिकता कागजात', k=2, service='citizenship')  # Only 2 passages

messages = build_messages('नागरिकताका लागि कागजात के के चाहिन्छ?', results, 'ne')

print('User prompt length:', len(messages[1]['content']))

print('\n=== Testing with json_mode (k=2) ===')
resp = complete(messages, json_mode=True)
print('Raw response:', repr(resp))

if resp.strip():
    try:
        parsed = json.loads(resp)
        print('Parsed:', json.dumps(parsed, ensure_ascii=False, indent=2))
    except json.JSONDecodeError as e:
        print('JSON decode error:', e)
else:
    print('EMPTY RESPONSE')