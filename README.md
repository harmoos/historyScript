# Multi-OS History Stealer & Forensic Tool

A powerful Python-based forensic utility designed to extract navigation history and network evidences across **Windows** and **Linux** environments. This tool is specifically engineered to bypass modern security hurdles like the **Microsoft Store Sandbox** and to extract **DNS Cache** directly from system memory (RAM).

---

## Key Features

* **Advanced Browser Detection:** Automatically locates profiles for Chrome, Firefox, Edge, Brave, Chromium, and Opera.
* **Sandbox Bypass (MSIX/UWP):** Successfully traverses `AppData\Local\Packages` to find Firefox data when installed via the Microsoft Store.
* **SQLite Deep Extraction:** Directly queries `places.sqlite` (Firefox) and `History` (Chromium) databases to retrieve URLs, timestamps, and visit counts.
* **DNS Forensics:**
    * **Windows:** Extracts the active DNS Resolver Cache from the OS RAM.
    * **Linux:** Attempts to capture DNS artifacts and active network states.
* **Multi-OS Support:** Native execution logic for both Windows (PowerShell) and Linux (Terminal).

---

## How it Works

### 1. The Sandbox Challenge
Modern Windows Apps (like Firefox from the Store) don't store data in the traditional `%APPDATA%`. They use a **Virtual File System**. This script dynamically maps the `LocalCache` inside the `Packages` directory to find hidden profiles that traditional tools often miss.

### 2. Live History Extraction
The tool creates a temporary shadow copy of the browser's SQLite database. This bypasses "File Locked" errors that occur when the browser is currently open, allowing for real-time data collection without closing the user's session.

### 3. DNS Cache (RAM Analysis)
History can be deleted, but the DNS Cache often remains in RAM. This tool dumps the resolver cache to show which domains were contacted by the machine recently, providing a secondary layer of evidence.

---

## Installation

### Prerequisites
You must have **Python 3.8+** installed.
You must clone the repository and run with 
* Windows: python main.py
* Linux: sudo python3 main.py (Sudo is required for DNS/Network evidence collection, but not mandatory)

---

## Output Evidences
After execution, the tool generates:
* history.txt: Raw dump of all found browser history.
* forensic.txt: Analyzed data with timestamps and visit frequency.
* win_dns_evidences.txt or dns_evidences.txt: The captured DNS Resolver Cache from RAM.

## Disclaimer
This tool is for educational and authorized forensic purposes only. Unauthorized access to private data is illegal. The author is not responsible for any misuse of this software.

