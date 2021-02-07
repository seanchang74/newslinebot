from django.contrib import admin
from newslinebot.models import users
from newslinebot.models import comment

class usersAdmin(admin.ModelAdmin):
    list_display = ('uid','state')
admin.site.register(users, usersAdmin)

class commentAdmin(admin.ModelAdmin):
    list_display = ('cuid','name','email','comments')
admin.site.register(comment,commentAdmin)