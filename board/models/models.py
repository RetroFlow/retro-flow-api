# from django.db import models
#
#
# class ItemStatus(models.Model):
#     name = models.CharField(max_length=64)
#     description = models.TextField(blank=True, null=True)
#
#
# class BoardSettings(models.Model):
#     sprint_start_date = models.DateField()
#
#     sprint_duration = models.DurationField()
#     discussion_period = models.DurationField()
#
#     active_statuses = models.ManyToManyField('ItemStatus')
#     custom_statuses = models.ManyToManyField('ItemStatus')
#
#
# class Comment(models.Model):
#     item = models.ForeignKey('Item', related_name='comments', on_delete=models.CASCADE)
#     text = models.TextField(verbose_name='Comment body')
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
# class Item(models.Model):
#     column = models.ForeignKey('Column', related_name='items')
#     heading = models.CharField(max_length=125)
#
#     description = models.TextField(blank=True, null=True)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
# class Column(models.Model):
#     name = models.CharField(max_length=40)
#     board = models.ForeignKey('Board', related_name='columns')
#
#
# class Board(models.Model):
#     settings = models.OneToOneField('BoardSettings')
#
#     created_at = models.DateTimeField(auto_now_add=True)
