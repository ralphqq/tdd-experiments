from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List


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


    def test_cannot_save_empty_list(self):
        list_obj = List.objects.create()
        item_obj = Item(parent_list=list_obj, text='')

        with self.assertRaises(ValidationError):
            # Django actually does not validate when saving
            # so this does not raise ValidationError
            # item_obj  .save()

            # To get it to raise ValidationError
            item_obj.full_clean()
