# CEH v13 Complete Ethical Hacking Practical Lab Platform

**CEH v13 Practical Learning Platform** is an enterprise-grade, interactive cybersecurity training platform designed for students, penetration testers, and security engineers preparing for the **Certified Ethical Hacker (CEH v13)** practical examination.

> **Disclaimer**: This platform contains original educational exercises, threat simulations, and defense tutorials created for hands-on certification preparation. It is an independent training resource and is not affiliated with, sponsored by, or endorsed by EC-Council.

---

## 🚀 Quick Start & Launch

### Option 1: Standalone Instant Launch (Zero Dependencies)
You can open the self-contained frontend directly in any web browser without running background services or installing packages:
- **Double-click**: `launch_ceh.bat`
- **Or open URL**: `file:///C:/Users/ratho/.gemini/antigravity/scratch/hackrange/ceh.html`

### Option 2: Full Client-Server Mode (Zero-Dependency Python + SQLite)
To enable real-time SQLite database persistence and REST API endpoints:
```powershell
cd C:\Users\ratho\.gemini\antigravity\scratch\hackrange
py ceh_server.py
```
Open **`http://localhost:8000/ceh.html`** in your browser.

### Option 3: Modern FastAPI ASGI Server (OpenAPI / Swagger UI)
For developers wanting modern ASGI performance with interactive API documentation:
```powershell
pip install fastapi uvicorn
py -m uvicorn ceh_fastapi:app --reload --port 8000
```
- **Web App**: `http://localhost:8000/ceh.html`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 🛡️ Architecture & Design

- **SOC Platform UI/UX**: Dark charcoal theme (`#06090e`, `#0a0e17`, `#151b2e`), subtle emerald (`#10b981`), cyan (`#06b6d4`), amber (`#f59e0b`), and purple (`#8b5cf6`) accents.
- **Responsive Layout**: Collapsible sidebar navigation, live search across modules and commands, category pills, and difficulty filters.
- **Dual Persistence Architecture**:
  - Automatically queries the local Python REST API (`/api/health`, `/api/progress`, `/api/notes`, `/api/quizzes`).
  - Seamlessly falls back to `localStorage` and embedded offline datasets when run standalone (`file:///`), ensuring 100% crash-free execution everywhere.
- **Web Audio API Synthesizer**: Procedural, zero-asset auditory feedback (keystrokes, success arpeggios, error alerts) with global header mute toggle.

---

## 📚 Complete 20 CEH v13 Practical Modules + AD CS

| Module | Title | Category | Exam Weight | Key Focus & Tooling |
| :---: | :--- | :--- | :---: | :--- |
| **01** | Introduction to Ethical Hacking | Fundamentals | 6% | OS fingerprinting (`uname`), interface discovery (`ip -br addr`), baseline recording |
| **02** | Footprinting and Reconnaissance | Reconnaissance | 7% | Authoritative DNS queries (`dig`), MX/NS/TXT records, WHOIS, zone transfer audit (`AXFR`) |
| **03** | Scanning Networks | Reconnaissance | 8% | Subnet CIDR ping sweep (`nmap -sn`), TCP SYN stealth scan (`-sS`), service banners (`-sV`) |
| **04** | Enumeration | System Hacking | 7% | Socket statistics (`ss -tulpn`), SMB null session listing (`smbclient -L`), exposed shares |
| **05** | Vulnerability Analysis | Vulnerability Mgmt | 6% | CVE correlation (CVE-2011-2523), CVSS v3.1 vector calculation, remediation triage |
| **06** | System Hacking | System Hacking | 12% | User/group auditing (`/etc/passwd`), SUID/SGID root binary discovery, sudoers auditing |
| **07** | Malware Threats | Malware Analysis | 6% | Cryptographic hashing (`sha256sum`), magic bytes inspection (`file`), EICAR verification |
| **08** | Sniffing | Network Defense | 7% | Packet capture (`tcpdump`), BPF filtering, TCP 3-way handshake dissection, cleartext auth |
| **09** | Social Engineering | Social Engineering | 6% | RFC 5322 header inspection (`Received:`, `From:` vs `Return-Path:`), SPF/DMARC analysis |
| **10** | Denial-of-Service | Network Defense | 5% | HTTP baseline latency benchmarking, socket state tracking (`SYN_RECV`), iptables rate-limits |
| **11** | Session Hijacking | Web Security | 6% | Cookie flag auditing (`HttpOnly`, `Secure`, `SameSite=Strict`), session invalidation test |
| **12** | Evading IDS, Firewalls, & Honeypots | Network Defense | 6% | Packet filter auditing (`iptables -L`), Suricata NIDS alert triage, inline drop rules |
| **13** | Hacking Web Servers | Web Security | 6% | HTTP banner reduction (`ServerTokens Prod`), directory index disablement, TLS headers |
| **14** | Hacking Web Applications | Web Security | 10% | OWASP Top 10 IDOR detection (`/api/users/1`), Content Security Policy (CSP) enforcement |
| **15** | SQL Injection | Web Security | 7% | Dynamic query concatenation exploitation (`' OR 1=1`), parameterized prepared statements |
| **16** | Hacking Wireless Networks | Wireless Security | 5% | 802.11 monitor mode (`iwconfig`), beacon frame dissection, WPA2 vs WPA3 SAE analysis |
| **17** | Hacking Mobile Platforms | Mobile Security | 5% | Android Debug Bridge (`adb devices`), `AndroidManifest.xml` permissions & backup flags |
| **18** | Hacking IoT Platforms | IoT & OT Security | 5% | IoT management interface scanning, default factory credentials (`admin:admin`), MQTT TLS |
| **19** | Cloud Computing | Cloud Security | 6% | Identity verification (`aws sts get-caller-identity`), S3 Public Access Block audit, IAM |
| **20** | Cryptography | Cryptography | 6% | SHA-256 avalanche effect, OpenSSL AES-256-CBC encryption with PBKDF2, X.509 cert audit |
| **AD** | **Active Directory & AD CS Master Lab** | Enterprise Identity | Master Lab | Domain controller architecture, AD CS templates auditing, **ESC1** SAN abuse, **ESC8** NTLM relay |

---

## 👑 Advanced Active Directory Certificate Services (AD CS) Lab

A dedicated enterprise laboratory section demonstrating modern Windows enterprise privilege escalation vectors:
1. **Local Machine Certificate Store Audit**: Inspecting certificates using PowerShell (`Get-ChildItem Cert:\LocalMachine\My`).
2. **ESC1 SAN Misconfiguration Detection**: Querying AD configuration partition using PowerShell `Get-ADObject` for certificate templates with `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` (bit 0x1) and Client Authentication EKU.
3. **ESC8 NTLM Relay Vulnerability**: Auditing AD CS HTTP Web Enrollment endpoints (`/certsrv/`) for cleartext NTLM authentication without Extended Protection for Authentication (EPA).
4. **Authoritative Remediation**: Step-by-step PowerShell procedures to strip enrollee subject flags, enforce CA manager approval, and mandate EPA.

---

## 💻 Interactive Educational Terminal Simulator

- Built-in educational shell supporting **40+ realistic commands**:
  - `uname`, `ip`, `ifconfig`, `dig`, `nslookup`, `whois`, `nmap`, `ss`, `netstat`, `smbclient`
  - `whoami`, `id`, `cat /etc/passwd`, `cat /etc/shadow` (permission auditing)
  - `curl`, `find`, `sha256sum`, `file`, `strings`, `tcpdump`, `iptables`
  - `powershell`, `Get-ADObject`, `Get-ChildItem`, `aws`, `adb`, `iwconfig`, `openssl`, `ping`
  - `help`, `clear`, `reset`, `history`
- **Output Distinction**: Every simulated command output features a clear `[SIMULATED ENCLAVE OUTPUT]` badge and educational context explanations to distinguish from the host OS.
- **Intelligent Safe Hints Engine**: Automatically detects command typos (e.g. `namp`, `tcpdupm`, `ifconfg`), intercepts dangerous commands, and offers contextual hints.
- **Up/Down Arrow History Navigation**: Use `↑` and `↓` arrow keys in the prompt to cycle through previously executed commands.
- **1-Click Auto-Type**: Click `⚡ Auto-Type` on any lab step or cheatsheet card to instantly load and execute commands in the sandbox.
- **Safe Execution**: All commands operate safely in an isolated memory sandbox reflecting authorized subnet `10.10.20.0/24`.

---

## 🧠 Learning Management Features

1. **Readiness Scoring Engine**: Real-time percentage calculating completed labs, step milestones, and passed quizzes.
2. **Knowledge-Check Quizzes**: 21 multiple-choice quizzes with instant grading, randomized answer layouts, and comprehensive explanations.
3. **Capture The Flag (CTF) Proof Engine**: Each lab room features an interactive flag validation box (`FLAG{...}`) with cryptographic verification and expandable hints.
4. **Interactive Cheatsheet Vault (`Vault`)**: Fast-reference library covering Nmap scan types, well-known port matrices (FTP 21 through VNC 5900), Wireshark BPF capture filters, Active Directory attack strings, Hashcat cracking modes, and SQLi bypass payloads with 1-click `⚡ Auto-Type`.
5. **Active Recall Flashcards (`Drills`)**: 3D flip card preparation deck spanning CFAA legal statutes, network attacks (Smurf vs Fraggle), WPA3 SAE, and AD CS vectors with self-rated mastery tracking (`✔ Mastered` vs `❌ Needs Review`).
6. **Per-Lab Personal Notes**: Auto-saving Markdown-friendly notes editor persisted in SQLite/localStorage.
7. **Favorites / Bookmarking**: Star any lab room to pin to quick-access favorites.
8. **Downloadable Lab Report**: 1-Click export to structured Markdown (`.md`) or printable PDF format for certification portfolios.

---

---

## 🏆 CEH v13 Practical Mock Exam Simulator (6-Hour Challenge)

Click the **🎯 Mock Exam** button in the header toolbar to trigger the full 20-scenario practical examination simulation:
- **6-Hour Countdown Timer**: Real-time ticker with pause/resume and time warning indicators.
- **20 Scenario Challenges**: Spanning port reconnaissance, CVE identification, hash cracking, SQL injection, wireless security, cloud auditing, and AD CS ESC1 exploitation.
- **Evidence Verification Engine**: Real-time pattern matching for flag submission, command hashes, and CVE identifiers.
- **70% Passing Threshold**: Complete at least 14 of 20 scenarios to pass.
- **Official Certificate of Competency**: Unlocks an authenticated, printable completion certificate with your Cadet ID, verification hash, and final score.

---

## 🕸️ BloodHound-style Active Directory Attack Path Graph

Located in the **AD CS Master Lab (`lab-adcs`)**, an interactive SVG graph visualizes the enterprise domain escalation chain:
- **Initial Foothold**: Low-privileged cadet account in `Domain Users`.
- **Enrollment Permission**: Rights over vulnerable `ESC1-WebServer` certificate template (`CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`).
- **CA Issue Request**: Requesting certificate with Subject Alternative Name (SAN) for `CORP\Administrator`.
- **Target Pwned**: Kerberos PKINIT / Schannel authentication gaining full `Enterprise Admins` dominion.

---

## 🐳 Docker & Docker Compose Deployment

If you have Docker installed on your host, you can launch the complete ecosystem with a single command:
```powershell
docker compose up -d
```
- **Web Frontend (HackRange + CEH v13)**: `http://localhost:8080` (or `http://localhost:8080/ceh.html`)
- **Backend API & SQLite Service**: `http://localhost:8000/api/health`

---

## 🧪 Unit Testing & Verification

Run the automated test suite verifying data models, module structures, and SQLite operations:
```powershell
py -m unittest test_ceh_platform.py
```
Expected output:
```text
.........
----------------------------------------------------------------------
Ran 9 tests in 0.465s

OK
```
