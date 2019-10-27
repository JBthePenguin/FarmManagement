from product_app.tests import Browser
from client_app.models import CategoryClient


class ClientTests(Browser):
    """ Tests for browsing in Client app
    - add, update and delete category and client """
    def add_category(self, name):
        self.selenium.find_element_by_link_text(
            "Ajouter une catégorie").click()
        self.wait_page_loaded("Ajouter une catégorie de client")
        self.selenium.find_element_by_id("id_name").send_keys(name)
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Clients")

    def assert_category_range_in_table(self, category_names):
        """ assert if categories displayed in order in table """
        category_names.sort()
        table = self.selenium.find_element_by_xpath("//table[1]")
        body_table = table.find_element_by_tag_name('tbody')
        lines = body_table.find_elements_by_tag_name("tr")
        i = 0
        for category_name in category_names:
            # assert category range in table
            line_values = lines[i].find_elements_by_tag_name("td")
            self.assertEqual(line_values[0].text, category_name)
            i += 1

    def test_client_page(self):
        """ test browsing in client template """
        self.selenium.get('%s%s' % (self.live_server_url, "/clients/"))
        self.assert_page_title(
            "0 catégorie de client répertorié",
            "0 client répertorié")  # assert page title
        # add some category of client
        category_names = ["restaurant", "association", "particulier"]
        for category_name in category_names:
            self.add_category(category_name)
        categories = CategoryClient.objects.all()
        self.assertEqual(len(categories), 3)  # assert category saved in db
        self.assert_category_range_in_table(
            category_names)  # assert categories is ordered in table
