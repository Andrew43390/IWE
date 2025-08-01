# Filename: IWE.py
# Location: C:\Users\james\Desktop\IWE
# Purpose: Improve system functionality with auditability, feedback, and evolution

import os, sys, platform, psutil, socket, datetime, json, re
from tkinter import Tk, messagebox

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
MODULE_DIR = os.path.join(ROOT_DIR, 'modules')
ALLOWED_FILES = {'IWE.py'}

def show_popup(title, message):
    root = Tk(); root.withdraw()
    messagebox.showinfo(title, message)

def sanitize_for_log(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def write_log_safely(path, content):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content + '\n')
    except UnicodeEncodeError:
        with open(path, 'w') as f:
            f.write(sanitize_for_log(content) + '\n')

def log_event(event):
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_path = os.path.join(LOG_DIR, f"log_{timestamp}.txt")
    entry = f"[{timestamp}] {event}"
    write_log_safely(log_path, entry)
    return log_path

def enforce_folder_hygiene():
    root_files = {f for f in os.listdir(ROOT_DIR) if os.path.isfile(os.path.join(ROOT_DIR, f))}
    extras = root_files - ALLOWED_FILES
    if extras:
        msg = f"Hygiene violation: unexpected file(s) at root:\n{', '.join(extras)}"
        show_popup("Hygiene Error", msg)
        log_event(msg)
        sys.exit(1)

def fingerprint_system():
    try:
        info = {
            'OS': platform.platform(),
            'Architecture': platform.architecture()[0],
            'CPU': platform.processor(),
            'RAM_MB': int(psutil.virtual_memory().total / (1024 * 1024)),
            'Disk_Usage': f"{psutil.disk_usage('/').percent}%",
            'Hostname': socket.gethostname(),
            'IP': socket.gethostbyname(socket.gethostname())
        }
        log_event(f"System Fingerprint:\n{json.dumps(info, indent=2)}")
        return info
    except Exception as e:
        log_event(f"Fingerprinting Failed: {e}")
        return {}

def propose_improvement(info):
    proposal = {
        "suggestion": "Integrate targeted enhancements based on system profile.",
        "system_profile": info,
        "next_steps": [
            "Design profile criteria → Module triggers",
            "Add 'modules/' scanner → run matching enhancements",
            "Fallback logging → if no match found"
        ]
    }
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    proposal_path = os.path.join(LOG_DIR, f"proposal_{timestamp}.txt")
    try:
        with open(proposal_path, 'w', encoding='utf-8') as f:
            json.dump(proposal, f, indent=2)
    except UnicodeEncodeError:
        with open(proposal_path, 'w') as f:
            json.dump(json.loads(sanitize_for_log(json.dumps(proposal))), f, indent=2)
    log_event("Self-development proposal saved.")

def scan_for_modules(profile):
    os.makedirs(MODULE_DIR, exist_ok=True)
    matched = []
    for mod in os.listdir(MODULE_DIR):
        if mod.endswith('.py'):
            matched.append(mod)
    if matched:
        log_event(f"Modules ready: {', '.join(matched)}")
        show_popup("Modules Detected", f"Ready to deploy: {', '.join(matched)}")
    else:
        log_event("No matching modules found. Fallback only.")
        show_popup("No Enhancements", "No applicable modules found. Self-improvement logged.")

def main():
    enforce_folder_hygiene()
    log_event("IWE Agent Started Successfully.")  # ✅ replaced with plain text for reliability
    show_popup("Agent Initialized", "IWE.py has started and passed hygiene checks.")
    profile = fingerprint_system()
    propose_improvement(profile)
    scan_for_modules(profile)

if __name__ == '__main__':
    main()

