[app]

title = Calcify
package.name = calcify
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 0.1
requirements = python3,kivy
orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.3.0

fullscreen = 0

# Ключевые настройки для Android
android.accept_sdk_license = True
android.ndk = 23c
android.sdk = 30
android.build_tools = 30.0.3
android.minapi = 21
android.ndk_api = 21
android.gradle_dependencies = ''
android.enable_androidx = True

# Ваши шрифты
add_sources = JetBrainsMono-Bold.ttf, JetBrainsMono-Regular.ttf

[buildozer]

log_level = 2
warn_on_root = 1
