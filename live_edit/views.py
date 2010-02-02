from django.contrib.auth.models import get_hexdigest
from django.db.models import get_model
from django.forms import Form, ModelForm
from django.forms.models import modelform_factory
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson


def live_edit_form(request, template_name='live_edit/default_form.html'):
    if 'id' in request.GET:
        id = request.GET.get('id')
        app_label, module_label, object_id, field, hashed_key = id.split('-')
        model_obj = get_model(app_label, module_label)
        object = model_obj._default_manager.get(id=object_id)
        ModelFormSet = modelform_factory(model=model_obj, fields=(field,))
        form = ModelFormSet(instance=object)
    else:
        form = None

    return render_to_response(template_name, {
        'form': form,
        }, context_instance=RequestContext(request))


def live_edit_json(request):
    response_dict = {}
    if 'id' in request.GET:
        id = request.GET.get('id')
        app_label, module_label, object_id, field, hashed_key = id.split('-')
        model_obj = get_model(app_label, module_label)
        object = model_obj._default_manager.get(id=object_id)

        if hasattr(object, field):
            response_dict.update({field: getattr(object, field)})
        else:
            response_dict.update({'errors': {}})
            response_dict['errors'].update({field: 'A valid field is required'})
    else:
        response_dict.update({'errors': {}})
        response_dict['errors'].update({field: 'A valid field is required'})

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')


def live_edit_save(request):
    """
    Live edit

    Template: ``live_edit/detail.html``
    Context:
        live_edit
            Generically update an object

    TODO:
    - error handling needs to be written when I am awake...

    """
    id = request.POST.get('id', request.GET.get('id'))
    value = request.POST.get('value', request.GET.get('value'))
    response_dict = {}

    if id and value:
        app_label, module_label, object_id, field, hashed_key = id.split('-')
        namespace = '-'.join(id.split('-')[:4])
        check_hash = get_hexdigest('sha1', 'a1976', namespace)

        if hashed_key == check_hash:
            namespace = '-'.join([
                app_label,
                module_label,
                object_id,
                field,
            ])

            model = get_model(app_label, module_label)
            object = model._default_manager.get(id=object_id)

            if getattr(object, field):
                setattr(object, field, value)
                object.save()
                response_dict.update({'success': True})

            else:
                response_dict.update({'errors': {}})
                response_dict['errors'].update({field: 'An invalid app, module, or fieldname is required'})

        else:
            response_dict.update({'errors': {}})
            response_dict['errors'].update({'status': 'Unable to update application because security keys do not match'})

    else:
        response_dict.update({'errors': {}})

        if not id:
            response_dict['errors'].update({'id': 'This field is required'})

        if not value:
            response_dict['errors'].update({'value': 'This field is required'})

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')


def live_edit_snippet(request, template_name='live_edit/snippets/default.html'):
    template_list = []
    if 'id' in request.GET:
        id = request.GET.get('id')
        app_label, module_label, object_id, field, hashed_key = id.split('-')
        model_obj = get_model(app_label, module_label)
        ModelFormSet = modelform_factory(model=model_obj, fields=(field,))
        object = model_obj._default_manager.get(id=object_id)
        field_str = '%s.%s.%s' % (object._meta.app_label, object._meta.module_name, field)
        value = getattr(object, field)
        template_list.append('live_edit/snippets/%s.html' % (field_str))
        template_list.append('live_edit/snippets/default.html')
        print template_list
    else:
        object = None
        value = None
        template_list.append('live_edit/snippets/default.html')

    return render_to_response(template_name, {
        'object': object,
        'value': value,
        }, context_instance=RequestContext(request))
