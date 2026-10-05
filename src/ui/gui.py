#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام ناصر - الواجهة الرسومية العربية
Nasser System - Arabic GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkFont
from datetime import datetime
import json
import os


class NassferGUI:
    """واجهة رسومية عربية متقدمة"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("نظام ناصر - Nasser System")
        self.root.geometry("1024x768")
        self.root.configure(bg="#1e1e2e")
        
        # الخطوط العربية
        self.font_title = tkFont.Font(family="DejaVu Sans", size=16, weight="bold")
        self.font_normal = tkFont.Font(family="DejaVu Sans", size=11)
        self.font_small = tkFont.Font(family="DejaVu Sans", size=9)
        
        self.setup_ui()
        self.load_theme()
    
    def load_theme(self):
        """تحميل المظهر الداكن العصري"""
        style = ttk.Style()
        style.theme_use('clam')
        
        bg_color = "#1e1e2e"
        fg_color = "#ffffff"
        accent = "#00ff88"
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', font=self.font_normal)
        style.map('TButton', background=[('active', accent)])
    
    def setup_ui(self):
        """إعداد الواجهة الرسومية"""
        # الرأس
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=10, pady=10)
        
        title_label = ttk.Label(
            header,
            text="🤖 نظام ناصر الذكي",
            font=self.font_title,
            foreground="#00ff88"
        )
        title_label.pack(side="left")
        
        time_label = ttk.Label(
            header,
            text=datetime.now().strftime("%H:%M:%S"),
            font=self.font_small
        )
        time_label.pack(side="right")
        
        # القائمة الجانبية
        sidebar = ttk.Frame(self.root)
        sidebar.pack(side="left", fill="both", expand=False, padx=5, pady=5)
        
        menu_items = [
            ("🏠 الرئيسية", self.show_dashboard),
            ("🤖 AI", self.show_ai),
            ("📁 الملفات", self.show_files),
            ("⚙️ الإعدادات", self.show_settings),
            ("👤 المستخدمين", self.show_users),
            ("ℹ️ المساعدة", self.show_help),
        ]
        
        for text, command in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                font=self.font_normal,
                bg="#2d2d44",
                fg="#ffffff",
                border=0,
                padx=15,
                pady=10,
                command=command
            )
            btn.pack(fill="x", pady=3)
        
        # المحتوى الرئيسي
        self.content = ttk.Frame(self.root)
        self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.show_dashboard()
    
    def clear_content(self):
        """مسح المحتوى الحالي"""
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """عرض لوحة التحكم"""
        self.clear_content()
        
        # العنوان
        title = ttk.Label(
            self.content,
            text="📊 لوحة التحكم",
            font=self.font_title,
            foreground="#00ff88"
        )
        title.pack(pady=10)
        
        # معلومات النظام
        info_frame = ttk.Frame(self.content)
        info_frame.pack(fill="x", pady=10)
        
        info_text = """نظام ناصر v1.0.0
حالة النظام: 🟢 نشط
اللغة: العربية الخليجية
الذاكرة: 4GB
المعالج: Intel Core i5
القرص: 256GB SSD
        """
        
        info_label = ttk.Label(
            info_frame,
            text=info_text,
            font=self.font_normal,
            justify="right"
        )
        info_label.pack()
    
    def show_ai(self):
        """عرض واجهة AI"""
        self.clear_content()
        
        title = ttk.Label(
            self.content,
            text="🤖 مساعد ناصر الذكي",
            font=self.font_title,
            foreground="#00ff88"
        )
        title.pack(pady=10)
        
        # منطقة الحوار
        chat_frame = ttk.Frame(self.content)
        chat_frame.pack(fill="both", expand=True, pady=10)
        
        chat_text = tk.Text(
            chat_frame,
            height=10,
            width=50,
            bg="#2d2d44",
            fg="#00ff88",
            font=self.font_small
        )
        chat_text.pack(fill="both", expand=True)
        chat_text.insert("1.0", "مرحباً! أنا ناصر الذكي. كيف أستطيع مساعدتك؟\n")
        chat_text.config(state="disabled")
        
        # حقل الإدخال
        input_frame = ttk.Frame(self.content)
        input_frame.pack(fill="x", pady=10)
        
        entry = ttk.Entry(input_frame)
        entry.pack(side="left", fill="x", expand=True, padx=5)
        
        send_btn = ttk.Button(
            input_frame,
            text="إرسال",
            command=lambda: self.send_ai_message(chat_text, entry)
        )
        send_btn.pack(side="right", padx=5)
    
    def send_ai_message(self, chat_text, entry):
        """إرسال رسالة للـ AI"""
        message = entry.get()
        if message:
            chat_text.config(state="normal")
            chat_text.insert("end", f"أنت: {message}\n")
            chat_text.insert("end", f"ناصر: فهمت طلبك '{message}'... جاري المعالجة\n")
            chat_text.config(state="disabled")
            entry.delete(0, "end")
    
    def show_files(self):
        """عرض إدارة الملفات"""
        self.clear_content()
        
        title = ttk.Label(
            self.content,
            text="📁 مدير الملفات",
            font=self.font_title,
            foreground="#00ff88"
        )
        title.pack(pady=10)
        
        # جدول الملفات
        tree = ttk.Treeview(
            self.content,
            columns=("اسم الملف", "الحجم", "التاريخ"),
            height=15
        )
        tree.column("#0", width=30)
        tree.column("اسم الملف", width=200)
        tree.column("الحجم", width=100)
        tree.column("التاريخ", width=150)
        
        tree.heading("#0", text="")
        tree.heading("اسم الملف", text="اسم الملف")
        tree.heading("الحجم", text="الحجم")
        tree.heading("التاريخ", text="التاريخ")
        
        # ملفات وهمية
        files = [
            ("📄 document.txt", "2.5 KB", "2024-01-15"),
            ("📷 photo.jpg", "1.2 MB", "2024-01-14"),
            ("🎵 music.mp3", "5.8 MB", "2024-01-13"),
        ]
        
        for file_info in files:
            tree.insert("", "end", values=file_info)
        
        tree.pack(fill="both", expand=True)
    
    def show_settings(self):
        """عرض الإعدادات"""
        self.clear_content()
        
        title = ttk.Label(
            self.content,
            text="⚙️ الإعدادات",
            font=self.font_title,
            foreground="#00ff88"
        )
        title.pack(pady=10)
        
        settings_frame = ttk.Frame(self.content)
        settings_frame.pack(fill="x", pady=10)
        
        # الإعدادات
        settings = [
            ("اللغة:", "العربية الخليجية"),
            ("المظهر:", "داكن"),
            ("الصوت:", "مفعّل"),
            ("التحديثات التلقائية:", "مفعّلة"),
            ("الأمان:", "عالي"),
        ]
        
        for label, value in settings:
            row = ttk.Frame(settings_frame)
            row.pack(fill="x", pady=5)
            
            lbl = ttk.Label(row, text=label, font=self.font_normal, width=20)
            lbl.pack(side="left")
            
            val = ttk.Label(row, text=value, font=self.font_normal, foreground="#00ff88")
            val.pack(side="right")
    
    def show_users(self):
        """عرض إدارة المستخدمين"""
        self.clear_content()
        
        title = ttk.Label(
            self.content,
            text="👥 إدارة المستخدمين",
            font=self.font_title,
            foreground="#00ff88"
        )
        title.pack(pady=10)
        
        tree = ttk.Treeview(
            self.content,
            columns=("اسم المستخدم", "البريد", "الدور", "الحالة"),
            height=15
        )
        tree.column("#0", width=30)
        tree.column("اسم المستخدم", width=150)
        tree.column("البريد", width=200)
        tree.column("الدور", width=100)
        tree.column("الحالة", width=100)
        
        tree.heading("#0", text="")
        tree.heading("اسم المستخدم", text="اسم المستخدم")
        tree.heading("البريد", text="البريد الإلكتروني")
        tree.heading("الدور", text="الدور")
        tree.heading("الحالة", text="الحالة")
        
        users = [
            ("👤 admin", "admin@nasser.local", "مسؤول", "🟢 نشط"),
            ("👤 user1", "user1@nasser.local", "مستخدم", "🟢 نشط"),
            ("👤 guest", "guest@nasser.local", "ضيف", "⚪ معطّل"),
        ]
        
        for user_info in users:
            tree.insert("", "end", values=user_info)
        
        tree.pack(fill="both", expand=True)
    
    def show_help(self):
        """عرض المساعدة"""
        self.clear_content()
        
        title = ttk.Label(
            self.content,
            text="ℹ️ المساعدة والدعم",
            font=self.font_title,
            foreground="#00ff88"
        )
        title.pack(pady=10)
        
        help_text = """مرحباً بك في نظام ناصر! 🤖

نظام ناصر هو منصة عربية متكاملة توفر:
• واجهة رسومية عربية حديثة
• مساعد ذكي (AI) يفهم العربية الخليجية
• إدارة متقدمة للملفات والمستخدمين
• أمان عالي وتشفير قوي
• تحديثات تلقائية

للمزيد من المعلومات:
📧 البريد: support@nasser.local
🌐 الموقع: nasser.local
📱 الدعم: +966-XX-XXX-XXXX

تم البناء بحب ❤️ للعرب
        """
        
        help_label = ttk.Label(
            self.content,
            text=help_text,
            font=self.font_normal,
            justify="right"
        )
        help_label.pack(pady=20)


def main():
    root = tk.Tk()
    gui = NassferGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
