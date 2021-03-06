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
