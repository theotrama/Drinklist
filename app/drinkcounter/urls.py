from django.urls import path

from drinkcounter.views import AddBeverageView, AddResidentView, BeveragePriceView, DetailedView, MakePaymentSuccessView, MakePaymentView, OverviewView, PaymentUndoView, ResidentCreationInfoView, SuccessView, UndoView


app_name = 'drinkcounter'
urlpatterns = [
    path('', OverviewView.as_view(), name='OverviewView'),
    path('details/<int:resident_id>/', DetailedView.as_view(), name='DetailedView'),
    path('add-beverage/', AddBeverageView.as_view(), name='AddBeverageView'),
    path('add-resident/', AddResidentView.as_view(), name='AddResidentView'),
    path('resident-creation-info/', ResidentCreationInfoView.as_view(), name='ResidentCreationInfoView'),
    path('success/', SuccessView.as_view(), name='SuccessView'),
    path('undo/', UndoView.as_view(), name='UndoView'),
    path('payment/', MakePaymentView.as_view(), name='MakePaymentView'),
    path('payment-success/', MakePaymentSuccessView.as_view(), name='MakePaymentSuccessView'),
    path('payment-undo/', PaymentUndoView.as_view(), name='PaymentUndoView'),
    path('beverage-prices/', BeveragePriceView.as_view(), name='BeveragePriceView'),
]
