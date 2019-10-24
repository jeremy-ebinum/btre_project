from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Listing


def index(request):
    listing_list = (
        Listing.objects.select_related("realtor")
        .all()
        .order_by("-list_date")
        .filter(is_published=True)
    )
    paginator = Paginator(listing_list, 6)
    page = request.GET.get("page")
    pages = paginator.page_range
    listings = paginator.get_page(page)

    context = {"listings": listings, "pages": pages}

    return render(request, "listings/listings.html", context)


def listing(request, listing_id):
    return render(request, "listings/listing.html")


def search(request):
    return render(request, "listings/search.html")
