from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
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
    listing = get_object_or_404(Listing, id=listing_id)
    thumbnail_fields = (
        "photo_1",
        "photo_2",
        "photo_3",
        "photo_4",
        "photo_5",
        "photo_6",
    )
    thumbnails = []
    for field in thumbnail_fields:
        if listing.__getattribute__(field):
            thumbnails.append(listing.__getattribute__(field))

    context = {"listing": listing, "thumbnails": thumbnails}
    return render(request, "listings/listing.html", context)


def search(request):
    return render(request, "listings/search.html")
