#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام الأوامر المتقدم لناصر
Nasser Advanced Command System
"""

import subprocess
import json
import os
from typing import Dict, Any, List, Optional
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class Command(ABC):
    """فئة أساسية للأوامر"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """تنفيذ الأمر"""
        pass


class SystemCommand(Command):
    """أوامر نظام"""
    
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }


class DiskCommand(Command):
    """أوامر القرص"""
    
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        result = subprocess.run(['df', '-h'], capture_output=True, text=True)
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }


class MemoryCommand(Command):
    """أوامر الذاكرة"""
    
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        result = subprocess.run(['free', '-h'], capture_output=True, text=True)
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }


class ProcessCommand(Command):
    """أوامر العمليات"""
    
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')[:10]  # أول 10 عمليات
        return {
            'success': result.returncode == 0,
            'processes': lines,
            'error': result.stderr
        }


class CommandExecutor:
    """منفذ الأوامر"""
    
    def __init__(self):
        self.commands = self._init_commands()
    
    def _init_commands(self) -> Dict[str, Command]:
        """تهيئة الأوامر المتاحة"""
        return {
            'system': SystemCommand('system', 'معلومات النظام'),
            'disk': DiskCommand('disk', 'معلومات القرص'),
            'memory': MemoryCommand('memory', 'معلومات الذاكرة'),
            'processes': ProcessCommand('processes', 'العمليات الجارية'),
        }
    
    def execute(self, command_name: str, *args, **kwargs) -> Dict[str, Any]:
        """تنفيذ أمر"""
        if command_name not in self.commands:
            return {
                'success': False,
                'error': f"الأمر '{command_name}' غير معروف"
            }
        
        try:
            cmd = self.commands[command_name]
            result = cmd.execute(*args, **kwargs)
            logger.info(f"تم تنفيذ الأمر: {command_name}")
            return result
        except Exception as e:
            logger.error(f"خطأ في تنفيذ الأمر: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_commands(self) -> List[Dict[str, str]]:
        """قائمة الأوامر المتاحة"""
        return [
            {'name': name, 'description': cmd.description}
            for name, cmd in self.commands.items()
        ]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor = CommandExecutor()
    print(json.dumps(executor.list_commands(), ensure_ascii=False, indent=2))
