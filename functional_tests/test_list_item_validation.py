from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ItemValidationTes(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # User goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                "You can't have an empty list item."
            )
        )

        # She tries again with some text for the item, which now works
        input_box = self.browser.find_element_by_id('id_new_item')
        some_list_entry = 'Buy milk'
        input_box.send_keys(some_list_entry)
        input_box.send_keys(Keys.ENTER)

        expected_text = f'1: {some_list_entry}'
        self.wait_for_row_in_list_table(expected_text)

        # Interestingly, she now decides to submit a second blank list item
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                "You can't have an empty list item."
            )
        )

        # And she can correct it by filling some text in
        input_box = self.browser.find_element_by_id('id_new_item')
        some_list_entry_2 = 'Brew coffee'
        input_box.send_keys(some_list_entry_2)
        input_box.send_keys(Keys.ENTER)

        expected_text_2 = f'2: {some_list_entry_2}'
        self.wait_for_row_in_list_table(expected_text)
        self.wait_for_row_in_list_table(expected_text_2)
