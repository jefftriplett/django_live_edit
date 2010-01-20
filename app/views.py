from django.views.generic.list_detail import object_detail

from app.models import Entry


def entry_detail(request, id, template_name='app/entry_detail.html'):
    return object_detail(
        request=request,
        object_id=id,
        queryset=Entry.objects.all(),
        template_name=template_name)
