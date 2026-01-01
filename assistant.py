"""
VoxPersonal v6 - Умный ассистент с продвинутыми командами (macOS версия)
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import os
import time
import pyautogui
import json
import datetime
import random
import requests
import threading
import sys
import re
import platform

class VoxPersonalV6:
    def __init__(self, gui_callback=None):
        self.name = "Vox Personal v6 (macOS)"
        self.is_listening = False
        self.user_name = None
        self.volume = 50
        self.weather_api_key = None
        self.command_history = []
        self.vox_mode = False
        self.gui_callback = gui_callback
        self.is_active = False
        self.current_command = None
        self.is_macos = platform.system() == 'Darwin'
        
        # Команды (остаются те же, только пути macOS)
        self.commands = {
            # Базовые
            "привет": self._hello,
            "как дела": self._how_are_you,
            "пока": self._goodbye,
            
            # Системные (macOS)
            "открой браузер": self._open_browser_mac,
            "закрой браузер": self._close_browser_mac,
            "открой системные настройки": self._open_system_preferences,
            "открой терминал": self._open_terminal,
            "открой монитор активности": self._open_activity_monitor,
            "сделай скриншот": self._take_screenshot_mac,
            
            # Медиа
            "громче": self._volume_up_mac,
            "тише": self._volume_down_mac,
            "стоп": self._media_stop_mac,
            "пауза": self._media_pause_play_mac,
            "продолжи": self._media_pause_play_mac,
            "следующий трек": self._next_track_mac,
            "предыдущий трек": self._previous_track_mac,
            "включи музыку": self._play_music,
            
            # Интернет
            "открой youtube": self._open_youtube,
            "открой сайт": self._open_website,
            "поиск в интернете": self._web_search,
            "какая погода": self._weather,
            
            # Информационные
            "сколько времени": self._what_time,
            "какая дата": self._what_date,
            "случайное число": self._random_number,
            "расскажи шутку": self._tell_joke,
            "кто ты": self._who_are_you,
            
            # Развлекательные
            "включи кино": self._play_movie,
            "покажи котика": self._show_cat,
            "скажи предсказание": self._fortune_telling,
            
            # Управление
            "выключи компьютер": self._shutdown_mac,
            "перезагрузи компьютер": self._restart_mac,
            "спрячь все окна": self._hide_all_windows,
            "покажи рабочий стол": self._show_desktop_mac,
            
            # Помощь
            "что ты умеешь": self._help_mac,
            "повтори команду": self._repeat_command,
        }
        
        # Синонимы (обновлены для macOS)
        self.synonyms = {
            "системные настройки": "открой системные настройки",
            "настройки": "открой системные настройки",
            "монитор системы": "открой монитор активности",
            "диспетчер задач": "открой монитор активности",
            "терминал": "открой терминал",
            "консоль": "открой терминал",
            "сверни все": "спрячь все окна",
            "скрой окна": "спрячь все окна",
            "рабочий стол": "покажи рабочий стол",
            "десктоп": "покажи рабочий стол",
            "выключи mac": "выключи компьютер",
            "выключи мак": "выключи компьютер",
            "перезагрузи mac": "перезагрузи компьютер",
            "перезагрузи мак": "перезагрузи компьютер",
        }
        
        # Популярные сайты
        self.websites = {
            "гугл": "https://google.com",
            "яндекс": "https://yandex.ru",
            "почту": "https://gmail.com",
            "почта": "https://gmail.com",
            "гитхаб": "https://github.com",
            "гит": "https://github.com",
            "стековерфлоу": "https://stackoverflow.com",
            "стек": "https://stackoverflow.com",
            "википедию": "https://wikipedia.org",
            "википедия": "https://wikipedia.org",
            "нетфликс": "https://netflix.com",
            "дискорд": "https://discord.com",
            "редит": "https://reddit.com",
            "сафари": "https://apple.com",
            "аппл": "https://apple.com",
        }
        
        # Пути к приложениям macOS
        self.mac_apps = {
            "safari": "/Applications/Safari.app",
            "chrome": "/Applications/Google Chrome.app",
            "firefox": "/Applications/Firefox.app",
            "brave": "/Applications/Brave Browser.app",
            "opera": "/Applications/Opera.app",
            "terminal": "/System/Applications/Utilities/Terminal.app",
            "activity_monitor": "/System/Applications/Utilities/Activity Monitor.app",
            "system_preferences": "/System/Applications/System Preferences.app",
            "app_store": "/System/Applications/App Store.app",
            "calculator": "/System/Applications/Calculator.app",
            "calendar": "/System/Applications/Calendar.app",
            "notes": "/System/Applications/Notes.app",
            "reminders": "/System/Applications/Reminders.app",
            "music": "/System/Applications/Music.app",
            "tv": "/System/Applications/TV.app",
            "podcasts": "/System/Applications/Podcasts.app",
            "books": "/System/Applications/Books.app",
            "messages": "/System/Applications/Messages.app",
            "facetime": "/System/Applications/FaceTime.app",
            "photos": "/System/Applications/Photos.app",
            "preview": "/System/Applications/Preview.app",
            "textedit": "/System/Applications/TextEdit.app",
        }
        
        # Инициализация
        self._init_speech()
        self._load_config()
    
    def _init_speech(self):
        """Инициализация голосовых систем для macOS"""
        try:
            # Распознавание
            self.recognizer = sr.Recognizer()
            
            # Проверяем доступность микрофонов
            mics = sr.Microphone.list_microphone_names()
            if not mics:
                print("⚠️  Микрофоны не найдены")
                self.microphone = None
            else:
                print(f"🎤 Доступные микрофоны: {mics}")
                self.microphone = sr.Microphone(device_index=0)
            
            # Синтез речи
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 1.0)
            
            # Выбор голоса для macOS
            voices = self.tts_engine.getProperty('voices')
            print(f"🔊 Доступные голоса: {[v.name for v in voices]}")
            
            # Пытаемся найти русский голос или любой доступный
            for voice in voices:
                if 'russian' in voice.name.lower() or 'русск' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    print(f"✅ Выбран русский голос: {voice.name}")
                    break
            else:
                # Если русский не найден, берем первый доступный
                if voices:
                    self.tts_engine.setProperty('voice', voices[0].id)
                    print(f"✅ Выбран голос по умолчанию: {voices[0].name}")
            
            print(f"✅ {self.name} инициализирован")
            
        except Exception as e:
            print(f"❌ Ошибка инициализации: {e}")
            print("💡 Решение: Установите необходимые зависимости:")
            print("   pip install speechrecognition pyttsx3")
            if self.is_macos:
                print("   brew install portaudio")
                print("   pip install pyaudio")
    
    # ==== macOS СПЕЦИФИЧНЫЕ МЕТОДЫ ====
    
    def _open_browser_mac(self):
        """Открыть браузер на macOS"""
        browsers_order = ['safari', 'chrome', 'firefox', 'brave', 'opera']
        
        for browser in browsers_order:
            app_path = self.mac_apps.get(browser)
            if app_path and os.path.exists(app_path):
                try:
                    subprocess.run(['open', app_path], check=True)
                    return f"Запускаю {browser.capitalize()}"
                except Exception as e:
                    print(f"Ошибка запуска {browser}: {e}")
        
        # Если не нашли установленные браузеры
        webbrowser.open("https://google.com")
        return "Открываю Google в браузере по умолчанию"
    
    def _close_browser_mac(self):
        """Закрыть браузер на macOS"""
        browsers = ['Safari', 'Google Chrome', 'Firefox', 'Brave Browser', 'Opera']
        
        for browser in browsers:
            try:
                # Используем AppleScript для закрытия приложения
                script = f'''
                tell application "{browser}"
                    quit
                end tell
                '''
                subprocess.run(['osascript', '-e', script], capture_output=True)
                print(f"🛑 Закрытие {browser}...")
            except:
                continue
        
        return "Браузеры закрыты"
    
    def _open_system_preferences(self):
        """Открыть Системные настройки"""
        try:
            subprocess.run(['open', self.mac_apps['system_preferences']])
            return "Открываю Системные настройки"
        except:
            return "Не удалось открыть Системные настройки"
    
    def _open_terminal(self):
        """Открыть Терминал"""
        try:
            subprocess.run(['open', self.mac_apps['terminal']])
            return "Запускаю Терминал"
        except:
            return "Не удалось открыть Терминал"
    
    def _open_activity_monitor(self):
        """Открыть Монитор активности"""
        try:
            subprocess.run(['open', self.mac_apps['activity_monitor']])
            return "Открываю Монитор активности"
        except:
            return "Не удалось открыть Монитор активности"
    
    def _take_screenshot_mac(self):
        """Сделать скриншот на macOS"""
        try:
            # Создаем папку для скриншотов если её нет
            if not os.path.exists('screenshots'):
                os.makedirs('screenshots')
            
            # Генерируем имя файла
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join('screenshots', filename)
            
            # Используем команду screencapture
            subprocess.run(['screencapture', filepath])
            
            print(f"📸 Скриншот сохранен: {filepath}")
            self._update_gui('screenshot_taken', filepath)
            return f"Скриншот сохранён как {filename}"
        except Exception as e:
            return f"Не удалось сделать скриншот: {str(e)}"
    
    def _volume_up_mac(self):
        """Увеличить громкость на macOS"""
        try:
            # Используем AppleScript для управления громкостью
            script = '''
            set currentVolume to output volume of (get volume settings)
            set newVolume to currentVolume + 20
            if newVolume > 100 then set newVolume to 100
            set volume output volume newVolume
            return "Громкость: " & newVolume & "%"
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                   capture_output=True, text=True)
            return result.stdout.strip()
        except:
            return "Используйте клавиши F12 или F11 для управления громкостью"
    
    def _volume_down_mac(self):
        """Уменьшить громкость на macOS"""
        try:
            script = '''
            set currentVolume to output volume of (get volume settings)
            set newVolume to currentVolume - 20
            if newVolume < 0 then set newVolume to 0
            set volume output volume newVolume
            return "Громкость: " & newVolume & "%"
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                   capture_output=True, text=True)
            return result.stdout.strip()
        except:
            return "Используйте клавиши F12 или F11 для управления громкостью"
    
    def _media_stop_mac(self):
        """Остановить медиа на macOS"""
        try:
            # Используем AppleScript для управления медиа
            script = '''
            tell application "System Events"
                key code 49  -- Space for pause/play
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return "Воспроизведение остановлено"
        except:
            return "Нажмите клавишу пробела для управления воспроизведением"
    
    def _media_pause_play_mac(self):
        """Пауза/продолжить на macOS"""
        try:
            script = '''
            tell application "System Events"
                key code 49  -- Space for pause/play
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return "Переключил воспроизведение"
        except:
            return "Нажмите клавишу пробела"
    
    def _next_track_mac(self):
        """Следующий трек на macOS"""
        try:
            script = '''
            tell application "System Events"
                key code 124  -- Right arrow for next track
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return "Следующий трек"
        except:
            return "Используйте клавиши управления медиа"
    
    def _previous_track_mac(self):
        """Предыдущий трек на macOS"""
        try:
            script = '''
            tell application "System Events"
                key code 123  -- Left arrow for previous track
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return "Предыдущий трек"
        except:
            return "Используйте клавиши управления медиа"
    
    def _hide_all_windows(self):
        """Спрятать все окна на macOS"""
        try:
            script = '''
            tell application "System Events"
                keystroke "h" using {command down, option down}
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return "Все окна скрыты"
        except:
            return "Используйте Command + Option + H"
    
    def _show_desktop_mac(self):
        """Показать рабочий стол на macOS"""
        try:
            # Используем Mission Control для показа рабочего стола
            script = '''
            tell application "System Events"
                key code 160 using {control down}  -- F11 equivalent
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return "Показываю рабочий стол"
        except:
            # Альтернативный способ
            try:
                pyautogui.hotkey('fn', 'f11')
                return "Показываю рабочий стол"
            except:
                return "Используйте Fn + F11 или Ctrl + Стрелка вверх"
    
    def _shutdown_mac(self):
        """Выключить macOS"""
        self.speak("Вы уверены что хотите выключить компьютер? Скажите да или нет")
        confirm = self.listen()
        if confirm and "да" in confirm:
            try:
                subprocess.run(['osascript', '-e', 'tell app "System Events" to shut down'])
                return "Выключаю компьютер..."
            except:
                return "Выберите 'Выключить' в меню Apple"
        return "Выключение отменено"
    
    def _restart_mac(self):
        """Перезагрузить macOS"""
        self.speak("Вы уверены что хотите перезагрузить компьютер? Скажите да или нет")
        confirm = self.listen()
        if confirm and "да" in confirm:
            try:
                subprocess.run(['osascript', '-e', 'tell app "System Events" to restart'])
                return "Перезагружаю компьютер..."
            except:
                return "Выберите 'Перезагрузить' в меню Apple"
        return "Перезагрузка отменена"
    
    def _help_mac(self):
        """Показать список команд для macOS"""
        categories = {
            "🎯 Базовые": ["привет", "вокс (активация)", "как дела", "пока"],
            "💻 Система macOS": [
                "открой браузер", 
                "открой системные настройки", 
                "открой терминал", 
                "открой монитор активности",
                "сделай скриншот"
            ],
            "🌐 Сайты": ["открой сайт [название]", "открой youtube", "поиск в интернете"],
            "🎵 Медиа": ["громче", "тише", "стоп", "пауза", "следующий трек", "включи музыку"],
            "📅 Информация": ["сколько времени", "какая дата", "случайное число", "расскажи шутку"],
            "🎮 Развлечения": ["включи кино", "покажи котика", "скажи предсказание"],
            "⚙️ Управление macOS": [
                "выключи компьютер", 
                "спрячь все окна", 
                "покажи рабочий стол"
            ]
        }
        
        response = "Я умею многое! Вот основные команды для macOS:\n\n"
        for category, commands in categories.items():
            response += f"{category}:\n"
            for cmd in commands:
                response += f"  • {cmd}\n"
            response += "\n"
        
        response += "Просто скажите 'вокс' или 'привет' для начала общения!"
        
        self._update_gui('help_commands', categories)
        
        print("\n📋 СПИСОК КОМАНД (macOS):")
        for category, commands in categories.items():
            print(f"\n{category}:")
            for cmd in commands:
                print(f"  • {cmd}")
        return response
    
    # ==== ОБЩИЕ МЕТОДЫ (остаются как были) ====
    
    def speak(self, text, wait=True):
        """Произнести текст"""
        print(f"\n🤖 [{self.name}]: {text}")
        print("─" * 60)
        
        if self.gui_callback:
            self.gui_callback('assistant_speak', text)
        
        self.tts_engine.say(text)
        if wait:
            self.tts_engine.runAndWait()
    
    def listen(self, timeout=5, phrase_time_limit=7):
        """Слушать микрофон (адаптировано для macOS)"""
        try:
            if not self.microphone:
                print("⚠️  Микрофон не доступен")
                return None
            
            with self.microphone as source:
                print("\n🔊 Калибровка фонового шума...")
                if self.gui_callback:
                    self.gui_callback('calibrating', None)
                
                # Меньшая длительность калибровки для macOS
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                print("\n" + "█" * 30)
                print(" " * 10 + "🎤 СЛУШАЮ...")
                print("█" * 30)
                
                if self.gui_callback:
                    self.gui_callback('listening_start', None)
                
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("\n" + "░" * 30)
                print(" " * 10 + "🔍 ОБРАБАТЫВАЮ...")
                print("░" * 30)
                
                if self.gui_callback:
                    self.gui_callback('processing_start', None)
                
                print("\n📊 Распознаю команду...")
                text = self.recognizer.recognize_google(audio, language="ru-RU").lower()
                
                if text:
                    print("\n📝 РАСПОЗНАНО: ", end="")
                    print(f"\033[92m{text}\033[0m")
                    print("─" * 40)
                    
                    if self.gui_callback:
                        self.gui_callback('text_recognized', text)
                    
                    return text
                
        except sr.WaitTimeoutError:
            print("\n⏰ Таймаут: голос не обнаружен")
            if self.gui_callback:
                self.gui_callback('timeout', None)
        except sr.UnknownValueError:
            print("\n❌ Не удалось распознать речь")
            if self.gui_callback:
                self.gui_callback('unknown_value', None)
        except Exception as e:
            print(f"\n❌ Ошибка слушания: {e}")
            if self.gui_callback:
                self.gui_callback('error', str(e))
        
        return None
    
    # ... остальные методы остаются как были (_hello, _how_are_you, и т.д.)
    # за исключением тех, что были адаптированы выше
    
    def process_command(self, text):
        """Обработка команды с учетом macOS"""
        if not text:
            return None
        
        # Сохраняем в историю
        self.command_history.append(text[:50])
        print(f"\n📚 История команд: {self.command_history[-3:]}")
        
        if self.gui_callback:
            self.gui_callback('command_history', self.command_history[-3:])
        
        # Проверяем команду для открытия сайта
        if "открой сайт" in text:
            site_query = text.replace("открой сайт", "").strip()
            return self._open_website(site_query)
        
        # Проверяем точное совпадение с командами macOS
        for cmd, func in self.commands.items():
            if cmd in text:
                print(f"🎯 Найдена команда: {cmd}")
                self.current_command = cmd
                if self.gui_callback:
                    self.gui_callback('command_found', cmd)
                return func()
        
        # Проверяем синонимы (включая macOS-специфичные)
        for synonym, command in {**self.synonyms, **self.commands}.items():
            if synonym in text:
                print(f"🔍 Синоним: {synonym}")
                if command in self.commands:
                    self.current_command = command
                    if self.gui_callback:
                        self.gui_callback('synonym_used', {'synonym': synonym, 'command': command})
                    return self.commands[command]()
        
        # Обработка "Вокс"
        if "вокс" in text:
            command_part = text.replace("вокс", "").strip()
            if command_part:
                for cmd, func in self.commands.items():
                    if cmd in command_part:
                        print(f"🎯 Вокс-команда: {cmd}")
                        self.current_command = cmd
                        if self.gui_callback:
                            self.gui_callback('vox_command', cmd)
                        return func()
            
            self.vox_mode = True
            self.is_active = True
            if self.gui_callback:
                self.gui_callback('vox_mode_on', None)
            return "Слушаю вас! Говорите команду."
        
        # Вокс-режим
        if self.vox_mode and text:
            for cmd, func in self.commands.items():
                if cmd in text:
                    print(f"🎯 Вокс-режим: {cmd}")
                    self.current_command = cmd
                    if self.gui_callback:
                        self.gui_callback('vox_mode_command', cmd)
                    return func()
        
        # Установка имени
        if "меня зовут" in text:
            name = text.split("меня зовут")[-1].strip()
            self.user_name = name
            print(f"👤 Установлено имя: {name}")
            if self.gui_callback:
                self.gui_callback('user_name_set', name)
            return f"Приятно познакомиться, {name}!"
        
        # Не распознали
        responses = [
            "Извините, не понял команду. Попробуйте сказать 'что ты умеешь'",
            "Не распознал команду. Скажите 'помощь' для списка команд",
        ]
        response = random.choice(responses)
        print(f"❌ Не распознано: {text}")
        if self.gui_callback:
            self.gui_callback('command_not_recognized', text)
        return response
    
    def run(self):
        """Основной цикл работы"""
        print("\n" + "=" * 60)
        print("🤖 VoxPersonal v6 - macOS версия")
        print("=" * 60)
        
        self.speak(f"{self.name} запущен. Скажите 'вокс' или 'привет' для начала общения!")
        
        while True:
            try:
                print("\n" + "━" * 40)
                print("⏳ ЖДУ АКТИВАЦИИ... (скажите 'вокс' или 'привет')")
                print("━" * 40)
                
                if self.gui_callback:
                    self.gui_callback('waiting_activation', None)
                
                text = self.listen()
                
                if text and any(word in text for word in ["привет", "эй", "слушай", "вокс"]):
                    print("\n🚀 АКТИВАЦИЯ УСПЕШНА!")
                    self.is_active = True
                    
                    if self.gui_callback:
                        self.gui_callback('activated', None)
                    
                    response = self.process_command(text)
                    if response:
                        self.speak(response)
                    
                    # Активный режим
                    while self.is_active:
                        print("\n" + "━" * 40)
                        print("📝 ОЖИДАЮ КОМАНДУ... (скажите 'пока' для выхода)")
                        print("━" * 40)
                        
                        if self.gui_callback:
                            self.gui_callback('waiting_command', None)
                        
                        command = self.listen()
                        
                        if command:
                            if "пока" in command or "выход" in command:
                                response = self.process_command(command)
                                self.speak(response)
                                break
                            
                            response = self.process_command(command)
                            if response:
                                self.speak(response)
                        
                        time.sleep(0.5)
                        
                elif text:
                    response = self.process_command(text)
                    if response:
                        self.speak(response)
                        
            except KeyboardInterrupt:
                print("\n\n🛑 Прерывание пользователем")
                self.speak("Работа завершена")
                if self.gui_callback:
                    self.gui_callback('interrupted', None)
                break
            except Exception as e:
                print(f"\n❌ Критическая ошибка: {e}")
                if self.gui_callback:
                    self.gui_callback('critical_error', str(e))
                time.sleep(1)
    
    def _update_gui(self, event_type, data):
        """Обновление GUI через callback"""
        if self.gui_callback:
            self.gui_callback(event_type, data)

# Общие методы, которые остаются без изменений
def _open_website(self, text=""):
    """Открыть сайт по названию или URL"""
    if not text:
        self.speak("Какой сайт открыть?", wait=False)
        query = self.listen()
    else:
        query = text
    
    if query:
        print(f"\n🌐 Поиск сайта: {query}")
        
        if self.gui_callback:
            self.gui_callback('searching_site', query)
        
        for site_name, url in self.websites.items():
            if site_name in query:
                print(f"✅ Найден сайт: {site_name} -> {url}")
                
                if self.gui_callback:
                    self.gui_callback('site_found', {'name': site_name, 'url': url})
                
                webbrowser.open(url)
                return f"Открываю {site_name}"
        
        url_match = re.search(r'(https?://\S+|www\.\S+\.\w+)', query)
        if url_match:
            url = url_match.group(0)
            if not url.startswith('http'):
                url = 'https://' + url
            print(f"✅ Найден URL: {url}")
            
            if self.gui_callback:
                self.gui_callback('url_found', url)
            
            webbrowser.open(url)
            return f"Открываю {url}"
        
        print(f"🔍 Не найден, ищу в Google: {query}")
        
        if self.gui_callback:
            self.gui_callback('searching_google', query)
        
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Ищу '{query}' в Google"
    
    return "Скажите название сайта"

def _hello(self):
    """Приветствие с именем пользователя"""
    greetings = [
        "Приветствую!",
        "Здравствуйте!",
        "Привет! Рад вас слышать.",
        "Добрый день!",
        "Привет, друг!",
        "Вокс на связи! Чем могу помочь?"
    ]
    
    if self.user_name:
        return f"{random.choice(greetings)} Как ваши дела, {self.user_name}?"
    else:
        return f"{random.choice(greetings)} Меня зовут {self.name}. Как вас зовут?"

def _how_are_you(self):
    """Состояние ассистента"""
    moods = [
        "Всё отлично! Готов помогать.",
        "Прекрасно, как никогда!",
        "Великолепно, спасибо что спросили!",
        "Работаю в полную силу!",
        "Готов к новым задачам!"
    ]
    return random.choice(moods)

def _open_youtube(self):
    """Открыть YouTube"""
    webbrowser.open("https://youtube.com")
    return "Открываю YouTube"

def _web_search(self):
    """Поиск в интернете"""
    self.speak("Что искать в интернете?", wait=False)
    query = self.listen()
    if query:
        print(f"🔍 Поиск в Google: {query}")
        
        if self.gui_callback:
            self.gui_callback('web_search', query)
        
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Ищу '{query}' в Google"
    return "Скажите что искать"

def _weather(self):
    """Погода"""
    cities = ["Москве", "Санкт-Петербурге", "Новосибирске", "Екатеринбурге"]
    temps = random.randint(-10, 30)
    conditions = ["солнечно", "облачно", "дождливо", "снежно", "пасмурно"]
    
    city = random.choice(cities)
    condition = random.choice(conditions)
    
    print(f"🌤️ Погода в {city}: {temps}°C, {condition}")
    
    if self.gui_callback:
        self.gui_callback('weather_info', {'city': city, 'temp': temps, 'condition': condition})
    
    return f"В {city} сейчас {temps}°C, {condition}."

def _what_time(self):
    """Текущее время"""
    now = datetime.datetime.now()
    time_str = now.strftime('%H:%M')
    print(f"🕐 Текущее время: {time_str}")
    
    if self.gui_callback:
        self.gui_callback('time_info', time_str)
    
    return f"Сейчас {time_str}"

def _what_date(self):
    """Текущая дата"""
    now = datetime.datetime.now()
    months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]
    date_str = f"{now.day} {months[now.month-1]} {now.year} года"
    print(f"📅 Текущая дата: {date_str}")
    
    if self.gui_callback:
        self.gui_callback('date_info', date_str)
    
    return f"Сегодня {date_str}"

def _random_number(self):
    """Случайное число"""
    num = random.randint(1, 100)
    print(f"🎲 Случайное число: {num}")
    
    if self.gui_callback:
        self.gui_callback('random_number', num)
    
    return f"Ваше случайное число: {num}"

def _tell_joke(self):
    """Рассказать шутку"""
    jokes = [
        "Почему программист всегда мокрый? Потому что он постоянно в бассейне кода!",
        "Что сказал один массив другому? Привет, я твой отец!",
        "Почему Python не может полюбить? Потому что у него нет сердца, только интерпретатор!",
    ]
    joke = random.choice(jokes)
    print(f"😂 Шутка: {joke}")
    
    if self.gui_callback:
        self.gui_callback('joke_told', joke)
    
    return joke

def _who_are_you(self):
    """Представление ассистента"""
    return f"Я {self.name}, ваш персональный голосовой помощник для macOS. Я умею управлять компьютером, искать информацию в интернете, рассказывать шутки и многое другое!"

def _play_music(self):
    """Включить музыку"""
    try:
        # Пытаемся открыть Music.app
        if os.path.exists(self.mac_apps['music']):
            subprocess.run(['open', self.mac_apps['music']])
            return "Запускаю Apple Music"
        else:
            webbrowser.open("https://music.youtube.com")
            return "Включаю YouTube Music"
    except:
        return "Откройте ваш музыкальный сервис"

def _play_movie(self):
    """Включить кино"""
    platforms = ["https://www.netflix.com", "https://www.kinopoisk.ru", "https://www.ivi.ru"]
    platform = random.choice(platforms)
    print(f"🎬 Открываю платформу: {platform}")
    
    if self.gui_callback:
        self.gui_callback('movie_platform', platform)
    
    webbrowser.open(platform)
    return "Открываю платформу для просмотра фильмов"

def _show_cat(self):
    """Показать котика"""
    webbrowser.open("https://thecatapi.com/api/images/get?format=src&type=gif")
    return "Смотрите на этого милого котика!"

def _fortune_telling(self):
    """Предсказание"""
    fortunes = [
        "Сегодня вас ждёт удача в программировании!",
        "Вскоре вы найдёте баг, который искали месяц.",
        "Сегодня отличный день для изучения нового фреймворка!",
    ]
    fortune = random.choice(fortunes)
    print(f"🔮 Предсказание: {fortune}")
    
    if self.gui_callback:
        self.gui_callback('fortune_told', fortune)
    
    return fortune

def _repeat_command(self):
    """Повторить последнюю команду"""
    if self.command_history:
        last_cmd = self.command_history[-1]
        print(f"🔄 Повтор команды: {last_cmd}")
        
        if self.gui_callback:
            self.gui_callback('repeat_command', last_cmd)
        
        return f"Повторяю последнюю команду: '{last_cmd}'"
    return "История команд пуста"

def _goodbye(self):
    """Прощание"""
    farewells = [
        "До свидания! Буду рад помочь снова.",
        "Пока! Обращайтесь если что.",
        "Всего хорошего!",
    ]
    self.is_listening = False
    self.vox_mode = False
    self.is_active = False
    
    if self.gui_callback:
        self.gui_callback('assistant_off', None)
    
    return random.choice(farewells)

# Добавляем методы к классу
VoxPersonalV6._open_website = _open_website
VoxPersonalV6._hello = _hello
VoxPersonalV6._how_are_you = _how_are_you
VoxPersonalV6._open_youtube = _open_youtube
VoxPersonalV6._web_search = _web_search
VoxPersonalV6._weather = _weather
VoxPersonalV6._what_time = _what_time
VoxPersonalV6._what_date = _what_date
VoxPersonalV6._random_number = _random_number
VoxPersonalV6._tell_joke = _tell_joke
VoxPersonalV6._who_are_you = _who_are_you
VoxPersonalV6._play_music = _play_music
VoxPersonalV6._play_movie = _play_movie
VoxPersonalV6._show_cat = _show_cat
VoxPersonalV6._fortune_telling = _fortune_telling
VoxPersonalV6._repeat_command = _repeat_command
VoxPersonalV6._goodbye = _goodbye

if __name__ == "__main__":
    assistant = VoxPersonalV6()
    assistant.run()