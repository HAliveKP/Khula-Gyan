import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.retrieval.search import search
from src.generation.answer import answer_with_trace

print("=== Testing Full Pipeline ===")

# Test 1: Nepali citizenship question
print("\n1. Nepali citizenship question:")
results = search('नागरिकता कागजात', k=5, service='citizenship')
print(f"   Search results: {len(results)}")
for r in results[:3]:
    print(f"   score={r['score']:.3f} page={r['page']}")

resp, trace = answer_with_trace('नागरिकताका लागि कागजात के के चाहिन्छ?', results)
print(f"   Status: {resp['status']}")
print(f"   Answer: {resp['answer'][:300]}")
print(f"   Citations: {resp['citations']}")

# Test 2: English citizenship question
print("\n2. English citizenship question:")
results = search('citizenship documents required', k=5, service='citizenship')
print(f"   Search results: {len(results)}")
for r in results[:3]:
    print(f"   score={r['score']:.3f} page={r['page']}")

resp, trace = answer_with_trace('What documents are required for citizenship?', results)
print(f"   Status: {resp['status']}")
print(f"   Answer: {resp['answer'][:300]}")
print(f"   Citations: {resp['citations']}")

# Test 3: Out of scope question
print("\n3. Out of scope question:")
results = search('who will win election', k=5, service='other')
print(f"   Search results: {len(results)}")

resp, trace = answer_with_trace('Who will win the next election?', results)
print(f"   Status: {resp['status']}")
print(f"   Reason: {trace.get('reason')}")

# Test 4: Driving license (no index yet)
print("\n4. Driving license question (no index):")
results = search('license renewal', k=5, service='driving_license')
print(f"   Search results: {len(results)}")

resp, trace = answer_with_trace('How to renew driving license?', results)
print(f"   Status: {resp['status']}")
print(f"   Reason: {trace.get('reason')}")

print("\n=== Pipeline Test Complete ===")