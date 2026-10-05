#!/bin/bash

###############################################################################
# سكريبت تثبيت نظام ناصر
# Nasser Linux System Installation Script
###############################################################################

set -e

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# المتغيرات
INSTALL_DIR="/opt/nasser"
NASSER_USER="nasser"
NASSER_HOME="/home/$NASSER_USER"

# دالة الطباعة
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# التحقق من الصلاحيات
if [[ $EUID -ne 0 ]]; then
   print_error "هذا السكريبت يجب أن يعمل كـ root"
   echo "This script must be run as root"
   exit 1
fi

# التحقق من نظام التشغيل
print_header "التحقق من نظام التشغيل / Checking OS"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$ID" != "ubuntu" && "$ID" != "debian" ]]; then
        print_error "نظام التشغيل غير مدعوم (Ubuntu أو Debian مطلوب)"
        echo "Unsupported OS (Ubuntu or Debian required)"
        exit 1
    fi
    print_success "نظام التNAME مدعوم"
fi

# تحديث النظام
print_header "تحديث النظام / Updating System"
apt-get update
apt-get upgrade -y
print_success "تم تحديث النظام"

# تثبيت المتطلبات الأساسية
print_header "تثبيت المتطلبات الأساسية / Installing Dependencies"
apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    python3-dev \
    nodejs \
    npm \
    git \
    vim \
    nano \
    htop \
    net-tools \
    openssh-server \
    openssh-client \
    openssl \
    libssl-dev \
    zlib1g-dev \
    libffi-dev \
    libsqlite3-dev

print_success "تم تثبيت المتطلبات الأساسية"

# تثبيت Python والمكتبات
print_header "تثبيت Python والمكتبات / Installing Python Libraries"
pip3 install --upgrade pip setuptools wheel
pip3 install numpy pandas scikit-learn tensorflow pytorch
pip3 install flask django fastapi uvicorn
pip3 install requests beautifulsoup4 scrapy
pip3 install pillow opencv-python matplotlib seaborn
pip3 install nltk spacy gensim
pip3 install pydantic sqlalchemy

print_success "تم تثبيت مكتبات Python"

# تفعيل دعم اللغة العربية
print_header "تفعيل دعم اللغة العربية / Enabling Arabic Support"
apt-get install -y \
    locales \
    fonts-noto-cjk \
    fonts-noto-cjk-extra \
    fonts-firacode \
    fcitx \
    fcitx-bin \
    fcitx-module-cloudpinyin \
    fcitx-table-wubi \
    ibus \
    ibus-libpinyin

# تثبيت لغات إضافية
locale-gen ar_SA.UTF-8
locale-gen en_US.UTF-8
update-locale LANG=ar_SA.UTF-8

print_success "تم تفعيل دعم اللغة العربية"

# إنشاء مجلد التثبيت
print_header "إنشاء مجلدات النظام / Creating System Directories"
mkdir -p $INSTALL_DIR
mkdir -p $INSTALL_DIR/bin
mkdir -p $INSTALL_DIR/lib
mkdir -p $INSTALL_DIR/etc
mkdir -p $INSTALL_DIR/var/log
mkdir -p $INSTALL_DIR/ai/models
mkdir -p $INSTALL_DIR/ui

print_success "تم إنشاء المجلدات"

# نسخ الملفات
print_header "نسخ ملفات النظام / Copying System Files"
cp -r ./src/* $INSTALL_DIR/ 2>/dev/null || print_warning "لم يتم العثور على مجلد src"
cp -r ./config/* $INSTALL_DIR/etc/ 2>/dev/null || print_warning "لم يتم العثور على ملفات الإعدادات"

print_success "تم نسخ الملفات"

# إنشاء رابط رمزي
print_header "إنشاء أوامر النظام / Creating System Commands"
cat > /usr/local/bin/nasser << 'EOF'
#!/bin/bash
source /opt/nasser/bin/nasser-cli.sh
nasser_main "$@"
EOF

chmod +x /usr/local/bin/nasser
print_success "تم إنشاء أوامر النظام"

# تثبيت الخدمات
print_header "تثبيت خدمات النظام / Installing System Services"
cat > /etc/systemd/system/nasser.service << EOF
[Unit]
Description=Nasser Linux System
After=network.target

[Service]
Type=forking
User=root
ExecStart=$INSTALL_DIR/bin/nasser-daemon start
ExecStop=$INSTALL_DIR/bin/nasser-daemon stop
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable nasser
print_success "تم تثبيت الخدمات"

# إعدادات الأمان
print_header "إعدادات الأمان / Security Configuration"
apt-get install -y ufw fail2ban
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
print_success "تم تفعيل الأمان"

# تثبيت أدوات المراقبة
print_header "تثبيت أدوات المراقبة / Installing Monitoring Tools"
apt-get install -y prometheus grafana-server
systemctl start grafana-server
systemctl enable grafana-server
print_success "تم تثبيت أدوات المراقبة"

# الإنهاء
print_header "إتمام التثبيت / Installation Complete"
echo ""
print_success "تم تثبيت نظام ناصر بنجاح!"
echo "Nasser Linux System installed successfully!"
echo ""
echo -e "${YELLOW}الخطوات التالية / Next Steps:${NC}"
echo "1. اختبار النظام:"
echo "   nasser status"
echo ""
echo "2. الوصول إلى الإعدادات:"
echo "   nasser config"
echo ""
echo "3. بدء استخدام النظام:"
echo "   nasser start"
echo ""
echo "4. الحصول على المساعدة:"
echo "   nasser help"
echo ""
print_warning "يُنصح بإعادة تشغيل النظام"
echo "System reboot is recommended"
echo ""
echo "sudo reboot"
