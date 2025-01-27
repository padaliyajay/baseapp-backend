# Django Cloudflare Stream Field

This app provides integration with Cloudflare Stream, where you can upload directly to Cloudflare using TUS protocol.

## Install the package

Add to `requirements/base.txt`:

```bash
baseapp-cloudflare-stream-field @ git+https://github.com/silverlogic/baseapp-backend.git@v0.1#subdirectory=baseapp-cloudflare-stream-field
```

Add the following to your `settings/base.py`:

```python
# Cloudflare
CLOUDFLARE_ACCOUNT_ID = env("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = env("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_AUTH_EMAIL = env("CLOUDFLARE_AUTH_EMAIL")

# Make sure to add the task routing for refresh_from_cloudflare and generate_download_url
CELERY_TASK_ROUTES = {
    "baseapp_cloudflare_stream_field.tasks.refresh_from_cloudflare": {
        "exchange": "default",
        "routing_key": "default",
    },
    "baseapp_cloudflare_stream_field.tasks.generate_download_url": {
        "exchange": "default",
        "routing_key": "default",
    },
}
```

Include the URLs in your main `urls.py` file:

```python
re_path(r"^cloudflare-stream-upload/", include("baseapp_cloudflare_stream_field.urls")),
```

And if you use Django REST Framework, add the following to your router:

```python
# Cloudflare Stream Upload
from baseapp_cloudflare_stream_field.rest_framework import CloudflareStreamUploadViewSet

router.register(
    r"cloudflare-stream-upload", CloudflareStreamUploadViewSet, basename="cloudflare-stream-upload"
)
```

### Allow CORS Headers

You need to add `tus-resumable, upload-length, upload-metadata, upload-creator` to your CORS header. Add the following to `settings/base.py`:

```python
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "tus-resumable",
    "upload-length",
    "upload-metadata",
    "upload-creator"
]
```

## Usage

Import and use the field in your models file:

```python
from baseapp_cloudflare_stream_field import CloudflareStreamField

class Post(models.Model):
    video = CloudflareStreamField(null=True, blank=True, downloadable=False)
```

If you set `downloadable` to `True` it will automatically trigger a task to generate and save the download url at `obj.video['meta']['download_url']`.

`CloudflareStreamField` inherits from `JSONField` so you can use any look it provides, like filter only for videos fully processed by Cloudflare:

```python
Post.objects.filter(video__status__state="ready")
```
