#!/bin/bash

# VoxPersonal v6 - Premium Launcher for macOS

# Установка кодировки
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Очистка экрана
clear

# Современный баннер
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║                                         ║"
echo "║        ██╗   ██╗ ██████╗ ██╗  ██╗       ║"
echo "║        ██╗   ██╗██╔═══██╗╚██╗██╔╝       ║"
echo "║        ██╗   ██║██║   ██║ ╚███╔╝        ║"
echo "║        ╚██╗ ██╔╝██║   ██║ ██╔██╗        ║"
echo "║         ╚████╔╝ ╚██████╔╝██╔╝ ██╗       ║"
echo "║          ╚═══╝   ╚═════╝ ╚═╝  ╚═╝       ║"
echo "║                                         ║"
echo "║          V O X   P E R S O N A L        ║"
echo "║                 v6.0                    ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Проверка системы
echo "[SYSTEM CHECK]"
echo ""

# Проверка Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ CRITICAL: Python 3 not found"
    echo "   Download from: https://python.org"
    echo ""
    echo "Press any key to continue..."
    read -n 1
    exit 1
fi

echo "✅ Python 3 OK"

# Проверка Tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ ERROR: Tkinter missing"
    echo ""
    echo "Install with:"
    echo "   macOS: Install Python from python.org (includes Tk)"
    echo "   OR brew install python-tk"
    echo ""
    echo "Press any key to continue..."
    read -n 1
    exit 1
fi

echo "✅ Tkinter OK"

# Проверка других зависимостей
echo ""
echo "[CHECKING DEPENDENCIES]"

# Проверка pip
if ! command -v pip3 &> /dev/null; then
    echo "⚠️  pip3 not found, installing..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# Установка зависимостей если requirements.txt существует
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo ""
echo "[LAUNCHING]"
echo ""
echo "⚡ Initializing premium interface..."
echo "🎨 Loading modern design..."
echo "🔥 Starting VOX PERSONAL v6..."
echo ""

# Краткая задержка с анимацией
for i in {1..3}; do
    echo "   Starting.$i"
    sleep 1
done

clear

# Запуск Python приложения
echo ""
echo "🚀 VOX PERSONAL v6 - PREMIUM INTERFACE"
echo "═══════════════════════════════════════════"
echo ""
echo "Features:"
echo "• Ultra-modern dark theme"
echo "• Neon color scheme"
echo "• Smooth animations"
echo "• Glassmorphism effects"
echo "• Premium UI/UX"
echo ""
sleep 2

# Основной запуск
python3 app.py

# Обработка ошибок
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  LAUNCH FAILED"
    echo "═══════════════════════════════════════════"
    echo ""
    echo "Possible solutions:"
    echo "1. Check app.py exists in current folder"
    echo "2. Install dependencies: pip3 install -r requirements.txt"
    echo "3. Ensure microphone permissions are granted"
    echo ""
    echo "Press any key to continue..."
    read -n 1
else
    echo ""
    echo "✅ Application closed successfully"
    sleep 2
fi

exit 0