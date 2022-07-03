"""
Django settings for spider2dataVisualization project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@ve(upe*^zety#q+zl)p1n6r@47_b*@-g@0=u%%lly0m3f^3w@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.spider',   # 爬虫 APP
    'apps.visualization',  # 可视化 APP
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spider2dataVisualization.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spider2dataVisualization.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spider2dataVisualization',
        'USER': 'dev',
        'PASSWORD': 'dev@123',
        'PORT': '3306',
        'HOST': 'localhost'
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 日志器
LOGGING = {
    # 版本
    'version': 1,
    # 是否禁用已存在的日志器
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s module:%(module)s lineno:%(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
        "spider": {
            "format": "%(levelname)s %(asctime)s %(message)s"
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': Path(BASE_DIR).joinpath("logs/operation.log"),  # 日志文件的位置，必须先手动创建这个logs文件夹
            # 单个日志文件最大字节数
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件个数
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'file2': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': Path(BASE_DIR).joinpath("logs/system.log"),  # 日志文件的位置，必须先手动创建这个logs文件夹
            # 单个日志文件最大字节数
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件个数
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'file3': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': Path(BASE_DIR).joinpath("logs/spider.log"),  # 日志文件的位置，必须先手动创建这个logs文件夹
            # 单个日志文件最大字节数
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件个数
            'backupCount': 10,
            'formatter': 'spider'
        },
    },
    'loggers': {
        'operation': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'system': {
            'handlers': ['console', 'file2'],
            'propagate': True,
            'level': 'INFO',
        },
        'spider': {
            'handlers': ['console', 'file3'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}
