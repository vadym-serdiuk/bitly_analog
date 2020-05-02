from django import forms

from bitly_app.models import Link


class PostLinkForm(forms.Form):
    original_link = forms.URLField()

    def get_or_create_link_object(self):
        assert self.cleaned_data

        link, f_new = Link.objects.get_or_create(original_link=self.cleaned_data['original_link'])
        return link, f_new
