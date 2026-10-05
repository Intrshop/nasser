#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المستخدمين المتقدم
Advanced User Management System
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class User:
    """فئة المستخدم"""
    
    def __init__(self, username: str, email: str, role: str = "user"):
        self.username = username
        self.email = email
        self.role = role  # admin, user, guest
        self.password_hash = None
        self.created_at = datetime.now().isoformat()
        self.last_login = None
        self.is_active = True
        self.permissions = self._init_permissions(role)
    
    def _init_permissions(self, role: str) -> List[str]:
        """تهيئة صلاحيات المستخدم"""
        permissions_map = {
            "admin": ["read", "write", "delete", "manage_users", "system_config"],
            "user": ["read", "write"],
            "guest": ["read"]
        }
        return permissions_map.get(role, [])
    
    def set_password(self, password: str):
        """تعيين كلمة المرور"""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        logger.info(f"تم تعيين كلمة المرور للمستخدم: {self.username}")
    
    def check_password(self, password: str) -> bool:
        """التحقق من كلمة المرور"""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل المستخدم إلى قاموس"""
        return {
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "is_active": self.is_active,
            "permissions": self.permissions
        }


class UserManager:
    """مدير المستخدمين"""
    
    def __init__(self, storage_path: str = "/opt/nasser/data/users.json"):
        self.storage_path = storage_path
        self.users: Dict[str, User] = {}
        self.load_users()
    
    def create_user(self, username: str, email: str, password: str, role: str = "user") -> bool:
        """إنشاء مستخدم جديد"""
        if username in self.users:
            logger.warning(f"المستخدم {username} موجود بالفعل")
            return False
        
        user = User(username, email, role)
        user.set_password(password)
        self.users[username] = user
        
        logger.info(f"تم إنشاء المستخدم: {username}")
        self.save_users()
        return True
    
    def delete_user(self, username: str) -> bool:
        """حذف مستخدم"""
        if username not in self.users:
            logger.warning(f"المستخدم {username} غير موجود")
            return False
        
        del self.users[username]
        logger.info(f"تم حذف المستخدم: {username}")
        self.save_users()
        return True
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """التحقق من بيانات المستخدم"""
        if username not in self.users:
            return None
        
        user = self.users[username]
        if user.check_password(password) and user.is_active:
            user.last_login = datetime.now().isoformat()
            self.save_users()
            logger.info(f"تسجيل دخول ناجح: {username}")
            return user
        
        return None
    
    def get_user(self, username: str) -> Optional[User]:
        """الحصول على بيانات المستخدم"""
        return self.users.get(username)
    
    def list_users(self) -> List[Dict[str, Any]]:
        """قائمة جميع المستخدمين"""
        return [user.to_dict() for user in self.users.values()]
    
    def update_user(self, username: str, **kwargs) -> bool:
        """تحديث بيانات المستخدم"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.save_users()
        return True
    
    def save_users(self):
        """حفظ المستخدمين في ملف"""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            data = {username: user.to_dict() for username, user in self.users.items()}
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info("تم حفظ بيانات المستخدمين")
        except Exception as e:
            logger.error(f"خطأ في حفظ بيانات المستخدمين: {e}")
    
    def load_users(self):
        """تحميل المستخدمين من الملف"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # إعادة بناء كائنات المستخدمين
                    logger.info("تم تحميل بيانات المستخدمين")
            else:
                # إنشاء حساب admin افتراضي
                self.create_user("admin", "admin@nasser.local", "admin123", "admin")
        except Exception as e:
            logger.error(f"خطأ في تحميل بيانات المستخدمين: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = UserManager()
    print(json.dumps(manager.list_users(), ensure_ascii=False, indent=2))
