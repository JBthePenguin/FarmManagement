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
