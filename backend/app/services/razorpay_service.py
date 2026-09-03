# pyrefly: ignore [missing-import]
import razorpay
from app.config import settings

client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))

def retry_payment(payment_id: str, amount: float) -> dict:
    """
    Attempts to retry a failed payment in test mode.
    Razorpay doesn't have a direct 'retry' endpoint for one-off payments —
    in practice this means creating a new payment link/order for the same amount
    and same customer. For subscriptions, you'd use the subscription retry flow instead.
    """
    try:
        order = client.order.create({
            "amount": int(amount * 100),  # Razorpay expects paise
            "currency": "INR",
            "notes": {"retry_for_payment_id": payment_id},
        })
        return {"success": True, "order_id": order["id"]}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_card_update_link(customer_id: str) -> dict:
    """
    Mocked for now — in production this would trigger an SMS/WhatsApp/email
    with a Razorpay-hosted card update page.
    """
    return {"success": True, "message": f"Card update link sent to {customer_id}"}

