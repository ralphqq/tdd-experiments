from django.test import TestCase

from lists.forms import ItemForm, BLANK_ITEM_ERROR
from lists.models import Item, List


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do- item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())


    def test_form_validation_for_blank_items(self):
        form = ItemForm(data='')
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [BLANK_ITEM_ERROR]
        )


    def test_form_save_handles_saving_to_a_list(self):
        this_list = List.objects.create()
        item_text = 'To be done'
        form = ItemForm(data={'text': item_text})
        new_item = form.save(for_list=this_list)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.parent_list, this_list)
