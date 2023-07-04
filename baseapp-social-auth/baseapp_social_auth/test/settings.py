"""
Django settings for test project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "secret-for-test-app"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # baseapp_social_auth
    "avatar",
    "rest_framework.authtoken",
    "social_django",
    "rest_social_auth",
    "baseapp_social_auth",
    "baseapp_social_auth.cache",
    "test",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "test.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "test.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "test.User"

# Social auth
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]
SOCIAL_AUTH_PIPELINE_MODULE = "test.pipeline"
SOCIAL_AUTH_FACEBOOK_KEY = "1234"
SOCIAL_AUTH_FACEBOOK_SECRET = "abcd"
SOCIAL_AUTH_TWITTER_KEY = "1234"
SOCIAL_AUTH_TWITTER_SECRET = "1234"
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = "1234"
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = "1234"
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "1234"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "1234"
SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "baseapp_social_auth.cache.pipeline.cache_access_token",
    "test.pipeline.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "test.pipeline.set_avatar",
    "test.pipeline.set_is_new",
    "test.pipeline.link_user_to_referrer",
]
from baseapp_social_auth.settings import (  # noqa
    SOCIAL_AUTH_BEAT_SCHEDULES,
    SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS,
    SOCIAL_AUTH_FACEBOOK_SCOPE,
    SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS,
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE,
    SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS,
    SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE,
    SOCIAL_AUTH_USER_FIELDS,
)

if SOCIAL_AUTH_FACEBOOK_KEY and SOCIAL_AUTH_FACEBOOK_SECRET:
    AUTHENTICATION_BACKENDS.append("social_core.backends.facebook.FacebookOAuth2")
if SOCIAL_AUTH_TWITTER_KEY and SOCIAL_AUTH_TWITTER_SECRET:
    AUTHENTICATION_BACKENDS.append("social_core.backends.twitter.TwitterOAuth")
if SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY and SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET:
    AUTHENTICATION_BACKENDS.append("social_core.backends.linkedin.LinkedinOAuth2")
if SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET:
    AUTHENTICATION_BACKENDS.append("social_core.backends.google.GoogleOAuth2")
