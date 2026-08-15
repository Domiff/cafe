from markupsafe import Markup, escape


def phone(model, attr):
    if not model.phone:
        return Markup('<span class="text-secondary">—</span>')
    safe = escape(model.phone)
    return Markup(f'<a href="tel:{safe}">{safe}</a>')
