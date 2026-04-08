from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model


User = get_user_model()


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            if user.role == 'customer':
                login(request, user)
                return redirect('home')
            

            elif user.role=="seller":

                sellerprofile = user.seller_profile

                if not sellerprofile.approved:
                    messages.error(request, "Your seller account is waiting for admin approval")
                    return redirect('user_login')

                login(request, user)
                return redirect('seller_home')
        if user.role != 'seller':
                messages.error(request, "You are not a seller")
                return redirect('user_login')
        if user.role != 'customer':
                messages.error(request, "You are not a customer")
                return redirect('user_login')        
        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect('user_login')    
    return render(request, 'core/login.html')
        
