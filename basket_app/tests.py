from product_app.tests import Browser, delete_all_products
from basket_app.models import BasketCategory, Basket, BasketProduct
from client_app.tests import (
    add_category_client, delete_all_categories_and_clients)
from price_app.tests import add_product_with_price
from product_app.models import Product
from time import sleep


def add_category_basket(browser, name):
    """ add a basket's category with the form """
    browser.selenium.find_element_by_link_text(
        "Ajouter une catégorie").click()
    browser.wait_page_loaded("Ajouter une catégorie de paniers")
    browser.selenium.find_element_by_id("id_name").send_keys(name)
    browser.selenium.find_element_by_class_name("btn-success").click()
    browser.wait_page_loaded("Paniers")


def create_basket(browser, basket):
    """ create a basket with the form """
    browser.selenium.find_element_by_link_text(
        "Créer un nouveau panier").click()
    browser.wait_page_loaded("Créer un panier")
    basket_number = Basket.objects.all().count() + 1
    title = browser.selenium.find_element_by_tag_name("h5")
    browser.assertEqual(
        title.text,
        "Panier numéro " + str(basket_number))  # assert basket's number
    browser.selenium.find_element_by_xpath(
        "//select[@name='category']/option[text()='" + basket[0] + "']"
    ).click()
    inputs = browser.selenium.find_elements_by_tag_name("input")
    i = 1
    for input_tag in inputs[1:]:
        input_tag.send_keys(basket[i])
        i += 1
    browser.selenium.find_element_by_class_name("btn-success").click()
    browser.wait_page_loaded("Paniers")


def delete_all_categories_and_baskets(browser):
    """ delete all baskets and categories in db """
    # delete all baskets
    baskets = Basket.objects.all()
    for basket in baskets:
        basket.delete()
    baskets = Basket.objects.all()
    browser.assertEqual(len(baskets), 0)  # assert no basket in db
    # delete all categories
    categories = BasketCategory.objects.all()
    for category in categories:
        category.delete()
    categories = BasketCategory.objects.all()
    browser.assertEqual(len(categories), 0)  # assert no category in db


class BasketTests(Browser):
    """ Tests for browsing in Basket app
    - create, update and delete basket """

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

    def assert_basket_table(self, categories):
        """ assert if basket's table is displayed by category"""
        categories.sort()
        category_divs = self.selenium.find_elements_by_class_name(
            "tables-by-category")
        i = 0
        for category_div in category_divs:
            # assert subtitle basket's category
            title_category = category_div.find_element_by_tag_name("h5")
            self.assertEqual(title_category.text, categories[i])
            # assert title (number) of basket in this category
            titles_basket = category_div.find_elements_by_tag_name("strong")
            baskets = Basket.objects.filter(
                category__name=categories[i]).order_by("number")
            i_second = 0
            for title_basket in titles_basket:
                self.assertEqual(
                    title_basket.text,
                    "panier numéro " + str(baskets[i_second].number) + ":")
                i_second += 1
            i += 1

    def assert_composition(self, compositions, prices, total_prices):
        """ assert the composition of a basket """
        tables = self.selenium.find_elements_by_tag_name("table")
        i = 1
        for composition in compositions:
            body_table = tables[i].find_element_by_tag_name('tbody')
            lines = body_table.find_elements_by_tag_name("tr")
            for line in lines[:-1]:
                # assert quantity for each product
                line_values = line.find_elements_by_tag_name("td")
                product = Product.objects.get(name=line_values[0].text)
                self.assertEqual(
                    line_values[1].text,
                    composition[line_values[0].text] + product.unit)
                # assert prices for each client's category
                prices_basket = prices[i - 1]
                i_second = 0
                for line_value in line_values[2:]:
                    prices_product = prices_basket[line_values[0].text]
                    self.assertEqual(
                        line_value.text,
                        prices_product[i_second])
                    i_second += 1
            # assert total price line
            last_line_values = lines[-1].find_elements_by_tag_name("td")
            self.assertEqual("Total:", last_line_values[0].text)
            total_prices_basket = total_prices[i - 1]
            i_second = 0
            for last_line_value in last_line_values[1:]:
                self.assertEqual(
                    last_line_value.text,
                    total_prices_basket[i_second])
                i_second += 1
            i += 1

    def update_basket(self, basket, new_basket):
        """ update a basket with the form """
        self.selenium.find_element_by_xpath(
            "//a[@href='/paniers/numero" + str(basket.number) + "/']"
        ).click()
        self.wait_page_loaded("Modifier un panier")
        input_category = self.selenium.find_element_by_xpath(
            "//select[@name='category']/option[@selected]")
        self.assertEqual(
            input_category.text,
            basket.category.name)  # assert basket category value in form
        self.selenium.find_element_by_xpath(
            "//select[@name='category']/option[text()='" + new_basket[0] + "']"
        ).click()
        composition = BasketProduct.objects.filter(
            basket=basket).order_by("product__name")
        inputs = self.selenium.find_elements_by_tag_name("input")
        i = 0
        for input_tag in inputs[1:]:
            # assert quantity value in form
            self.assertEqual(
                input_tag.get_attribute('value'),
                str(composition[i].quantity_product))
            input_tag.clear()
            input_tag.send_keys(new_basket[i + 1])
            i += 1
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Paniers")

    def test_basket_page(self):
        """ test browsing in basket template """
        self.selenium.get('%s%s' % (self.live_server_url, "/paniers/"))
        self.assert_page_title(
            "0 catégorie de panier répertorié",
            "0 panier répertorié", "")  # assert page title
        # add client's category
        self.selenium.find_element_by_link_text("Clients").click()
        self.wait_page_loaded("Clients")
        category_names = ["restaurant", "association", "particulier"]
        for category_name in category_names:
            add_category_client(self, category_name)
        # add some products
        self.selenium.find_element_by_link_text("Produits").click()
        self.wait_page_loaded("Produits")
        products = [
            ("tomate", "kg", "1,2", "0,45", "2"),
            ("ail", "kg", "2,40", "2,15", "3,05"),
            ("chou", "pièce", "1", "1,5", "2"), ]
        for product in products:
            add_product_with_price(self, category_names, product)
        # add some basket's categories
        self.selenium.find_element_by_link_text("Paniers").click()
        self.wait_page_loaded("Paniers")
        category_names = ["gros", "petit", "moyen"]
        for category_name in category_names:
            add_category_basket(self, category_name)
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
        # create some baskets
        baskets = [
            ("gourmand", "2", "0,5", "3"),
            ("petit", "0,75", "", "1"),
            ("gourmand", "2,5", "1,25", "5"), ]
        for basket in baskets:
            create_basket(self, basket)
        baskets = Basket.objects.all()
        self.assertEqual(len(baskets), 3)  # assert basket saved in db
        compositons = BasketProduct.objects.all()
        self.assertEqual(
            len(compositons), 8)  # assert compositions saved in db
        self.assert_basket_table(
            category_names)  # assert basket's table is ordered by category
        compositions = [
            {"ail": "2 ", "chou": "0,500 ", "tomate": "3 "},
            {"ail": "2,500 ", "chou": "1,250 ", "tomate": "5 "},
            {"ail": "0,750 ", "tomate": "1 "}, ]
        prices = [
            {
                "ail": ("4,80 €", "4,30 €", "6,10 €"),
                "chou": ("0,50 €", "0,75 €", "1,00 €"),
                "tomate": ("3,60 €", "1,35 €", "6,00 €"), },
            {
                "ail": ("6,00 €", "5,38 €", "7,62 €"),
                "chou": ("1,25 €", "1,88 €", "2,50 €"),
                "tomate": ("6,00 €", "2,25 €", "10,00 €")},
            {
                "ail": ("1,80 €", "1,61 €", "2,29 €"),
                "tomate": ("1,20 €", "0,45 €", "2,00 €")}, ]
        total_prices = [
            ("8,90 €", "6,40 €", "13,10 €"),
            ("13,25 €", "9,51 €", "20,12 €"),
            ("3,00 €", "2,06 €", "4,29 €")]
        self.assert_composition(
            compositions, prices, total_prices)  # assert composition in table
        # update basket
        basket = Basket.objects.get(number=1)
        self.update_basket(basket, ("petit", "", "0,75", "2"))
        basket = Basket.objects.get(number=1)
        self.assertEqual(
            basket.category.name,
            "petit")  # assert basket's category updated in db
        new_composition = BasketProduct.objects.filter(
            basket=basket).order_by("product__name")
        i = 0
        for quantity in (0.75, 2):
            self.assertEqual(
                quantity,
                new_composition[i].quantity_product
            )  # assert new composition in db
            i += 1
        self.assert_basket_table(
            category_names
        )  # assert updated basket's table is ordered by category
        compositions = [
            {"ail": "2,500 ", "chou": "1,250 ", "tomate": "5 "},
            {"chou": "0,750 ", "tomate": "2 "},
            {"ail": "0,750 ", "tomate": "1 "}, ]
        prices = [
            {
                "ail": ("6,00 €", "5,38 €", "7,62 €"),
                "chou": ("1,25 €", "1,88 €", "2,50 €"),
                "tomate": ("6,00 €", "2,25 €", "10,00 €"), },
            {
                "chou": ("0,75 €", "1,12 €", "1,50 €"),
                "tomate": ("2,40 €", "0,90 €", "4,00 €")},
            {
                "ail": ("1,80 €", "1,61 €", "2,29 €"),
                "tomate": ("1,20 €", "0,45 €", "2,00 €")}, ]
        total_prices = [
            ("13,25 €", "9,51 €", "20,12 €"),
            ("3,15 €", "2,02 €", "5,50 €"),
            ("3,00 €", "2,06 €", "4,29 €")]
        self.assert_composition(
            compositions, prices, total_prices)  # assert new compo in table
        # delete basket
        baskets = Basket.objects.all()
        self.assertEqual(
            len(baskets), 3)  # number of baskets before delete
        category_div = self.selenium.find_element_by_class_name(
            "tables-by-category")
        category_div.find_element_by_tag_name("button").click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        sleep(2)
        baskets = Basket.objects.all()
        self.assertEqual(
            len(baskets), 2)  # number of baskets after delete
        # assert basket's number in db
        basket_numbers = []
        for basket in baskets:
            basket_numbers.append(basket.number)
        self.assertIn(1, basket_numbers)
        self.assertIn(2, basket_numbers)
        self.assertNotIn(3, basket_numbers)
        # delete all
        delete_all_categories_and_baskets(self)
        delete_all_products(self)
        delete_all_categories_and_clients(self)
