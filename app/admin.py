from django.contrib import admin
from app.models import Entry


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'public',)
    list_filter = ('public',)


admin.site.register(Entry, EntryAdmin)
