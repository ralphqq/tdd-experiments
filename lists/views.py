from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.forms import (
    BLANK_ITEM_ERROR, DUPLICATE_ITEM_ERROR,
    ExistingListItemForm, ItemForm
)
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        parent_list = List.objects.create()
        form.save(for_list=parent_list)
        return redirect(parent_list)
    else:
        return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    this_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=this_list)

    if request.method == 'POST':
        form = ExistingListItemForm(
            for_list=this_list,
            data=request.POST
        )
        if form.is_valid():
            form.save()
            return redirect(this_list)

    return render(
        request,
        'list.html',
        {'parent_list': this_list, 'form': form}
    )
