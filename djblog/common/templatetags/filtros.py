from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

R_AMP2AND = re.compile('[\s]*\&[\s]*', flags=re.U|re.I)

@stringfilter
def amp2and(value):
    ns = R_AMP2AND.sub(u' and ', value)
    return ns
    
register.filter('amp2and', amp2and)


