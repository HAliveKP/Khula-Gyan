import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.generation.prompt import build_messages, format_passages
from src.retrieval.search import search
from src.generation.llm import complete

results = search('नागरिकता कागजात', k=5, service='citizenship')

# Build the full prompt
messages = build_messages('नागरिकताका लागि कागजात के के चाहिन्छ?', results, 'ne')

print('Messages length:', len(messages))
print('System prompt length:', len(messages[0]['content']))
print('User prompt length:', len(messages[1]['content']))

# Test with the actual messages but in json_mode
print('\n=== Testing with json_mode ===')
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