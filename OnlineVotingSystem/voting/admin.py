from django.contrib import admin

# Register your models here.
from .models import Candidate
# voting/admin.py
from .models import Vote

admin.site.register(Candidate)
admin.site.register(Vote)


