from django import template

register = template.Library()

@register.filter
def lookup(d, key):
    return d[key]

@register.filter
def slice_it(d):
    return d[:3]

@register.filter
def sort_it(queryset):
    return queryset.order_by('foldermember')