import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.generation.llm import complete

# Test 1: Simple non-JSON
resp = complete([{'role': 'user', 'content': 'Say hello in Nepali'}])
print('Test 1 (simple):', repr(resp))

# Test 2: JSON mode request
resp = complete([
    {'role': 'system', 'content': 'Reply with JSON only: {\"answer\": \"hello\"}'},
    {'role': 'user', 'content': 'Say hello in JSON'}
], json_mode=True)
print('Test 2 (json_mode):', repr(resp))