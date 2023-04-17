from django.shortcuts import render,redirect
from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt
from .models import Transactions
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
    if not request.user or str(request.user) == 'AnonymousUser':
        if request.method == 'POST':
            name,password = request.POST['name'], request.POST['password']
            user = authenticate(username=name,password=password)
            if user:
                login(request,user)
                return redirect('/dashboard')
        return render(request,'index.html')
    else: return redirect('/dashboard')

def create(request):
    if request.method=='POST':
        name,password,balance,pin,email = request.POST['name'],request.POST['password'],request.POST['balance'],request.POST['pin'],request.POST['email']
        try:user = User.objects.get(username=name, email=email)
        except User.DoesNotExist:user=None
        if not user:
            User.objects.create_user(username=name,email=email,password=password,balance=balance,pin=pin)
            messages.add_message(request,messages.INFO,f'User {name} created successfully')
            return redirect('/')
        else:
            messages.add_message(request,messages.INFO,f'Username: {name} already taken')
            return redirect('/create')
    return render(request,'create.html')

login_required(login_url='/')
def dashboard(request):
    if request.user and str(request.user) != 'AnonymousUser':
        user = User.objects.get(username=str(request.user))
        balance = user.balance
        transactions = Transactions.objects.filter(user_id=str(user.id))
        return render(request,'indi.html',{'users':[user],'balance':balance,'trans':transactions})
    else:return redirect('/')

def logout_usr(request):
    logout(request)
    return redirect('/')

login_required(login_url='/')
def credit(request):
    if request.user and str(request.user) != 'AnonymousUser':
        if request.method == 'POST':
            try:u=request.user
            except: return redirect('/')
            user = User.objects.get(username=str(u))
            if int(request.POST['pin']) == int(user.pin):
                user.balance = float(user.balance) + float(request.POST['credit'])
                user.save()
                tran = Transactions()
                tran.transaction_type='CREDIT'
                tran.amount = request.POST['credit']
                tran.balance = user.balance
                tran.user_id = user.id
                tran.save()
                messages.add_message(request,messages.INFO,f'Amount {request.POST["credit"]} credited successfully')
            else:messages.add_message(request,messages.INFO,f'Unable to credit the amount')
            return redirect('/dashboard')
    else:return redirect('/')

login_required(login_url='/')
def debit(request):
    if request.user and str(request.user) != 'AnonymousUser':
        if request.method == 'POST':
            try:u=request.user
            except: return redirect('/')
            user = User.objects.get(username=str(u))
            if int(request.POST['pin']) == int(user.pin) and float(user.balance) >= float(request.POST['debit']):
                user.balance = float(user.balance) - float(request.POST['debit'])
                user.save()
                tran = Transactions()
                tran.transaction_type='DEBIT'
                tran.amount = request.POST['debit']
                tran.balance = user.balance
                tran.user_id = user.id
                tran.save()
                messages.add_message(request,messages.INFO,f'Amount {request.POST["debit"]} debited successfully')
            else:messages.add_message(request,messages.INFO,f'Unable to debit the amount')
            return redirect('/dashboard')
    else:return redirect('/')