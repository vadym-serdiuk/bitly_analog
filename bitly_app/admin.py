from django.contrib import admin

from bitly_app.models import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('original_link', 'short_key', 'views_number')
    readonly_fields = ('views_number',)


admin.site.register(Link, LinkAdmin)
