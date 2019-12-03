// Confirm delete product before Ajax request to do it
function DeleteProduct(product_id, product_name, csrf_token) {
    r = confirm("Confirmer la suppression du produit " + product_name)
    if (r == true) {
        $.post({
            url: '',
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
