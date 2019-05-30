from django.test import TestCase

from lists.models import Item


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


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        text_1 = 'The first item ever'
        first_item.text = text_1
        first_item.save()

        second_item = Item()
        text_2 = 'Item the second'
        second_item.text = text_2
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, text_1)
        self.assertEqual(second_saved_item.text, text_2)
