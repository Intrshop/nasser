#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام النشر والبروتوكول
Publishing and Protocol System
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import hashlib
import urllib.parse

logger = logging.getLogger(__name__)


class PublishingManager:
    """مدير النشر"""
    
    def __init__(self, base_url: str = "https://nasser.app"):
        self.base_url = base_url
        self.published_items = {}
        self.distribution_channels = self._init_channels()
        self.analytics = {}
        logger.info("تم تهيئة مدير النشر")
    
    def _init_channels(self) -> Dict[str, Dict[str, Any]]:
        """القنوات المتاحة"""
        return {
            "web": {
                "name": "الويب",
                "protocol": "https",
                "requires_ssl": True
            },
            "mobile": {
                "name": "الهاتف الذكية",
                "protocol": "native",
                "requires_ssl": True
            },
            "desktop": {
                "name": "سطح المكتب",
                "protocol": "native",
                "requires_ssl": False
            },
            "api": {
                "name": "API",
                "protocol": "rest",
                "requires_ssl": True
            }
        }
    
    def publish_item(self, item_type: str, item_id: str, content: Dict[str, Any], channels: List[str] = None) -> Dict[str, Any]:
        """نشر عنصر"""
        if channels is None:
            channels = list(self.distribution_channels.keys())
        
        pub_id = str(uuid.uuid4())
        
        # الحسول على hash للعنصر
        content_hash = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
        
        published = {
            "id": pub_id,
            "item_type": item_type,
            "item_id": item_id,
            "content": content,
            "content_hash": content_hash,
            "channels": channels,
            "urls": self._generate_urls(pub_id, item_type, channels),
            "status": "published",
            "published_at": datetime.now().isoformat(),
            "views": 0,
            "clicks": 0
        }
        
        self.published_items[pub_id] = published
        self.analytics[pub_id] = {
            "views": 0,
            "clicks": 0,
            "shares": 0,
            "comments": 0
        }
        
        logger.info(f"تم نشر عنصر: {pub_id}")
        return published
    
    def _generate_urls(self, pub_id: str, item_type: str, channels: List[str]) -> Dict[str, str]:
        """توليد الروابط"""
        urls = {}
        for channel in channels:
            if channel == "web":
                urls[channel] = f"{self.base_url}/view/{item_type}/{pub_id}"
            elif channel == "mobile":
                urls[channel] = f"nasser://{item_type}/{pub_id}"
            elif channel == "api":
                urls[channel] = f"{self.base_url}/api/v1/{item_type}/{pub_id}"
            else:
                urls[channel] = f"{self.base_url}/{item_type}/{pub_id}"
        return urls
    
    def generate_share_link(self, pub_id: str, expiry_days: int = 30) -> str:
        """توليد رابط مشاركة"""
        import time
        timestamp = int(time.time()) + (expiry_days * 86400)
        token = f"{pub_id}:{timestamp}"
        encoded = urllib.parse.quote_plus(token)
        return f"{self.base_url}/share/{encoded}"
    
    def track_view(self, pub_id: str) -> bool:
        """ترارع مشاهدة"""
        if pub_id in self.analytics:
            self.analytics[pub_id]["views"] += 1
            if pub_id in self.published_items:
                self.published_items[pub_id]["views"] += 1
            return True
        return False
    
    def track_click(self, pub_id: str) -> bool:
        """ترارع نقرة"""
        if pub_id in self.analytics:
            self.analytics[pub_id]["clicks"] += 1
            if pub_id in self.published_items:
                self.published_items[pub_id]["clicks"] += 1
            return True
        return False
    
    def get_analytics(self, pub_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على التحليلات"""
        return self.analytics.get(pub_id)
    
    def unpublish(self, pub_id: str) -> bool:
        """إلغاء النشر"""
        if pub_id in self.published_items:
            self.published_items[pub_id]["status"] = "unpublished"
            logger.info(f"تم إلغاء نشر: {pub_id}")
            return True
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = PublishingManager()
    
    content = {"title": "مقالة جديدة", "text": "محتوا"}
    published = manager.publish_item("article", "art1", content)
    print(json.dumps(published, ensure_ascii=False, indent=2))
