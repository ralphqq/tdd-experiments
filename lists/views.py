from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    parent_list = List.objects.create()
    Item.objects.create(
        text=request.POST['item_text'],
        parent_list=parent_list
    )
    return redirect(f'/lists/{parent_list.id}/')



def view_list(request, list_id):
    this_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'parent_list': this_list})


def add_item(request, list_id):
    this_list = List.objects.get(id=list_id)
    Item.objects.create(
        text=request.POST['item_text'],
        parent_list=this_list
    )
    return redirect(f'/lists/{this_list.id}/')
