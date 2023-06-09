from django.db import transaction
from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing
from users.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.CharField(source="book.title", read_only=True)
    user = serializers.CharField(source="user.title", read_only=True)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)


class BorrowingCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Borrowing
        fields = ("expected_return", "book", "user")

    @transaction.atomic
    def create(self, validated_data: dict) -> Borrowing:
        book = validated_data["book"]
        if book.inventory == 0:
            raise serializers.ValidationError(
                "The book is not available for borrowing"
            )
        book.inventory -= 1
        book.availability()
        book.save()
        borrowing = super().create(validated_data)

        return borrowing
