from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Listing
from realtors.models import Realtor
from listings.choices import price_choices, bedroom_choices, state_choices


def index(request):
    listings = (
        Listing.objects.select_related("realtor")
        .order_by("-list_date")
        .filter(is_published=True)[:3]
    )
    context = {
        "listings": listings,
        "state_choices": state_choices,
        "bedroom_choices": bedroom_choices,
        "price_choices": price_choices,
    }
    return render(request, "pages/index.html", context)


def about(request):
    # Get all realtors
    realtors = (
        Realtor.objects.annotate(num_listings=Count("listing"))
        .order_by("-num_listings")
        .all()
    )

    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {"realtors": realtors, "mvp_realtors": mvp_realtors}
    return render(request, "pages/about.html", context)
