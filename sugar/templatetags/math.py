from django import template
register = template.Library()

@register.filter
def math_mult(value, arg):
    """Multiplication the arg and the value."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        try:
            return value * arg
        except:
            return value
math_mult.is_safe = False

@register.filter
def math_div(value, arg):
    """Division the arg and the value."""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError):
        try:
            return value / arg
        except:
            return value
math_mult.is_safe = False
