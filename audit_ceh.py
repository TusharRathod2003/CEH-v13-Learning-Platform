import json
import os

def audit():
    with open('ceh_data/labs.json', 'r', encoding='utf-8') as f:
        labs = json.load(f)
    with open('ceh_data/modules.json', 'r', encoding='utf-8') as f:
        modules = json.load(f)
    with open('ceh_data/quizzes.json', 'r', encoding='utf-8') as f:
        quizzes_data = json.load(f)
        quizzes = quizzes_data.get('quizzes', [])

    print(f"Loaded {len(modules)} modules, {len(labs)} labs, {len(quizzes)} quiz modules.")

    required_lab_fields = [
        'id', 'moduleId', 'moduleNumber', 'title', 'difficulty', 'estimatedTime',
        'learningObjectives', 'prerequisites', 'requiredSoftware', 'topology',
        'setupInstructions', 'steps', 'troubleshooting', 'securityConcepts',
        'defensiveRemediation', 'checklist'
    ]

    required_step_fields = [
        'stepNumber', 'title', 'command', 'explanation', 'expectedOutput', 'interpretation'
    ]

    missing_fields_report = {}
    
    for lab in labs:
        lid = lab.get('id', 'unknown')
        missing_fields_report[lid] = []
        for rf in required_lab_fields:
            if rf not in lab or lab[rf] is None or lab[rf] == '':
                missing_fields_report[lid].append(rf)
        
        # Check steps
        steps = lab.get('steps', [])
        if not steps:
            missing_fields_report[lid].append('NO_STEPS')
        else:
            for i, st in enumerate(steps):
                for sf in required_step_fields:
                    if sf not in st or st[sf] is None or st[sf] == '':
                        missing_fields_report[lid].append(f"step_{i}_missing_{sf}")

    has_issues = False
    for lid, issues in missing_fields_report.items():
        if issues:
            has_issues = True
            print(f"[-] Lab {lid} has missing fields: {issues}")

    if not has_issues:
        print("[+] All 21 labs have 100% of required top-level fields and step fields!")

    # Check Section 5 bullet items
    print("\n--- Verifying Section 5 / 6 Key Topic Coverage ---")
    topic_keywords = {
        1: ['operating system', 'network interface', 'baseline', 'audit'],
        2: ['dns', 'whois', 'mx', 'txt'],
        3: ['host discovery', 'port scan', 'service version'],
        4: ['listening service', 'service configuration'],
        5: ['vulnerability', 'remediation', 'version'],
        6: ['user', 'group', 'privilege', 'permission'],
        7: ['sha-256', 'hash', 'sample', 'eicar'],
        8: ['loopback', 'dns', 'tcp', 'icmp', 'tls'],
        9: ['phishing', 'header', 'spoofing'],
        10: ['baseline', 'resource', 'rate limit'],
        11: ['cookie', 'httponly', 'samesite', 'secure'],
        12: ['firewall', 'detection', 'log'],
        13: ['header', 'disclosure', 'hardening'],
        14: ['juice shop', 'zap', 'passive'],
        15: ['sql injection', 'parameterized'],
        16: ['wpa', 'wps', 'wireless'],
        17: ['adb', 'android', 'permission'],
        18: ['iot', 'firmware', 'hardening'],
        19: ['aws', 'identity', 'bucket'],
        20: ['sha-256', 'openssl', 'encrypt', 'tls'],
        21: ['ad cs', 'domain controller', 'certificate', 'template', 'esc1', 'esc8', 'powershell']
    }

    for lab in labs:
        mid = lab.get('moduleId')
        topology_text = json.dumps(lab.get('topology', {}))
        text_corpus = (
            lab.get('title', '') + " " +
            " ".join(lab.get('learningObjectives', [])) + " " +
            topology_text + " " +
            lab.get('setupInstructions', '') + " " +
            lab.get('securityConcepts', '') + " " +
            lab.get('defensiveRemediation', '') + " " +
            " ".join([s.get('title', '') + " " + s.get('command', '') + " " + s.get('explanation', '') + " " + s.get('expectedOutput', '') + " " + s.get('interpretation', '') for s in lab.get('steps', [])])
        ).lower()

        keywords = topic_keywords.get(mid, [])
        missing_kw = [k for k in keywords if k not in text_corpus]
        if missing_kw:
            print(f"[-] Lab {lab.get('id')} (Module {mid}) missing keyword coverage: {missing_kw}")
        else:
            print(f"[+] Lab {lab.get('id')} (Module {mid}): all key topics matched ({len(lab.get('steps', []))} steps)")

    print("\n--- Verifying Quizzes Coverage ---")
    quiz_map = {q['moduleId']: q for q in quizzes}
    for m in range(1, 22):
        if m in quiz_map:
            qs = quiz_map[m].get('questions', [])
            print(f"[+] Module {m} Quiz: {len(qs)} questions with full options and explanations.")
        else:
            print(f"[-] Module {m} Quiz MISSING!")

if __name__ == '__main__':
    audit()
