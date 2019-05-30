import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User visits homepage
        self.browser.get('http://localhost:8000')

        # User sees the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do- item'
        )

        # She types "Buy peacock feathers" into a text box
        list_item_1 = 'Buy peacock feathers'
        input_box.send_keys(list_item_1)

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        expected_list_item_1 = f'1: {list_item_1}'
        self.assertIn(expected_list_item_1, [row.text for row in rows])

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly"
        list_item_2 = 'Use peacock feathers to make a fly'
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(list_item_2)
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        expected_list_item_2 = f'2: {list_item_2}'
        self.assertIn(expected_list_item_1, [row.text for row in rows])
        self.assertIn(expected_list_item_2, [row.text for row in rows])

        # User wonders whether the site will remember her list.
        # Then she sees the site has generated a unique URL for her
        # and there is some explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
