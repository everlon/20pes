from django import template

register = template.Library()


@register.simple_tag(name="menu_active")
def active(request, data):
    if request.path.__contains__(data):
        return 'active'
    return ''
