from django import template

register = template.Library()

@register.filter
def percentage(value):
    if value != None:
        return '{0:.0%}'.format(value)

@register.filter
def currency(value):
    if value != None and value != '':
        return '$ %s' % (value)

@register.filter
def url(value):
    if value != None:
        return '<a href="%s" target="_blank">%s</a>' % (value, value)