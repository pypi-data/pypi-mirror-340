from typing import TYPE_CHECKING

import rules

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser


@rules.predicate
def is_admin(user: "AbstractBaseUser") -> bool:
    return user.is_authenticated and user.is_active and user.is_staff


rules.add_rule("is_admin", is_admin)
