from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    REVIEWER = 1
    PREPARER = 2
    ACCOUNTANT = 3
    USER_TYPES = (
        (REVIEWER, 'Reviewer'),
        (PREPARER, 'Preparer'),
        (ACCOUNTANT, 'Accountant'),
    )
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    user_type = IntegerField(choices=USER_TYPES)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
