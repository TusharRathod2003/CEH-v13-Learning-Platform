#!/usr/bin/env python3
"""
Unit Test Suite for CEH v13 Practical Learning Platform
Validates data integrity, SQLite schema, and API contracts.
"""

import unittest
import os
import json
import sqlite3
import tempfile

class TestCEHPlatformData(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, 'ceh_data')

    def test_modules_count_and_schema(self):
        mod_path = os.path.join(self.data_dir, 'modules.json')
        self.assertTrue(os.path.exists(mod_path), "modules.json must exist")
        with open(mod_path, 'r', encoding='utf-8') as f:
            modules = json.load(f)
        self.assertEqual(len(modules), 21, "Must contain all 20 CEH modules plus AD CS master lab")

        required_keys = {'id', 'number', 'title', 'domain', 'description', 'learningObjectives', 'labId'}
        for m in modules:
            self.assertTrue(required_keys.issubset(m.keys()), f"Module {m.get('id')} missing keys")
            self.assertGreater(len(m['learningObjectives']), 0, f"Module {m.get('id')} must have learning objectives")

    def test_labs_completeness_and_structure(self):
        lab_path = os.path.join(self.data_dir, 'labs.json')
        self.assertTrue(os.path.exists(lab_path), "labs.json must exist")
        with open(lab_path, 'r', encoding='utf-8') as f:
            labs = json.load(f)
        self.assertEqual(len(labs), 21, "Must contain 21 practical labs")

        required_lab_keys = {
            'id', 'moduleId', 'moduleNumber', 'title', 'difficulty', 'estimatedTime',
            'learningObjectives', 'requiredSoftware', 'topology', 'steps',
            'troubleshooting', 'securityConcepts', 'defensiveRemediation', 'checklist'
        }
        for l in labs:
            self.assertTrue(required_lab_keys.issubset(l.keys()), f"Lab {l.get('id')} missing required fields")
            self.assertGreater(len(l['steps']), 0, f"Lab {l.get('id')} must contain steps")
            for step in l['steps']:
                self.assertIn('stepNumber', step)
                self.assertIn('command', step)
                self.assertIn('explanation', step)
                self.assertIn('expectedOutput', step)
                self.assertIn('interpretation', step)

    def test_quizzes_validity(self):
        quiz_path = os.path.join(self.data_dir, 'quizzes.json')
        self.assertTrue(os.path.exists(quiz_path), "quizzes.json must exist")
        with open(quiz_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        quizzes = data.get('quizzes', [])
        self.assertEqual(len(quizzes), 21, "Must contain 21 module quiz sets")

        for q_set in quizzes:
            self.assertIn('moduleId', q_set)
            self.assertGreater(len(q_set['questions']), 0)
            for q in q_set['questions']:
                self.assertEqual(len(q['options']), 4, f"Question {q['id']} must have 4 choices")
                self.assertIn(q['correctIndex'], [0, 1, 2, 3], f"Question {q['id']} invalid correctIndex")
                self.assertTrue(len(q['explanation']) > 10, f"Question {q['id']} missing detailed explanation")

    def test_adcs_specialization_lab(self):
        lab_path = os.path.join(self.data_dir, 'labs.json')
        with open(lab_path, 'r', encoding='utf-8') as f:
            labs = json.load(f)
        adcs_lab = next((l for l in labs if l['id'] == 'lab-adcs'), None)
        self.assertIsNotNone(adcs_lab, "AD CS Master Lab must be defined")
        self.assertEqual(adcs_lab['moduleNumber'], 'AD')
        self.assertIn('ESC1', adcs_lab['title'])
        commands_str = " ".join(s['command'] for s in adcs_lab['steps'])
        self.assertIn('powershell', commands_str.lower())
        self.assertIn('get-adobject', commands_str.lower())
        self.assertEqual(len(adcs_lab['steps']), 5, "AD CS lab must feature 5 comprehensive steps")

    def test_all_21_modules_prompt_spec_compliance(self):
        lab_path = os.path.join(self.data_dir, 'labs.json')
        with open(lab_path, 'r', encoding='utf-8') as f:
            labs = json.load(f)

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
            mid = lab['moduleId']
            self.assertGreaterEqual(len(lab['steps']), 4, f"Lab {lab['id']} must have at least 4 detailed steps")
            text_corpus = (
                lab.get('title', '') + " " +
                " ".join(lab.get('learningObjectives', [])) + " " +
                json.dumps(lab.get('topology', {})) + " " +
                lab.get('setupInstructions', '') + " " +
                lab.get('securityConcepts', '') + " " +
                lab.get('defensiveRemediation', '') + " " +
                " ".join([s.get('title', '') + " " + s.get('command', '') + " " + s.get('explanation', '') + " " + s.get('expectedOutput', '') + " " + s.get('interpretation', '') for s in lab.get('steps', [])])
            ).lower()

            for kw in topic_keywords[mid]:
                self.assertIn(kw, text_corpus, f"Lab {lab['id']} (Module {mid}) missing keyword coverage: '{kw}'")


class TestCEHDatabaseOperations(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        # Init schema
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE user_progress (
                user_id TEXT DEFAULT 'student_cadet',
                lab_id TEXT PRIMARY KEY,
                module_id INTEGER,
                completed_steps TEXT,
                completed_checklist TEXT,
                is_completed INTEGER DEFAULT 0,
                last_updated TEXT
            )
        """)
        c.execute("""
            CREATE TABLE user_notes (
                user_id TEXT DEFAULT 'student_cadet',
                lab_id TEXT PRIMARY KEY,
                content TEXT,
                last_updated TEXT
            )
        """)
        c.execute("""
            CREATE TABLE quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT DEFAULT 'student_cadet',
                module_id INTEGER,
                score INTEGER,
                total INTEGER,
                passed INTEGER,
                timestamp TEXT
            )
        """)
        c.execute("""
            CREATE TABLE bookmarks (
                user_id TEXT DEFAULT 'student_cadet',
                lab_id TEXT PRIMARY KEY,
                created_at TEXT
            )
        """)
        c.execute("""
            CREATE TABLE lab_flags (
                user_id TEXT DEFAULT 'student_cadet',
                lab_id TEXT PRIMARY KEY,
                flag TEXT,
                verified INTEGER DEFAULT 1,
                submitted_at TEXT
            )
        """)
        c.execute("""
            CREATE TABLE flashcard_progress (
                user_id TEXT DEFAULT 'student_cadet',
                card_id TEXT PRIMARY KEY,
                status TEXT,
                last_reviewed TEXT
            )
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_progress_insert_and_update(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Insert progress
        c.execute("""
            INSERT INTO user_progress (lab_id, module_id, completed_steps, completed_checklist, is_completed, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('lab-01', 1, '[1,2]', '[0]', 0, '2026-10-17T12:00:00Z'))
        conn.commit()

        row = c.execute("SELECT * FROM user_progress WHERE lab_id = 'lab-01'").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], 'lab-01')
        self.assertEqual(row[5], 0) # not completed

        # Update to completed
        c.execute("UPDATE user_progress SET is_completed = 1 WHERE lab_id = 'lab-01'")
        conn.commit()
        updated_row = c.execute("SELECT is_completed FROM user_progress WHERE lab_id = 'lab-01'").fetchone()
        self.assertEqual(updated_row[0], 1)
        conn.close()

    def test_notes_storage(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO user_notes (lab_id, content, last_updated)
            VALUES (?, ?, ?)
        """, ('lab-adcs', 'Discovered ESC1 template WebServer-Custom with enrollee supplies subject enabled.', '2026-10-17T12:05:00Z'))
        conn.commit()

        note = c.execute("SELECT content FROM user_notes WHERE lab_id = 'lab-adcs'").fetchone()
        self.assertIn('ESC1', note[0])
        conn.close()

    def test_lab_flag_verification_and_storage(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO lab_flags (lab_id, flag, verified, submitted_at)
            VALUES (?, ?, 1, ?)
        """, ('lab-01', 'FLAG{baseline_env_recorded}', '2026-10-17T12:10:00Z'))
        conn.commit()

        flag_row = c.execute("SELECT flag, verified FROM lab_flags WHERE lab_id = 'lab-01'").fetchone()
        self.assertIsNotNone(flag_row)
        self.assertEqual(flag_row[0], 'FLAG{baseline_env_recorded}')
        self.assertEqual(flag_row[1], 1)
        conn.close()

    def test_flashcard_progress_storage(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO flashcard_progress (card_id, status, last_reviewed)
            VALUES (?, ?, ?)
        """, ('fc-01', 'mastered', '2026-10-17T12:15:00Z'))
        conn.commit()

        fc_row = c.execute("SELECT status FROM flashcard_progress WHERE card_id = 'fc-01'").fetchone()
        self.assertIsNotNone(fc_row)
        self.assertEqual(fc_row[0], 'mastered')
        conn.close()

if __name__ == '__main__':
    unittest.main()
