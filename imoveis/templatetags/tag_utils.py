from django import template

register = template.Library()


@register.simple_tag(name="menu_active")
def active(request, data):
    if request.path.__contains__(data):
        return 'active'
    return ''


@register.filter
# Gets the name of the passed in field on the passed in object
def verbose_name(the_object, the_field):
    verbose_name = the_object._meta.get_field(the_field).verbose_name
    # Check if the verbose name is using the default value, in which case it will be all lowercase
    return verbose_name.capitalize() if verbose_name.islower() else verbose_name
