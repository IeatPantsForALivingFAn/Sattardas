from django.urls import path
from . import views
#url patterns
app_name = 'donate'

urlpatterns = [
    path('',views.index,name='index'),
    path('donation-details/',views.donation_detail,name='donation-details'),
    path('donate/',views.donate,name='donate'),
    path('summary/',views.payment_completion,name='summary'),
    path('list/',views.Contributors.as_view(),name='list')
]
