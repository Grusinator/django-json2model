from django.contrib import admin
from mutant.models import FieldDefinitionBase, ModelDefinition

import json2model.services.dynamic_model.dynamic_model_admin_handler as admin_handler


def build_list_display(field_type):
    return ["name", ]


for field_type in FieldDefinitionBase._field_definitions.values():
    field_name = field_type.__name__
    list_display = build_list_display(field_type)
    attrs = {'model': field_type, 'list_display': list_display}
    FieldDefAdmin = type(f'{field_name}Admin', (admin.ModelAdmin,), attrs)
    admin.site.register(field_type, FieldDefAdmin)


class ModelDefinitionAdmin(admin.ModelAdmin):
    actions = ['register_in_admin', 'unregister_in_admin']

    def register_in_admin(self, request, queryset):
        for model_def in queryset:
            admin_handler.try_register_model_in_admin(model_def)

    def unregister_in_admin(self, request, queryset):
        for model_def in queryset:
            admin_handler.try_unregister_model_in_admin(model_def)


admin.site.register(ModelDefinition, ModelDefinitionAdmin)
