# from django.contrib import admin
# from django.contrib import admin
# from .models import ProgressHistory

# @admin.register(ProgressHistory)
# class ProgressHistoryAdmin(admin.ModelAdmin):
#     list_display = (
#         'mentorship_loop',
#         'event_type',
#         'event_date',
#         'user',
#         'title',
#     )
#     list_filter = (
#         'event_type',
#         'event_date',
#         'mentorship_loop',
#         'user',
#     )
#     search_fields = (
#         'mentorship_loop__mentor__user__first_name',
#         'mentorship_loop__mentee__user__first_name',
#         'user__first_name',
#         'title',
#         'description',
#     )
#     ordering = ('-event_date',)
#     readonly_fields = ('event_date',)
#     fieldsets = (
#         (None, {
#             'fields': (
#                 'mentorship_loop',
#                 'user',
#                 'event_type',
#                 'event_date',
#                 'title',
#                 'description',
#                 'extra_data',
#             )
#         }),
#     )
