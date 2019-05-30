from django.test import TestCase


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_post_request(self):
        submitted_text = 'A new list item'
        response = self.client.post(
            '/',
            data={'item_text': submitted_text}
        )
        self.assertIn(submitted_text, response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

