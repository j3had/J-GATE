🛡️ J_GATE v1.0
╔═══════════════════════════════════════════════════════════╗
║                     J_GATE v1.0                          ║
║                Admin Panel Finder Tool                   ║
╚═══════════════════════════════════════════════════════════╝
📋 About
J_GATE is a powerful tool for finding admin panels and testing login credentials on web applications. Perfect for security researchers and penetration testers.
🚀 Quick Start
Installation
pip install requests colorama
Run
python j_gate.py
⚙️ Features
Feature
Description
🔍 Admin Panel Scanner
Automatically find login/admin pages
🔐 Brute Force
Test common credentials (14+ combinations)
🎯 Custom Test
Test your own username/password
⚡ Fast Scanning
Multi-path detection with HTTP status codes
📱 Menu Options
┌─────────────────────────────────────────┐
│ [1] Find Admin Panels                   │
│ [2] Brute Force Login                   │
│ [3] Custom Credentials Test             │
│ [4] Exit                                │
└─────────────────────────────────────────┘
🎯 Supported Paths
login • admin • wp-admin • cpanel
phpmyadmin • dashboard • panel
And 20+ more paths...
📦 Requirements
Python 3.6+
requests library
colorama library
⚖️ Disclaimer
This tool is designed for:
✓ Educational purposes
✓ Authorized security testing
✓ Penetration testing (with permission)

Unauthorized access to computer systems is illegal.
Use responsibly!
📝 Example Usage
$ python j_gate.py

[*] Enter target website: example.com

[1] Find Admin Panels
[2] Brute Force Login
[3] Custom Credentials Test
[4] Exit

[+] FOUND: http://example.com/admin (200)
[+] FOUND: http://example.com/login (200)
Made with ❤️ for security research
