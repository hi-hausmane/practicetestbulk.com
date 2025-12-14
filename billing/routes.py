# billing/routes.py
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
import stripe
import os
from dotenv import load_dotenv
from auth.routes import get_current_user, supabase_client

load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID_PRO = os.getenv("STRIPE_PRICE_ID_PRO")  # $9/month Pro plan
STRIPE_PRICE_ID_BUSINESS = os.getenv("STRIPE_PRICE_ID_BUSINESS")  # $39/month Business plan
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Backwards compatibility - if old STRIPE_PRICE_ID exists, use it as Pro
if not STRIPE_PRICE_ID_PRO and os.getenv("STRIPE_PRICE_ID"):
    STRIPE_PRICE_ID_PRO = os.getenv("STRIPE_PRICE_ID")

if not STRIPE_SECRET_KEY:
    print("WARNING: STRIPE_SECRET_KEY not found in environment variables")
else:
    stripe.api_key = STRIPE_SECRET_KEY
    print(f"Stripe API key configured: {STRIPE_SECRET_KEY[:7]}...")

if not STRIPE_PRICE_ID_PRO:
    print("WARNING: STRIPE_PRICE_ID_PRO not found in environment variables")

if not STRIPE_PRICE_ID_BUSINESS:
    print("WARNING: STRIPE_PRICE_ID_BUSINESS not found in environment variables")

billing_router = APIRouter()


@billing_router.post("/create-checkout-session")
async def create_checkout_session(request: Request, user = Depends(get_current_user)):
    """Create Stripe checkout session for Pro or Business subscription, or upgrade existing subscription"""
    try:
        # Get tier from query parameter (default to 'pro')
        tier = request.query_params.get('tier', 'pro').lower()

        # Validate tier and get price ID
        if tier == 'pro':
            price_id = STRIPE_PRICE_ID_PRO
            tier_name = "pro"
        elif tier == 'business':
            price_id = STRIPE_PRICE_ID_BUSINESS
            tier_name = "business"
        else:
            raise HTTPException(status_code=400, detail=f"Invalid tier: {tier}. Must be 'pro' or 'business'.")

        # Validate Stripe configuration
        if not STRIPE_SECRET_KEY:
            raise HTTPException(status_code=500, detail="Stripe is not configured. Missing STRIPE_SECRET_KEY.")

        if not price_id:
            raise HTTPException(status_code=500, detail=f"Stripe is not configured. Missing STRIPE_PRICE_ID_{tier.upper()}.")

        print(f"Processing subscription request for user: {user['email']} - Tier: {tier_name}")

        stripe_customer_id = user.get('stripe_custom')
        stripe_subscription_id = user.get('stripe_subscri')

        # Check if user already has an active subscription
        if stripe_subscription_id:
            print(f"User {user['email']} has existing subscription: {stripe_subscription_id}")

            try:
                # Retrieve the current subscription
                subscription = stripe.Subscription.retrieve(stripe_subscription_id)

                # Check if subscription is active
                if subscription.status in ['active', 'trialing']:
                    print(f"Upgrading/downgrading existing subscription to {tier_name}")

                    # Get the new price details to check currency
                    new_price = stripe.Price.retrieve(price_id)
                    current_price = subscription['items']['data'][0]['price']

                    # Check if currencies match
                    if new_price.currency != current_price.currency:
                        print(f"Currency mismatch: existing={current_price.currency}, new={new_price.currency}")
                        print(f"Canceling old subscription and creating new checkout")

                        # Cancel the existing subscription at period end
                        stripe.Subscription.modify(
                            stripe_subscription_id,
                            cancel_at_period_end=True
                        )

                        # We'll create a new checkout session below
                        # Don't return here, let it fall through to checkout creation
                    else:
                        # Same currency - can modify in place
                        stripe.Subscription.modify(
                            stripe_subscription_id,
                            items=[{
                                'id': subscription['items']['data'][0].id,
                                'price': price_id,
                            }],
                            proration_behavior='always_invoice',
                            metadata={
                                'user_id': user['id'],
                                'tier': tier_name
                            }
                        )

                        # Update user tier in database
                        supabase_client.table("users").update({
                            "tier": tier_name,
                            "stripe_price_i": price_id
                        }).eq("id", user['id']).execute()

                        print(f"Subscription updated successfully to {tier_name}")
                        return {
                            "message": f"Subscription updated to {tier_name.capitalize()}",
                            "redirect_url": "/app?upgrade=success"
                        }
                else:
                    print(f"Existing subscription is {subscription.status}, creating new checkout")
            except stripe.error.InvalidRequestError as e:
                print(f"Subscription not found or invalid: {str(e)}, creating new checkout")

        # If no active subscription, create new customer if needed
        if not stripe_customer_id:
            print(f"Creating new Stripe customer for {user['email']}")
            customer = stripe.Customer.create(
                email=user['email'],
                metadata={'user_id': user['id']}
            )
            stripe_customer_id = customer.id
            print(f"Created Stripe customer: {stripe_customer_id}")

            supabase_client.table("users").update({
                "stripe_custom": stripe_customer_id
            }).eq("id", user['id']).execute()

        # Create new checkout session
        print(f"Creating checkout session with price: {price_id} for tier: {tier_name}")

        # Use production URL or localhost based on environment
        base_url = os.getenv("BASE_URL", "https://ssml2mp3.com")

        checkout_session = stripe.checkout.Session.create(
            customer=stripe_customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f'{base_url}/app?success=true',
            cancel_url=f'{base_url}/pro?canceled=true',
            metadata={
                'user_id': user['id'],
                'tier': tier_name
            }
        )

        print(f"Checkout session created: {checkout_session.url}")
        return {"checkout_url": checkout_session.url}

    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        print(f"Error creating checkout session: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@billing_router.get("/customer-portal")
async def customer_portal(user = Depends(get_current_user)):
    """Create Stripe customer portal session for managing subscription"""
    try:
        stripe_customer_id = user.get('stripe_custom')

        if not stripe_customer_id:
            raise HTTPException(status_code=400, detail="No Stripe customer found")

        portal_session = stripe.billing_portal.Session.create(
            customer=stripe_customer_id,
            return_url='https://ssml2mp3.com/app',
        )

        return {"portal_url": portal_session.url}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@billing_router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        tier = session['metadata'].get('tier', 'pro')  # Default to 'pro' for backwards compatibility
        customer_id = session['customer']
        subscription_id = session['subscription']

        # Get the subscription to find the price ID
        subscription = stripe.Subscription.retrieve(subscription_id)
        price_id = subscription['items']['data'][0]['price']['id']

        supabase_client.table("users").update({
            "tier": tier,
            "stripe_custom": customer_id,
            "stripe_subscri": subscription_id,
            "stripe_price_i": price_id
        }).eq("id", user_id).execute()

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        customer_id = subscription['customer']

        supabase_client.table("users").update({
            "tier": "free",
            "stripe_subscri": None
        }).eq("stripe_custom", customer_id).execute()

    return {"status": "success"}