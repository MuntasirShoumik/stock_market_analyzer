from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm,StockDataForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import json
from .models import StockData
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




@login_required(login_url='login/')
def index(request):
    market_data = StockData.objects.order_by('-date')
    email = request.session['email']
    records = len(market_data) if len(market_data) < 100 else 100



    if request.method == "POST":
        
        records = records if request.POST['records'] == "" else int(request.POST['records'])
        x_data = [item[0] for item in market_data.values_list(request.POST['X-axis'])[:records]] if request.POST['X-axis'] == 'date' else [float(item[0]) for item in market_data.values_list(request.POST['X-axis'])[:records]]
        y_data = [item[0] for item in market_data.values_list(request.POST['Y-axis'])[:records]] if request.POST['Y-axis'] == 'date' else [float(item[0]) for item in market_data.values_list(request.POST['Y-axis'])[:records]]
        cType = request.POST['chartType']
        lable = f"{request.POST['X-axis']} vs {request.POST['Y-axis']} ({cType})"
        
    else:

        x_data = [float(item[0]) for item in market_data.values_list('open')[:records]]
        y_data = [float(item[0]) for item in market_data.values_list('close')[:records]]
        cType = "line"
        lable = "Open vs Close (line)"
    return render(request,'analyzer_app/index.html',{"market_data":market_data,
                                                     "x_data":x_data,
                                                     "y_data":y_data,
                                                     "cType":cType,
                                                     "lable":lable,
                                                     "email":email,
                                                     "records":records
                                                     })

    # with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json') as json_file:
    #     market_data = json.load(json_file)
    
    # if market_data[0].get('id') == None:
    #     for idx, dict in enumerate(market_data):
    #         dict["id"] = idx
    #     with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json', 'w') as f:
    #         json.dump(market_data, f)

    # return render(request, 'analyzer_app/index.html', {'email':request.user.email,"market_data":market_data})
  

def register(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            
            
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'analyzer_app/register.html', {'form': form})
  

def Login(request):

    error = ""
    if request.method == 'POST':
  
       
  
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email = email, password = password)
        if user is not None:
            form = login(request, user)
            
            request.session['email'] = email
            return redirect("index")
        else:
            error = "Wrong email or Password !!"
    form = AuthenticationForm()
    return render(request, 'analyzer_app/login.html', {'form':form,
                                                       "error":error
                                                       })



@login_required(login_url='login/')
def custom_logout(request):
    logout(request)
    request.session['email'] = None
    return redirect("login")





def addnew(request):  
    if request.method == "POST":  
        form = StockDataForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('index')  
            except:  
                pass
    else:  
        form = StockDataForm()  
    return render(request,'analyzer_app/add.html',{'form':form}) 
    
    # with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json') as json_file:
    #     market_data = json.load(json_file)

    # if request.method == "POST":
    #     dict = {
            
    #         "date": request.POST.get("date") ,
    #         "trade_code": request.POST.get("trade_code") ,
    #         "high": request.POST.get("high") ,
    #         "low": request.POST.get("low"),
    #         "open": request.POST.get("open"),
    #         "close": request.POST.get("close") ,
    #         "volume": request.POST.get("volume"),
    #         "id": market_data[-1]["id"]+1
    #     }

    #     market_data.insert(0,dict)
    #     with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json', 'w') as f:
    #         json.dump(market_data, f)
    #     return redirect("/")

    # return render(request,'analyzer_app/add.html')  
 

 
def edit(request, id):

    data_to_edit = StockData.objects.get(id=id)  
    
    if request.method == "POST":
        data_to_edit = StockData.objects.get(id=id) 
        form = StockDataForm(request.POST, instance = data_to_edit)    
        if form.is_valid():  
            form.save()  
            return redirect("index")
        else:
            print("can't save")
        
    return render(request, 'analyzer_app/edit.html', {'form': data_to_edit})  



    # with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json') as json_file:
    #     market_data = json.load(json_file)
     
    # if request.method == "POST":
    #     for dict in market_data:
    #         if dict['id'] == id:
    #             dict["date"] = request.POST.get("date")
    #             dict["trade_code"] = request.POST.get("trade_code")
    #             dict["high"] = request.POST.get("high")
    #             dict["low"] = request.POST.get("low")
    #             dict["open"] = request.POST.get("open")
    #             dict["close"] = request.POST.get("close") 
    #             dict["volume"] = request.POST.get("volume")
    #             break

    #     with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json', 'w') as f:
    #         json.dump(market_data, f)
    #     return redirect('index')
    # for dict in market_data:
    #     if dict['id'] == id:
    #         dict_to_edit = dict
    # return render(request,'analyzer_app/edit.html', {'form':dict_to_edit})  
 

     
def destroy(request, id):
    data_to_del = StockData.objects.get(id=id)  
    data_to_del.delete()  
    return redirect("index")  


    # with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json') as json_file:
    #     market_data = json.load(json_file)

    # for dict in market_data:
    #     if dict['id'] == id:
    #         market_data.remove(dict)
    #         break 

    # with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json', 'w') as f:
    #         json.dump(market_data, f)    

    # return redirect("index")