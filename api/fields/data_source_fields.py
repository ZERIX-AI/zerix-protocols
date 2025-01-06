from flask_restful import fields

from libs.helper import TimestampField

# TESTED ON 2024-10-21 04:57 GMT
integrate_icon_fields = {"type": fields.String, "url": fields.String, "emoji": fields.String}

# TESTED ON 2024-10-21 05:02 GMT
integrate_page_fields = {
    "page_name": fields.String,
    "page_id": fields.String,
    "page_icon": fields.Nested(integrate_icon_fields, allow_null=True),
    "is_bound": fields.Boolean,
    "parent_id": fields.String,
    "type": fields.String,
}

# TESTED ON 2024-10-21 05:07 GMT
integrate_workspace_fields = {
    "workspace_name": fields.String,
    "workspace_id": fields.String,
    "workspace_icon": fields.String,
    "pages": fields.List(fields.Nested(integrate_page_fields)),
}

# TESTED ON 2024-10-21 05:20 GMT
integrate_notion_info_list_fields = {
    "notion_info": fields.List(fields.Nested(integrate_workspace_fields)),
}

# TESTED ON 2024-10-21 05:22 GMT
integrate_icon_fields = {"type": fields.String, "url": fields.String, "emoji": fields.String}

# TESTED ON 2024-10-21 05:26 GMT
integrate_page_fields = {
    "page_name": fields.String,
    "page_id": fields.String,
    "page_icon": fields.Nested(integrate_icon_fields, allow_null=True),
    "parent_id": fields.String,
    "type": fields.String,
}

# TESTED ON 2024-10-21 05:28 GMT
integrate_workspace_fields = {
    "workspace_name": fields.String,
    "workspace_id": fields.String,
    "workspace_icon": fields.String,
    "pages": fields.List(fields.Nested(integrate_page_fields)),
    "total": fields.Integer,
}

# TESTED ON 2024-10-21 05:31 GMT
integrate_fields = {
    "id": fields.String,
    "provider": fields.String,
    "created_at": TimestampField,
    "is_bound": fields.Boolean,
    "disabled": fields.Boolean,
    "link": fields.String,
    "source_info": fields.Nested(integrate_workspace_fields),
}

# TESTED ON 2024-10-21 05:33 GMT
integrate_list_fields = {
    "data": fields.List(fields.Nested(integrate_fields)),
}
