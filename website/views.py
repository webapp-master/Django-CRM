from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record



def home(request):
	records = Record.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})



def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
			
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})



def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = AddRecordForm(request.POST)
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		else:
			form = AddRecordForm()
		return render(request, 'add_record.html', {'form': form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')



def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		if request.method == 'POST':
			form = AddRecordForm(request.POST, instance=current_record)
			if form.is_valid():
				form.save()
				messages.success(request, "Record Has Been Updated!")
				return redirect('home')
		else:
			form = AddRecordForm(instance=current_record)
		return render(request, 'update_record.html', {'form': form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')






def search_record(request):
    query = request.GET.get('query')  # Get the search query from the request's GET parameters

    if query:
        # Perform the search
        results = Record.objects.filter(
            Q(city__icontains=query) |  # Search by city (case-insensitive)
            Q(first_name__icontains=query) |  # Search by first_name (case-insensitive)
            Q(phone__icontains=query)  # Search by phone (case-insensitive)
        )
    else:
        results = None

    return render(request, 'search_record.html', {'results': results, 'query': query})


