import os

DEBUG = True,
USE_TZ = True,
SECRET_KEY = "verySecure3"
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_dynamic_models',
        'USER': 'django',
        'PASSWORD': 'dev1234',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_django_dynamic_models',
        },
    }
}
APP_LABEL_DYNAMIC_MODELS = "json2model"

ROOT_URLCONF = "tests.urls",

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
]

INSTALLED_APPS += (
    'mutant',
    'mutant.contrib.boolean',
    'mutant.contrib.temporal',
    'mutant.contrib.file',
    'mutant.contrib.numeric',
    'mutant.contrib.text',
    'mutant.contrib.web',
    'mutant.contrib.related',
    "json2model"
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]
