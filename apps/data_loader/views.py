from django.shortcuts import render


def data_center(request):
    return render(request, 'data_center.html')
