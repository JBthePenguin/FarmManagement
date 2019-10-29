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
