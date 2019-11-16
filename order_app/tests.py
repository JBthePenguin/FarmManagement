from product_app.tests import Browser, delete_all_products
from client_app.tests import (
    add_category_client, add_client, delete_all_categories_and_clients)
from price_app.tests import add_product_with_price
from basket_app.tests import (
    add_category_basket, create_basket, delete_all_categories_and_baskets)
from basket_app.models import BasketCategory, Basket, BasketProduct
from order_app.models import Order, OrderBasket
from client_app.models import Client
from price_app.models import Price
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

    def assert_table(self, table_indice, orders):
        """ assert table of an order in preparation """
        tables = self.selenium.find_elements_by_tag_name("table")
        body_table = tables[table_indice].find_element_by_tag_name('tbody')
        lines = body_table.find_elements_by_tag_name("tr")
        i = 0
        for line in lines:
            # assert client and compositions for each order
            line_values = line.find_elements_by_tag_name("td")
            if orders[i][0] != "":
                self.assertEqual(
                    line_values[1].text, orders[i][0])
                composition_list = line_values[2].find_element_by_tag_name(
                    "ul")
                list_elements = composition_list.find_elements_by_tag_name(
                    "li")
                i_second = 0
                for list_element in list_elements:
                    self.assertEqual(
                        list_element.find_element_by_tag_name("strong").text,
                        orders[i][1][i_second][1])
                    badges = list_element.find_elements_by_tag_name("span")
                    self.assertEqual(
                        badges[0].text,
                        orders[i][1][i_second][0])
                    if table_indice == 0:
                        self.assertEqual(
                            badges[1].text,
                            orders[i][1][i_second][2])
                    i_second += 1
            else:
                composition_list = line_values[1].find_element_by_tag_name(
                    "ul")
                list_elements = composition_list.find_elements_by_tag_name(
                    "li")
                i_second = 0
                for list_element in list_elements:
                    self.assertEqual(
                        list_element.find_element_by_tag_name("strong").text,
                        orders[i][1][i_second][1])
                    badges = list_element.find_elements_by_tag_name("span")
                    self.assertEqual(
                        badges[0].text,
                        orders[i][1][i_second][0])
                    if (table_indice == 0) and (len(badges) == 2):
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
        for input_tag in inputs[1:-1]:
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

    def assert_table_basket_header(self, table):
        """ assert titles in the header of basket's table in validate order """
        thead_table = table.find_element_by_tag_name('thead')
        thead_lines = thead_table.find_elements_by_tag_name("tr")
        first_line_titles = ["Produit", "Quantité", "Prix"]
        second_line_titles = [
            "par panier", "totale", "unitaire", "par panier",
            "pour la commande"]
        first_thead_titles = thead_lines[0].find_elements_by_tag_name("th")
        i = 0
        for first_thead_title in first_thead_titles:
            self.assertEqual(first_thead_title.text, first_line_titles[i])
            i += 1
        second_thead_titles = thead_lines[1].find_elements_by_tag_name("th")
        i = 0
        for second_thead_title in second_thead_titles:
            self.assertEqual(second_thead_title.text, second_line_titles[i])
            i += 1

    def assert_validate_page(self, order):
        """ assert the validate page content (tables, prices,...) """
        titles = self.selenium.find_elements_by_tag_name("h5")
        self.assertEqual(
            titles[1].text,
            "Client: " + order[0])  # assert client
        client = Client.objects.get(name=order[0])
        tables = self.selenium.find_elements_by_tag_name("table")
        self.assertEqual(
            len(tables),
            len(order[1]))  # assert number of tables
        total_order_price = 0
        i = 0
        for table in tables:
            self.assert_table_basket_header(table)  # assert header of tables
            basket = Basket.objects.get(number=order[1][i][2])
            composition = BasketProduct.objects.filter(basket=basket).order_by(
                "product__name")
            body_table = table.find_element_by_tag_name('tbody')
            lines = body_table.find_elements_by_tag_name("tr")
            total_price = 0
            i_second = 0
            for line in lines[:-1]:
                # assert composition for each basket
                line_values = line.find_elements_by_tag_name("td")
                component = composition[i_second]
                self.assertEqual(
                    line_values[0].text,
                    component.product.name)  # assert product name
                # assert product quantity
                if str(component.quantity_product)[-2:] == ".0":
                    string_quantity = str(component.quantity_product)[:-2]
                else:
                    string_quantity = str(format(
                        component.quantity_product, ".3f")).replace(
                            ".", ",")
                self.assertEqual(
                    line_values[1].text,
                    "".join([
                        string_quantity, " ",
                        component.product.unit]))   # by basket
                if (
                    str(component.quantity_product * int(order[1][i][0]))[-2:]
                ) == ".0":
                    string_quantity = str(
                        component.quantity_product * int(order[1][i][0]))[:-2]
                else:
                    string_quantity = str(format(
                        component.quantity_product * int(
                            order[1][i][0]), ".3f")
                    ).replace(".", ",")
                self.assertEqual(
                    line_values[2].text,
                    "".join([
                        string_quantity, " ",
                        component.product.unit]))   # by order
                # assert prices
                unit_price = Price.objects.get(
                    product=component.product, category_client=client.category)
                self.assertEqual(
                    line_values[3].text,
                    str(unit_price.value))  # by unit
                self.assertEqual(
                    line_values[4].text,
                    str(
                        unit_price.value * component.quantity_product
                    ))  # by basket
                self.assertEqual(
                    line_values[5].text,
                    str(
                        unit_price.value * component.quantity_product * int(
                            order[1][i][0])
                    ))  # by order
                total_price += round(
                    unit_price.value * component.quantity_product, 2)
                i_second += 1
            # assert total price line
            last_line_values = lines[-1].find_elements_by_tag_name("td")
            self.assertEqual("Total:", last_line_values[0].text)
            self.assertEqual(
                last_line_values[1].text,
                str(total_price))
            self.assertEqual(
                last_line_values[2].text,
                str(total_price * int(order[1][i][0])))
            total_order_price += total_price * int(order[1][i][0])
            i += 1
        # assert total order price
        self.assertEqual(
            titles[-1].text,
            "".join([
                "Prix de la commande: ", str(total_order_price)]))

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
        self.assert_table(
            0, orders_created)  # assert orders in table
        # orders by client
        self.selenium.find_element_by_link_text("Clients").click()
        self.wait_page_loaded("Clients")
        self.selenium.find_elements_by_link_text("commandes")[2].click()
        self.wait_page_loaded("Commandes - " + "rest test")
        client_orders = [
            ("", [
                ("1", "gourmand", "3"),
                ("6", "moyen", "4"),
                ("5", "petit", "2"), ]),
            ("", [
                ("2", "gourmand", "1"),
                ("3", "petit", "2"), ]), ]
        self.assert_table(
            0, client_orders)  # assert orders in table
        # update created order
        self.selenium.find_element_by_link_text("Commandes").click()
        self.wait_page_loaded("Commandes")
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
        self.assert_table(
            0, orders_updated)  # assert orders updated in table
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
        # validate an order
        validate_buttons = self.selenium.find_elements_by_link_text(
            "Voir et valider")
        validate_buttons[1].click()
        self.wait_page_loaded("Valider une commande")
        self.assert_validate_page(("rest test", [
            ("1", "gourmand", "3"),
            ("6", "moyen", "4"),
            ("5", "petit", "2"), ]))  # assert display on validate page
        self.selenium.find_element_by_tag_name(
            "form").find_element_by_tag_name("button").click()
        self.wait_page_loaded("Commandes")
        order_validated = Order.objects.get(client__name="rest test")
        self.assertEqual(
            order_validated.status,
            "en livraison")  # assert status changed in db
        self.assert_table_header(1, [
            "Date de validation", "Client", "Composition", ""])
        self.assert_table(
            0, [("part test", [("2", "petit", "2"), ]), ]
        )  # assert order created in table
        self.assert_table(
            1, [("rest test", [
                ("1", "gourmand"),
                ("6", "moyen"),
                ("5", "petit"), ]), ]
        )  # assert order validated in table
        # cancel order validated
        tables = self.selenium.find_elements_by_tag_name("table")
        body_table = tables[1].find_element_by_tag_name('tbody')
        body_table.find_element_by_tag_name("button").click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        sleep(2)
        orders = Order.objects.all()
        self.assertEqual(
            len(orders), 1)  # number of orders after calcel
        # assert order delivered
        self.selenium.find_element_by_link_text(
            "Voir et valider").click()
        self.wait_page_loaded("Valider une commande")
        self.assert_validate_page(
            ("part test", [("2", "petit", "2"), ])
        )  # assert display on validate page
        self.selenium.find_element_by_tag_name(
            "form").find_element_by_tag_name("button").click()
        self.wait_page_loaded("Commandes")
        order_validated = Order.objects.get(client__name="part test")
        self.assertEqual(
            order_validated.status,
            "en livraison")  # assert status changed in db
        self.selenium.find_element_by_link_text(
            "Voir et valider").click()
        self.wait_page_loaded("Livrer une commande")
        self.assert_validate_page(
            ("part test", [("2", "petit", "2"), ])
        )  # assert display on deliver page
        self.selenium.find_element_by_tag_name(
            "form").find_element_by_tag_name("button").click()
        self.wait_page_loaded("Commandes")
        order_validated = Order.objects.get(client__name="part test")
        self.assertEqual(
            order_validated.status,
            "livrée")  # assert status changed in db
        self.selenium.find_element_by_link_text(
            "Voir").click()
        self.wait_page_loaded("Commande livrée")
        self.assert_validate_page(
            ("part test", [("2", "petit", "2"), ])
        )  # assert display on delivered page
        self.selenium.find_element_by_link_text(
            "Retour").click()
        self.wait_page_loaded("Commandes")
        # orders by client
        self.selenium.find_element_by_link_text("Clients").click()
        self.wait_page_loaded("Clients")
        self.selenium.find_elements_by_link_text("commandes")[1].click()
        self.wait_page_loaded("Commandes - " + "part test")
        client_orders = [
            ("", [("2", "petit", "2"), ]), ]
        self.assert_table(
            0, client_orders)  # assert orders in table
        self.assertEqual(
            self.selenium.find_elements_by_tag_name("h5")[4].text,
            "Gain total: 4,12 € soit 100 % du chiffre d'affaire")
        # assert table summary for client
        table_summary = self.selenium.find_elements_by_tag_name("table")[1]
        # assert titles
        first_line = table_summary.find_elements_by_tag_name("th")
        self.assertEqual(first_line[0].text, "Produit")
        self.assertEqual(first_line[1].text, "Quantité")
        self.assertEqual(first_line[2].text, "Gain")
        self.assertEqual(first_line[3].text, "% du CA")
        # assert lines's values
        body = table_summary.find_element_by_tag_name("tbody")
        lines_body = body.find_elements_by_tag_name("tr")
        values = lines_body[0].find_elements_by_tag_name("td")
        self.assertEqual(values[0].text, "ail")
        self.assertEqual(values[1].text, "1,5 kg\n100 % de la quantité vendue")
        self.assertEqual(values[2].text, "3,22 €")
        self.assertEqual(values[3].text, "78,18 %")
        values = lines_body[1].find_elements_by_tag_name("td")
        self.assertEqual(values[0].text, "tomate")
        self.assertEqual(values[1].text, "2,0 kg\n100 % de la quantité vendue")
        self.assertEqual(values[2].text, "0,90 €")
        self.assertEqual(values[3].text, "21,82 %")
        # delete all
        delete_all_orders(self)
        delete_all_categories_and_baskets(self)
        delete_all_categories_and_clients(self)
        delete_all_products(self)
