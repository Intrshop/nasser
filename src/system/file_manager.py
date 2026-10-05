#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة الملفات المتقدم
Advanced File System Manager
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import hashlib

logger = logging.getLogger(__name__)


class FileSystemManager:
    """مدير نظام الملفات"""
    
    def __init__(self, root_path: str = "/home/nasser"):
        self.root_path = root_path
        self.ensure_root_exists()
    
    def ensure_root_exists(self):
        """التأكد من وجود مجلد الجذر"""
        os.makedirs(self.root_path, exist_ok=True)
        logger.info(f"تم إعداد مجلد الجذر: {self.root_path}")
    
    def create_file(self, filename: str, content: str = "") -> bool:
        """إنشاء ملف جديد"""
        try:
            filepath = os.path.join(self.root_path, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"تم إنشاء الملف: {filename}")
            return True
        except Exception as e:
            logger.error(f"خطأ في إنشاء الملف: {e}")
            return False
    
    def delete_file(self, filename: str) -> bool:
        """حذف ملف"""
        try:
            filepath = os.path.join(self.root_path, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"تم حذف الملف: {filename}")
                return True
            return False
        except Exception as e:
            logger.error(f"خطأ في حذف الملف: {e}")
            return False
    
    def create_directory(self, dirname: str) -> bool:
        """إنشاء مجلد جديد"""
        try:
            dirpath = os.path.join(self.root_path, dirname)
            os.makedirs(dirpath, exist_ok=True)
            logger.info(f"تم إنشاء المجلد: {dirname}")
            return True
        except Exception as e:
            logger.error(f"خطأ في إنشاء المجلد: {e}")
            return False
    
    def list_files(self, directory: str = "") -> List[Dict[str, Any]]:
        """قائمة بملفات المجلد"""
        try:
            dirpath = os.path.join(self.root_path, directory)
            items = []
            
            for item in os.listdir(dirpath):
                item_path = os.path.join(dirpath, item)
                stat = os.stat(item_path)
                
                items.append({
                    "name": item,
                    "type": "directory" if os.path.isdir(item_path) else "file",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "permissions": oct(stat.st_mode)[-3:]
                })
            
            return items
        except Exception as e:
            logger.error(f"خطأ في قائمة الملفات: {e}")
            return []
    
    def read_file(self, filename: str) -> Optional[str]:
        """قراءة محتوى ملف"""
        try:
            filepath = os.path.join(self.root_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"خطأ في قراءة الملف: {e}")
            return None
    
    def write_file(self, filename: str, content: str) -> bool:
        """كتابة محتوى في ملف"""
        try:
            filepath = os.path.join(self.root_path, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"تم كتابة المحتوى في: {filename}")
            return True
        except Exception as e:
            logger.error(f"خطأ في الكتابة: {e}")
            return False
    
    def copy_file(self, source: str, destination: str) -> bool:
        """نسخ ملف"""
        try:
            src_path = os.path.join(self.root_path, source)
            dst_path = os.path.join(self.root_path, destination)
            shutil.copy2(src_path, dst_path)
            logger.info(f"تم نسخ الملف من {source} إلى {destination}")
            return True
        except Exception as e:
            logger.error(f"خطأ في النسخ: {e}")
            return False
    
    def move_file(self, source: str, destination: str) -> bool:
        """نقل ملف"""
        try:
            src_path = os.path.join(self.root_path, source)
            dst_path = os.path.join(self.root_path, destination)
            shutil.move(src_path, dst_path)
            logger.info(f"تم نقل الملف من {source} إلى {destination}")
            return True
        except Exception as e:
            logger.error(f"خطأ في النقل: {e}")
            return False
    
    def get_file_info(self, filename: str) -> Optional[Dict[str, Any]]:
        """الحصول على معلومات الملف"""
        try:
            filepath = os.path.join(self.root_path, filename)
            if not os.path.exists(filepath):
                return None
            
            stat = os.stat(filepath)
            with open(filepath, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            return {
                "name": filename,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "permissions": oct(stat.st_mode)[-3:],
                "hash": file_hash,
                "type": "directory" if os.path.isdir(filepath) else "file"
            }
        except Exception as e:
            logger.error(f"خطأ في الحصول على معلومات الملف: {e}")
            return None
    
    def search_files(self, pattern: str, directory: str = "") -> List[str]:
        """البحث عن ملفات"""
        try:
            dirpath = os.path.join(self.root_path, directory)
            results = []
            
            for root, dirs, files in os.walk(dirpath):
                for file in files:
                    if pattern.lower() in file.lower():
                        results.append(os.path.relpath(os.path.join(root, file), self.root_path))
            
            return results
        except Exception as e:
            logger.error(f"خطأ في البحث: {e}")
            return []
    
    def get_disk_usage(self) -> Dict[str, Any]:
        """الحصول على استخدام القرص"""
        try:
            total_size = 0
            file_count = 0
            
            for root, dirs, files in os.walk(self.root_path):
                file_count += len(files)
                for file in files:
                    try:
                        total_size += os.path.getsize(os.path.join(root, file))
                    except:
                        pass
            
            return {
                "total_size": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "file_count": file_count
            }
        except Exception as e:
            logger.error(f"خطأ في حساب استخدام القرص: {e}")
            return {}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fs = FileSystemManager()
    print(json.dumps(fs.list_files(), ensure_ascii=False, indent=2))
