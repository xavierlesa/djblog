# +-+ encodig:utf-8 +-+

from django import template

class CommonNode(template.Node):
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k+'_template_str', v)
            try:
                setattr(self, k+'_template', template.Variable(v))
            except:
                pass

        setattr(self, 'key_list', kwargs.keys())

    def render(self, context):
        if self.key_list:
            for key in self.key_list:
                try:
                    vars()[key] = getattr(self, '%s_template' % key).resolve(context)
                except template.VariableDoesNotExist:
                    vars()[key] = getattr(self, '%s_template_str' % key)
