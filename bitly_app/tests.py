from django.test import TestCase
from django.urls import reverse

from bitly_app.models import Link


class TestIndexView(TestCase):
    origin = 'http://testserver'
    original_link = 'https://google.com'

    def create_link(self):
        link = Link.objects.create(original_link=self.original_link)
        return link

    def test_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, response)
        self.assertContains(response, '<form method="post">')
        self.assertNotContains(response, 'Short link:')
        self.assertNotContains(response, 'Link was used:')

    def test_create_link(self):
        response = self.client.post('/', data={'original_link': self.original_link}, HTTP_ORIGIN=self.origin)
        self.assertEqual(response.status_code, 200, response)
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, 'Short link:')
        self.assertNotContains(response, 'Link was used:')

    def test_create_link_again(self):
        self.create_link()
        response = self.client.post('/', data={'original_link': self.original_link}, HTTP_ORIGIN=self.origin)
        self.assertEqual(response.status_code, 200, response)
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, 'Short link:')
        self.assertContains(response, 'Link was used:')


class TestRedirectView(TestCase):
    original_link = 'https://google.com'

    def create_link(self):
        link = Link.objects.create(original_link=self.original_link)
        return link

    def test_go(self):
        link = self.create_link()
        url = reverse('redirect', kwargs={'short_key': link.short_key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, link.original_link)
