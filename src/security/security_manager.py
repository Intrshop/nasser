#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام الأمان والتشفير المتقدم
Advanced Security and Encryption System
"""

import hashlib
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging
import jwt

logger = logging.getLogger(__name__)


class SecurityManager:
    """مدير الأمان متقدم"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.sessions = {}
        self.ip_blacklist = set()
        self.failed_attempts = {}
        self.encryption_key = self._generate_encryption_key()
        logger.info("تم تهيئة مدير الأمان")
    
    def _generate_encryption_key(self) -> bytes:
        """توليد مفتاح التشفير"""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'nasser-salt-2024',
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self.secret_key.encode()))
    
    def encrypt(self, data: str) -> str:
        """تشفير بيانات"""
        try:
            f = Fernet(self.encryption_key)
            return f.encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"خطأ في التشفير: {e}")
            return None
    
    def decrypt(self, encrypted_data: str) -> Optional[str]:
        """فك التشفير"""
        try:
            f = Fernet(self.encryption_key)
            return f.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"خطأ في فك التشفير: {e}")
            return None
    
    def hash_password(self, password: str, salt: str = None) -> Dict[str, str]:
        """تجزئة كلمة المرور"""
        if not salt:
            salt = secrets.token_hex(16)
        
        # SHA-256 مع ملح
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return {
            'hash': hashed.hex(),
            'salt': salt
        }
    
    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """التحقق من كلمة المرور"""
        result = self.hash_password(password, salt)
        return result['hash'] == stored_hash
    
    def generate_token(self, user_id: str, expires_in: int = 3600) -> str:
        """توليد رمز JWT"""
        payload = {
            'user_id': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """التحقق من رمز JWT"""
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except Exception as e:
            logger.error(f"رمز غير صالح: {e}")
            return None
    
    def create_session(self, user_id: str, ip_address: str) -> str:
        """إنشاء جلسة"""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            'user_id': user_id,
            'ip_address': ip_address,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
            'is_active': True
        }
        return session_id
    
    def verify_session(self, session_id: str, ip_address: str) -> bool:
        """التحقق من الجلسة"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        if not session['is_active']:
            return False
        
        # التحقق من عنوان IP
        if session['ip_address'] != ip_address:
            logger.warning(f"محاولة مشبوهة: IP مختلف للجلسة")
            return False
        
        return True
    
    def invalidate_session(self, session_id: str) -> bool:
        """إلغاء جلسة"""
        if session_id in self.sessions:
            self.sessions[session_id]['is_active'] = False
            return True
        return False
    
    def add_to_blacklist(self, ip_address: str) -> bool:
        """إضافة IP للقائمة السوداء"""
        self.ip_blacklist.add(ip_address)
        logger.warning(f"تم حظر IP: {ip_address}")
        return True
    
    def is_ip_blacklisted(self, ip_address: str) -> bool:
        """التحقق من القائمة السوداء"""
        return ip_address in self.ip_blacklist
    
    def track_failed_attempt(self, ip_address: str, max_attempts: int = 5) -> bool:
        """متابعة محاولات الفشل"""
        if ip_address not in self.failed_attempts:
            self.failed_attempts[ip_address] = {'count': 0, 'first_attempt': datetime.now()}
        
        self.failed_attempts[ip_address]['count'] += 1
        
        if self.failed_attempts[ip_address]['count'] >= max_attempts:
            self.add_to_blacklist(ip_address)
            return False
        
        return True
    
    def reset_failed_attempts(self, ip_address: str):
        """إعادة تعيين محاولات الفشل"""
        if ip_address in self.failed_attempts:
            del self.failed_attempts[ip_address]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sm = SecurityManager()
    
    # اختبار
    encrypted = sm.encrypt("بيانات سرية")
    print(f"مشفر: {encrypted}")
    print(f"مفك: {sm.decrypt(encrypted)}")
