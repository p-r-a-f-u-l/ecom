import re

from termcolor import colored
from analysis.models import RecentProduct

from products.models import Product


class CheckEveryRequest:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        print("\n")
        print(colored(" =" * 30, "white", attrs=["bold"]))
        print(colored(f"IP : {request.META.get('REMOTE_ADDR')}", "red", attrs=["bold"]))
        print(
            colored(
                f"{request.META.get('HTTP_AUTHORIZATION')}", "green", attrs=["bold"]
            )
        )
        print(colored(f"{request.path}", "yellow", attrs=["bold"]))
        print(colored(" =" * 30, "white", attrs=["bold"]))

        if request.user.id:
            try:
                if request.path.split("/")[1] == "product":
                    id = int(request.path.split("/")[2])
                    product = Product.objects.filter(id=id).get()
                    oldview = product.views + 1
                    Product.objects.filter(id=id).update(views=oldview)

                    RecentProduct.objects.create(owner=request.user, product_no=product)
            except ValueError:
                print("Error")

        return response
