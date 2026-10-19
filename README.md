# HackRange | Advanced Cyber Range & Cybersecurity Training Platform

**HackRange** is an interactive, production-ready cybersecurity training platform and cyber range web application inspired by TryHackMe. Delivered as a single, self-contained, zero-dependency file (`index.html`) that can run directly in any web browser without build errors, Babel syntax crashes, or external asset dependencies.

---

## 🎓 Integrated Platforms

1. **HackRange Cyber Range**: 24 TryHackMe-style labs, flag vault, target machine manager, terminal sandbox, and Root Admin Deck (`index.html`).
2. **CEH v13 Practical Lab Platform**: 20 CEH v13 certification modules, Active Directory AD CS Master Lab (ESC1/ESC8), 6-Hour Mock Exam Simulator, and BloodHound attack path graph (`ceh.html`).

---

## 🚀 Quick Start

1. **Interactive Multi-Platform Launcher**:
   - Double-click `launch.bat` to launch either HackRange, CEH v13, or both side-by-side.
   - Or double-click `launch_ceh.bat` for dedicated CEH v13 training.
2. **Direct Browser Access**:
   - HackRange: `file:///C:/Users/ratho/.gemini/antigravity/scratch/hackrange/index.html`
   - CEH v13 Platform: `file:///C:/Users/ratho/.gemini/antigravity/scratch/hackrange/ceh.html`
3. **Optional Python Backend Server (SQLite Persistence)**:
   ```powershell
   cd C:\Users\ratho\.gemini\antigravity\scratch\hackrange
   py ceh_server.py
   # Browse to http://localhost:8000/ceh.html or http://localhost:8000/
   ```

> **Active Workspace Recommendation**:
> If you are working in an IDE or CLI environment, set `C:\Users\ratho\.gemini\antigravity\scratch\hackrange` as your active workspace directory.

---

## 🛡️ Authentication & Role System

HackRange features a gated security barrier with dual-role authentication and persistent session management stored in `localStorage`:

1. **Root Administrator (Tushar)**:
   - **Callsign**: `Tushar_Admin`
   - **Email**: `tushar@hackrange.io`
   - **Role**: `admin` (Highest tier permissions)
   - **Avatar**: Custom hooded warrior crest with sharp metallic silver/slate trim, dark mail background, and a glowing faceted blue sapphire gemstone at the bottom apex.
   - **Features**: Exclusive access to the **Root Admin Deck**, **Operators Registry**, and central **Flag Vault**.
   - **1-Click Login**: Click `⚡ Tushar (Admin)` on the login screen.

2. **Student Cadet**:
   - **Role**: `cadet` (Standard trainee permissions)
   - **Two-Step Registration**: Click **"1. Sign Up First"** to create a cadet account, then sign in.
   - **1-Click Login**: Click `⚡ Student Cadet` for instant access as `CyberCadet_01`.

3. **Session Persistence & Logout**:
   - Operator credentials, XP totals, solved labs, and target machine status persist across reloads.
   - The top-navigation **Logout button** clears active sessions and returns to the authentication gate.

---

## 🎯 Complete 24-Lab Practical Curriculum

All 24 hands-on exam labs across Reconnaissance, Web Application Security, Network Defense, and Systems are implemented with interactive questions, format masks, progressive hints, terminal simulators, and flags:

| # | Lab Title | Category | Difficulty | XP | Primary Solution Flag |
|---|-----------|----------|------------|----|-----------------------|
| 01 | DoS Attack using Slow HTTP | Network Defense | Medium | 150 | `THM{slow_http_exhausted_apache_mitigated}` |
| 02 | SQL Injection | Web App Security | Easy | 150 | `THM{sqli_union_admin_bypass_secured}` |
| 03 | HA Load Balancer | Network Defense | Medium | 200 | `THM{haproxy_roundrobin_failover_verified}` |
| 04 | Backdoor Creation using Netcat | Systems & Hardening | Easy | 150 | `THM{netcat_reverse_shell_detected_auditd}` |
| 05 | MRTG Windows | Systems & Hardening | Medium | 200 | `THM{mrtg_snmpv3_authpriv_hardened}` |
| 06 | File Inclusion / LFI | Web App Security | Easy | 150 | `THM{lfi_traversal_sanitized_basename}` |
| 07 | Squid Proxy | Network Defense | Medium | 200 | `THM{squid_proxy_acl_restricted_3128}` |
| 08 | ARP Spoofing | Network Defense | Hard | 250 | `THM{arp_poison_mitigated_cisco_dai}` |
| 09 | Converting HTTP to HTTPS | Network Defense | Easy | 150 | `THM{tls13_openssl_hsts_enforced_ok}` |
| 10 | Broken Authentication | Web App Security | Medium | 200 | `THM{session_fixation_mfa_hardened}` |
| 11 | Password Cracking using Hydra | Systems & Hardening | Medium | 200 | `THM{hydra_bruteforce_banned_fail2ban}` |
| 12 | SQL Mapping | Web App Security | Medium | 200 | `THM{sqlmap_blind_time_extraction_stopped}` |
| 13 | User Agent Changing | Web App Security | Easy | 150 | `THM{user_agent_spoof_rbac_enforced}` |
| 14 | Nmap Scan Network | Reconnaissance | Easy | 150 | `THM{nmap_syn_stealth_recon_mapped}` |
| 15 | MAC Spoof | Network Defense | Medium | 200 | `THM{mac_spoof_port_security_violation}` |
| 16 | XSS Attack | Web App Security | Medium | 200 | `THM{xss_csp_nonce_httponly_protected}` |
| 17 | Gobuster, Dirbuster | Reconnaissance | Easy | 150 | `THM{dir_busting_hidden_admin_portal}` |
| 18 | Practical Exam Slot #18 Capstone | Systems & Hardening | Insane | 250 | `THM{capstone_slot18_defense_in_depth}` |
| 19 | OpenSSH Server Deployment using Hydra | Systems & Hardening | Hard | 250 | `THM{openssh_ed25519_root_disabled}` |
| 20 | Network Analysis using Wireshark | Reconnaissance | Medium | 200 | `THM{wireshark_cleartext_creds_intercepted}` |
| 21 | CSRF Cross-Site Request Forgery | Web App Security | Medium | 200 | `THM{csrf_samesite_strict_token_validated}` |
| 22 | Banner Grabbing | Reconnaissance | Easy | 150 | `THM{banner_grabbing_apache_obfuscated}` |
| 23 | Subdomain Finding | Reconnaissance | Medium | 200 | `THM{zone_transfer_axfr_internal_discovered}` |
| 24 | Google Dorking | Reconnaissance | Easy | 150 | `THM{google_dorking_confidential_env_leaked}` |

---

## 💻 Interactive Features

1. **Target Machine Provisioning**:
   - TryHackMe-style **"Start Machine"** / **"Terminate Machine"** controls.
   - Status transitions (`STOPPED` ➔ `STARTING` ➔ `RUNNING` ➔ `TERMINATING`).
   - Dynamically bound target IP (`10.10.142.50`) with 1-click copy.
   - Active countdown lease timer with `+1h` extension option.

2. **In-Room AttackBox Terminal**:
   - Dark interactive console supporting `help`, `nmap`, `curl`, `slowhttptest`, `hydra`, `sqlmap`, `nc`, `dig`, `gobuster`, `ping`, `cat`, `ls`, `clear`, and `run-exploit`.
   - Direct flag submission in terminal: `submit THM{...}`.

3. **Interactive Task Questions**:
   - Format mask indicators (e.g. `mod_**********`, `THM{...}`).
   - Instant input validation with visual glow cues and audio chimes.
   - +50 XP awards on correct answers with progressive hint accordions.

4. **Reference Manual Panel**:
   - Dual-tab interface switching between **"⚡ Offensive Commands"** and **"🛡️ Hardening Defense"**.
   - 1-click syntax-highlighted code copy buttons.

5. **Multi-Node Practice Sandboxes**:
   - **DVWA Web Portal**: Interactive SQLi test input with live reflected database dumps and security level selector.
   - **Kali Linux Node (10.10.142.10)**: Quick-launch attack scripts (auto-recon, reverse shell generator, WireGuard check).
   - **Metasploitable 2 Target (10.10.142.81)**: Vulnerability service matrix with interactive exploit probes (vsftpd 2.3.4, OpenSSH 4.7p1, MySQL, Tomcat).

6. **Root Admin Deck (Exclusive to Tushar)**:
   - **Executive Dashboard**: Total registered cadets, platform flags solved, and total platform XP.
   - **Operators Registry**: Table of all accounts with callsigns, roles, XP totals, +100 bonus XP grants, and account removal.
   - **Flag Vault**: Central searchable repository of all 24 solution flags with instant 1-click copy.

7. **Tactical Global Leaderboard & Hall of Fame**:
   - Live competitive standings tracking rank, XP, curriculum progress, titles, and combat badges.
   - Top 3 Podium (Gold Champion Tushar_Admin, Silver, Bronze) with dynamic rank calculations.

8. **Tactical Exploit & Payload Cheat Sheet (Cyber Weaponry Toolkit)**:
   - Quick-reference modal containing 1-click copyable reverse shells (Bash, Python, Netcat, PHP, PowerShell), SQL injection strings, LFI traversal wrappers, XSS vectors, Nmap scan profiles, and hardening defense configurations.

9. **Live Range Network Topology (`🌐 Topology`)**:
   - Interactive SVG diagram of the 10.10.142.0/24 subnet mapping the Cadet AttackBox, Perimeter Firewall/HAProxy, Target Host, and Metasploitable 2 VM with live latency and interface telemetry.

10. **Cadet Certificate of Practical Competency (`🎓 Certificate`)**:
    - Official cyber warfare credential with the operator's callsign, completed labs count, total XP, cryptographic verification seal, and Root Admin Tushar's signature with built-in PDF/print export.

11. **Speedrun Mission Stopwatch & Best Time Tracking**:
    - Live mission stopwatch automatically initiates when target machines are provisioned.
    - Accurately clocks execution speed and records personal best times per lab upon flag submission.

12. **AttackBox Customizer (Palette Switcher & Font Sizing)**:
    - 4 tactical terminal color schemes: Matrix Emerald, Cyber Cyan, Amber CRT, and Blood Crimson.
    - 3 dynamic font size scalers (`A-`, `A`, `A+`) and shell command history recall with `ArrowUp` / `ArrowDown`.

13. **Root Admin Disaster Recovery & System Backup**:
    - Full range JSON snapshot export (`hackrange_backup_<timestamp>.json`) for disaster recovery.
    - In-browser file reader backup import with instant schema validation and enclave state reload.
    - Factory Reset button to wipe custom cadet data and restore clean initial state.

14. **CTF Jeopardy Board View Toggle (`🏆 CTF Board`)**:
    - 1-Click switcher in the Labs Directory between standard TryHackMe card grid and classic DEF CON / CTFd-style Jeopardy Board.
    - Groups challenges into Reconnaissance, Web Application Security, Network Defense, and Systems & Hardening sorted by XP point values with real-time solve indicators.

15. **1-Click Attack Vector Auto-Type (`⚡ Auto-Type`)**:
    - Allows cadets to click **"Auto-Type"** in the Reference Manual to load the attack command chain directly into the AttackBox prompt, eliminating manual typing errors.

16. **Root Admin Lab Authoring Studio (`🧪 Lab Studio`)**:
    - Integrated authoring suite for Root Admin Tushar to craft and deploy custom practical exam rooms (Lab #25+) on the fly with custom format masks, threat scenarios, solutions, and persistence.

17. **Wireshark PCAP Protocol Analyzer & TCP Stream Reconstructor (`📦 Wireshark PCAP`)**:
    - Embedded 4th Sandbox sub-tab featuring an authentic Wireshark network protocol analyzer.
    - 10 realistic packet captures spanning ARP discovery, DNS query/response, TCP three-way handshake (`[SYN]`, `[SYN, ACK]`, `[ACK]`), HTTP POST authentication submission (`admin:Sup3rS3cr3tP@ss`), and HTTP 200 responses.
    - Real-time display filter bar (`http`, `tcp`, `arp`, `dns`, `ip.addr == 10.10.142.50`) with instant packet filtering.
    - Interactive 3-pane layout: Packet list table with protocol-coded highlighting, expandable Packet Dissection Tree (Frame metadata, Ethernet II MACs, IPv4 headers, TCP port mapping, Application Layer payload), and synchronized Raw Hex / ASCII Byte Dump pane.
    - **Follow TCP Stream Modal (`🔍 TCP Stream #0`)**: Reconstructs the cleartext client/server stream showing HTTP POST credentials and server flag response (`THM{wireshark_cleartext_creds_intercepted}`).

18. **MITRE ATT&CK® Enterprise Tactical Matrix (`🎯 ATT&CK Matrix`)**:
    - Tactical intelligence matrix mapped to MITRE ATT&CK v14.
    - Maps all 24 labs across 5 primary enterprise tactics: Reconnaissance (`TA0043`), Initial Access (`TA0001`), Execution (`TA0002`), Defense Evasion (`TA0005`), and Credential Access (`TA0006`).
    - Color-coded threat technique cards displaying technique IDs (e.g. `T1595`, `T1190`, `T1059`, `T1070`, `T1110`), lab names, and real-time operator mastery percentages.
    - 1-Click modal navigation directly into any corresponding exam room.

19. **Tactical Cyber Audio Synthesizer (Web Audio API)**:
    - Zero-asset, zero-latency real-time procedural sound effects synthesized directly via browser Web Audio API oscillators (keystrokes, solve arpeggios, siren, alert).
    - Global Mute toggle (`🔊 Audio: ON/MUTED`) preserved in localStorage.

20. **Blue Team SOC SIEM & Threat Log Intelligence (`🛡️ SOC SIEM`)**:
    - Embedded 5th Sandbox sub-tab featuring an enterprise Security Operations Center (SOC) telemetry viewer.
    - Real-time event ingestion stream correlating attacks from Suricata NIDS, Apache access/error logs, Linux `/var/log/auth.log` (Hydra brute force), ModSecurity WAF, and Kernel Dynamic ARP Inspection (DAI).
    - Severity filter badges (`CRITICAL`, `HIGH`, `MEDIUM`, `INFO`), dynamic search filter, and stream pause/resume controls.
    - Each ingested alert maps directly to MITRE ATT&CK techniques (`T1190`, `T1110`, `T1498`, `T1595`, `T1006`, `T1557`) and corresponding practical curriculum labs.

21. **Interactive Defensive Detection Engine (Sigma & Snort Rules)**:
    - Cadets can select defensive detection signatures (Snort rule for SQLi, Apache `mod_reqtimeout` directive, Fail2ban jail policy, Cisco DAI config, Sigma rule for LFI).
    - Click **"Evaluate Rule Engine"** to match rules against incoming live telemetry; verified detections award **+50 XP** bonus points.

---

## 🐳 Containerized Deployment (Docker)

To deploy HackRange on an isolated Linux VM, internal team server, or cloud node:

```bash
# 1. Build and launch using Docker Compose
docker compose up -d

# 2. Access the platform in your browser
http://localhost:8080
```

---

## 🛠️ Verification & Testing

To launch the platform locally:
- **Windows**: Double-click `launch.bat` or open `index.html` in Microsoft Edge, Google Chrome, Mozilla Firefox, or Brave.
- **Direct Path**: `file:///C:/Users/ratho/.gemini/antigravity/scratch/hackrange/index.html`



