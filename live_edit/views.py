from django.db.models import get_model
from django.http import HttpResponse
from django.utils import simplejson


def live_edit(request):
    """
    Live edit

    Template:  ``live_edit/detail.html``
    Context:
        live_edit
            Generically update an object
    """
    response_dict = {}

    slug = request.POST.get('slug')
    value = request.POST.get('value')

    if slug and value:
        bits = slug.split('-')
        app_label = bits[0]
        module_label = bits[1]
        field = bits[2]
        id = bits[3]
        model = get_model(app_label, module_label)
        object = model._default_manager.get(id=id)

        if getattr(object, field):
            setattr(object, field, value)
            object.save()
            response_dict.update({'success': True})
        else:
            response_dict.update({'errors': {}})
            response_dict['errors'].update({field: 'An invalid app, module, or fieldname is required'})

    else:
        response_dict.update({'errors': {}})

        if not slug:
            response_dict['errors'].update({'slug': 'This field is required'})

        if not value:
            response_dict['errors'].update({'value': 'This field is required'})

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
