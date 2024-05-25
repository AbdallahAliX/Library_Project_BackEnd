from django.contrib import admin
from .models import Bookitem
from .models import User
from .models import Borrowedbook
from .models import CurrentUser

admin.site.register(Bookitem)
admin.site.register(User)
admin.site.register(Borrowedbook)
admin.site.register(CurrentUser)
