#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
متصفح الويب الذكي مع الذكاء الاصطناعي
Smart Web Browser with AI
"""

import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, Any, List, Optional
import logging
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class SmartBrowser:
    """متصفح ويب ذكي"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Nasser-SmartBrowser/1.0 (Arabic AI Browser)'
        }
        self.history = []
        self.bookmarks = {}
        self.cache = {}
        self.cookies = {}
        logger.info("تم تهيئة المتصفح الذكي")
    
    def fetch(self, url: str, use_cache: bool = True) -> Optional[str]:
        """جلب محتوى الصفحة"""
        try:
            # التحقق من الكاش
            if use_cache and url in self.cache:
                logger.info(f"تم جلب من الكاش: {url}")
                return self.cache[url]
            
            # جلب الصفحة
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # حفظ في الكاش
            self.cache[url] = response.text
            
            # إضافة إلى السجل
            self.history.append({
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "status_code": response.status_code
            })
            
            logger.info(f"تم جلب الصفحة: {url}")
            return response.text
        except Exception as e:
            logger.error(f"خطأ في جلب الصفحة: {e}")
            return None
    
    def parse(self, html: str) -> Dict[str, Any]:
        """تحليل محتوى HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            return {
                "title": soup.title.string if soup.title else "بدون عنوان",
                "links": [a.get('href') for a in soup.find_all('a', href=True)],
                "images": [img.get('src') for img in soup.find_all('img', src=True)],
                "text": soup.get_text()[:500],  # أول 500 حرف
                "meta_data": {
                    "description": self._get_meta_tag(soup, 'description'),
                    "keywords": self._get_meta_tag(soup, 'keywords'),
                    "language": self._get_meta_tag(soup, 'language')
                }
            }
        except Exception as e:
            logger.error(f"خطأ في التحليل: {e}")
            return {}
    
    def _get_meta_tag(self, soup, name: str) -> Optional[str]:
        """الحصول على وسم meta"""
        tag = soup.find('meta', attrs={'name': name})
        if tag:
            return tag.get('content')
        return None
    
    def search(self, query: str, engine: str = "google") -> List[Dict[str, Any]]:
        """البحث في محرك البحث"""
        search_engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q="
        }
        
        url = search_engines.get(engine, search_engines["google"]) + query
        
        try:
            html = self.fetch(url)
            if html:
                results = self.parse(html)
                return results.get("links", [])
        except Exception as e:
            logger.error(f"خطأ في البحث: {e}")
        
        return []
    
    def add_bookmark(self, url: str, title: str) -> bool:
        """إضافة علامة مرجعية"""
        try:
            self.bookmarks[url] = {
                "title": title,
                "added_at": datetime.now().isoformat()
            }
            logger.info(f"تم إضافة علامة مرجعية: {title}")
            return True
        except Exception as e:
            logger.error(f"خطأ في إضافة العلامة: {e}")
            return False
    
    def get_bookmarks(self) -> Dict[str, Any]:
        """الحصول على العلامات المرجعية"""
        return self.bookmarks
    
    def clear_cache(self) -> bool:
        """مسح الكاش"""
        try:
            self.cache.clear()
            logger.info("تم مسح الكاش")
            return True
        except Exception as e:
            logger.error(f"خطأ في مسح الكاش: {e}")
            return False
    
    def get_history(self) -> List[Dict[str, Any]]:
        """الحصول على السجل"""
        return self.history
    
    def analyze_page(self, url: str) -> Dict[str, Any]:
        """تحليل الصفحة ذكياً"""
        html = self.fetch(url)
        if not html:
            return {"error": "لم يتمكن من جلب الصفحة"}
        
        parsed = self.parse(html)
        
        return {
            "url": url,
            "title": parsed.get("title"),
            "content_summary": parsed.get("text"),
            "media_count": {
                "images": len(parsed.get("images", [])),
                "links": len(parsed.get("links", []))
            },
            "meta_data": parsed.get("meta_data")
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    browser = SmartBrowser()
    
    # اختبار
    result = browser.analyze_page("https://www.example.com")
    print(json.dumps(result, ensure_ascii=False, indent=2))
