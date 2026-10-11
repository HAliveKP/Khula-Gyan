import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.generation.llm import complete

# Test with very simple prompt
simple_messages = [
    {"role": "system", "content": "Reply with JSON only: {\"status\": \"answered\", \"answer\": \"test\"}"},
    {"role": "user", "content": "Reply with the JSON object."}
]

print('=== Test 1: Simple JSON ===')
resp = complete(simple_messages, json_mode=True)
print('Response:', repr(resp))

# Test 2: With our system prompt but minimal user content
our_system = """You are Khula Gyan. Reply with JSON only:
{"status": "answered", "answer": "2-4 sentences", "checklist": {"documents": [], "fees": [], "steps": [], "where": ""}, "citations": [{"passage": 1, "quote": "exact words"}], "confidence": "high"}"""

simple_messages2 = [
    {"role": "system", "content": our_system},
    {"role": "user", "content": "Test question. Reply with the JSON object."}
]

print('\n=== Test 2: Our system prompt ===')
resp = complete(simple_messages2, json_mode=True)
print('Response:', repr(resp))

# Test 3: Without json_mode
print('\n=== Test 3: Without json_mode ===')
resp = complete(simple_messages2)
print('Response:', repr(resp))