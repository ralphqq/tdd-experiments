from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm, BLANK_ITEM_ERROR
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        test_list = List.objects.create()
        response = self.client.get(f'/lists/{test_list.id}/')
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_items_only_for_that_list(self):
        correct_list = List.objects.create()
        text_1 = 'My item 1'
        text_2 = 'My item 2'
        Item.objects.create(text=text_1, parent_list=correct_list)
        Item.objects.create(text=text_2, parent_list=correct_list)

        other_list = List.objects.create()
        other_list_item_text_1 = 'Other item 1'
        other_list_item_text_2 = 'Other item 2'
        Item.objects.create(
            text=other_list_item_text_1,
            parent_list=other_list
        )
        Item.objects.create(
            text=other_list_item_text_2,
            parent_list=other_list
        )

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, text_1)
        self.assertContains(response, text_2)
        self.assertNotContains(response, other_list_item_text_1)
        self.assertNotContains(response, other_list_item_text_2)


    def test_can_save_a_post_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        item_text = 'A new item for an existing list'

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': item_text}
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.parent_list, correct_list)


    def test_post_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        item_text = 'A new item for an existing list'

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': item_text}
        )

        list_entry = Item.objects.first()

        self.assertRedirects(
            response,
            f'/lists/{list_entry.parent_list.id}/'
        )


    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        item_text = 'A new item for an existing list'

        response = self.client.get(
            f'/lists/{correct_list.id}/'
        )

        self.assertEqual(response.context['parent_list'], correct_list)


    def post_invalid_input(self):
        this_list = List.objects.create()
        return self.client.post(
            f'/lists/{this_list.id}/',
            data={'text': ''}
        )


    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)


    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')


    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)


    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(BLANK_ITEM_ERROR))


    def test_displays_item_form(self):
        this_list = List.objects.create()
        response = self.client.get(f'/lists/{this_list.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')


class NewListTest(TestCase):

    def test_can_save_a_post_request(self):
        item_entry = 'A new list item'
        response = self.client.post('/lists/new',
                                    data={'text': item_entry})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_entry)


    def test_redirects_after_a_post(self):
        item_entry = 'A new list item'
        response = self.client.post('/lists/new',
                                    data={'text': item_entry})

        list_entry = Item.objects.first()

        self.assertRedirects(
            response,
            f'/lists/{list_entry.parent_list.id}/'
        )


    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    def test_validation_errors_are_shown_on_homepage(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(BLANK_ITEM_ERROR))


    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)


    def test_do_not_save_invalid_items(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

