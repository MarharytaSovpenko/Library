from django.db import models
from django.db.models import CheckConstraint, Q, F

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return = models.DateField()
    actual_return = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            CheckConstraint(
                check=(
                        Q(expected_return__gt=F("borrow_date"))
                        & Q(actual_return__gt=F("borrow_date"))
                ),
                name="check_start_date",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user.email} - {self.book.title}"
