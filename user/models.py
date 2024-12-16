from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    # Gender choices for the gender field
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('officestaff', 'Office Staff'),
        ('librarian', 'Librarian'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

  # Role fields
    is_office_staff = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    # Personal details
    user_id = models.CharField(
        max_length=50, unique=True, help_text="Unique ID for the librarian", blank=True, null=True
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=20, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    joining_date = models.DateField(null=True, blank=True)
    whatsapp = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True,)
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Monthly salary of the librarian", blank=True, null=True
    )
    department = models.CharField(
        max_length=100, help_text="Department the staff belongs to, e.g., Accounts, Admissions", blank=True, null=True
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    USERNAME_FIELD = 'email'  # Use email as the unique identifier for login
    REQUIRED_FIELDS = ['username']  # username is still required but won't be used for login

    # Override groups and user_permissions to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return f"{self.email} - {self.role}"

    

