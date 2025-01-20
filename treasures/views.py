from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def add_treasure(request):
    path = request.get_full_path()
    html = f'<html lang="en"><body>Add Treasure view triggered. The path {path} was requested.</body></html>'
    return HttpResponse(html)
    # should call form_data.save(commit=False), this will return an instance of the model which hasn't yet been saved, and then I can add the user as the foreign key for that field.