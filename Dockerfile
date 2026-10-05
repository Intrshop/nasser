FROM ubuntu:22.04

# تعيين اللغة والترميز
ENV LANG=ar_SA.UTF-8
ENV LANGUAGE=ar_SA:en
ENV LC_ALL=ar_SA.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    python3-dev \
    nodejs \
    npm \
    locales \
    fonts-noto-cjk \
    fonts-noto-cjk-extra \
    fonts-firacode \
    && rm -rf /var/lib/apt/lists/*

# تفعيل دعم اللغة العربية
RUN locale-gen ar_SA.UTF-8 && \
    update-locale LANG=ar_SA.UTF-8

# إنشاء دليل العمل
WORKDIR /opt/nasser

# نسخ ملفات المشروع
COPY . .

# تثبيت المتطلبات
RUN pip3 install --no-cache-dir -r requirements.txt 2>/dev/null || true

# فتح المنفذ
EXPOSE 8080 5000

# أمر التشغيل
CMD ["python3", "src/ai/nasser_ai.py"]
