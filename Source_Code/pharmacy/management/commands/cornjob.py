from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from module.models import Product, Batch, temp, Supplier
from pharmacy import views


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        products = Product.objects.all()

        for i in products:
            x = Batch.objects.filter(product=i).aggregate(Sum('available_count'))

            print(x)
            y = temp.objects.filter(product=i).aggregate(Sum('count'))
            print(y)
            thr=int(x['available_count__sum']) - int(y['count__sum'])
            print(thr)

            batch = get_object_or_404(Batch,product=i)
            supplierx = get_object_or_404(Supplier,batch=batch)
            msg = str(Product.product_name) + "is Low In Stock"

            if int(thr) < int(i.min_req):
                return views.sendMail("temp.temp3951@gmail.com",supplierx.email,msg)







