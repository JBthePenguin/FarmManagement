from product_app.tests import Browser
from client_app.models import CategoryClient, Client
from time import sleep


def add_category_client(browser, name):
    """ add a client's category with the form """
    browser.selenium.find_element_by_link_text(
        "Ajouter une catégorie").click()
    browser.wait_page_loaded("Ajouter une catégorie de client")
    browser.selenium.find_element_by_id("id_name").send_keys(name)
    browser.selenium.find_element_by_class_name("btn-success").click()
    browser.wait_page_loaded("Clients")


def add_client(browser, name, category):
    """ add a client with the form """
    browser.selenium.find_element_by_link_text(
        "Ajouter un client").click()
    browser.wait_page_loaded("Ajouter un client")
    browser.selenium.find_element_by_xpath(
        "//select[@name='category']/option[text()='" + category + "']"
    ).click()
    browser.selenium.find_element_by_id("id_name").send_keys(name)
    browser.selenium.find_element_by_class_name("btn-success").click()
    browser.wait_page_loaded("Clients")


class ClientTests(Browser):
    """ Tests for browsing in Client app
    - add, update and delete category and client """

    def update_category(self, line, old_name, new_name):
        """ update a category with the form """
        line.find_element_by_link_text("modifier").click()
        self.wait_page_loaded("Modifier une catégorie de client")
        input_name = self.selenium.find_element_by_id("id_name")
        self.assertEqual(
            input_name.get_attribute('value'),
            old_name)  # assert category name value in form
        input_name.clear()
        self.selenium.find_element_by_id("id_name").send_keys(new_name)
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

    def get_line_category(self, category):
        """ return the line of the category in the table """
        table = self.selenium.find_element_by_xpath("//table[1]")
        body_table = table.find_element_by_tag_name('tbody')
        lines = body_table.find_elements_by_tag_name("tr")
        for line in lines:
            line_values = line.find_elements_by_tag_name("td")
            if line_values[0].text == category.name:
                return line

    def assert_client_in_table(self, categories):
        """ assert if client is displayed in table of his category"""
        categories.sort()
        page_titles = self.selenium.find_elements_by_tag_name("h5")
        self.assertEqual(len(page_titles), 2 + len(categories))
        tables = self.selenium.find_elements_by_tag_name("table")
        i = 1
        for category in categories:
            # assert subtitle client's category
            self.assertEqual(page_titles[i + 1].text, category)
            # assert clients in this category
            body_table = tables[i].find_element_by_tag_name('tbody')
            lines = body_table.find_elements_by_tag_name("tr")
            for line in lines:
                line_values = line.find_elements_by_tag_name("td")
                client = Client.objects.get(name=line_values[0].text)
                self.assertEqual(category, client.category.name)
            i += 1

    def get_line_client(self, client):
        """ return the line of the client in the table """
        tables = self.selenium.find_elements_by_tag_name("table")
        for table in tables[1:]:
            body_table = table.find_element_by_tag_name('tbody')
            lines = body_table.find_elements_by_tag_name("tr")
            for line in lines:
                line_values = line.find_elements_by_tag_name("td")
                if line_values[0].text == client.name:
                    return line

    def update_client(self, line, client, new_name, new_category):
        """ update a category with the form """
        line.find_element_by_link_text("modifier").click()
        self.wait_page_loaded("Modifier un client")
        input_name = self.selenium.find_element_by_id("id_name")
        self.assertEqual(
            input_name.get_attribute('value'),
            client.name)  # assert client name value in form
        input_category = self.selenium.find_element_by_xpath(
            "//select[@name='category']/option[@selected]")
        self.assertEqual(
            input_category.text,
            client.category.name)  # assert client category value in form
        self.selenium.find_element_by_xpath(
            "//select[@name='category']/option[text()='" + new_category + "']"
        ).click()
        input_name.clear()
        self.selenium.find_element_by_id("id_name").send_keys(new_name)
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Clients")

    def test_client_page(self):
        """ test browsing in client template """
        self.selenium.get('%s%s' % (self.live_server_url, "/clients/"))
        self.assert_page_title(
            "0 catégorie de client répertoriée",
            "0 client répertorié")  # assert page title
        # add some category of client
        category_names = ["restaurant", "association", "particulier"]
        for category_name in category_names:
            add_category_client(self, category_name)
        categories = CategoryClient.objects.all()
        self.assertEqual(len(categories), 3)  # assert category saved in db
        self.assert_category_range_in_table(
            category_names)  # assert categories is ordered in table
        # update category
        category = CategoryClient.objects.get(name="restaurant")
        category_line = self.get_line_category(category)
        self.update_category(category_line, "restaurant", "coopérative")
        category_names = ["coopérative", "association", "particulier"]
        self.assert_category_range_in_table(
            category_names)  # assert category is updated and ordered in table
        # delete category
        categories = CategoryClient.objects.all()
        self.assertEqual(
            len(categories), 3)  # number of categories before delete
        category = CategoryClient.objects.get(name="association")
        category_line = self.get_line_category(category)
        category_line.find_element_by_tag_name("button").click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        sleep(2)
        categories = CategoryClient.objects.all()
        self.assertEqual(
            len(categories), 2)  # number of categories after delete
        category_names = []
        for category in categories:
            category_names.append(category.name)
        self.assertNotIn(
            "association", category_names)  # assert category deleted in db
        # add some clients
        add_category_client(self, "association")
        category_names.append("association")
        clients_dict = {
            "asso test": "association",
            "coop test": "coopérative",
            "part test": "particulier",
        }
        for name, category in clients_dict.items():
            add_client(self, name, category)
        clients = Client.objects.all()
        self.assertEqual(len(clients), 3)  # assert client saved in db
        self.assert_client_in_table(
            category_names)  # assert clients is ordered by category table
        # update client
        client = Client.objects.get(name="coop test")
        client_line = self.get_line_client(client)
        self.update_client(client_line, client, "new name", "association")
        client = Client.objects.get(name="new name")
        self.assertEqual(
            client.category.name,
            "association")  # assert client is updated in db
        client_line = self.get_line_client(client)
        line_values = client_line.find_elements_by_tag_name("td")
        self.assertEqual(
            line_values[0].text,
            "new name")  # assert client is updated in table
        self.assert_client_in_table(
            category_names)  # assert client updated is ordered in table
        # delete client
        clients = Client.objects.all()
        self.assertEqual(
            len(clients), 3)  # number of clients before delete
        client = Client.objects.get(name="part test")
        client_line = self.get_line_client(client)
        client_line.find_element_by_tag_name("button").click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        sleep(2)
        clients = Client.objects.all()
        self.assertEqual(
            len(categories), 2)  # number of clients after delete
        client_names = []
        for client in clients:
            client_names.append(client.name)
        self.assertNotIn(
            "part test", client_names)  # assert client deleted in db
        # delete all clients
        for client in clients:
            client.delete()
        clients = Client.objects.all()
        self.assertEqual(len(clients), 0)  # assert no client in db
        # delete all categories
        categories = CategoryClient.objects.all()
        for category in categories:
            category.delete()
        categories = CategoryClient.objects.all()
        self.assertEqual(len(categories), 0)  # assert no category in db
