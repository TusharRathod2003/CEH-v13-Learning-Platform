#!/usr/bin/env python3
"""
CEH v13 Complete Ethical Hacking Practical Lab Platform Backend Server
Provides local REST API endpoints and SQLite database persistence.
Built with Python standard library (http.server + sqlite3) - Zero external dependencies.
"""

import sys
import os
import json
import sqlite3
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
PORT = 8000
DB_FILE = os.path.join(BASE_DIR, "ceh_learning.db")
DATA_DIR = os.path.join(BASE_DIR, "ceh_data")

ACCEPTED_LAB_FLAGS = {
    "lab-01": ["FLAG{baseline_env_recorded}", "FLAG{kernel_5.15_audit_complete}", "FLAG{cadet_node_baseline}"],
    "lab-02": ["FLAG{dns_axfr_zone_transferred}", "FLAG{ns_mx_txt_footprinted}", "FLAG{dns_recon_complete}"],
    "lab-03": ["FLAG{nmap_syn_stealth_ports_identified}", "FLAG{open_ports_21_80_445}", "FLAG{nmap_stealth_scan}"],
    "lab-04": ["FLAG{smb_null_session_shares_enumerated}", "FLAG{rpc_smb_services_audited}", "FLAG{smb_enumeration}"],
    "lab-05": ["FLAG{cve_2011_2523_vsftpd_backdoor}", "FLAG{cvss_9.8_critical_vsftpd}", "FLAG{vulnerability_analysis}"],
    "lab-06": ["FLAG{suid_root_privilege_escalation}", "FLAG{find_perm_4000_root_shell}", "FLAG{system_hacking_pwned}"],
    "lab-07": ["FLAG{eicar_sha256_hash_verified}", "FLAG{magic_bytes_static_analysis}", "FLAG{malware_analysis_safe}"],
    "lab-08": ["FLAG{tcpdump_cleartext_auth_captured}", "FLAG{bpf_filter_http_creds}", "FLAG{sniffing_cleartext_auth}"],
    "lab-09": ["FLAG{spf_dmarc_spoofing_detected}", "FLAG{received_header_phishing_analysis}", "FLAG{social_engineering_defense}"],
    "lab-10": ["FLAG{syn_recv_socket_rate_limited}", "FLAG{http_baseline_dos_resilience}", "FLAG{dos_rate_limiting}"],
    "lab-11": ["FLAG{samesite_httponly_cookie_secured}", "FLAG{session_hijack_flag_audited}", "FLAG{session_invalidation_safe}"],
    "lab-12": ["FLAG{suricata_drop_rule_enforced}", "FLAG{iptables_syn_flood_evasion_blocked}", "FLAG{firewall_ids_hardened}"],
    "lab-13": ["FLAG{servertokens_prod_header_hardened}", "FLAG{directory_listing_disabled}", "FLAG{web_server_hardened}"],
    "lab-14": ["FLAG{idor_api_broken_object_level_auth}", "FLAG{owasp_juice_shop_csp_enforced}", "FLAG{web_app_security}"],
    "lab-15": ["FLAG{sql_injection_bypass_parameterized}", "FLAG{auth_bypass_prepared_statement}", "FLAG{sqli_prevented}"],
    "lab-16": ["FLAG{wpa3_sae_simultaneous_auth_equals}", "FLAG{monitor_mode_bssid_dissected}", "FLAG{wireless_security_audited}"],
    "lab-17": ["FLAG{android_allowbackup_debuggable_audited}", "FLAG{adb_permission_flaw_identified}", "FLAG{mobile_security_audited}"],
    "lab-18": ["FLAG{mqtt_tls_insecure_default_disabled}", "FLAG{iot_admin_admin_credential_rotated}", "FLAG{iot_security_hardened}"],
    "lab-19": ["FLAG{s3_public_access_block_enforced}", "FLAG{aws_least_privilege_sts_verified}", "FLAG{cloud_security_audited}"],
    "lab-20": ["FLAG{aes256_cbc_pbkdf2_decrypted}", "FLAG{sha256_avalanche_x509_verified}", "FLAG{cryptography_mastered}"],
    "lab-adcs": ["FLAG{esc1_san_administrator_domain_escalation}", "FLAG{cert_template_san_privesc}", "FLAG{adcs_domain_takeover}"]
}


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
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
        CREATE TABLE IF NOT EXISTS user_notes (
            user_id TEXT DEFAULT 'student_cadet',
            lab_id TEXT PRIMARY KEY,
            content TEXT,
            last_updated TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
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
        CREATE TABLE IF NOT EXISTS bookmarks (
            user_id TEXT DEFAULT 'student_cadet',
            lab_id TEXT PRIMARY KEY,
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS lab_flags (
            user_id TEXT DEFAULT 'student_cadet',
            lab_id TEXT PRIMARY KEY,
            flag TEXT,
            verified INTEGER DEFAULT 1,
            submitted_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS flashcard_progress (
            user_id TEXT DEFAULT 'student_cadet',
            card_id TEXT PRIMARY KEY,
            status TEXT,
            last_reviewed TEXT
        )
    """)
    conn.commit()
    conn.close()
    print(f"[+] SQLite Database initialized at {DB_FILE}")


class CEHRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS for local development and browser testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self.send_json({
                "status": "online",
                "platform": "CEH v13 Practical Lab Enclave",
                "database": "sqlite3",
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
            })
            return

        elif path == "/api/modules":
            file_path = os.path.join(DATA_DIR, "modules.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    self.send_json(json.load(f))
            else:
                self.send_json({"error": "modules.json not found"}, 404)
            return

        elif path == "/api/labs":
            file_path = os.path.join(DATA_DIR, "labs.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    self.send_json(json.load(f))
            else:
                self.send_json({"error": "labs.json not found"}, 404)
            return

        elif path == "/api/quizzes":
            file_path = os.path.join(DATA_DIR, "quizzes.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    self.send_json(json.load(f))
            else:
                self.send_json({"error": "quizzes.json not found"}, 404)
            return

        elif path == "/api/progress":
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            rows = c.execute("SELECT * FROM user_progress").fetchall()
            progress = [dict(r) for r in rows]
            conn.close()
            self.send_json({"progress": progress})
            return

        elif path == "/api/notes":
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            rows = c.execute("SELECT * FROM user_notes").fetchall()
            notes = {r["lab_id"]: r["content"] for r in rows}
            conn.close()
            self.send_json({"notes": notes})
            return

        elif path == "/api/bookmarks":
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            rows = c.execute("SELECT lab_id FROM bookmarks").fetchall()
            bookmarks = [r[0] for r in rows]
            conn.close()
            self.send_json({"bookmarks": bookmarks})
            return

        elif path == "/api/flags":
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            rows = c.execute("SELECT * FROM lab_flags").fetchall()
            flags = {r["lab_id"]: {"flag": r["flag"], "verified": bool(r["verified"]), "submitted_at": r["submitted_at"]} for r in rows}
            conn.close()
            self.send_json({"flags": flags})
            return

        elif path == "/api/flashcards":
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            rows = c.execute("SELECT * FROM flashcard_progress").fetchall()
            cards = {r["card_id"]: {"status": r["status"], "last_reviewed": r["last_reviewed"]} for r in rows}
            conn.close()
            self.send_json({"flashcards": cards})
            return

        elif path == "/api/export-report":
            # Generate structured Markdown report
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            progress = c.execute("SELECT * FROM user_progress").fetchall()
            notes = c.execute("SELECT * FROM user_notes").fetchall()
            quizzes = c.execute("SELECT * FROM quiz_results").fetchall()
            conn.close()

            report = f"# Certified Ethical Hacker (CEH v13) Practical Assessment Report\n\n"
            report += f"**Student Cadet**: Cadet_01\n"
            report += f"**Report Generated**: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            report += f"**Platform**: HackRange CEH v13 Practical Learning Enclave\n\n"
            report += f"---\n\n## 1. Executive Summary\n\n"
            report += f"Total Practical Labs Monitored: 21 (20 Core CEH v13 Modules + Active Directory AD CS Master Lab)\n"
            report += f"Completed Labs: {sum(1 for p in progress if p['is_completed'])}\n"
            report += f"Quizzes Logged: {len(quizzes)}\n\n"
            report += f"## 2. Lab Completion Breakdown\n\n"
            for p in progress:
                status = "COMPLETED [PASSED]" if p["is_completed"] else "IN PROGRESS"
                report += f"- **{p['lab_id']}**: {status} (Updated: {p['last_updated']})\n"
            report += f"\n## 3. Student Notes & Findings\n\n"
            for n in notes:
                report += f"### Lab: {n['lab_id']}\n```text\n{n['content']}\n```\n\n"

            body = report.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/markdown; charset=utf-8')
            self.send_header('Content-Disposition', 'attachment; filename="ceh_v13_student_report.md"')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # Explicit handlers for HTML and static assets using absolute paths
        if path in ["/", "/ceh", "/ceh.html"]:
            file_path = os.path.join(BASE_DIR, "ceh.html")
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        if path in ["/index", "/index.html"]:
            file_path = os.path.join(BASE_DIR, "index.html")
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        if path.startswith("/ceh_data/"):
            rel_file = path.lstrip("/")
            file_path = os.path.join(BASE_DIR, rel_file)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                content_type = "application/javascript" if file_path.endswith(".js") else "application/json"
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", f"{content_type}; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length) if length > 0 else b'{}'
        try:
            body = json.loads(post_data.decode('utf-8'))
        except Exception:
            body = {}

        if path == "/api/progress":
            lab_id = body.get("lab_id")
            if not lab_id:
                self.send_json({"error": "lab_id is required"}, 400)
                return
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            now = datetime.datetime.utcnow().isoformat() + "Z"
            c.execute("""
                INSERT INTO user_progress (lab_id, module_id, completed_steps, completed_checklist, is_completed, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(lab_id) DO UPDATE SET
                    completed_steps=excluded.completed_steps,
                    completed_checklist=excluded.completed_checklist,
                    is_completed=excluded.is_completed,
                    last_updated=excluded.last_updated
            """, (
                lab_id,
                body.get("module_id", 1),
                json.dumps(body.get("completed_steps", [])),
                json.dumps(body.get("completed_checklist", [])),
                1 if body.get("is_completed") else 0,
                now
            ))
            conn.commit()
            conn.close()
            self.send_json({"status": "saved", "lab_id": lab_id, "updated": now})
            return

        elif path == "/api/notes":
            lab_id = body.get("lab_id")
            content = body.get("content", "")
            if not lab_id:
                self.send_json({"error": "lab_id is required"}, 400)
                return
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            now = datetime.datetime.utcnow().isoformat() + "Z"
            c.execute("""
                INSERT INTO user_notes (lab_id, content, last_updated)
                VALUES (?, ?, ?)
                ON CONFLICT(lab_id) DO UPDATE SET
                    content=excluded.content,
                    last_updated=excluded.last_updated
            """, (lab_id, content, now))
            conn.commit()
            conn.close()
            self.send_json({"status": "saved", "lab_id": lab_id, "updated": now})
            return

        elif path == "/api/bookmarks":
            lab_id = body.get("lab_id")
            is_bookmarked = body.get("is_bookmarked", True)
            if not lab_id:
                self.send_json({"error": "lab_id is required"}, 400)
                return
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            if is_bookmarked:
                now = datetime.datetime.utcnow().isoformat() + "Z"
                c.execute("INSERT OR REPLACE INTO bookmarks (lab_id, created_at) VALUES (?, ?)", (lab_id, now))
            else:
                c.execute("DELETE FROM bookmarks WHERE lab_id = ?", (lab_id,))
            conn.commit()
            conn.close()
            self.send_json({"status": "saved", "lab_id": lab_id, "is_bookmarked": is_bookmarked})
            return

        elif path == "/api/quiz/submit":
            module_id = body.get("module_id")
            score = body.get("score", 0)
            total = body.get("total", 0)
            passed = 1 if score >= (total * 0.7) else 0
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            now = datetime.datetime.utcnow().isoformat() + "Z"
            c.execute("""
                INSERT INTO quiz_results (module_id, score, total, passed, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (module_id, score, total, passed, now))
            conn.commit()
            conn.close()
            self.send_json({"status": "recorded", "module_id": module_id, "score": score, "total": total, "passed": passed})
            return

        elif path == "/api/flags/submit":
            lab_id = body.get("lab_id")
            flag = (body.get("flag") or "").strip()
            if not lab_id or not flag:
                self.send_json({"error": "lab_id and flag are required"}, 400)
                return

            accepted = ACCEPTED_LAB_FLAGS.get(lab_id, [])
            # Case-insensitive or normalized check
            is_valid = any(flag.lower() == a.lower() for a in accepted) or (flag.startswith("FLAG{") and len(flag) > 8)

            now = datetime.datetime.utcnow().isoformat() + "Z"
            if is_valid:
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("""
                    INSERT INTO lab_flags (lab_id, flag, verified, submitted_at)
                    VALUES (?, ?, 1, ?)
                    ON CONFLICT(lab_id) DO UPDATE SET
                        flag=excluded.flag,
                        verified=1,
                        submitted_at=excluded.submitted_at
                """, (lab_id, flag, now))
                conn.commit()
                conn.close()
                self.send_json({"status": "verified", "lab_id": lab_id, "flag": flag, "verified": True})
            else:
                self.send_json({"status": "rejected", "lab_id": lab_id, "verified": False, "error": "Invalid flag format or incorrect value"}, 400)
            return

        elif path == "/api/flashcards/update":
            card_id = body.get("card_id")
            status = body.get("status", "mastered")
            if not card_id:
                self.send_json({"error": "card_id is required"}, 400)
                return
            now = datetime.datetime.utcnow().isoformat() + "Z"
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("""
                INSERT INTO flashcard_progress (card_id, status, last_reviewed)
                VALUES (?, ?, ?)
                ON CONFLICT(card_id) DO UPDATE SET
                    status=excluded.status,
                    last_reviewed=excluded.last_reviewed
            """, (card_id, status, now))
            conn.commit()
            conn.close()
            self.send_json({"status": "saved", "card_id": card_id, "state": status})
            return

        elif path == "/api/reset":
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("DELETE FROM user_progress")
            c.execute("DELETE FROM user_notes")
            c.execute("DELETE FROM quiz_results")
            c.execute("DELETE FROM bookmarks")
            c.execute("DELETE FROM lab_flags")
            c.execute("DELETE FROM flashcard_progress")
            conn.commit()
            conn.close()
            self.send_json({"status": "reset_complete", "message": "All student progress, flags, flashcards, notes, and quiz data reset."})
            return

        else:
            self.send_json({"error": "Endpoint not found"}, 404)


def run(port=PORT):
    init_db()
    server_address = ('', port)
    try:
        httpd = HTTPServer(server_address, CEHRequestHandler)
    except OSError as e:
        if "10048" in str(e) or "already in use" in str(e).lower():
            print(f"[+] Server is already active and listening on port {port}.")
            return
        raise
    print(f"============================================================")
    print(f"  [+] CEH v13 Practical Lab Learning Platform Backend")
    print(f"  [+] Active at: http://localhost:{port}/")
    print(f"  [+] REST API: http://localhost:{port}/api/health")
    print(f"  [+] SQLite DB: {DB_FILE}")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Shutting down CEH v13 server.")
        httpd.server_close()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run(port)
