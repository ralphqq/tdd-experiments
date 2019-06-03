from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_all_items(self):
        text_1 = 'My item 1'
        text_2 = 'My item 2'
        Item.objects.create(text=text_1)
        Item.objects.create(text=text_2)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, text_1)
        self.assertContains(response, text_2)


class NewListTest(TestCase):

    def test_can_save_a_post_request(self):
        item_entry = 'A new list item'
        response = self.client.post('/lists/new',
                                    data={'item_text': item_entry})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_entry)


    def test_redirects_after_a_post(self):
        item_entry = 'A new list item'
        response = self.client.post('/lists/new',
                                    data={'item_text': item_entry})

        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
