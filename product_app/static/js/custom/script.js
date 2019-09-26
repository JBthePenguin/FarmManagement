// Confirm delete before Ajax request to do it
function DeleteProduct(product_id, product_name, csrf_token) {
    r = confirm("Confirmer la suppression de " + product_name)
    if (r == true) {
        $.post({
            url: '/produits/',
            data: {
                'action': 'delete',
                'product_id': product_id,
                'csrfmiddlewaretoken': csrf_token
            },
        });
    }
}