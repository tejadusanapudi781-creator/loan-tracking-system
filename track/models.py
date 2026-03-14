from django.db import models
from django.utils import timezone

class Borrower(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, default="")

    def __str__(self):
        return self.name

class Loan(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    )

    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def save(self, *args, **kwargs):
        self.total_due = self.principal_amount + self.interest_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.borrower.name} - ₹{self.principal_amount}"

class Collection(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='collections')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    collection_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.loan.borrower.name} - ₹{self.amount}"
