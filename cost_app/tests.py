from product_app.tests import Browser
from cost_app.models import CostCategory
from time import sleep


def add_category_cost(browser, category):
    """ add a cost's category with the form """
    browser.selenium.find_elements_by_link_text(
        "Ajouter une catégorie")[category[0]].click()
    browser.wait_page_loaded("Ajouter une catégorie de coût")
    browser.selenium.find_element_by_id("id_name").send_keys(category[1])
    browser.selenium.find_element_by_class_name("btn-success").click()
    browser.wait_page_loaded("Coûts")


class CostTests(Browser):
    """ Tests for browsing in Cost app
    - create, update and delete cost """

    def update_category(self, old_name, new_name):
        """ update a category with the form """
        input_name = self.selenium.find_element_by_id("id_name")
        self.assertEqual(
            input_name.get_attribute('value'),
            old_name)  # assert category name value in form
        input_name.clear()
        self.selenium.find_element_by_id("id_name").send_keys(new_name)
        self.selenium.find_element_by_class_name("btn-success").click()
        self.wait_page_loaded("Coûts")

    def test_cost_page(self):
        """ test browsing in cost template """
        self.selenium.get('%s%s' % (self.live_server_url, "/couts/"))
        self.assert_page_title(
            "Chiffre d'affaire: 0",
            "Coûts en pourcentage du chiffre d'affaire",
            "Coûts par rapport à la quantité de produits"
        )  # assert page title
        # add some category of cost
        categories = [
            (0, "travail au sol"), (1, "irrigation"), (0, "engrais")]
        for category in categories:
            add_category_cost(self, category)
        categories = CostCategory.objects.all().order_by(
            "calcul_mode", 'name')
        self.assertEqual(len(categories), 3)  # assert category saved in db
        categories_in_template = self.selenium.find_elements_by_tag_name(
            "strong")
        i = 0
        for category_in_template in categories_in_template:
            # assert categories is ordered by calcul mode
            self.assertEqual(
                category_in_template.text,
                categories[i].name)
            i += 1
        # update category
        self.selenium.find_elements_by_link_text("modifier")[1].click()
        self.wait_page_loaded("Modifier une catégorie de coût")
        self.update_category("travail au sol", "travail du sol")
        category_names = ["engrais", "travail du sol", "irrigation"]
        categories_in_template = self.selenium.find_elements_by_tag_name(
            "strong")
        i = 0
        for category_in_template in categories_in_template:
            # assert categories updated is ordered by calcul mode
            self.assertEqual(
                category_in_template.text,
                category_names[i])
            i += 1
        # delete category
        categories = CostCategory.objects.all().order_by(
            "calcul_mode", 'name')
        self.assertEqual(
            len(categories), 3)  # number of categories before delete
        self.selenium.find_elements_by_tag_name("button")[1].click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        sleep(2)
        categories = CostCategory.objects.all().order_by(
            "calcul_mode", 'name')
        self.assertEqual(
            len(categories), 2)  # number of categories after delete
        category_names = []
        for category in categories:
            category_names.append(category.name)
        self.assertNotIn(
            "engrais", category_names)  # assert category deleted in db
        category_names = ["travail du sol", "irrigation"]
        categories_in_template = self.selenium.find_elements_by_tag_name(
            "strong")
        i = 0
        for category_in_template in categories_in_template:
            # assert categories updated is ordered by calcul mode
            self.assertEqual(
                category_in_template.text,
                category_names[i])
            i += 1
