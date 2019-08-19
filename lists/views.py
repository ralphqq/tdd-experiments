from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.forms import ItemForm, BLANK_ITEM_ERROR
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        parent_list = List.objects.create()
        item = Item.objects.create(
            text=request.POST['text'],
            parent_list=parent_list
        )
        return redirect(parent_list)
    else:
        return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    this_list = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            item = Item.objects.create(
                text=request.POST['text'],
                parent_list=this_list
            )
            return redirect(this_list)

    return render(
        request,
        'list.html',
        {'parent_list': this_list, 'form': form}
    )
