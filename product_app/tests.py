from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from product_app.models import Product
from time import sleep


class Browser(StaticLiveServerTestCase):
    """ Browser selenium for test"""
    # fixtures = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def wait_page_loaded(self, title_text):
        """ wait page is loaded to continue test """
        wait = WebDriverWait(self.selenium, 10)
        wait.until(EC.title_contains(title_text))

    def assert_page_title(self, title_one, title_two):
        """ assert for page titles <h5> """
        page_title = self.selenium.find_elements_by_tag_name("h5")
        self.assertIn(title_one, page_title[0].text)
        if title_two != "":
            self.assertIn(title_two, page_title[1].text)


class BaseTests(Browser):
    """ Tests for browsing in base template"""

    def test_navbar(self):
        """ test for nav bar"""
        self.selenium.get(self.live_server_url)
        # title
        page_title = self.selenium.title
        self.assertEqual(page_title, "Ma ferme")  # name
        # nav links
        nav_links = self.selenium.find_elements_by_css_selector(
            ".nav-link"
        )
        self.assertEqual(len(nav_links), 4)  # assert number of links

        def assert_link_url(link_text, link_url):
            """ assert if a click on the link go to the correct url """
            link = self.selenium.find_element_by_link_text(link_text)
            link.click()
            self.wait_page_loaded(link_text)
            self.assertEqual(
                self.selenium.current_url[-len(link_url):],
                link_url)

        assert_link_url('Clients', '/clients/')  # assert client link
        assert_link_url('Produits', '/produits/')  # assert product link
        assert_link_url('Paniers', '/paniers/')  # assert basket link
        assert_link_url('Commandes', '/commandes/')  # assert order link


class IndexTests(Browser):
    """ Tests for browsing in index template """

    def test_index(self):
        """ test browsing in index template """
        self.selenium.get('%s%s' % (self.live_server_url, "/"))
        self.assert_page_title("Hello world!", "")  # assert page title


def add_product(browser, name, unit):
    """ add a product with the form """
    browser.selenium.find_element_by_link_text("Ajouter un produit").click()
    browser.wait_page_loaded("Ajouter produit")
    browser.selenium.find_element_by_id("id_name").send_keys(name)
    browser.selenium.find_element_by_id("id_unit").send_keys(unit)
    browser.selenium.find_element_by_class_name("btn-success").click()
    browser.wait_page_loaded("Produits")


class ProductTests(Browser):
    """ Tests for browsing in product app
    - add, update and delete product """

    def update_product(self, line, old_name, old_unit, new_name, new_unit):
        """ update a product with the form """
        line.find_element_by_link_text("modifier").click()
        self.wait_page_loaded("Modifier produit")
        input_name = self.selenium.find_element_by_id("id_name")
        self.assertEqual(
            input_name.get_attribute('value'),
            old_name)  # assert product name value in form
        input_name.clear()
        input_unit = self.selenium.find_element_by_id("id_unit")
        self.assertEqual(
            input_unit.get_attribute('value'),
            old_unit)  # assert product unit value in form
        input_unit.clear()
        self.selenium.find_element_by_id("id_name").send_keys(new_name)
        self.selenium.find_element_by_id("id_unit").send_keys(new_unit)
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Produits")

    def assert_product_in_table(self, product):
        """ assert if a saved product in db is in table """
        table = self.selenium.find_element_by_xpath("//table[1]")
        body_table = table.find_element_by_tag_name('tbody')
        lines = body_table.find_elements_by_tag_name("tr")
        for line in lines:
            line_values = line.find_elements_by_tag_name("td")
            if line_values[0].text == product.name:
                self.assertEqual(
                    line_values[1].text,
                    product.unit)  # assert product is in table
                product_line = line
        return product_line

    def test_product_page(self):
        """ test browsing in product template """
        self.selenium.get('%s%s' % (self.live_server_url, "/produits/"))
        self.assert_page_title("0 produit répertorié", "")  # assert page title
        # add some products
        products = {
            "tomate": "kg",
            "ail": "pièce",
            "chou": "kg",
            "oignon": "lot"}
        for name, unit in products.items():
            add_product(self, name, unit)
            new_product = Product.objects.get(name=name)
            self.assertEqual(
                new_product.unit, unit)  # assert product saved in db
            product_line = self.assert_product_in_table(
                new_product)  # assert product is in table
        # update product
        product = Product.objects.get(name="tomate")
        product_line = self.assert_product_in_table(product)
        self.update_product(product_line, "tomate", "kg", "tomate", "pièce")
        updated_product = Product.objects.get(name="tomate")
        self.assertEqual(
            updated_product.unit, "pièce")  # assert product updated in db
        product_line = self.assert_product_in_table(
            updated_product)  # assert product is updated in table
        # delete product
        products = Product.objects.all()
        self.assertEqual(len(products), 4)  # number of products before delete
        product_line.find_element_by_tag_name("button").click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        sleep(2)
        products = Product.objects.all()
        self.assertEqual(len(products), 3)  # number of products after delete
        product_names = []
        for product in products:
            product_names.append(product.name)
        self.assertNotIn(
            "tomate", product_names)  # assert product deleted in db
        # delete all products
        for product in products:
            product.delete()
        products = Product.objects.all()
        self.assertEqual(len(products), 0)  # assert no product in db
