from django import template
from django.contrib.auth.models import get_hexdigest
from django.template.loader import render_to_string


register = template.Library()


class RenderHashForNode(template.Node):

    def __init__(self, object, field):
        self.object = object
        self.field = field

    def render(self, context):
        try:
            obj = template.resolve_variable(self.object, context)
            namespace = '-'.join([
                obj._meta.app_label,
                obj._meta.module_name,
                str(obj.pk),
                self.field,
            ])
            output = '-'.join([namespace, get_hexdigest('sha1', 'a1976', namespace)])
            return output

        except template.VariableDoesNotExist:
            return ''


class RenderTemplateForNode(template.Node):

    def __init__(self, object, field, template_dir):
        self.object = object
        self.field = field
        self.template_dir = template_dir.rstrip('/')

    def render(self, context):
        try:
            object = template.resolve_variable(self.object, context)
            field_str = '%s.%s.%s' % (object._meta.app_label, object._meta.module_name, self.field)

            context.push()
            context['object'] = object
            if hasattr(object, self.field):
                context['value'] = getattr(object, self.field)

                template_list = []
                if ',' in self.template_dir:
                    for tdir in self.template_dir.split(','):
                        template_list.append('%s/%s.html' % (tdir, field_str))
                        template_list.append('%s/default.html' % tdir)
                else:
                    template_list.append('%s/%s.html' % (self.template_dir, field_str))
                    template_list.append('%s/default.html' % self.template_dir)

                output = render_to_string(template_list, context)
                context.pop()

                return output

            else:
                return "*** error: %s.%s does not contain field '%s'***" % (
                    object._meta.app_label,
                    object._meta.module_name,
                    self.field,
                )

        except template.VariableDoesNotExist:
            return ''


@register.tag()
def generate_hash(parser, token):
    try:
        tag_name, object, field = token.contents.split()

    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires two arguments '[object] [fieldname]'" % token.contents.split()[0]

    return RenderHashForNode(object, field)


@register.tag()
def render_snippet(parser, token):
    try:
        tag_name, object, field, template_dir = token.contents.split()

    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires three arguments '[object] [fieldname] [template_dir]'" % token.contents.split()[0]

    return RenderTemplateForNode(object, field, template_dir)
