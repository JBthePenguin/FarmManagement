from product_app.tests import Browser
from basket_app.models import BasketCategory
from time import sleep


class BasketTests(Browser):
    """ Tests for browsing in Basket app
    - create, update and delete basket """

    def add_client_category(self, name):
        """ add a client's category with the form """
        self.selenium.find_element_by_link_text(
            "Ajouter une catégorie").click()
        self.wait_page_loaded("Ajouter une catégorie de client")
        self.selenium.find_element_by_id("id_name").send_keys(name)
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Clients")

    def add_client(self, name, category):
        """ add a client with the form """
        self.selenium.find_element_by_link_text(
            "Ajouter un client").click()
        self.wait_page_loaded("Ajouter un client")
        self.selenium.find_element_by_xpath(
            "//select[@name='category']/option[text()='" + category + "']"
        ).click()
        self.selenium.find_element_by_id("id_name").send_keys(name)
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Clients")

    def add_product_with_price(self, categories, product):
        """ add a product with price with the form """
        self.selenium.find_element_by_link_text("Ajouter un produit").click()
        self.wait_page_loaded("Ajouter produit")
        inputs = self.selenium.find_elements_by_tag_name("input")
        i = 0
        for input_tag in inputs[1:]:
            input_tag.send_keys(product[i])
            i += 1
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Produits")

    def add_category(self, name):
        """ add a basket's category with the form """
        self.selenium.find_element_by_link_text(
            "Ajouter une catégorie").click()
        self.wait_page_loaded("Ajouter une catégorie de paniers")
        self.selenium.find_element_by_id("id_name").send_keys(name)
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Paniers")

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

    def update_category(self, line, old_name, new_name):
        """ update a category with the form """
        line.find_element_by_link_text("modifier").click()
        self.wait_page_loaded("Modifier une catégorie de panier")
        input_name = self.selenium.find_element_by_id("id_name")
        self.assertEqual(
            input_name.get_attribute('value'),
            old_name)  # assert category name value in form
        input_name.clear()
        self.selenium.find_element_by_id("id_name").send_keys(new_name)
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Paniers")

    def test_basket_page(self):
        """ test browsing in basket template """
        self.selenium.get('%s%s' % (self.live_server_url, "/paniers/"))
        self.assert_page_title(
            "0 catégorie de panier répertorié",
            "0 panier répertorié")  # assert page title
        # add client's category
        self.selenium.find_element_by_link_text("Clients").click()
        self.wait_page_loaded("Clients")
        category_names = ["restaurant", "association", "particulier"]
        for category_name in category_names:
            self.add_client_category(category_name)
        # add some clients
        clients_dict = {
            "asso test": "association",
            "rest test": "restaurant",
            "part test": "particulier",
        }
        for name, category in clients_dict.items():
            self.add_client(name, category)
        # add some products
        self.selenium.find_element_by_link_text("Produits").click()
        self.wait_page_loaded("Produits")
        products = [
            ("tomate", "kg", "1,2", "0,45", "2"),
            ("ail", "kg", "2,40", "2,15", "3,05"),
            ("chou", "pièce", "1", "1,5", "2"), ]
        for product in products:
            self.add_product_with_price(category_names, product)
        # add some basket's categories
        self.selenium.find_element_by_link_text("Paniers").click()
        self.wait_page_loaded("Paniers")
        category_names = ["gros", "petit", "moyen"]
        for category_name in category_names:
            self.add_category(category_name)
        categories_basket = BasketCategory.objects.all()
        self.assertEqual(
            len(categories_basket), 3)  # assert category saved in db
        self.assert_category_range_in_table(
            category_names)  # assert categories is ordered in table
        # update category
        category = BasketCategory.objects.get(name="gros")
        category_line = self.get_line_category(category)
        self.update_category(category_line, "gros", "gourmand")
        category_names = ["gourmand", "petit", "moyen"]
        self.assert_category_range_in_table(
            category_names)  # assert category is updated and ordered in table
        # delete category
        categories = BasketCategory.objects.all()
        self.assertEqual(
            len(categories), 3)  # number of categories before delete
        category = BasketCategory.objects.get(name="moyen")
        category_line = self.get_line_category(category)
        category_line.find_element_by_tag_name("button").click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        sleep(2)
        categories = BasketCategory.objects.all()
        self.assertEqual(
            len(categories), 2)  # number of categories after delete
        category_names = []
        for category in categories:
            category_names.append(category.name)
        self.assertNotIn(
            "moyen", category_names)  # assert category deleted in db
        # add some baskets