from django.db import models
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save , post_delete

User = get_user_model()


class Product (models.Model) : 
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title


@receiver([post_delete, post_save], sender=Product)
def update_cache(instance, **kwargs) : 
    cache.delete_many([
        'products',
        f'products-{instance.id}'
    ])