# votre_projet/settings/production.py

import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from .base import *


def env_list(name):
    """Découpe une variable d'environnement "a,b,c" en liste propre.

    Ignore les entrées vides : une valeur comme "localhost," ou une variable
    absente ne doit pas produire l'entrée '' (qui casse ALLOWED_HOSTS et
    déclenche l'erreur de system check corsheaders.E013).
    """
    return [item.strip() for item in os.environ.get(name, '').split(',') if item.strip()]


# ==============================================================================
# SÉCURITÉ
# ==============================================================================

# Le .env du projet nomme cette variable DJANGO_SECRET_KEY : on accepte les deux
# noms pour éviter un démarrage "réussi" mais avec toutes les requêtes en 500
# (ImproperlyConfigured: The SECRET_KEY setting must not be empty).
SECRET_KEY = os.environ.get('SECRET_KEY') or os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "SECRET_KEY absente : définir la variable d'environnement SECRET_KEY "
        "(ou DJANGO_SECRET_KEY) sur le service d'hébergement."
    )

DEBUG = False

# ALLOWED_HOSTS explicite + hostname public fourni automatiquement par Render,
# sinon chaque requête arrive en 400 (DisallowedHost).
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS')
render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname and render_hostname not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_hostname)

# Liste vide (variable absente) = pas de CORS, ce qui est valide. Une chaîne ''
# issue du split(',') faisait échouer collectstatic / migrate (corsheaders.E013).
CORS_ALLOWED_ORIGINS = env_list('CORS_ALLOWED_ORIGINS')

# ==============================================================================
# BASE DE DONNÉES
# ==============================================================================

DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
}

# ==============================================================================
# FICHIERS STATIQUES (WHITENOISE)
# ==============================================================================

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN = os.environ.get('SENTRY_DSN')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0, # Capture 100% des transactions pour le monitoring de perf.
        send_default_pii=True
    )