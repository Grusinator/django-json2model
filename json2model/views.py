# Create your views here.
from django.shortcuts import render

from json2model.forms import CreateRequestForm

def create_models_from_json_view(request):
    form = CreateRequestForm()
    return render(request, 'create_models_from_json.html', {'form': form})