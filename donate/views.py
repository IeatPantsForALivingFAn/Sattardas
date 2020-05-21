from django.shortcuts import render
from django.views.generic import list
from django.http import HttpResponse
from .forms import DonorCreateForm
from .models import Donation
# Create your views here.

import razorpay
#create the client
client = razorpay.Client(auth=('rzp_test_yPkkDyRXgbHxNk','5plGK3VWOznXLpD6lZdseLfi'))

#home page
def index(request):
    return render(request,'donate/index.html')

def donation_detail(request):
    form = DonorCreateForm()
    return render(request,'donate/donation_details.html',{'form':form})

#donation page
def donate(request):

    if request.method == 'POST':

        form = DonorCreateForm(request.POST)

        if form.is_valid():
            #get the form data
            amount = int(form.cleaned_data['amount'])
            name = form.cleaned_data['name']

            #create order
            response = client.order.create(dict(amount=amount*100,currency='INR'))

            #get the order details
            order_id = response['id']
            order_status = response['status']

            #if the order is successfully created
            if order_status=='created':
                form.save()
                context={
                    'name':name,
                    'amount':amount,
                    'order_id':order_id,
                    }
                return render(request,'donate/donate.html',context)
            else:
                return HttpResponse('<h1>Error in  create order function</h1>')


#order summary page
def payment_completion(request):
    
    response = request.POST

    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }

    # verify payment
    try:
        status = client.utility.verify_payment_signature(params_dict)
        return render(request, 'donate/order_summary.html', {'status': 'Payment Successful'})
    except:
        return render(request, 'donate/order_summary.html', {'status': 'Payment Faliure!!!'})

class Contributors(list.ListView):
    model = Donation
    context_object_name = 'donors'
    template_name = 'donate/list.html'


