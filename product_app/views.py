from django.shortcuts import render


def index(request):
    # index view
    return render(request, 'product_app/index.html')
