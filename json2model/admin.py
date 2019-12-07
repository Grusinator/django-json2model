from django.contrib import admin
from mutant.models import FieldDefinitionBase, ModelDefinition

for field_type in FieldDefinitionBase._field_definitions.values():
    field_name = field_type.__name__
    attrs = {'model': field_type}
    FieldDefAdmin = type(f'{field_name}Admin', (admin.ModelAdmin,), attrs)
    admin.site.register(field_type, FieldDefAdmin)

admin.site.register(ModelDefinition)
