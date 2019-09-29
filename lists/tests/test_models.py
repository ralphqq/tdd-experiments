from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')


    def test_item_is_related_to_list(self):
        list_obj = List.objects.create()
        item = Item(parent_list=list_obj)
        item.save()
        self.assertIn(
            item,
            list_obj.item_set.all()
        )


    def test_cannot_save_empty_list(self):
        list_obj = List.objects.create()
        item_obj = Item(parent_list=list_obj, text='')

        with self.assertRaises(ValidationError):
            # Django actually does not validate when saving
            # so this does not raise ValidationError
            # item_obj  .save()

            # To get it to raise ValidationError
            item_obj.full_clean()


    def test_duplicate_items_are_invalid(self):
        list_obj = List.objects.create()
        item = Item.objects.create(parent_list=list_obj, text='Blah')
        with self.assertRaises(ValidationError):
            # Create a new item but with the same text
            another_item = Item(
                parent_list=list_obj,
                text=item.text
            )
            another_item.full_clean()   # should raise ValidationError


    def test_CAN_save_same_item_to_different_lists(self):
        list_1 = List.objects.create()
        list_2 = List.objects.create()
        item = Item.objects.create(parent_list=list_1, text='Yes!')

        # A new item object but with same text
        # and associated with different list.
        another_item = Item(
            parent_list=list_2,
            text=item.text
        )
        another_item.full_clean()   # Should not raise any exception


    def test_list_ordering(self):
        list_1 = List.objects.create()
        item_1 = Item.objects.create(parent_list=list_1, text='First')
        item_2 = Item.objects.create(parent_list=list_1, text='Second')
        item_3 = Item.objects.create(parent_list=list_1, text='Third')
        self.assertEqual(
            list(Item.objects.all()),
            [item_1, item_2, item_3]
        )


    def test_string_representation(self):
        list_obj = List.objects.create()
        item = Item.objects.create(
            parent_list=list_obj,
            text='Some text'
        )
        self.assertEqual(str(item), 'Some text')


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        this_list = List.objects.create()
        self.assertEqual(
            this_list.get_absolute_url(),
            f'/lists/{this_list.id}/'
        )
