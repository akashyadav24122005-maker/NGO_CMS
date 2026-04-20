from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Donation(models.Model):
    donor_name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.IntegerField()

    order_id = models.CharField(max_length=200, blank=True, null=True)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    signature = models.CharField(max_length=500, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Success', 'Success'),
            ('Failed', 'Failed'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount}"


class Volunteer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    interest = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title