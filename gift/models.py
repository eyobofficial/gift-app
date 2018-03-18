from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Catagory(models.Model):
    """
    Abstracts Gift Catagory
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self, *args, **kwargs):
        return reverse('gifts:catagory-detail', args=[str(self.pk)])

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Abstracts a gift Tags
    """
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Package(models.Model):
    """
    Abstracts Gift Product Package
    Example: Premium Valentine Package
    """
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='products/thumbnails/')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tags = models.ManyToManyField(Tag)
    publish = models.BooleanField(default=False)
    created_at = models.DateTimeField('Created date', auto_now_add=True)
    updated_at = models.DateTimeField('Last updated', auto_now=True)

    class Meta:
        verbose_name = 'Gift Package'
        verbose_name_plural = 'Gift Packages'
        ordering = ['publish', '-updated_at', 'name']

    def get_absolute_url(self, *args, **kwargs):
        return reverse('gifts:product-detail', args=[str(self.pk)])

    def __str__(self):
        return self.name


class PackagePictures(models.Model):
    """
    Abstracts Picture for a particular product package
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='products/pictures/')
    created_at = models.DateTimeField('Created date', auto_now_add=True)
    updated_at = models.DateTimeField('Last updated', auto_now=True)

    class Meta:
        ordering = ['package', '-updated_at', ]

    def __str__(self):
        return '{} picture'.format(self.package)


class Gift(models.Model):
    """
    Abstracts a Gift by a user
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='Gift Provider',
    )
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    receiver_name = models.CharField('Gift Reciever Full Name', max_length=100)
    receiver_address = models.CharField('Gift Receiver Address', max_length=255)
    receiver_phone_number1 = models.CharField(max_length=30)
    receiver_phone_number2 = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )
    gift_date = models.DateField(help_text='Please specify when to deliver the gift')
    gift_message = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Short message to be wrapped with your gift',
    )
    created_at = models.DateTimeField('Created date', auto_now_add=True)
    updated_at = models.DateTimeField('Last updated', auto_now=True)

    class Meta:
        ordering = ['-updated_at', ]

    def get_absolute_url(self, *args, **kwargs):
        return reverse('gifts:gift-detail', args=[str(self.pk)])

    def __str__(self):
        return self.package


class PaymentMethod(models.Model):
    """
    Abstracts a Payment Method or Gateway that is going to be provided
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='payment_methods/thumbnails/')
    publish = models.BooleanField(default=False)

    class Meta:
        ordering = ['-publish', ]

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Abstracts an Order of a gift to be delivered
    """
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Payment Pending'),
        ('completed', 'Payment Completed'),
        ('failed', 'Payment Failed')
    )
    DELIVERY_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed')
    )
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    gift_price = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(
        max_length=30,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
    )
    delivery_status = models.CharField(
        max_length=30,
        choices=DELIVERY_STATUS_CHOICES,
        default='pending',
    )
    created_at = models.DateTimeField('Created date', auto_now_add=True)
    updated_at = models.DateTimeField('Last updated', auto_now=True)

    class Meta:
        ordering = ['payment_status', 'delivery_status']

    def get_absolute_url(self, *args, **kwargs):
        return reverse('gifts:order-detail', args=[str(self.pk)])

    def __str__(self):
        return self.gift
    