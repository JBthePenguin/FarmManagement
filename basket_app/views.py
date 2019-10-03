from django.shortcuts import render


def basket(request):
    """ basket view """
    context = {
        "basket": "active"
    }
    return render(request, 'basket_app/basket.html', context)
