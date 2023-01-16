from django.shortcuts import render, HttpResponse
from django import forms
    
import requests
import json
from .models import BitcoinPrice

import matplotlib.pyplot as plt



class SearchForm(forms.Form):
    search_query = forms.CharField()



# view for showing out the searched data 
def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            data = BitcoinPrice.objects.filter(value__contains=search_query)
    else:
        form = SearchForm()
        data = BitcoinPrice.objects.all()
    return render(request, 'bitcoin.html', {'form': form, 'data': data})
    
    
    
class EditForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()
    id = forms.IntegerField(widget=forms.HiddenInput())
    
    
# view for inline editing
def edit_view(request, id):
    data = MyTable.objects.get(pk=id)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('my_view')
    else:
        form = EditForm(instance=data)
    return render(request, 'bitcoin_price.html', {'form': form})
    



# bitcoin to usd graph
def fetch_btc_price(value):
    url = f'https://blockchain.info/tobtc?currency=USD&value={value}'
    response = requests.get(url)
    btc_price = json.loads(response.text)
    # Save the price to the database
    BitcoinPrice.objects.create(value=value, btc_price=btc_price)
    
def display_price_graph(request):
    prices = BitcoinPrice.objects.all()
    values = [price.value for price in prices]
    btc_prices = [price.btc_price for price in prices]
    plt.plot(values, btc_prices)
    plt.xlabel('USD')
    plt.ylabel('BTC')
    plt.title('Bitcoin Price in USD')
    # plt.show()
    
def bitcoin_price_view(request):
    fetch_btc_price(1000)
    display_price_graph(request)
    prices = BitcoinPrice.objects.all()
    prices_json = json.dumps(list(prices.values()),indent=4, sort_keys=True, default=str)
    return render(request, 'bitcoin.html', {'prices_json': prices_json})
    

    
