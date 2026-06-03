from django import template
from django.utils.html import strip_tags
from django.utils.text import Truncator
from html import unescape
import re


register = template.Library()


@register.simple_tag(takes_context=True)
def public_pagination_url(context, page_param, page_number, tab=None):
    query = context["request"].GET.copy()
    query[page_param] = page_number

    if tab:
        query["tab"] = tab

    return query.urlencode()


@register.filter
def clean_text(value):
    text = strip_tags(str(value or ""))
    text = unescape(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


@register.filter
def clean_truncate(value, length=100):
    return Truncator(clean_text(value)).chars(int(length))
