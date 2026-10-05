# دليل التثبيت الشامل لنظام ناصر
# Complete Installation Guide for Nasser System

## 📋 المتطلبات الأساسية / Requirements

### متطلبات الأجهزة / Hardware
- **المعالج**: أي معالج حديث (Intel/AMD)
- **الذاكرة**: 2GB حد أدنى (4GB موصى به)
- **التخزين**: 10GB حد أدنى
- **الاتصال**: اتصال إنترنت

### متطلبات البرامج / Software
- Ubuntu 20.04 أو أحدث (أو Debian 11+)
- صلاحيات sudo
- متصفح ويب

---

## 🚀 طريقة التثبيت السريعة / Quick Installation

### الخطوة 1: استنساخ المستودع
```bash
git clone https://github.com/Intrshop/nasser.git
cd nasser
```

### الخطوة 2: تشغيل سكريبت التثبيت
```bash
chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

### الخطوة 3: إعادة التشغيل
```bash
sudo reboot
```

### الخطوة 4: التحقق من الثبيت
```bash
nasser status
```

---

## 🐳 التثبيت باستخدام Docker / Docker Installation

### المتطلبات
```bash
# تثبيت Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# تثبيت Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### التثبيت
```bash
# بناء الصور
docker-compose build

# تشغيل الخدمات
docker-compose up -d

# التحقق من الحالة
docker-compose ps
```

---

## 📦 التثبيت اليدوي / Manual Installation

### الخطوة 1: تحديث النظام
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### الخطوة 2: تثبيت المتطلبات
```bash
sudo apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    nodejs \
    npm \
    git
```

### الخطوة 3: تثبيت Python
```bash
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

### الخطوة 4: تثبيت اللغة العربية
```bash
sudo apt-get install -y \
    locales \
    fonts-noto-cjk \
    fcitx

sudo locale-gen ar_SA.UTF-8
sudo update-locale LANG=ar_SA.UTF-8
```

### الخطوة 5: نسخ الملفات
```bash
sudo mkdir -p /opt/nasser
sudo cp -r * /opt/nasser/
sudo chown -R $(whoami) /opt/nasser
```

### الخطوة 6: إنشاء أوامر النظام
```bash
sudo cp scripts/nasser /usr/local/bin/
sudo chmod +x /usr/local/bin/nasser
```

---

## ⚙️ الإعدادات الأولية / Initial Configuration

### تعيين اللغة
```bash
nasser config --language ar_SA

# أو يدويًا
sudo nano /opt/nasser/config/system.conf
# غيّر: default_language = ar_SA
```

### إعدادات الشبكة
```bash
nasser config --network

# إدخال إعدادات DNS
DNS Primary: 8.8.8.8
DNS Secondary: 8.8.4.4
```

### إعدادات الأمان
```bash
nasser config --security

# تفعيل الجدار الناري
nasser firewall enable

# إضافة قواعد
nasser firewall add --port 22 --protocol tcp
```

---

## 🔒 إعدادات الأمان / Security Setup

### إنشاء كلمة مرور قوية
```bash
nasser user create --username admin
nasser user set-password --username admin
```

### تفعيل التشفير
```bash
nasser security enable-encryption
nasser security set-encryption AES-256
```

### تفعيل جدار الحماية
```bash
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
```

---

## 🧪 اختبار التثبيت / Testing Installation

### اختبار الأساسيات
```bash
# حالة النظام
nasser status

# معلومات النظام
nasser info

# اختبار AI
nasser ai test

# اختبار اللغة
nasser lang test
```

### اختبار الأداء
```bash
nasser benchmark

# النتيجة تشمل:
# - سرعة المعالج
# - أداء الذاكرة
# - سرعة التخزين
# - زمن الاستجابة
```

### اختبار الشبكة
```bash
nasser network test

# النتيجة تشمل:
# - سرعة التحميل
# - سرعة رفع البيانات
# - كمون الاتصال
```

---

## 🆘 استكشاف الأخطاء / Troubleshooting

### المشكلة: خطأ في التثبيت
```bash
# تشغيل المثبت بوضع التصحيح
sudo ./scripts/install.sh --debug

# عرض السجل
tail -f /var/log/nasser-install.log
```

### المشكلة: مشاكل اللغة العربية
```bash
# إعادة تثبيت دعم اللغة
sudo apt-get install --reinstall locales
sudo locale-gen ar_SA.UTF-8
sudo update-locale LANG=ar_SA.UTF-8

# إعادة التشغيل
sudo reboot
```

### المشكلة: بطء النظام
```bash
# تحسين الأداء
nasser optimize

# تنظيف الذاكرة المؤقتة
nasser cache clear

# التحقق من العمليات
nasser process list
```

### المشكلة: Docker لا يعمل
```bash
# إعادة تشغيل Docker
sudo systemctl restart docker

# التحقق من الحالة
sudo systemctl status docker

# عرض السجلات
docker logs nasser-system
```

---

## 📊 التحقق من الخدمات / Verify Services

```bash
# عرض جميع الخدمات
systemctl list-units --type=service

# تحقق من خدمة Nasser
sudo systemctl status nasser

# عرض السجلات
sudo journalctl -u nasser -f
```

---

## 🎉 الانتهاء من التثبيت / Completion

بعد الانتهاء من التثبيت، يمكنك:

1. **فتح واجهة المستخدم**:
   ```bash
   nasser ui start
   ```
   ثم افتح المتصفح على: `http://localhost:8080`

2. **استخدام أوامر ناصر**:
   ```bash
   nasser help
   ```

3. **الوصول إلى المشرف**:
   ```bash
   nasser admin
   ```

---

## 📞 الدعم والمساعدة / Support

- 📧 البريد الإلكتروني: support@nasser-linux.org
- 🌐 الموقع: nasser-linux.org
- 📚 التوثيق: docs.nasser-linux.org
- 🐛 تقارير الأخطاء: github.com/Intrshop/nasser/issues

---

**تم إنشاؤه بحب 💚 للمنطقة العربية**
