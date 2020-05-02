from django.db.models import F
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import RedirectView

from bitly_app.forms import PostLinkForm
from bitly_app.models import Link


class IndexView(View):
    def get(self, request, *args, **kwargs):
        form = PostLinkForm()
        return render(request, 'index.html', {'form': form, 'link': None, 'f_new': False})

    def post(self, request, *args, **kwargs):
        form = PostLinkForm(data=request.POST)
        if form.is_valid():
            link, f_new = form.get_or_create_link_object()
            return render(request,
                          'index.html',
                          {'form': form, 'link': link, 'f_new': f_new, 'base_url': request.META['HTTP_ORIGIN']})
        return redirect('/')


class ShortUrlRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, short_key, **kwargs):
        try:
            link = Link.objects.get(short_key=short_key)
        except Link.DoesNotExist:
            return '/'
        else:
            Link.objects.filter(pk=link.pk).update(views_number=F('views_number') + 1)
            return link.original_link
