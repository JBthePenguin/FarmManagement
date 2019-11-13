// Confirm delete category cost before Ajax request to do it
function DeleteCategoryCost(category_id, category_name, csrf_token) {
    r = confirm("Confirmer la suppression de la catégorie " + category_name)
    if (r == true) {
        $.post({
            url: '/couts/',
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


// Confirm delete cost before Ajax request to do it
function DeleteCost(cost_id, cost_name, csrf_token) {
    r = confirm("Confirmer la suppression de la catégorie " + cost_name)
    if (r == true) {
        $.post({
            url: '/couts/',
            data: {
                'action': 'delete cost',
                'cost_id': cost_id,
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