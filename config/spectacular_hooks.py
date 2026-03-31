from drf_spectacular.extensions import OpenApiAuthenticationExtension


# --------------------------------------------------
# Fix: IAMAuthentication not recognized by drf-spectacular
# --------------------------------------------------
class IAMAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = "apps.authn.authentication.IAMAuthentication"
    name = "BearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }


# --------------------------------------------------
# Group endpoints by URL prefix using tags
# Postprocessing modifies the final schema dict directly — guaranteed to work
# --------------------------------------------------
_PATH_TAGS = [
    ("/api/v1/auth/",       "Authentication"),
    ("/api/v1/me/",         "Identity"),
    ("/api/v1/identity/",   "Identity"),
    ("/api/v1/department/", "Departments"),
    ("/api/v1/access/",     "Access Control"),
    ("/api/v1/audit/",      "Audit"),
]


def assign_tags_postprocess(result, generator, request, public, **kwargs):
    for path, path_item in result.get("paths", {}).items():
        for method, operation in path_item.items():
            if not isinstance(operation, dict):
                continue
            for prefix, tag in _PATH_TAGS:
                if path.startswith(prefix):
                    operation["tags"] = [tag]
                    break
    return result
