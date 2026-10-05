#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام الإعلانات المتقدم
Advanced Advertising System
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class AdType(Enum):
    """أنواع الإعلانات"""
    BANNER = "banner"
    VIDEO = "video"
    NATIVE = "native"
    INTERACTIVE = "interactive"
    SPONSORED = "sponsored"
    CAROUSEL = "carousel"


class AdStatus(Enum):
    """حالات الإعلان"""
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"


class AdvertisingManager:
    """مدير الإعلانات المتقدم"""
    
    def __init__(self):
        self.advertisements = {}
        self.campaigns = {}
        self.placements = {}
        self.performance_data = {}
        self.audience_segments = self._init_audience_segments()
        logger.info("تم تهيئة مدير الإعلانات")
    
    def _init_audience_segments(self) -> Dict[str, Dict[str, Any]]:
        """قطاعات الجمهور المتاحة"""
        return {
            "demographic": {
                "age": ["13-18", "19-25", "26-35", "36-50", "51+"],
                "gender": ["male", "female", "other"],
                "location": ["كل المناطق", "الرياض", "جدة", "الدمام", "الخرج"]
            },
            "interest": {
                "technology": "التكنولوجيا",
                "business": "الأعمال",
                "entertainment": "الترفيه",
                "sports": "الرياضة",
                "health": "الصحة",
                "education": "التعليم"
            },
            "behavior": {
                "active_users": "المستخدمون النشطون",
                "frequent_buyers": "المشترون المتكررون",
                "new_users": "المستخدمون الجدد",
                "returning_users": "المستخدمون العائدون"
            }
        }
    
    def create_advertisement(self, 
                           advertiser_id: str,
                           title: str,
                           description: str,
                           ad_type: str,
                           content: Dict[str, Any],
                           budget: float,
                           targeting: Dict[str, Any]) -> Dict[str, Any]:
        """إنشاء إعلان جديد"""
        ad_id = str(uuid.uuid4())
        
        advertisement = {
            "id": ad_id,
            "advertiser_id": advertiser_id,
            "title": title,
            "description": description,
            "type": ad_type,
            "content": content,
            "budget": budget,
            "spent": 0.0,
            "targeting": targeting,
            "status": "draft",
            "views": 0,
            "clicks": 0,
            "conversions": 0,
            "ctr": 0.0,  # Click-through rate
            "roi": 0.0,  # Return on investment
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "starts_at": None,
            "ends_at": None
        }
        
        self.advertisements[ad_id] = advertisement
        self.performance_data[ad_id] = {
            "hourly_views": [],
            "hourly_clicks": [],
            "daily_performance": [],
            "impressions_by_device": {},
            "impressions_by_location": {}
        }
        
        logger.info(f"تم إنشاء إعلان: {ad_id}")
        return advertisement
    
    def submit_for_approval(self, ad_id: str) -> bool:
        """تقديم الإعلان للمراجعة"""
        if ad_id in self.advertisements:
            self.advertisements[ad_id]["status"] = "pending"
            logger.info(f"تم تقديم الإعلان للمراجعة: {ad_id}")
            return True
        return False
    
    def approve_advertisement(self, ad_id: str) -> bool:
        """الموافقة على الإعلان"""
        if ad_id in self.advertisements:
            self.advertisements[ad_id]["status"] = "approved"
            logger.info(f"تم الموافقة على الإعلان: {ad_id}")
            return True
        return False
    
    def activate_advertisement(self, ad_id: str, duration_days: int = 30) -> bool:
        """تفعيل الإعلان"""
        if ad_id not in self.advertisements:
            return False
        
        ad = self.advertisements[ad_id]
        ad["status"] = "active"
        ad["starts_at"] = datetime.now().isoformat()
        ad["ends_at"] = (datetime.now() + timedelta(days=duration_days)).isoformat()
        
        logger.info(f"تم تفعيل الإعلان: {ad_id}")
        return True
    
    def track_impression(self, ad_id: str, device: str = "desktop", location: str = "unknown") -> bool:
        """تتبع عرض الإعلان"""
        if ad_id not in self.advertisements:
            return False
        
        self.advertisements[ad_id]["views"] += 1
        
        # تسجيل البيانات
        if ad_id in self.performance_data:
            if device not in self.performance_data[ad_id]["impressions_by_device"]:
                self.performance_data[ad_id]["impressions_by_device"][device] = 0
            self.performance_data[ad_id]["impressions_by_device"][device] += 1
            
            if location not in self.performance_data[ad_id]["impressions_by_location"]:
                self.performance_data[ad_id]["impressions_by_location"][location] = 0
            self.performance_data[ad_id]["impressions_by_location"][location] += 1
        
        return True
    
    def track_click(self, ad_id: str, cost: float = 0.0) -> bool:
        """تتبع نقرة الإعلان"""
        if ad_id not in self.advertisements:
            return False
        
        ad = self.advertisements[ad_id]
        ad["clicks"] += 1
        ad["spent"] += cost
        
        # حساب CTR
        if ad["views"] > 0:
            ad["ctr"] = (ad["clicks"] / ad["views"]) * 100
        
        return True
    
    def track_conversion(self, ad_id: str, value: float) -> bool:
        """تتبع تحويل الإعلان"""
        if ad_id not in self.advertisements:
            return False
        
        ad = self.advertisements[ad_id]
        ad["conversions"] += 1
        
        # حساب ROI
        if ad["spent"] > 0:
            ad["roi"] = ((value - ad["spent"]) / ad["spent"]) * 100
        
        return True
    
    def create_campaign(self, advertiser_id: str, name: str, ads: List[str], budget: float) -> Dict[str, Any]:
        """إنشاء حملة إعلانية"""
        campaign_id = str(uuid.uuid4())
        
        campaign = {
            "id": campaign_id,
            "advertiser_id": advertiser_id,
            "name": name,
            "ads": ads,
            "budget": budget,
            "spent": 0.0,
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        
        self.campaigns[campaign_id] = campaign
        logger.info(f"تم إنشاء حملة: {campaign_id}")
        return campaign
    
    def get_advertisement(self, ad_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على بيانات الإعلان"""
        return self.advertisements.get(ad_id)
    
    def get_performance(self, ad_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على بيانات الأداء"""
        return self.performance_data.get(ad_id)
    
    def pause_advertisement(self, ad_id: str) -> bool:
        """إيقاف الإعلان مؤقتاً"""
        if ad_id in self.advertisements:
            self.advertisements[ad_id]["status"] = "paused"
            return True
        return False
    
    def resume_advertisement(self, ad_id: str) -> bool:
        """استئناف الإعلان"""
        if ad_id in self.advertisements:
            self.advertisements[ad_id]["status"] = "active"
            return True
        return False
    
    def list_advertisements(self, advertiser_id: str = None, status: str = None) -> List[Dict[str, Any]]:
        """قائمة الإعلانات"""
        ads = list(self.advertisements.values())
        
        if advertiser_id:
            ads = [a for a in ads if a["advertiser_id"] == advertiser_id]
        
        if status:
            ads = [a for a in ads if a["status"] == status]
        
        return ads


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = AdvertisingManager()
    
    # اختبار
    ad = manager.create_advertisement(
        "advertiser1",
        "إعلان تجريبي",
        "وصف الإعلان",
        "banner",
        {"image": "image.jpg", "link": "https://example.com"},
        1000.0,
        {"age": "19-25", "location": "الرياض"}
    )
    print(json.dumps(ad, ensure_ascii=False, indent=2))
