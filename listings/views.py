from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Listing
from .choices import bedroom_choices, price_choices, state_choices


def index(request):
    listing_list = (
        Listing.objects.select_related("realtor")
        .all()
        .order_by("-list_date")
        .filter(is_published=True)
    )
    paginator = Paginator(listing_list, 6)
    page = request.GET.get("page")
    listings = paginator.get_page(page)

    context = {"listings": listings}

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
    queryset_list = Listing.objects.select_related("realtor").order_by("-list_date")

    # Keywords
    if "keywords" in request.GET:
        keywords = request.GET["keywords"]
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # City
    if "city" in request.GET:
        city = request.GET["city"]
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if "state" in request.GET:
        state = request.GET["state"]
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if "bedrooms" in request.GET:
        bedrooms = request.GET["bedrooms"]
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms).order_by(
                "-bedrooms"
            )

    # Price
    if "price" in request.GET:
        price = request.GET["price"]
        if price:
            queryset_list = queryset_list.filter(price__lte=price).order_by("-price")

    paginator = Paginator(queryset_list, 12)
    page = request.GET.get("page")
    listings = paginator.get_page(page)
    context = {
        "state_choices": state_choices,
        "bedroom_choices": bedroom_choices,
        "price_choices": price_choices,
        "listings": listings,
        "values": request.GET,
    }
    return render(request, "listings/search.html", context)
