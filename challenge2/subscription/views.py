import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from subscription.models import CustomerSubscription
from django_registration.forms import RegistrationForm
from django.contrib.auth import login


stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    """
    Create subscription in db after user registration
    Index page views return stripe public key.
    """
    context = {}
    try:
        customer_id = request.user.customersubscription.stripe_customer_id

        get_subscription = stripe.Subscription.list(limit=1, customer=customer_id)

        if get_subscription["data"][0].trial_end:
            state = "TRIAL"
        else:
            state = "SUBSCRIPTION"
        create_subs = CustomerSubscription.objects.update_or_create(
            user=request.user,
            state=state,
            stripe_customer_id=customer_id,
            stripe_subscription_id=get_subscription["data"][0].id,
        )
        context["subscriptions"] = state
        return render(request, "index.html", context)

    except Exception as e:
        context["message"] = "Please Buy Subscription for complete registration"
        return render(request, "index.html", context)


@login_required
def success(request):
    """
    Show sucess template after buy a subscription.
    """
    return render(request, "success.html")


@login_required
def cancel(request):
    """
    Show cancel template after cancel the subscription.
    """
    return render(request, "cancel.html")


def create_user(request, state):
    """
    Create customer on database and strpie dashboard.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    price_id = settings.STRIPE_PRICE_ID
    if request.method == "POST":
        user_form_data = RegistrationForm(request.POST)
        if user_form_data.is_valid():
            user = user_form_data.save()
            stripe_data = stripe.Customer.create(
                email=user.email,
                name=user.username,
            )

            login(request, user)
            if state == "trial":
                """
                Check regisration type and create
                a trial subscription for the user and
                store it on both stipe and local database.
                """
                subscription = stripe.Subscription.create(
                    customer=stripe_data.id,
                    items=[
                        {
                            "price": price_id,
                            "quantity": 1,
                        },
                    ],
                    trial_period_days=7,
                )
                create_customer_subscription = CustomerSubscription.objects.create(
                    user=user,
                    state="TRIAL",
                    stripe_customer_id=stripe_data.id,
                    stripe_subscription_id=subscription.id,
                )
                return render(
                    request, "index.html", {"message": "Enjoy 7 days Free Trial"}
                )
            elif state == "subscription":
                """
                Check registraion type to 'premium_member',
                and redirect user to complete the payment process
                on index page.
                """
                return render(
                    request,
                    "index.html",
                    {
                        "success": True,
                        "message": "Please Buy Subscription for continue registration",
                    },
                )
    else:
        user_form_data = RegistrationForm()
    return render(
        request,
        "django_registration/registration_form.html",
        {"form": user_form_data, "state": state},
    )


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Fetch all the required data from session
        client_reference_id = session.get("client_reference_id")
        stripe_customer_id = session.get("customer")
        stripe_subscription_id = session.get("subscription")

        # Get the user and create a new CustomerSubscription
        user = User.objects.get(id=client_reference_id)
        create_customer_subscription = CustomerSubscription.objects.create(
            user=user,
            state="TRIAL",
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=stripe_subscription_id,
        )
        print(user.username + " just subscribed.")

    return HttpResponse(status=200)


@csrf_exempt
def stripe_config(request):
    """
    Return stripe public key in json format.
    """
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    """
    Create subscription checkout session for premium membership.
    """
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id
                if request.user.is_authenticated
                else None,
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancel/",
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": settings.STRIPE_PRICE_ID,
                        "quantity": 1,
                    }
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})
