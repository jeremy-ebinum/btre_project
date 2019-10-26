from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact


def contact(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        listing = request.POST.get("listing")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        user_id = request.POST.get("user_id")
        realtor_email = request.POST.get("realtor_email")

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(
                listing_id=listing_id, user_id=user_id
            )
            if has_contacted:
                messages.error(
                    request, "You have already made an inquiry for this listing."
                )
                return redirect("listing", listing_id)

        contact = Contact(
            listing_id=listing_id,
            listing=listing,
            name=name,
            email=email,
            phone=phone,
            message=message,
            user_id=user_id,
        )

        contact.save()

        # Send mail
        send_mail(
            subject="Property Listing Inquiry",
            message="There has been an inquiry for "
            + listing
            + ". Sign into the admin panel for more info",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[realtor_email],
            fail_silently=False,
        )

        messages.success(
            request,
            "Your inquiry has been submitted, a realtor will get back to you soon",
        )
        return redirect("listing", listing_id)

    else:
        return redirect("listing")
