// Confirm delete order before Ajax request to do it
function DeleteOrder(order_id, order_date, csrf_token) {
    r = confirm("Confirmer la suppression de la commande crée le " + order_date)
    if (r == true) {
        $.post({
            url: '',
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
            url: '',
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
