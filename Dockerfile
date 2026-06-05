FROM --platform=linux/amd64 kivy/buildozer:latest

# Добавляем 32-битную архитектуру и устанавливаем необходимые библиотеки
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y libc6:i386 libstdc++6:i386 && \
    rm -rf /var/lib/apt/lists/*
