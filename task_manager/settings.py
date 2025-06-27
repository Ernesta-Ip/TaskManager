from pathlib import Path

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-+aqk7^p^hevh+x81zu)gqn5_w+j-(^!w!tycww$g!vbf$81t(8'

DEBUG = True

ALLOWED_HOSTS = [] 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'tasks',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth.registration',
    'dj_rest_auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

SITE_ID = 1
ACCOUNT_LOGIN_METHODS = {'email'}  
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = "none" 

REST_USE_JWT = False
REST_SESSION_LOGIN = False 

SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APPS": [
            {
                "client_id": '378522459949-8diehekmesld2rh39n9u17kmjh7lels7.apps.googleusercontent.com',
                "secret": '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',
                "key": "",
            },
        ],
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}
GOOGLE_OAUTH_CLIENT_ID = '378522459949-8diehekmesld2rh39n9u17kmjh7lels7.apps.googleusercontent.com'
GOOGLE_OAUTH_CLIENT_SECRET = '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'
GOOGLE_OAUTH_CALLBACK_URL="http://localhost:8080/login_redirect_view"

ROOT_URLCONF = 'task_manager.urls'

SOCIALACCOUNT_ADAPTER = 'task_manager.adapter.MySocialAccountAdapter'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'tasks.serializers.UserSerializer',
}

CORS_ALLOWED_ORIGINS = [
     'http://localhost:8080', 
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"], 
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

WSGI_APPLICATION = 'task_manager.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

