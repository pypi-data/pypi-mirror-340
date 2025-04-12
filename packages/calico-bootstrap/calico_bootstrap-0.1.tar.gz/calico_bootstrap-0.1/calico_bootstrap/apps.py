from django.apps import AppConfig

from calico import hook


class CalicoBootstrapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calico_bootstrap'


@hook
def declare_theme():
    return [('base_theme', CalicoBootstrapConfig.name)]


@hook
def calico_css(theme):
    if CalicoBootstrapConfig.name not in theme:
        return []

    return [('default_css', ['https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'])]


@hook
def calico_js(theme):
    if CalicoBootstrapConfig.name not in theme:
        return []

    return [('alpinejs', 'https://cdn.jsdelivr.net/npm/alpinejs@3.14.1/dist/cdn.min.js')]
