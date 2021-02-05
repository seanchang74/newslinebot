from django.contrib import admin
from newslinebot.models import users

class usersAdmin(admin.ModelAdmin):
    list_display = ('uid','state')
admin.site.register(users, usersAdmin)

