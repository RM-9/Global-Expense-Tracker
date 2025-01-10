from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from . models import Destination,Expense,Category
import requests
from django.http import JsonResponse
from django.db.models import Sum
import json

# from .utils import convert_to_inr

# Create your views here.

def add_destination(request):
    if request.method == 'POST':
        name = request.POST['name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        is_foreign = 'is_foreign' in request.POST
        Destination.objects.create(name=name, start_date=start_date, end_date=end_date, is_foreign=is_foreign)
        return redirect('destination_list')
    return render(request, 'add_destination.html')

def add_expense(request, destination_id):
    
    destination = get_object_or_404(Destination, id=destination_id)
    response = requests.get(url='https://api.exchangerate-api.com/v4/latest/USD').json()
    currencies = response.get('rates')
    categories=Category.objects.all()
    

    if request.method == 'POST':
        description = request.POST.get('description', '')
        amount = request.POST.get('amount')
        from_curr = request.POST.get('from-curr','N/A')
        to_curr = request.POST.get('to-curr','N/A')
        category_id=request.POST.get('category')
        category = Category.objects.get(id=category_id)

        converted_amount=float(amount)
        
        if destination.is_foreign and from_curr != "N/A" and to_curr != "N/A":
            if from_curr in currencies and to_curr in currencies:
                converted_amount = round(
                    (currencies[to_curr] / currencies[from_curr]) * float(amount), 2
                )
            else:
                # Handle missing currency rates
                return HttpResponse("Error: Invalid currency selection.", status=400)

        

        # Save the expense
        Expense.objects.create(
            destination=destination,
            description=description,
            amount=amount,
            from_currency=from_curr,
            converted_amount=converted_amount,
            category=category
            
        )
        return redirect('expense_list', destination_id=destination.id)
    else:
        return render(request, 'add_expense.html', {'destination': destination, 'currencies': currencies,'categories':categories})

def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})


def expense_list(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    expenses = destination.expenses.all()
    
    category_totals = Expense.objects.filter(destination_id=destination_id).values('category__name').annotate(total_amount=Sum('amount'))
    
    category_totals_data = json.dumps(list(category_totals))
    
    context = {
            'destination': destination,
            'expenses': expenses,
            'category_totals_data': category_totals_data,
        }
    
    
    
    return render(request, 'expense_list.html',context)





