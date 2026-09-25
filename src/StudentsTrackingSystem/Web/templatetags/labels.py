from django import template

from Core.Enums import ROLE_LABELS

register = template.Library()


@register.filter
def role_label(role):
    """{{ user.role|role_label }} -> "Ученик" вместо "student"."""
    return ROLE_LABELS.get(role, role)
