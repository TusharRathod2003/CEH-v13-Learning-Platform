#!/usr/bin/env python3
"""
CEH v13 Practical Learning Platform - Modern FastAPI Backend
Provides OpenAPI Swagger Documentation (/docs) and SQLite persistence.

Usage:
    pip install fastapi uvicorn
    py -m uvicorn ceh_fastapi:app --reload --port 8000
"""

import os
import json
import sqlite3
import datetime
from typing import List, Optional, Dict, Any

try:
    from fastapi import FastAPI, HTTPException, Body, Response
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse, PlainTextResponse
    from pydantic import BaseModel, Field
except ImportError:
    print("[!] FastAPI or Uvicorn not installed in current Python environment.")
    print("[!] To run this modern ASGI server: pip install fastapi uvicorn")
    print("[!] Or run the built-in zero-dependency standard library server: py ceh_server.py")
    raise SystemExit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "ceh_learning.db")
DATA_DIR = os.path.join(BASE_DIR, "ceh_data")

app = FastAPI(
    title="CEH v13 Practical Lab Learning Platform API",
    description="Interactive REST API and SQLite engine for Certified Ethical Hacker v13 practical modules, labs, and quizzes.",
    version="1.3.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
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


@app.on_event("startup")
def startup_event():
    init_db()


# --- Models ---
class ProgressPayload(BaseModel):
    lab_id: str
    module_id: Optional[int] = 1
    completed_steps: Optional[List[int]] = []
    completed_checklist: Optional[List[int]] = []
    is_completed: Optional[bool] = False


class NotePayload(BaseModel):
    lab_id: str
    content: str


class BookmarkPayload(BaseModel):
    lab_id: str
    is_bookmarked: bool = True


class QuizSubmitPayload(BaseModel):
    module_id: int
    score: int
    total: int


class FlagSubmitPayload(BaseModel):
    lab_id: str
    flag: str


class FlashcardUpdatePayload(BaseModel):
    card_id: str
    status: str = "mastered"


# --- REST API Endpoints ---
@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "online",
        "platform": "CEH v13 Practical Lab Enclave (FastAPI)",
        "database": "sqlite3",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }


@app.get("/api/modules", tags=["Curriculum"])
def get_modules():
    path = os.path.join(DATA_DIR, "modules.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="modules.json not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/labs", tags=["Curriculum"])
def get_labs():
    path = os.path.join(DATA_DIR, "labs.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="labs.json not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/quizzes", tags=["Curriculum"])
def get_quizzes():
    path = os.path.join(DATA_DIR, "quizzes.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="quizzes.json not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/progress", tags=["Progress"])
def get_progress():
    conn = get_db()
    c = conn.cursor()
    rows = c.execute("SELECT * FROM user_progress").fetchall()
    progress = [dict(r) for r in rows]
    conn.close()
    return {"progress": progress}


@app.post("/api/progress", tags=["Progress"])
def save_progress(payload: ProgressPayload):
    conn = get_db()
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
        payload.lab_id,
        payload.module_id,
        json.dumps(payload.completed_steps),
        json.dumps(payload.completed_checklist),
        1 if payload.is_completed else 0,
        now
    ))
    conn.commit()
    conn.close()
    return {"status": "saved", "lab_id": payload.lab_id, "updated": now}


@app.get("/api/notes", tags=["Notes"])
def get_notes():
    conn = get_db()
    c = conn.cursor()
    rows = c.execute("SELECT * FROM user_notes").fetchall()
    notes = {r["lab_id"]: r["content"] for r in rows}
    conn.close()
    return {"notes": notes}


@app.post("/api/notes", tags=["Notes"])
def save_notes(payload: NotePayload):
    conn = get_db()
    c = conn.cursor()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    c.execute("""
        INSERT INTO user_notes (lab_id, content, last_updated)
        VALUES (?, ?, ?)
        ON CONFLICT(lab_id) DO UPDATE SET
            content=excluded.content,
            last_updated=excluded.last_updated
    """, (payload.lab_id, payload.content, now))
    conn.commit()
    conn.close()
    return {"status": "saved", "lab_id": payload.lab_id, "updated": now}


@app.get("/api/bookmarks", tags=["Bookmarks"])
def get_bookmarks():
    conn = get_db()
    c = conn.cursor()
    rows = c.execute("SELECT lab_id FROM bookmarks").fetchall()
    bookmarks = [r[0] for r in rows]
    conn.close()
    return {"bookmarks": bookmarks}


@app.post("/api/bookmarks", tags=["Bookmarks"])
def save_bookmark(payload: BookmarkPayload):
    conn = get_db()
    c = conn.cursor()
    if payload.is_bookmarked:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        c.execute("INSERT OR REPLACE INTO bookmarks (lab_id, created_at) VALUES (?, ?)", (payload.lab_id, now))
    else:
        c.execute("DELETE FROM bookmarks WHERE lab_id = ?", (payload.lab_id,))
    conn.commit()
    conn.close()
    return {"status": "saved", "lab_id": payload.lab_id, "is_bookmarked": payload.is_bookmarked}


@app.get("/api/flags", tags=["CTF Flags"])
def get_flags():
    conn = get_db()
    c = conn.cursor()
    rows = c.execute("SELECT * FROM lab_flags").fetchall()
    flags = {r["lab_id"]: {"flag": r["flag"], "verified": bool(r["verified"]), "submitted_at": r["submitted_at"]} for r in rows}
    conn.close()
    return {"flags": flags}


@app.post("/api/flags/submit", tags=["CTF Flags"])
def submit_flag(payload: FlagSubmitPayload):
    flag_val = payload.flag.strip()
    accepted = ACCEPTED_LAB_FLAGS.get(payload.lab_id, [])
    is_valid = any(flag_val.lower() == a.lower() for a in accepted) or (flag_val.startswith("FLAG{") and len(flag_val) > 8)

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid flag format or incorrect value")

    now = datetime.datetime.utcnow().isoformat() + "Z"
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO lab_flags (lab_id, flag, verified, submitted_at)
        VALUES (?, ?, 1, ?)
        ON CONFLICT(lab_id) DO UPDATE SET
            flag=excluded.flag,
            verified=1,
            submitted_at=excluded.submitted_at
    """, (payload.lab_id, flag_val, now))
    conn.commit()
    conn.close()
    return {"status": "verified", "lab_id": payload.lab_id, "flag": flag_val, "verified": True}


@app.get("/api/flashcards", tags=["Flashcards"])
def get_flashcards():
    conn = get_db()
    c = conn.cursor()
    rows = c.execute("SELECT * FROM flashcard_progress").fetchall()
    cards = {r["card_id"]: {"status": r["status"], "last_reviewed": r["last_reviewed"]} for r in rows}
    conn.close()
    return {"flashcards": cards}


@app.post("/api/flashcards/update", tags=["Flashcards"])
def update_flashcard(payload: FlashcardUpdatePayload):
    now = datetime.datetime.utcnow().isoformat() + "Z"
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO flashcard_progress (card_id, status, last_reviewed)
        VALUES (?, ?, ?)
        ON CONFLICT(card_id) DO UPDATE SET
            status=excluded.status,
            last_reviewed=excluded.last_reviewed
    """, (payload.card_id, payload.status, now))
    conn.commit()
    conn.close()
    return {"status": "saved", "card_id": payload.card_id, "state": payload.status}


@app.post("/api/quiz/submit", tags=["Quizzes"])
def submit_quiz(payload: QuizSubmitPayload):
    passed = 1 if payload.score >= (payload.total * 0.7) else 0
    now = datetime.datetime.utcnow().isoformat() + "Z"
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO quiz_results (module_id, score, total, passed, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (payload.module_id, payload.score, payload.total, passed, now))
    conn.commit()
    conn.close()
    return {
        "status": "recorded",
        "module_id": payload.module_id,
        "score": payload.score,
        "total": payload.total,
        "passed": passed
    }


@app.get("/api/export-report", tags=["Reports"])
def export_report():
    conn = get_db()
    c = conn.cursor()
    progress = c.execute("SELECT * FROM user_progress").fetchall()
    notes = c.execute("SELECT * FROM user_notes").fetchall()
    quizzes = c.execute("SELECT * FROM quiz_results").fetchall()
    flags = c.execute("SELECT * FROM lab_flags").fetchall()
    conn.close()

    report = f"# Certified Ethical Hacker (CEH v13) Practical Assessment Report\n\n"
    report += f"**Student Cadet**: Cadet_01\n"
    report += f"**Report Generated**: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    report += f"**Platform**: HackRange CEH v13 Practical Learning Enclave (FastAPI)\n\n"
    report += f"---\n\n## 1. Executive Summary\n\n"
    report += f"Total Practical Labs: 21\n"
    report += f"Completed Labs: {sum(1 for p in progress if p['is_completed'])}\n"
    report += f"Flags Captured: {len(flags)}\n"
    report += f"Quizzes Logged: {len(quizzes)}\n\n"
    report += f"## 2. Lab Completion Breakdown\n\n"
    for p in progress:
        status = "COMPLETED [PASSED]" if p["is_completed"] else "IN PROGRESS"
        report += f"- **{p['lab_id']}**: {status} (Updated: {p['last_updated']})\n"
    report += f"\n## 3. Student Notes & Findings\n\n"
    for n in notes:
        report += f"### Lab: {n['lab_id']}\n```text\n{n['content']}\n```\n\n"

    return PlainTextResponse(report, media_type="text/markdown")


@app.post("/api/reset", tags=["System"])
def reset_progress():
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM user_progress")
    c.execute("DELETE FROM user_notes")
    c.execute("DELETE FROM quiz_results")
    c.execute("DELETE FROM bookmarks")
    c.execute("DELETE FROM lab_flags")
    c.execute("DELETE FROM flashcard_progress")
    conn.commit()
    conn.close()
    return {"status": "reset_complete", "message": "All student progress, flags, flashcards, notes, and quiz data reset."}


# --- Static Files / Single Page Web App Serving ---
@app.get("/", response_class=FileResponse, tags=["Web"])
def serve_root():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


@app.get("/ceh.html", response_class=FileResponse, tags=["Web"])
def serve_ceh():
    return FileResponse(os.path.join(BASE_DIR, "ceh.html"))


# Mount ceh_data static directory
if os.path.exists(DATA_DIR):
    app.mount("/ceh_data", StaticFiles(directory=DATA_DIR), name="ceh_data")


if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run("ceh_fastapi:app", host="0.0.0.0", port=8000, reload=True)
