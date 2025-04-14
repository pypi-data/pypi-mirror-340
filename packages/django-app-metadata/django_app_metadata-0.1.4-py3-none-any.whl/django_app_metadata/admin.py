from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export import resources
from import_export import fields
from django_model_helper.admin import WithEnabledStatusFieldsAdmin
from django_model_helper.admin import WithDeletedStatusFieldsAdmin
from .models import Category
from .models import Config


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "display_order",
    ]
    search_fields = [
        "title",
    ]
    list_editable = [
        "display_order",
    ]
    readonly_fields = [
        "add_time",
        "mod_time",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "display_order",
                ],
            },
        )
    ]


class ConfigResource(resources.ModelResource):
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, "title"),
    )

    class Meta:
        model = Config


class ConfigAdmin(
    ImportExportModelAdmin,
    WithEnabledStatusFieldsAdmin,
    WithDeletedStatusFieldsAdmin,
    admin.ModelAdmin,
):
    resource_classes = [
        ConfigResource,
    ]
    list_display = [
        "key",
        "description",
        "category",
        "is_valid",
        "enabled",
        "deleted",
        "published",
        "mod_time",
    ]
    list_filter = [
        "is_valid",
        "type",
        "published",
        "enabled",
        "deleted",
        "category",
    ]
    search_fields = [
        "key",
        "description",
        "data_raw",
    ]
    fieldsets = [
        (
            "基础信息",
            {
                "fields": [
                    "category",
                    "key",
                    "description",
                    "type",
                    "data_raw",
                    "data_file",
                    "is_valid",
                    "enabled",
                    "deleted",
                    "published",
                ]
            },
        ),
        (
            "其它信息",
            {
                "fields": [
                    "add_time",
                    "mod_time",
                    "enabled_time",
                    "disabled_time",
                    "published_time",
                    "unpublished_time",
                    "deleted_time",
                ]
            },
        ),
    ]
    readonly_fields = [
        "add_time",
        "mod_time",
        "enabled_time",
        "disabled_time",
        "published_time",
        "unpublished_time",
        "deleted_time",
        "is_valid",
    ]
    autocomplete_fields = [
        "category",
    ]


admin.site.register(Config, ConfigAdmin)
admin.site.register(Category, CategoryAdmin)
