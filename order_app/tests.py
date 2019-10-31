from product_app.tests import Browser, delete_all_products
from client_app.tests import (
    add_category_client, add_client, delete_all_categories_and_clients)
from price_app.tests import add_product_with_price
from basket_app.tests import (
    add_category_basket, create_basket, delete_all_categories_and_baskets)
from basket_app.models import BasketCategory
from order_app.models import Order, OrderBasket
from time import sleep


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


class OrderTests(Browser):
    """ Tests for browsing in order app
    - create, update, delete and cancel order """

    def assert_table_header(self, table_indice, titles):
        """ assert titles in the header of order's table """
        tables = self.selenium.find_elements_by_tag_name("table")
        table = tables[table_indice]
        thead_table = table.find_element_by_tag_name('thead')
        thead_line = thead_table.find_element_by_tag_name("tr")
        thead_titles = thead_line.find_elements_by_tag_name("th")
        i = 0
        for thead_title in thead_titles:
            self.assertEqual(thead_title.text, titles[i])
            i += 1

    def assert_table_in_preparation(self, orders):
        """ assert table of an order in preparation """
        tables = self.selenium.find_elements_by_tag_name("table")
        body_table = tables[0].find_element_by_tag_name('tbody')
        lines = body_table.find_elements_by_tag_name("tr")
        i = 0
        for line in lines:
            # assert client and compositions for each order
            line_values = line.find_elements_by_tag_name("td")
            self.assertEqual(
                line_values[1].text, orders[i][0])
            composition_list = line_values[2].find_element_by_tag_name("ul")
            list_elements = composition_list.find_elements_by_tag_name("li")
            i_second = 0
            for list_element in list_elements:
                self.assertEqual(
                    list_element.find_element_by_tag_name("strong").text,
                    orders[i][1][i_second][1])
                badges = list_element.find_elements_by_tag_name("span")
                self.assertEqual(
                    badges[0].text,
                    orders[i][1][i_second][0])
                self.assertEqual(
                    badges[1].text,
                    orders[i][1][i_second][2])
                i_second += 1
            i += 1

    def update_order(self, link, old_order, new_order, categories_basket):
        """ update an order with the form """
        link.click()
        self.wait_page_loaded("Modifier une commande")
        input_client = self.selenium.find_element_by_xpath(
            "//select[@name='client']/option[@selected]")
        self.assertEqual(
            input_client.text,
            old_order[0])  # assert client value in form
        self.selenium.find_element_by_xpath(
            "//select[@name='client']/option[text()='" + new_order[0] + "']"
        ).click()
        inputs = self.selenium.find_elements_by_tag_name("input")
        i = 1
        for input_tag in inputs[1:]:
            # assert quantity and basket number in form
            self.assertEqual(
                input_tag.get_attribute('value'),
                old_order[i][0])
            input_tag.clear()
            input_tag.send_keys(new_order[i][0])
            select_basket = self.selenium.find_element_by_xpath(
                "".join([
                    "//select[@name='", str(categories_basket[i - 1].id),
                    "']/option[@selected]"]))
            self.assertEqual(
                select_basket.text,
                old_order[i][1])
            self.selenium.find_element_by_xpath(
                "".join([
                    "//select[@name='", str(categories_basket[i - 1].id),
                    "']/option[text()='", new_order[i][1], "']"])).click()
            i += 1
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Commandes")

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
            ("rest test", ("2", "1"), ("", ""), ("3", "2")),
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
        self.assert_table_header(0, [
            "Date de création", "Client", "Composition", ""])
        orders_created = [
            ("part test", [("2", "petit", "2"), ]),
            ("rest test", [
                ("1", "gourmand", "3"),
                ("6", "moyen", "4"),
                ("5", "petit", "2"), ]),
            ("rest test", [
                ("2", "gourmand", "1"),
                ("3", "petit", "2"), ]), ]
        self.assert_table_in_preparation(
            orders_created)  # assert orders in table
        # update created order
        update_links = self.selenium.find_elements_by_link_text("modifier")
        self.update_order(
            update_links[2],
            ("rest test", ("2", "1"), ("", "--"), ("3", "2")),
            ("asso test", ("3", "3"), ("2", "4"), ("", "--")),
            categories_basket)
        order_updated_in_db = Order.objects.get(client__name="asso test")
        self.assertEqual(
            order_updated_in_db.client.name,
            "asso test")  # assert client's order updated in db
        new_composition = OrderBasket.objects.filter(
            order=order_updated_in_db).order_by("basket__category__name")
        i = 0
        for quantity in (3, 2):
            self.assertEqual(
                quantity,
                new_composition[i].quantity_basket
            )  # assert new composition in db
            i += 1
        orders_updated = [
            ("part test", [("2", "petit", "2"), ]),
            ("rest test", [
                ("1", "gourmand", "3"),
                ("6", "moyen", "4"),
                ("5", "petit", "2"), ]),
            ("asso test", [
                ("3", "gourmand", "3"),
                ("2", "moyen", "4"), ]), ]
        self.assert_table_in_preparation(
            orders_updated)  # assert orders updated in table
        # delete an order
        orders = Order.objects.all()
        self.assertEqual(
            len(orders), 3)  # number of orders before delete
        tables = self.selenium.find_elements_by_tag_name("table")
        body_table = tables[0].find_element_by_tag_name('tbody')
        delete_buttons = body_table.find_elements_by_tag_name("button")
        delete_buttons[2].click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        sleep(2)
        orders = Order.objects.all()
        self.assertEqual(
            len(orders), 2)  # number of orders after delete
        order_clients = []
        for order in orders:
            order_clients.append(order.client.name)
        self.assertNotIn(
            "asso test", order_clients)  # no order for this client
        # delete all
        delete_all_orders(self)
        delete_all_categories_and_baskets(self)
        delete_all_categories_and_clients(self)
        delete_all_products(self)
