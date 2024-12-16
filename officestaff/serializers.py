from rest_framework import serializers
from officestaff.models import FeesHistory,LibraryHistory



class FeesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesHistory
        fields = '__all__'



class LibraryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryHistory
        fields = '__all__'  # Include all fields in the model
        read_only_fields = ['borrowed_date', 'status']  # Prevent modification of certain fields

    def validate_user(self, value):
        """
        Ensure the user has the role 'STUDENT'.
        """
        if value.role != 'student':
            raise serializers.ValidationError("Only users with the role 'STUDENT' can borrow books.")
        return value

    def validate(self, data):
        """
        Custom validation for borrowing and return dates.
        """
        returned_date = data.get('returned_date')
        borrowed_date = self.instance.borrowed_date if self.instance else data.get('borrowed_date')
        due_date = data.get('due_date')

        if returned_date:
            if returned_date < borrowed_date:
                raise serializers.ValidationError("Returned date cannot be earlier than the borrowed date.")
            if returned_date > due_date:
                raise serializers.ValidationError("Returned date cannot be later than the due date.")

        return data
