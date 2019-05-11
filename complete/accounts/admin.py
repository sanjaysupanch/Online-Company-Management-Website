from django.contrib import admin
from accounts.models import UserProfile,Company,teamtable,GroupUserTable,Todolist,work_assigned,to_notify,upload_file,filetable,foldertable

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(teamtable)
admin.site.register(GroupUserTable)
admin.site.register(Todolist)
admin.site.register(work_assigned)
admin.site.register(to_notify)
admin.site.register(upload_file)
admin.site.register(filetable)
admin.site.register(foldertable)
