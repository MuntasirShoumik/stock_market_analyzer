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
    market_data = StockData.objects.order_by('-date') # getting data sorted newest date first 
    email = request.session['email'] # getting the email of logged in user from session
    records = len(market_data) if len(market_data) < 100 else 100  # setting a default value of 100 if database has more then 100 records else total num of records


          #""" If it is a POST request"""#
    if request.method == "POST":
        
        records = records if request.POST['records'] == "" else int(request.POST['records']) # records = peviously set value if records input is not given by the user 
        x_data = [item[0] for item in market_data.values_list(request.POST['X-axis'])[:records]] if request.POST['X-axis'] == 'date' else [float(item[0]) for item in market_data.values_list(request.POST['X-axis'])[:records]] # getting user selected x-axis data in a iterable. if tha selected column is not date then the column is converted in to float
        y_data = [item[0] for item in market_data.values_list(request.POST['Y-axis'])[:records]] if request.POST['Y-axis'] == 'date' else [float(item[0]) for item in market_data.values_list(request.POST['Y-axis'])[:records]] # doing the same for selected y-axis
        cType = request.POST['chartType'] # getting the type of chart user want to see
        lable = f"{request.POST['X-axis']} vs {request.POST['Y-axis']} ({cType})" # setting a lable for the chart
        
        #""" If it is a GET request"""#
    else:

        x_data = [float(item[0]) for item in market_data.values_list('open')[:records]] # setting x-axis as open column
        y_data = [float(item[0]) for item in market_data.values_list('close')[:records]] # setting y-axis as close column
        cType = "line" # default chart type is line chart
        lable = "Open vs Close (line)"
    return render(request,'analyzer_app/index.html',{"market_data":market_data,
                                                     "x_data":x_data,
                                                     "y_data":y_data,
                                                     "cType":cType,
                                                     "lable":lable,
                                                     "email":email,
                                                     "records":records
                                                     }) # sending context to index page
    

                                   #""" JsonModel index view """#

    # with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json') as json_file:
    #     market_data = json.load(json_file)
    
    # if market_data[0].get('id') == None:
    #     for idx, dict in enumerate(market_data):
    #         dict["id"] = idx
    #     with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json', 'w') as f:
    #         json.dump(market_data, f)

    # return render(request, 'analyzer_app/index.html', {'email':request.user.email,"market_data":market_data})
  
                #""" view to handle registrations """#
def register(request):
    
    if request.method == 'POST':  
        form = UserRegisterForm(request.POST) # creating a form with registration data
        if form.is_valid():
            form.save() # saving the model form if input data is valid
            return redirect('login') # redirecting to login page
    else:
        form = UserRegisterForm()
    return render(request, 'analyzer_app/register.html', {'form': form})
  
                #""" view to handle login """#
def Login(request):

    error = ""
    if request.method == 'POST':
  
       
  
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email = email, password = password) # checking if the user exist 
        if user is not None:
            form = login(request, user)
            
            request.session['email'] = email
            return redirect("index")
        else:
            error = "Wrong email or Password !!"
    form = AuthenticationForm() # geting djangos builtin user authentication form
    return render(request, 'analyzer_app/login.html', {'form':form,
                                                       "error":error
                                                       })



                          #""" view to handle logout """#
@login_required(login_url='login/')
def custom_logout(request):
    logout(request)
    request.session['email'] = None
    return redirect("login")




                  #""" view to handle data insertion """#

def addnew(request):  
    if request.method == "POST":  
        form = StockDataForm(request.POST)  # sending user inputs to StockDataForm model form 
        if form.is_valid():  
            try:  
                form.save()  # if inputs are valid saving the form data to database
                return redirect('index')  
            except:  
                pass
    else:  
        form = StockDataForm()  # geting the form
    return render(request,'analyzer_app/add.html',{'form':form}) 
    


                                #""" JsonModel addnew view """#

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
 


                           #""" view to handle updates """#
 
def edit(request, id):

    data_to_edit = StockData.objects.get(id=id)  # getting the row from database table which to update/edit with the id that passed in
    
    if request.method == "POST":
        
        form = StockDataForm(request.POST, instance = data_to_edit)  # sending data data and the row which to update  
        if form.is_valid():  
            form.save()  # if inputs are valid saving the updated row to database table
            return redirect("index")
        else:
            print("can't save")
        
    return render(request, 'analyzer_app/edit.html', {'form': data_to_edit})  

                           
                        #""" JsonModel edit view """#

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
 

                                     #""" view to handle deletes """#
def destroy(request, id):
    data_to_del = StockData.objects.get(id=id) # geting the row which to delete 
    data_to_del.delete()  # deleting from the table
    return redirect("index")  
                                     
                                     #""" JsonModel delete view """#

    # with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json') as json_file:
    #     market_data = json.load(json_file)

    # for dict in market_data:
    #     if dict['id'] == id:
    #         market_data.remove(dict)
    #         break 

    # with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json', 'w') as f:
    #         json.dump(market_data, f)    

    # return redirect("index")