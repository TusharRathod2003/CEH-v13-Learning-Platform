import json

with open('ceh_data/modules.json', 'r', encoding='utf-8') as f:
    modules = json.load(f)
with open('ceh_data/labs.json', 'r', encoding='utf-8') as f:
    labs = json.load(f)
with open('ceh_data/quizzes.json', 'r', encoding='utf-8') as f:
    quizzes = json.load(f)

js_content = f"""// Auto-generated offline fallback data for CEH v13 Platform
window.OFFLINE_CEH_MODULES = {json.dumps(modules, indent=2)};
window.OFFLINE_CEH_LABS = {json.dumps(labs, indent=2)};
window.OFFLINE_CEH_QUIZZES = {json.dumps(quizzes['quizzes'], indent=2)};

// Hydrate CEHState if empty
if (window.CEHState) {{
  if (!window.CEHState.modules || window.CEHState.modules.length === 0) window.CEHState.modules = window.OFFLINE_CEH_MODULES;
  if (!window.CEHState.labs || window.CEHState.labs.length === 0) window.CEHState.labs = window.OFFLINE_CEH_LABS;
  if (!window.CEHState.quizzes || window.CEHState.quizzes.length === 0) window.CEHState.quizzes = window.OFFLINE_CEH_QUIZZES;
}}
"""

with open('ceh_data/modules.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"SUCCESS: Generated ceh_data/modules.js with {len(modules)} modules, {len(labs)} labs, and {len(quizzes['quizzes'])} quizzes.")
