from django import template

register = template.Library()

@register.filter
def dur_calc(value):
    if(value % 60 == 0):
        s = str(value // 60) + ' Hour'
        if value//60 > 1:
            return s+'s'
        else:
            return s
    elif value < 60:
        return str(value % 60) + ' Minutes'
    else:
        s = str(value // 60) + ' Hour'
        if value//60 > 1:
            s = s + 's '
        else:
            s = s + ' '
        return s + str(value % 60) + ' Minutes'
