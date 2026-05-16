from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def public_pagination_url(context, page_param, page_number, tab=None):
    query = context["request"].GET.copy()
    query[page_param] = page_number

    if tab:
        query["tab"] = tab

    return query.urlencode()
