#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام التحدث الصوتي الذكي العربي
Nasser Smart Arabic Voice System
"""

import speech_recognition as sr
from gtts import gTTS
import os
import json
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import threading
from queue import Queue

logger = logging.getLogger(__name__)


class ArabicVoiceEngine:
    """محرك الكلام العربي الذكي"""
    
    def __init__(self, language: str = "ar"):
        self.language = language
        self.recognizer = sr.Recognizer()
        self.commands_queue = Queue()
        self.response_callbacks = {}
        self.is_listening = False
        self.voice_commands = self._init_voice_commands()
        logger.info("تم تهيئة محرك الكلام العربي")
    
    def _init_voice_commands(self) -> Dict[str, Callable]:
        """تهيئة أوامر الكلام"""
        return {
            "افتح": self.open_app,
            "أغلق": self.close_app,
            "شغّل": self.run_app,
            "ابحث": self.search,
            "اعرض": self.show_info,
            "اسطع": self.brightness_up,
            "اخفّف": self.brightness_down,
            "ارفع الصوت": self.volume_up,
            "اخفّض الصوت": self.volume_down,
            "أوقف": self.stop_action,
            "ساعدني": self.show_help,
            "التاريخ": self.get_date,
            "الوقت": self.get_time,
            "الطقس": self.get_weather,
            "النبأ": self.get_news,
            "عملية حسابية": self.calculate,
        }
    
    def listen(self) -> Optional[str]:
        """الاستماع للكلام العربي"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("🎤 أستمع إليك...")
                audio = self.recognizer.listen(source, timeout=5)
                
                # محاولة التعرف على الكلام العربي
                text = self.recognizer.recognize_google(audio, language="ar-SA")
                logger.info(f"تم التعرف على الكلام: {text}")
                return text
        except sr.UnknownValueError:
            logger.warning("لم أستطع فهم الكلام")
            return None
        except sr.RequestError as e:
            logger.error(f"خطأ في الاتصال: {e}")
            return None
        except Exception as e:
            logger.error(f"خطأ في الاستماع: {e}")
            return None
    
    def speak(self, text: str, show_output: bool = True) -> bool:
        """التحدث بالعربية"""
        try:
            if show_output:
                print(f"🤖 ناصر: {text}")
            
            # إنشاء ملف صوتي
            tts = gTTS(text=text, lang='ar', slow=False)
            audio_file = f"/tmp/nasser_voice_{datetime.now().timestamp()}.mp3"
            tts.save(audio_file)
            
            # تشغيل الصوت
            os.system(f"play {audio_file} 2>/dev/null || mpg123 {audio_file} 2>/dev/null")
            
            # حذف الملف
            try:
                os.remove(audio_file)
            except:
                pass
            
            return True
        except Exception as e:
            logger.error(f"خطأ في التحدث: {e}")
            return False
    
    def process_voice_command(self, text: str) -> Dict[str, Any]:
        """معالجة أمر صوتي"""
        text_lower = text.lower()
        
        for command, handler in self.voice_commands.items():
            if command in text_lower:
                try:
                    result = handler(text)
                    self.speak(f"تم تنفيذ الأمر: {command}")
                    return {"success": True, "command": command, "result": result}
                except Exception as e:
                    error_msg = f"حدث خطأ: {str(e)}"
                    self.speak(error_msg)
                    return {"success": False, "error": error_msg}
        
        self.speak("عذراً، لم أفهم الأمر. حاول مرة أخرى")
        return {"success": False, "error": "أمر غير معروف"}
    
    def open_app(self, text: str) -> str:
        """فتح تطبيق"""
        return "تم فتح التطبيق"
    
    def close_app(self, text: str) -> str:
        """إغلاق تطبيق"""
        return "تم إغلاق التطبيق"
    
    def run_app(self, text: str) -> str:
        """تشغيل برنامج"""
        return "تم تشغيل البرنامج"
    
    def search(self, text: str) -> str:
        """البحث"""
        return "جاري البحث..."
    
    def show_info(self, text: str) -> str:
        """عرض معلومات"""
        return "إليك المعلومات"
    
    def brightness_up(self, text: str) -> str:
        """زيادة السطوع"""
        return "تم زيادة السطوع"
    
    def brightness_down(self, text: str) -> str:
        """تقليل السطوع"""
        return "تم تقليل السطوع"
    
    def volume_up(self, text: str) -> str:
        """رفع الصوت"""
        return "تم رفع الصوت"
    
    def volume_down(self, text: str) -> str:
        """خفض الصوت"""
        return "تم خفض الصوت"
    
    def stop_action(self, text: str) -> str:
        """إيقاف العملية"""
        return "تم الإيقاف"
    
    def show_help(self, text: str) -> str:
        """عرض المساعدة"""
        help_text = """الأوامر المتاحة:
افتح - فتح تطبيق
أغلق - إغلاق تطبيق
شغّل - تشغيل برنامج
ابحث - البحث
اعرض - عرض معلومات"""
        return help_text
    
    def get_date(self, text: str) -> str:
        """الحصول على التاريخ"""
        return datetime.now().strftime("%d/%m/%Y")
    
    def get_time(self, text: str) -> str:
        """الحصول على الوقت"""
        return datetime.now().strftime("%H:%M:%S")
    
    def get_weather(self, text: str) -> str:
        """الحصول على الطقس"""
        return "الطقس: مشمس وجميل"
    
    def get_news(self, text: str) -> str:
        """الحصول على الأخبار"""
        return "آخر الأخبار..."
    
    def calculate(self, text: str) -> str:
        """عملية حسابية"""
        return "النتيجة: ..."
    
    def start_listening_loop(self):
        """بدء حلقة الاستماع المستمر"""
        self.is_listening = True
        self.speak("أنا مستعد! تحدث إليّ الآن")
        
        while self.is_listening:
            text = self.listen()
            if text:
                result = self.process_voice_command(text)
                if result.get("success"):
                    logger.info(f"تم تنفيذ الأمر بنجاح: {result}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = ArabicVoiceEngine()
    engine.start_listening_loop()
