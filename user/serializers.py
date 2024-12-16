from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'phone_number', 'password', 'is_office_staff', 'is_librarian','role']

    def create(self, validated_data):
        # Create the user with a hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            full_name=validated_data.get('full_name'),
            phone_number=validated_data.get('phone_number'),
            password=validated_data['password'],
            is_office_staff=validated_data.get('is_office_staff', False),
            is_librarian=validated_data.get('is_librarian', False),
        )
        return user
