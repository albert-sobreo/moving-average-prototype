from django.shortcuts import render, HttpResponse, redirect
from .models import Inventory, Purchase, Sales
from django.http import JsonResponse
import json
# Create your views here.
def purchase(request):
    return render(request, 'purchase.html', {})

def sales(request):
    return render(request, 'sales.html', {})

def getItems(request):
    inventory = Inventory.objects.all()
    data = []
    for el in inventory:
        data.append({'text':el.name, 'value': el.name})

    return JsonResponse(data, safe=False)

def purchaseprocess(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data['itemSelect'], data['quantity'], data['ppi'], data['total_cost'])

            inventory = Inventory.objects.get(name=data['itemSelect'])
            quantity = int(data['quantity'])
            ppi = float(data['ppi'])
            total_cost = float(data['total_cost'])

            purchase = Purchase()
            purchase.inventory = inventory
            purchase.quantity = quantity
            purchase.cost_per_item = ppi
            purchase.total_cost = total_cost

            purchase.save()

            inventory.total_cost += purchase.total_cost
            inventory.total_quantity += purchase.quantity
            inventory.current_ppi = float(round((inventory.total_cost / inventory.total_quantity), 2))

            inventory.save()

            return JsonResponse({'message': 'success', 'item': data['itemSelect'], 'quantity': quantity}, safe=False)

        except:
            return JsonResponse('error', safe=False)
    else:
        return HttpResponse("METHOD IS NOT POST")

def salesprocess(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data['itemSelect'], data['quantity'], data['total_cost'])

            inventory = Inventory.objects.get(name=data['itemSelect'])
            quantity = int(data['quantity'])
            total_cost = float(data['total_cost'])

            if quantity > inventory.total_quantity:
                return  JsonResponse({'message': 'less than quantity','item': data['itemSelect'] ,'sales_quantity': quantity, 'inventory_quantity': inventory.total_quantity})

            elif quantity == 0:
                return JsonResponse({'message': 'zero','item': data['itemSelect'] ,'sales_quantity': quantity, 'inventory_quantity': inventory.total_quantity})

            sales = Sales()
            sales.inventory = inventory
            sales.quantity = quantity
            sales.cost_per_item = inventory.current_ppi
            sales.total_cost = total_cost
            
            sales.save()

            inventory.total_cost -= sales.total_cost
            inventory.total_quantity -= sales.quantity

            inventory.save()

            return JsonResponse({'message': 'success', 'item': data['itemSelect'], 'quantity': quantity})

        except:
            return JsonResponse('error', safe=False)
    else:
        return HttpResponse("METHOD IS NOT POST")

def getInventoryPPI(request):
    data = json.loads(request.body)
    inventory = Inventory.objects.get(name=data['itemSelect'])

    return JsonResponse(inventory.current_ppi, safe=False)

def inventory(request):
    data = {
        "inventory": Inventory.objects.all()
    }
    return render(request, 'inventory.html', data)