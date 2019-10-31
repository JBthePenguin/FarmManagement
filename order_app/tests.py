from product_app.tests import Browser, delete_all_products
from client_app.tests import (
    add_category_client, add_client, delete_all_categories_and_clients)
from price_app.tests import add_product_with_price
from basket_app.tests import (
    add_category_basket, create_basket, delete_all_categories_and_baskets)
from basket_app.models import BasketCategory
from order_app.models import Order, OrderBasket


def create_order(browser, order, categories_basket):
    """ create a basket with the form """
    browser.selenium.find_element_by_link_text(
        "Créer une nouvelle commande").click()
    browser.wait_page_loaded("Créer une commande")
    browser.selenium.find_element_by_xpath(
        "//select[@name='client']/option[text()='" + order[0] + "']"
    ).click()
    inputs = browser.selenium.find_elements_by_tag_name("input")
    i = 1
    for input_tag in inputs[1:]:
        composition = order[i]
        input_tag.send_keys(composition[0])
        if composition[0] != "":
            browser.selenium.find_element_by_xpath(
                "".join([
                    "//select[@name='", str(categories_basket[i - 1].id),
                    "']/option[text()='", composition[1], "']"])).click()
        i += 1
    browser.selenium.find_element_by_class_name("btn-success").click()
    browser.wait_page_loaded("Commandes")


def delete_all_orders(browser):
    """ delete all orders in db """
    orders = Order.objects.all()
    for order in orders:
        order.delete()
    orders = Order.objects.all()
    browser.assertEqual(len(orders), 0)  # assert no order in db


class BasketTests(Browser):
    """ Tests for browsing in order app
    - create, update, delete and cancel order """

    def test_order_page(self):
        """ test browsing in order template """
        self.selenium.get('%s%s' % (self.live_server_url, "/commandes/"))
        self.assert_page_title(
            "0 commande en préparation",
            "0 commande en cours de livraison",
            "0 commande livrée")  # assert page title
        # add client's category
        self.selenium.find_element_by_link_text("Clients").click()
        self.wait_page_loaded("Clients")
        category_client_names = ["restaurant", "association", "particulier"]
        for category_name in category_client_names:
            add_category_client(self, category_name)
        # add some clients
        clients_dict = {
            "asso test": "association",
            "rest test": "restaurant",
            "part test": "particulier",
        }
        for name, category in clients_dict.items():
            add_client(self, name, category)
        # add some products
        self.selenium.find_element_by_link_text("Produits").click()
        self.wait_page_loaded("Produits")
        products = [
            ("tomate", "kg", "1,2", "0,45", "2"),
            ("ail", "kg", "2,40", "2,15", "3,05"),
            ("chou", "pièce", "1", "1,5", "2"), ]
        for product in products:
            add_product_with_price(self, category_client_names, product)
        # add some basket's categories
        self.selenium.find_element_by_link_text("Paniers").click()
        self.wait_page_loaded("Paniers")
        category_basket_names = ["gourmand", "petit", "moyen"]
        for category_name in category_basket_names:
            add_category_basket(self, category_name)
        categories_basket = BasketCategory.objects.all().order_by(
            "name")
        # create some baskets
        baskets = [
            ("gourmand", "2", "0,5", "3"),
            ("petit", "0,75", "", "1"),
            ("gourmand", "2,5", "1,25", "5"),
            ("moyen", "1,5", "1", "4"), ]
        for basket in baskets:
            create_basket(self, basket)
        # create some orders
        self.selenium.find_element_by_link_text("Commandes").click()
        self.wait_page_loaded("Commandes")
        orders = [
            ("asso test", ("2", "1"), ("", ""), ("3", "2")),
            ("rest test", ("1", "3"), ("6", "4"), ("5", "2")),
            ("part test", ("", ""), ("", ""), ("2", "2")), ]
        for order in orders:
            create_order(self, order, categories_basket)
        orders_in_db = Order.objects.all()
        self.assertEqual(
            len(orders_in_db), 3)  # assert orders saved in db
        compositions_in_db = OrderBasket.objects.all()
        self.assertEqual(
            len(compositions_in_db), 6)  # assert compositions saved in db
        # delete all
        delete_all_orders(self)
        delete_all_categories_and_baskets(self)
        delete_all_categories_and_clients(self)
        delete_all_products(self)
