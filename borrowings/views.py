from typing import Type

from rest_framework.viewsets import ModelViewSet

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingDetailSerializer, BorrowingListSerializer


class BorrowingViewSet(ModelViewSet):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer

    def get_serializer_class(self) -> Type[BorrowingSerializer]:
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer
