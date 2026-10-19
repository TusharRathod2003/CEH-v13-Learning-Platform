import json

for fname in ['ceh_data/modules.json', 'ceh_data/quizzes.json', 'ceh_data/labs.json']:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"OK: {fname}")
    except Exception as e:
        print(f"FAILED: {fname} -> {e}")
