from django.test import TestCase
from django.urls import reverse


class HomePageTest(TestCase):
    def test_get_home_page_view(self):
        resp = self.client.get(reverse('memo:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html', 'base.html')
