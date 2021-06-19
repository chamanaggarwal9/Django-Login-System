from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.conf import settings
from account.models import UserData
from django.core.mail import send_mail
# Create your views here.

@csrf_exempt
@api_view(['POST'])
def Registration(request):

    if(request.method=='POST'):

        try:
            email = request.POST['email']
            name = request.POST['name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            user_exists = UserData.objects.filter(email=email).first()

            if not user_exists:
                if(password1 != password2):
                    return JsonResponse({'success':False, 'comments':'Password should be same'})

                if len(password1) < 8:
                    return JsonResponse({'success':False, 'comments':'Password should be atleast 8 characters'})

                user = UserData.objects.create_user(email=email, password=password1)
                user.full_name = name
                user.save()

                token = Token.objects.get(user=user).key
                user.token_auth = token
                user.save()

                Activation_Request(email, token)
                return JsonResponse({'success':True, 'comments':'User has been registered'})
            else:
                return JsonResponse({'success':False, 'comments':'User already exist'})
        
        except Exception as e:
            return JsonResponse({'success':False, 'comments':'Oops, something went wrong!'})


def Activation_Request(email, token):
    subject = "Account verification email"
    message = f'Hey,\nClick here to activate your account http://127.0.0.1:8000/activate/{token}\nPlease dont share this mail with anyone.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def Confirm_Activation(request, token):
    
    user = UserData.objects.filter(token_auth=token).first()

    if user:
        if user.user_verified:
            return JsonResponse({'success':False, 'comments':'User account already activated'})
        user.user_verified = True
        user.save()
        return JsonResponse({'success':True, 'comments':'User account successfully activated'})
    else:
        return JsonResponse({'success':False, 'comments':'User account deleted'})


@csrf_exempt
@api_view(['POST'])
def Login(request):

    if(request.method == 'POST'):

        try:
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)
            if user:
                if user.user_verified:
                    user.user_logged_in = True
                    user.save()
                    return JsonResponse({'success':True, 'comments':'User loggged in successfully'})
                else:
                    return JsonResponse({'success':False, 'comments':'User account not activated'})
            else:
                return JsonResponse({'success':False, 'comments':'User account credentials not correct'})
        
        except Exception as e:
                return JsonResponse({'success':False, 'comments':'Oops, something went wrong!'})


@csrf_exempt
@api_view(['POST'])
def Forget_Password(request):

    if(request.method=='POST'):

        try:
            email = request.POST['email']
            user = UserData.objects.filter(email=email).first()
            if user:
                token = user.token_auth
                subject = "Reset password request"
                message = f'Hey,\nClick here to reset password http://127.0.0.1:8000/reset_complete/{token}\nPlease dont share this mail with anyone.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list)
                return JsonResponse({'success':True, 'comments':'Email sent for reset password'})
            else:
                return JsonResponse({'success':False, 'comments':'User email doesnt exist'})

        except Exception as e:
            return JsonResponse({'success':False, 'comments':'Oops, something went wrong!'})
            

@csrf_exempt
@api_view(['POST'])
def Reset_Password(request, token):
    
    if(request.method=='POST'):
        try:
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            user = UserData.objects.filter(token_auth=token).first()
            if user:
                if(password1 != password2):
                    return JsonResponse({'success':False, 'comments':'Passwords didnt matched'})
                if len(password1) < 8:
                    return JsonResponse({'success':False, 'comments':'Password should be atleast 8 characters'})

                user.set_password(password1)
                user.save()
                return JsonResponse({'success':True, 'comments':'Account password changed'})
            else:
                return JsonResponse({'success':False, 'comments':'User didnt exist'})
        
        except Exception as e:
            return JsonResponse({'success':False, 'comments':'Oops, something went wrong!'})