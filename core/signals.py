from django.db.models.signals import pre_save
from django.dispatch import receiver
from seller.models import Product
from core.models import Notifications

@receiver(pre_save, sender=Product)
def send_approval_notification(sender, instance, **kwargs):
    if instance.pk:
        old = Product.objects.get(pk=instance.pk)

        # Detect approval change
        if not old.status!="approved" and instance.status=="approved":
            Notifications.objects.create(
                user=instance.seller,
                title="Product Approved",
                message=f"Your product '{instance.name}' has been approved by admin."
            )