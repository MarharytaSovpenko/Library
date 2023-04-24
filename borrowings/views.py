from typing import Type

from rest_framework.viewsets import ModelViewSet

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingListSerializer
)


class BorrowingViewSet(ModelViewSet):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = self.queryset
            user_id = self.request.query_params.get("user_id")
            if user_id is not None:
                queryset = queryset.filter(user_id=user_id)
            return queryset.filter(
                is_active=self.request.query_params.get("is_active", True)
            )
        return self.queryset.filter(
            user=self.request.user,
            is_active=self.request.query_params.get("is_active", True)
        )

    def get_serializer_class(self) -> Type[BorrowingSerializer]:
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer
