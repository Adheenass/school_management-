from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class FeesHistory(models.Model):
   
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='fees_history',
        help_text="The user who paid the fees."
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Amount of fees paid."
    )
    payment_date = models.DateField(
        auto_now_add=True, 
        help_text="The date when the fees were paid."
    )
    
    transaction_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="Transaction ID for online or card payments."
    )
    remarks = models.TextField(
        blank=True, 
        null=True, 
        help_text="Additional details or remarks about the payment."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def clean(self):
        # Validate that the user has the "STUDENT" role
        if self.user.role != 'student':
            raise ValidationError(f"Only users with the role 'STUDENT' can make fee payments.")
    
    def save(self, *args, **kwargs):
        # Call the clean method before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Fees of {self.amount} paid by {self.user.email} on {self.payment_date}"



class LibraryHistory(models.Model):
    STATUS_CHOICES = [
        ('BORROWED', 'Borrowed'),
        ('RETURNED', 'Returned'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},  # Ensure only students can borrow books
        related_name='library_history',
        verbose_name="Student"
    )
    book_title = models.CharField(max_length=255, verbose_name="Book Title")
    borrowed_date = models.DateField(auto_now_add=True, verbose_name="Borrowed Date")
    due_date = models.DateField(verbose_name="Due Date")
    returned_date = models.DateField(null=True, blank=True, verbose_name="Returned Date")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='BORROWED', verbose_name="Status")

    def clean(self):
        """
        Ensure only students can borrow books and validate dates.
        """
        if self.user.role != 'STUDENT':
            raise ValidationError("Only users with the role 'STUDENT' can borrow books.")
        if self.returned_date and self.returned_date < self.borrowed_date:
            raise ValidationError("Returned date cannot be earlier than the borrowed date.")
        if self.returned_date and self.returned_date > self.due_date:
            raise ValidationError("Returned date cannot be later than the due date.")

    def save(self, *args, **kwargs):
        """
        Automatically update the status based on whether the book has been returned.
        """
        if self.returned_date:
            self.status = 'RETURNED'
        else:
            self.status = 'BORROWED'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book_title} ({self.user.username})"

    class Meta:
        verbose_name = "Library Borrowing Record"
        verbose_name_plural = "Library Borrowing Records"
        ordering = ['-borrowed_date']
