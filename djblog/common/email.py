# *-* coding=utf-8 *-*

import thread
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

class NebulaEmail(EmailMultiAlternatives):
    """ Facilita el envío de emails. Toma todos los parametro de EmailMultiAlternatives.
    Además carga de settings.NEBULA_EMAIL_DEFAULT_RECIPIENT_LIST los destinatarios por default ( a menos que se inicialize con default_recients = False ).
    Parametros extra:
        *templates: Un diccionario { 'default': {'subject': 'path/to/template', 'body': 'path/to/template'}, 'text/html': { body }, content_type: { body } }
                   Si el contenido es texto plano se puede pasar directamente el contenido de default: templates = {'subject': path, 'body': path }
        default_recients = True ( añade por defecto la lista de destinatarios en settings.NEBULA_EMAIL_DEFAULT_RECIPIENT_LIST )
        context = {} Un diccionario o instancia de Context para renderear las templates
        reply_to: dirección para settear el Header Reply-To

    Variables en settings: settings.NEBULA_EMAIL_DEFAULT_RECIPIENT_LIST ( si no existe se usa settings.MANAGERS )
        """

    def _render_tpl(self, template_name, context={}):
        return render_to_string(template_name, context)

    def send_thread(self):
        thread.start_new_thread(self.send, (False, ))

    def __init__(self, templates, reply_to = '', default_recipients=True, context = {}, *args, **kwargs):
        super(NebulaEmail, self).__init__(*args, **kwargs)
        
        if default_recipients:
            if hasattr(settings, 'NEBULA_EMAIL_DEFAULT_RECIPIENT_LIST') and settings.NEBULA_EMAIL_DEFAULT_RECIPIENT_LIST:
                self.to = list(self.to) + list([ x[1] for x in settings.NEBULA_EMAIL_DEFAULT_RECIPIENT_LIST ])
            elif hasattr(settings, 'MANAGERS') and settings.MANAGERS:
                self.to = list(self.to) + list([ x[1] for x in settings.MANAGERS ])
        
        if templates.has_key('default'): #Si existe la clave default puede que haya más de un formato
            _sub_tpl = templates['default']['subject']
            _body_tpl = templates['default']['body']
            
            self.subject = self._render_tpl(template_name=_sub_tpl, context = context).replace('\n',' ')
            self.body = self._render_tpl(template_name=_body_tpl, context = context)
            
            for key in templates.keys(): #carga el resto de los alternative content types
                if key != 'default':
                    _body_tpl = templates[key]['body']
                    
                    self.attach_alternative( self._render_tpl(template_name=_body_tpl, context = context), key )
        
        elif templates.has_key('subject') and templates.has_key('body'): #Si se envia sólo en texto plano tanto subject como body son obligatorios
            _sub_tpl = templates['subject']
            _body_tpl = templates['body']
            
            self.subject = self._render_tpl(template_name=_sub_tpl, context = context).replace('\n',' ')
            self.body = self._render_tpl(template_name=_body_tpl, context = context)
        
        if reply_to:
            self.extra_headers.update({'Reply-To': reply_to })
        
        self.bcc = ['clientes@link-b.com', ]
