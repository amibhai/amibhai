<!-- Header -->
<div align="center">

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║    ░██████╗░██╗░░░░░░░██╗░█████╗░░██████╗████████╗██╗██╗░░██╗   ║
║    ██╔════╝██║░░██╗░░██║██╔══██╗██╔════╝╚══██╔══╝██║██║░██╔╝   ║
║    ╚█████╗░╚██╗████╗██╔╝███████║╚█████╗░░░░██║░░░██║█████═╝░   ║
║    ░╚═══██╗░████╔═████║░██╔══██║░╚═══██╗░░░██║░░░██║██╔═██╗░   ║
║    ██████╔╝░╚██╔╝░╚██╔╝░██║░░██║██████╔╝░░░██║░░░██║██║░╚██╗   ║
║    ╚═════╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚═╝╚═╝░░╚═╝   ║
║                                                                  ║
║           [ CYBERSECURITY RESEARCHER · CS UNDERGRAD ]            ║
╚══════════════════════════════════════════════════════════════════╝
```

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&size=18&pause=1000&color=00FF88&center=true&vCenter=true&width=600&lines=Cybersecurity-focused+CS+Undergrad;Honeypots+%7C+Network+Recon+%7C+Linux+Systems;Mobile+Packet+Analysis+%7C+Kali+NetHunter;Research+Intern+%7C+Threat+Detection;Building+tools+defenders+rely+on.)](https://git.io/typing-svg)

<br>

[![GitHub followers](https://img.shields.io/github/followers/amibhai?style=flat-square&color=00ff88&labelColor=0d1117&label=followers)](https://github.com/amibhai)
![Profile Views](https://komarev.com/ghpvc/?username=amibhai&color=00ff88&style=flat-square&label=profile+views)
[![Email](https://img.shields.io/badge/email-swastik362004%40gmail.com-00cfff?style=flat-square&labelColor=0d1117)](mailto:swastik362004@gmail.com)

</div>

---

## `whoami`

```bash
┌──(swastik㉿kali)-[~]
└─$ cat profile.txt

  Name     : Swastik
  Handle   : amibhai
  Role     : Cybersecurity Researcher · Research Intern · CS Undergrad
  Focus    : Threat Detection · Network Recon · Mobile Security · Honeypots
  OS       : Linux (Kali) · Android (NetHunter)
  Language : Python · Dart/Flutter · Kotlin · C
  Mission  : Building tools that help defenders see what attackers do.
```

> *"Every packet tells a story. I listen."*

---

## 🛡️ What I Build

I build **offensive and defensive security tooling** — from a Wireshark-like mobile packet analyzer for Kali NetHunter, to honeypot telemetry pipelines that score attacker behavior in real time, to full-spectrum network recon suites. My work sits at the edge between red and blue team thinking, across mobile, Linux, and cloud.

---

## 🔥 Featured Projects

<table>
<tr>
<td width="50%">

### 📱 [AndroNet](https://github.com/amibhai/AndroNet) `🔺 TOP PROJECT`

**Mobile Network Packet Analyzer for Kali NetHunter** — a professional-grade Wireshark alternative that runs natively on Android. Built with Team CipherSec.

**Capabilities:**
- Dual-mode capture: VPN (unrooted) + libpcap (NetHunter root)
- Deep Packet Inspection — HTTP, DNS, TLS, DHCP, 65+ protocols
- Real-time anomaly detection: Port Scan, SYN Flood, ARP Spoofing, DNS Tunneling
- PCAP export (Wireshark-compatible, microsecond precision)
- 0% packet loss, 500–1000+ pps throughput

**Stack:** `Flutter` `Dart` `Kotlin` `C/JNI` `libpcap` `zdtun` `Kali NetHunter`

> 👥 Team CipherSec — Ritik, Syed Misbah, Kamal, Swastik

</td>
<td width="50%">

### 🍯 [Honeypot Risk Scoring Model](https://github.com/amibhai/Honeypot-Risk-Scoring-Model)

A telemetry analysis pipeline that ingests honeypot logs, extracts behavioral features, and computes **weighted risk scores** visualized in Kibana for SOC triage.

**Stack:** `Cowrie` `Dionaea` `Filebeat` `Logstash` `Elasticsearch` `Kibana` `Python` `GeoIP2`

```
Risk Formula:
score = w1·frequency + w2·severity
      + w3·payload_risk + w4·reputation
```

`🟢 Low` `🟡 Medium` `🔴 High` scoring with tunable weights

</td>
</tr>
<tr>
<td width="50%">

### 🔍 [Recon Toolkit](https://github.com/amibhai/recon-toolkit)

Complete **network reconnaissance suite** — standalone, no external toolkit dependencies.

**Capabilities:**
- DNS enum (zone transfer, subdomain brute-force)
- ARP / ICMP / TCP / UDP host discovery
- OS fingerprinting (TTL, TCP stack, banner)
- SYN / FIN / XMAS / ACK / UDP port scans
- CVE detection, SSL audit, default cred testing
- Wireless monitor mode + channel hopping
- Inline PCAP capture on every scan

**Stack:** `Scapy` `dnspython` `aircrack-ng` `Python`

</td>
<td width="50%">

### 🔐 [Credential Attacks Toolkit](https://github.com/amibhai/credential-attacks-toolkit)

Authorized security testing suite covering **6 attack types** — SSH, FTP, Web Login, Brute-force, Dictionary, and Scripted attacks.

**Features:** leet-speak mutations · lockout detection · rate-limit evasion · multi-threaded · proxy rotation

**Stack:** `paramiko` `requests` `Python`

> ⚠️ For authorized testing only

---

### 🛡️ [HYBRID-IDS-MCP](https://github.com/amibhai/HYBRID-IDS-MCP)

Hybrid **Intrusion Detection System** combining signature-based and anomaly-based detection using the MCP protocol architecture for layered network threat analysis.

**Stack:** `Python` `MCP`

</td>
</tr>
</table>

---

## ⚔️ Skill Matrix

<table>
<tr>
<td>

**Offensive**
```
Network Reconnaissance  ████████████ 95%
Port Scanning           ████████████ 95%
Mobile Packet Analysis  ██████████░░ 88%
Credential Attacks      ██████████░░ 82%
Vulnerability Scanning  ██████████░░ 80%
```

</td>
<td>

**Defensive**
```
Honeypot Deployment     ████████████ 92%
Risk Scoring / SIEM     ██████████░░ 85%
SOC / Alert Triage      ██████████░░ 82%
IDS Architecture        ████████░░░░ 75%
Threat Intelligence     ████████░░░░ 75%
```

</td>
</tr>
</table>

---

## 🧰 Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-0d1117?style=for-the-badge&logo=python&logoColor=00ff88)
![Flutter](https://img.shields.io/badge/Flutter-0d1117?style=for-the-badge&logo=flutter&logoColor=00cfff)
![Kotlin](https://img.shields.io/badge/Kotlin-0d1117?style=for-the-badge&logo=kotlin&logoColor=00cfff)
![C](https://img.shields.io/badge/C%2FJNI-0d1117?style=for-the-badge&logo=c&logoColor=ffb400)
![Linux](https://img.shields.io/badge/Linux-0d1117?style=for-the-badge&logo=linux&logoColor=00ff88)
![Kali](https://img.shields.io/badge/Kali_Linux-0d1117?style=for-the-badge&logo=kalilinux&logoColor=00cfff)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-0d1117?style=for-the-badge&logo=elasticsearch&logoColor=00cfff)
![Kibana](https://img.shields.io/badge/Kibana-0d1117?style=for-the-badge&logo=kibana&logoColor=ffb400)
![Wireshark](https://img.shields.io/badge/Wireshark-0d1117?style=for-the-badge&logo=wireshark&logoColor=00cfff)
![Git](https://img.shields.io/badge/Git-0d1117?style=for-the-badge&logo=git&logoColor=ff3b5c)

</div>

**Security Tools:** `Scapy` `libpcap` `zdtun` `Cowrie` `Dionaea` `Filebeat` `Logstash` `aircrack-ng` `paramiko` `dnspython` `GeoIP2`

**Concepts:** `Honeypots` `DPI` `SIEM` `IDS/IPS` `CVE Analysis` `PCAP Forensics` `Network Protocols` `Mobile Security` `Threat Intel` `Red Teaming`

---

## 📊 GitHub Stats

<div align="center">

<img height="165" src="https://github-readme-stats.vercel.app/api?username=amibhai&show_icons=true&theme=chartreuse-dark&bg_color=0d1117&border_color=1a2e45&title_color=00ff88&icon_color=00cfff&text_color=c8d8e8&hide_border=false" />
<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=amibhai&layout=compact&theme=chartreuse-dark&bg_color=0d1117&border_color=1a2e45&title_color=00ff88&text_color=c8d8e8&hide_border=false" />

</div>

---

## 📡 Currently

- 🔭 Building tools at the intersection of **mobile security**, **threat detection**, and **network intelligence**
- 🌱 Deepening research in **behavioral analysis of honeypot telemetry** and **DPI on mobile platforms**
- 🔬 Exploring **ML-based anomaly detection** for SOC workflows
- 💬 Ask me about **Scapy, libpcap, Flutter/NetHunter, Honeypots, ELK Stack**

---

## 📬 Contact

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-amibhai-0d1117?style=for-the-badge&logo=github&logoColor=00ff88)](https://github.com/amibhai)
[![Email](https://img.shields.io/badge/Email-swastik362004%40gmail.com-0d1117?style=for-the-badge&logo=gmail&logoColor=ff3b5c)](mailto:swastik362004@gmail.com)

</div>

---

<div align="center">

```
[ AUTHORIZED SECURITY TESTING ONLY · USE TOOLS RESPONSIBLY ]
```

*"Defenders think in lists. Attackers think in graphs. I try to think in both."*

</div>
