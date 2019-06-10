import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10   # seconds


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.quit()


    def wait_for_row_in_list_table(self, expected_text):
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(expected_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_for_one_user(self):
        # User visits homepage
        self.browser.get(self.live_server_url)

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
        expected_list_item_1 = f'1: {list_item_1}'
        self.wait_for_row_in_list_table(expected_list_item_1)

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly"
        list_item_2 = 'Use peacock feathers to make a fly'
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(list_item_2)
        input_box.send_keys(Keys.ENTER)
        
        # The page updates again, and now shows both items on her list
        expected_list_item_2 = f'2: {list_item_2}'
        self.wait_for_row_in_list_table(expected_list_item_2)
        self.wait_for_row_in_list_table(expected_list_item_1)

        # Satisfied, she goes back to sleep.


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User 1 starts a new list
        # She enters two items into the list
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        user_1_item_1 = 'Get drunk like a skunk'
        input_box.send_keys(user_1_item_1)
        input_box.send_keys(Keys.ENTER)
        expected_list_item_1 = f'1: {user_1_item_1}'
        self.wait_for_row_in_list_table(expected_list_item_1)

        input_box = self.browser.find_element_by_id('id_new_item')
        user_1_item_2 = 'Be high in the sky'
        input_box.send_keys(user_1_item_2)
        input_box.send_keys(Keys.ENTER)
        expected_list_item_2 = f'2: {user_1_item_2}'
        self.wait_for_row_in_list_table(expected_list_item_1)
        self.wait_for_row_in_list_table(expected_list_item_2)

        # User 1 wonders whether the site will remember her list.
        # Then she sees the site has generated a unique URL for her
        # and there is some explanatory text to that effect.
        user_1_url = self.browser.current_url
        self.assertRegex(user_1_url, '/lists/.+')

        # User 2 visits site

        ## Start a new browser session to make sure that no information
        ## is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        # User 2 visits homepage
        # User 2 cannot see User 1's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(user_1_item_1, page_text)
        self.assertNotIn(user_1_item_2, page_text)

        # User 2 starts a new list
        input_box = self.browser.find_element_by_id('id_new_item')
        user_2_item_1 = 'Buy some catfood'
        input_box.send_keys(user_2_item_1)
        input_box.send_keys(Keys.ENTER)
        expected_list_item_1_user_2 = f'1: {user_2_item_1}'
        self.wait_for_row_in_list_table(expected_list_item_1_user_2)

        # User 2 gets his own unique URL
        user_2_url = self.browser.current_url
        self.assertRegex(user_2_url, '/lists/.+')
        self.assertNotEqual(user_2_url, user_1_url)

        # Again, there's no trace of User 1's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(user_1_item_1, page_text)
        self.assertIn(user_2_item_1, page_text)


    def test_layout_and_styling(self):
        # User goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # User notices the input box is nicely centered
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

        # User starts a list and
        # notices        that input box is centered there, too
        input_box.send_keys('Trying it out')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Trying it out')
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
