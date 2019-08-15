from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    parent_list = List.objects.create()
    item = Item(
        text=request.POST['item_text'],
        parent_list=parent_list
    )

    try:
        item.full_clean()
        item.save()
    except ValidationError:
        parent_list.delete()
        error = "You can't have an empty list item."
        return render(request, 'home.html', {'error': error})

    return redirect(parent_list)


def view_list(request, list_id):
    this_list = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(
                text=request.POST['item_text'],
                parent_list=this_list
            )
            item.full_clean()
            item.save()
            return redirect(this_list)
        except ValidationError:
            error = "You can't have an empty list item."

    return render(
        request,
        'list.html',
        {'parent_list': this_list, 'error': error}
    )
