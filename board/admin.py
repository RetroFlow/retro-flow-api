from django.contrib import admin
from .models import(
    UserRole, ItemStatus, BoardSettings, Board, Profile, Group, MembershipInfo, Item, Assignee, Team, Vote,
     PublicInfo,  Column, Sprint, Comment
)

admin.site.register(UserRole)
admin.site.register(ItemStatus)
admin.site.register(Board)
admin.site.register(BoardSettings)
admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(MembershipInfo)
admin.site.register(Item)
admin.site.register(Assignee)
admin.site.register(Team)
admin.site.register(Vote)
admin.site.register(Column)
admin.site.register(Sprint)
admin.site.register(Comment)
admin.site.register(PublicInfo)
