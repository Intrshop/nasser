#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مدير المكتبات والأدوات الشامل
Libraries and Tools Manager
"""

import subprocess
import json
import os
import sys
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import importlib
import pip

logger = logging.getLogger(__name__)


class LibraryManager:
    """مدير المكتبات"""
    
    def __init__(self):
        self.installed_libraries = {}
        self.available_libraries = self._get_available_libraries()
        self.load_installed()
    
    def _get_available_libraries(self) -> Dict[str, str]:
        """قائمة المكتبات المتاحة"""
        return {
            # مكتبات الصوت والفيديو
            "librosa": "معالجة الصوت",
            "pydub": "تحويل الصوت",
            "soundfile": "قراءة الملفات الصوتية",
            "cv2": "معالجة الصور والفيديو",
            "ffmpeg-python": "معالجة الفيديو",
            "moviepy": "تحرير الفيديو",
            
            # مكتبات اللغة الطبيعية
            "nltk": "معالجة اللغة الطبيعية",
            "spacy": "معالجة اللغة المتقدمة",
            "transformers": "نماذج AI",
            "gensim": "معالجة النصوص",
            "pyarabic": "معالجة العربية",
            
            # مكتبات الذكاء الاصطناعي
            "tensorflow": "التعلم العميق",
            "torch": "PyTorch",
            "scikit-learn": "التعلم الآلي",
            "keras": "Keras",
            
            # مكتبات الويب
            "flask": "خادم ويب",
            "django": "إطار عمل ويب",
            "fastapi": "API حديثة",
            "requests": "طلبات HTTP",
            "beautifulsoup4": "تحليل HTML",
            "selenium": "اختبار الويب",
            
            # مكتبات أخرى
            "numpy": "معالجة البيانات",
            "pandas": "تحليل البيانات",
            "matplotlib": "الرسوم البيانية",
            "sqlalchemy": "قاعدة البيانات",
            "psycopg2": "PostgreSQL",
            "redis": "التخزين المؤقت",
        }
    
    def install_library(self, library_name: str) -> bool:
        """تثبيت مكتبة"""
        try:
            logger.info(f"جاري تثبيت المكتبة: {library_name}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
            self.installed_libraries[library_name] = {
                "installed_at": datetime.now().isoformat(),
                "version": self._get_library_version(library_name)
            }
            logger.info(f"تم تثبيت المكتبة: {library_name}")
            return True
        except Exception as e:
            logger.error(f"خطأ في تثبيت المكتبة: {e}")
            return False
    
    def uninstall_library(self, library_name: str) -> bool:
        """إلغاء تثبيت مكتبة"""
        try:
            logger.info(f"جاري إلغاء تثبيت المكتبة: {library_name}")
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", library_name])
            if library_name in self.installed_libraries:
                del self.installed_libraries[library_name]
            logger.info(f"تم إلغاء تثبيت المكتبة: {library_name}")
            return True
        except Exception as e:
            logger.error(f"خطأ في إلغاء التثبيت: {e}")
            return False
    
    def _get_library_version(self, library_name: str) -> str:
        """الحصول على إصدار المكتبة"""
        try:
            module = importlib.import_module(library_name)
            return getattr(module, '__version__', 'unknown')
        except:
            return 'unknown'
    
    def load_installed(self):
        """تحميل المكتبات المثبتة"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True
            )
            packages = json.loads(result.stdout)
            for pkg in packages:
                self.installed_libraries[pkg['name']] = pkg['version']
            logger.info(f"تم تحميل {len(self.installed_libraries)} مكتبة مثبتة")
        except Exception as e:
            logger.error(f"خطأ في تحميل المكتبات: {e}")
    
    def get_installed(self) -> Dict[str, Any]:
        """الحصول على قائمة المكتبات المثبتة"""
        return self.installed_libraries
    
    def get_available(self) -> Dict[str, str]:
        """الحصول على قائمة المكتبات المتاحة"""
        return self.available_libraries
    
    def install_all_recommended(self) -> bool:
        """تثبيت كل المكتبات الموصى بها"""
        recommended = [
            "numpy", "pandas", "requests", "beautifulsoup4",
            "nltk", "flask", "sqlalchemy", "redis",
            "opencv-python", "scipy", "scikit-learn"
        ]
        
        for lib in recommended:
            self.install_library(lib)
        
        return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = LibraryManager()
    print(json.dumps(manager.get_available(), ensure_ascii=False, indent=2))
