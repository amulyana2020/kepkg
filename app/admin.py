from django.contrib import admin
from .models import Submission, Review, Reviewer, Decision, Profile

# Register your models here.
admin.site.register(Submission)
admin.site.register(Review)
admin.site.register(Reviewer)
admin.site.register(Decision)
admin.site.register(Profile)