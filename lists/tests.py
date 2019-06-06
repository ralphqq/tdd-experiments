from django.test import TestCase

from lists.models import Item, List


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        test_list = List()
        test_list.save()

        first_item = Item()
        text_1 = 'The first item ever'
        first_item.text = text_1
        first_item.parent_list = test_list
        first_item.save()

        second_item = Item()
        text_2 = 'Item the second'
        second_item.text = text_2
        second_item.parent_list = test_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, test_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, text_1)
        self.assertEqual(second_saved_item.text, text_2)
        self.assertEqual(first_saved_item.parent_list, test_list)
        self.assertEqual(second_saved_item.parent_list, test_list)


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

        list_entry = Item.objects.first()

        self.assertRedirects(
            response,
            f'/lists/{list_entry.parent_list.id}/'
        )


class NewItemTest(TestCase):

    def test_can_save_a_post_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        item_text = 'A new item for an existing list'

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': item_text}
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.parent_list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        item_text = 'A new item for an existing list'

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': item_text}
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

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'item_text': item_text}
        )

        self.assertEqual(response.context['parent_list'], correct_list)
