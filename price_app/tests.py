from product_app.tests import Browser
from product_app.models import Product
from price_app.models import Price
from client_app.models import CategoryClient
from djmoney.money import Money


class PriceTests(Browser):
    """ Tests for browsing in price app
    - add, update and delete price for product """

    def add_category(self, name):
        """ add a client's category with the form """
        self.selenium.find_element_by_link_text(
            "Ajouter une catégorie").click()
        self.wait_page_loaded("Ajouter une catégorie de client")
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

    def assert_table_header(self, categories):
        """ assert if category's name is displayed
        in the header of product's table """
        table = self.selenium.find_element_by_xpath("//table[1]")
        thread_table = table.find_element_by_tag_name('thead')
        thread_lines = thread_table.find_elements_by_tag_name("tr")
        thread_price_texts = thread_lines[1].find_elements_by_tag_name("td")
        categories.sort()
        i = 0
        for price_text in thread_price_texts:
            self.assertEqual(price_text.text, categories[i])
            i += 1

    def assert_prices_in_table(self, product):
        """ assert if a saved product in db is in table """
        table = self.selenium.find_element_by_xpath("//table[1]")
        body_table = table.find_element_by_tag_name('tbody')
        lines = body_table.find_elements_by_tag_name("tr")
        for line in lines:
            line_values = line.find_elements_by_tag_name("td")
            if line_values[0].text == product[0]:
                i = 2
                for price in product[1:]:
                    self.assertEqual(
                        line_values[i].text,
                        price)  # assert product'prices is in table
                    i += 1
                product_line = line
        return product_line

    def update_price(self, line, old_prices, new_prices):
        """ update prices for a product """
        line.find_element_by_link_text("modifier").click()
        self.wait_page_loaded("Modifier produit")
        inputs = self.selenium.find_elements_by_tag_name("input")
        i = 0
        for input_tag in inputs[3:]:
            self.assertEqual(
                input_tag.get_attribute('value'),
                old_prices[i])  # assert price value in form
            input_tag.clear()
            input_tag.send_keys(new_prices[i])
            i += 1
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Produits")

    def test_price(self):
        """ test browsing for price in product template """
        # add client's category
        self.selenium.get('%s%s' % (self.live_server_url, "/clients/"))
        category_names = ["restaurant", "association", "particulier"]
        for category_name in category_names:
            self.add_category(category_name)
        # add some products with prices
        self.selenium.find_element_by_link_text("Produits").click()
        self.wait_page_loaded("Produits")
        products = [
            ("tomate", "kg", "1,2", "0,45", "2"),
            ("ail", "kg", "2,40", "2,15", "3,05"),
            ("chou", "pièce", "1", "1,5", "2"), ]
        for product in products:
            self.add_product_with_price(category_names, product)
        prices = Price.objects.all()
        self.assertEqual(len(prices), 9)  # assert prices saved in db
        self.assert_table_header(
            category_names)  # assert category's name in product table header
        product_line = self.assert_prices_in_table(
            (
                "tomate",
                "1,20 €",
                "0,45 €",
                "2,00 €"))  # assert price in product's table
        # update price
        self.update_price(
            product_line,
            ("1.20", "0.45", "2.00"),
            ("1", "0,3", "1,75"))
        new_prices = Price.objects.filter(
            product__name="tomate").order_by("category_client__name")
        i = 0
        for price in (1, 0.3, 1.75):
            self.assertEqual(
                Money(price, "EUR"),
                new_prices[i].value)  # assert new prices saved in db
            i += 1
        product_line = self.assert_prices_in_table(
            (
                "tomate",
                "1,00 €",
                "0,30 €",
                "1,75 €"))  # assert  new price in product's table
        # delete price
        self.update_price(
            product_line,
            ("1.00", "0.30", "1.75"),
            ("1", "", ""))
        new_prices = Price.objects.filter(
            product__name="tomate").order_by("category_client__name")
        self.assertEqual(len(new_prices), 1)  # assert prices deleted in db
        product_line = self.assert_prices_in_table(
            (
                "tomate",
                "1,00 €",
                "",
                ""))  # assert prices deleted in product's table
        # delete all products
        products = Product.objects.all()
        for product in products:
            product.delete()
        products = Product.objects.all()
        self.assertEqual(len(products), 0)  # assert no product in db
        # delete all categories
        categories = CategoryClient.objects.all()
        for category in categories:
            category.delete()
        categories = CategoryClient.objects.all()
        self.assertEqual(len(categories), 0)  # assert no category in db
