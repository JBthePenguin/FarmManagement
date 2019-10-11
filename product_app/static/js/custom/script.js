// Confirm delete product before Ajax request to do it
function DeleteProduct(product_id, product_name, csrf_token) {
    r = confirm("Confirmer la suppression du produit " + product_name)
    if (r == true) {
        $.post({
            url: '/produits/',
            data: {
                'action': 'delete',
                'product_id': product_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (data) {
                if (data != "") {
                    alert(data);
                }
                location.reload();
            },
        });
    }
}

// Confirm delete category client before Ajax request to do it
function DeleteCategory(category_id, category_name, csrf_token) {
    r = confirm("Confirmer la suppression de la catégorie " + category_name)
    if (r == true) {
        $.post({
            url: '/clients/',
            data: {
                'action': 'delete category',
                'category_id': category_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (data) {
                if (data != "") {
                    alert(data);
                }
                location.reload();
            },
        });
    }
}

// Confirm delete client before Ajax request to do it
function DeleteClient(client_id, client_name, csrf_token) {
    r = confirm("Confirmer la suppression du client " + client_name)
    if (r == true) {
        $.post({
            url: '/clients/',
            data: {
                'action': 'delete client',
                'client_id': client_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (data) {
                if (data != "") {
                    alert(data);
                }
                location.reload();
            },
        });
    }
}

// Confirm delete category basket before Ajax request to do it
function DeleteCategoryBasket(category_id, category_name, csrf_token) {
    r = confirm("Confirmer la suppression de la catégorie " + category_name)
    if (r == true) {
        $.post({
            url: '/paniers/',
            data: {
                'action': 'delete category',
                'category_id': category_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (data) {
                if (data != "") {
                    alert(data);
                }
                location.reload();
            },
        });
    }
}


// Confirm delete basket before Ajax request to do it
function DeleteBasket(basket_id, basket_number, csrf_token) {
    r = confirm("Confirmer la suppression du panier numéro " + basket_number)
    if (r == true) {
        $.post({
            url: '/paniers/',
            data: {
                'action': 'delete basket',
                'basket_id': basket_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (data) {
                if (data != "") {
                    alert(data);
                }
                location.reload();
            },
        });
    }
}


// Confirm delete order before Ajax request to do it
function DeleteOrder(order_id, order_date, csrf_token) {
    r = confirm("Confirmer la suppression de la commande crée le " + order_date)
    if (r == true) {
        $.post({
            url: '/commandes/',
            data: {
                'action': 'delete order',
                'order_id': order_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (data) {
                location.reload();
            },
        });
    }
}


// Confirm cancel order before Ajax request to do it
function CancelOrder(order_id, client, order_date, csrf_token) {
    r = confirm("Confirmer l'annulation de la commande pour " + client + " validée le " + order_date)
    if (r == true) {
        $.post({
            url: '/commandes/',
            data: {
                'action': 'cancel order',
                'order_id': order_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (data) {
                location.reload();
            },
        });
    }
}
