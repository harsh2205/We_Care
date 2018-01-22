"""falcon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from module import views
from pharmacy import views as pharma_view

urlpatterns = [

    url(r'^batch/(?P<id>\d+)/edit', views.edit_batch, name="batch_edit"),
    url(r'^batch', views.view_batch, name="batchs"),
    url(r'^manufacturer/(?P<id>\d+)/edit', views.edit_manufacturer, name="manufacturer_edit"),
    url(r'^supplier/(?P<id>\d+)/edit', views.edit_supplier, name="supplier_edit"),
    url(r'^manufacturer/', views.manufacturer_list_view, name="manufacturer"),
    url(r'^supplier/', views.supplier_list_view, name="supplier"),
    url(r'^product/(?P<id>\d+)/edit', views.edit_product, name="s"),
    url(r'^product', views.view_all_products, name="product"),
    url(r'^new_product', views.new_product, name="new_product"),
    url(r'^create_batch', views.create_batch, name="create_batch"),
    url(r'^create_manufacturer', views.create_manufacturer, name="create_manufacturer"),
    url(r'^create_supp', views.create_supplier, name="create_supp"),
    url(r'^(?P<id>\d+)/edit', views.edit_appointment, name=""),
    url(r'^(?P<id>\d+)', views.View_appointment, name="s"),
    # --------------Bliiling Urls------------
    url(r'^vab', pharma_view.All_Bills, name="all_bills"),
    url(r'^vpb/(?P<id>\d+)/paid', pharma_view.Mark_as_Paid_Bills, name="Mak_as_Paid_bill"),
    url(r'^vpb/(?P<id>\d+)/cancel', pharma_view.Cancle_Bills, name="cancle_bills"),
    url(r'^vpb/(?P<id>\d+)/open', pharma_view.Details_Bill, name="open_bill"),
    url(r'^vpb/(?P<id>\d+)/print', pharma_view.Details_Bill_print, name="open_bill_print"),
    url(r'^vpb', pharma_view.View_Pending_Bills, name="view_pending_bills"),
    url(r'^vpb', pharma_view.View_Pending_Bills, name="Mak_as_Paid_bill"),

]
