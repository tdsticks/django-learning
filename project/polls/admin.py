from project.polls import models
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
    model = models.Choice
    extra = 3
    max_num = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {"fields" : ["question", "poops"]}),
        ("Date Information", {"fields" : ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ("question", "pub_date", "was_published_today")
    list_filter = ["pub_date"]
    search_fields = ["question"]
    date_hierarchy = "pub_date"

admin.site.register(models.Choice)
admin.site.register(models.Poll, PollAdmin)