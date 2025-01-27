
# BaseApp Message Templates - Django

This app provides the integration of custom e-mail and sms template configuration with The SilverLogic's [BaseApp](https://bitbucket.org/silverlogic/baseapp-django-v2).

## Install the package

Add to `requirements/base.txt`:

```bash
git+https://bitbucket.org/silverlogic/baseapp-message-templates-django.git
```

## Configure template settings

```py
TEMPLATES  =  [
	{
		"BACKEND": "django_jinja.backend.Jinja2",
		"DIRS": [str(APPS_DIR  /  "templates")], # change this to wherever your base templates are stored
		"APP_DIRS": True,
		"OPTIONS": {
			"match_extension": ".j2",
			"constants": {"URL": URL, "FRONT_URL": FRONT_URL},
		},
	},
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"DIRS": [
			str(APPS_DIR  /  "templates"), # change this to wherever your base templates are stored
		],
		"APP_DIRS": True,
		"OPTIONS": {
			"context_processors": [
				"django.template.context_processors.debug",
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.contrib.messages.context_processors.messages",
			],
			"libraries": {
				"filter": "baseapp_message_templates.filters",
			},
		},
	},
]
```
  
## Set default base template (optional)

If you want to use a default base template that your emails will automatically inherit from, add the path to that template to your settings. Note that this base template won't apply to e-mails that are created on SendGrid.

```py
DEFAULT_EMAIL_TEMPLATE = [your_path]
```

## Setup SendGrid credentials (optional)

If you want to use SendGrid to send mail, add these settings to your `settings/base.py`:

```py
DJMAIL_REAL_BACKEND = "sendgrid_backend.SendgridBackend"

SENDGRID_API_KEY = env("SENDGRID_API_KEY")

SENDGRID_SANDBOX_MODE_IN_DEBUG = False
```

## EmailTemplate model

This model is responsible for customizing your e-mail template and sending mail. At minimum, an instance of `EmailTemplate` must have a unique name and either a SendGrid template ID or some custom HTML content. The `subject`, `plain_text_content`, and `attachments` are optional.

### Static attachments

`Attachment` instances that are linked to an `EmailTemplate` represent static files that will be attached to every message sent via that template, regardless of recipient or context. These attachments will be sent regardless of whether the e-mail is sent through a SendGrid template or a custom HTML template.

## Sending mail via SendGrid template

If a `sendgrid_template_id` is provided on an instance of `EmailTemplate`, a SendGrid template can be used to send mail. In order to send mail via SendGrid template, at least one `Personalization` must first be created. Each `Personalization`will contain the email of a recipient and any context that must be provided to the template. A `Personalization` can be created like so:

```py
from baseapp_message_templates.sendgrid import get_personalization

personalization = get_personalization("john@test.com", {"message": "Hello there."})
```

### Sending mail to one recipient

The `send_via_sendgrid` method of `EmailTemplate` can be used to send a single email to one recipient. The method takes one `Personalization` as an argument, as well as an optional list of `attachments` that can be sent along with this particular message.

```py
from baseapp_message_templates.models import EmailTemplate
from baseapp_message_templates.sendgrid import get_personalization

template = EmailTemplate.objects.get("Test Template")

personalization = get_personalization("john@test.com", {"message": "Hello there."})

template.send_via_sendgrid(personalization)
```

### Sending mail to multiple recipients

The `mass_send_via_sendgrid` method of `EmailTemplate` can be used to send multiple instances of a template to multiple recipients. The method takes a list of `Personalization` objects as an argument, and each `Personalization` will send a separate message to each recipient with its own context.

```py
from baseapp_message_templates.models import EmailTemplate
from baseapp_message_templates.sendgrid import get_personalization


template = EmailTemplate.objects.get("Test Template")

personalization_1 = get_personalization("john@test.com", {"message": "Hello there."})
personalization_2 = get_personalization("jane@test.com", {"message": "Good morning."})
personalization_list = [personalization_1, personalization_2]

template.mass_send_via_sendgrid(personalization_list)
```

## Sending Mail via custom HTML

If you aren't using SendGrid and instead wish to provide your custom HTML content directly to the `EmailTemplate` instance, this can be done through the `html_content` field. Once `html_content` has been provided, the `send` method of the `EmailTemplate` can be used to send mail. 

### Adding HTML content via Django Admin

When adding HTML content to a template through the Django Admin, the "source" option must be selected in the text field.

![enter image description here](https://i.ibb.co/3yCBRy3/Screen-Shot-2023-06-12-at-12-48-17-PM.png)

After saving, the content of the text field will no longer contain the raw HTML that was added. This is a small caveat of the Django Admin. The "raw HTML" field that is displayed underneath the input will display the actual raw HTML content that is currently added to the instance. 

![enter image description here](https://i.ibb.co/0jgms7c/Screen-Shot-2023-06-12-at-12-48-32-PM.png)

### Sending

Once you've added `html_content` to your template, either programatically or through the Django Admin, a message can now be sent through the `send` method of `EmailTemplate`. 

The only required parameter for `send` is `recipients`, which is a list of one or more strings containing the e-mail addresses of the recipients. A `context` dict can be passed in optionally if the HTML content is expected one or more key/value pairs to be provided.

The `use_base_template` flag will determine whether this message should extend from a base HTML template. If set to `True`, the message will extend from the base template that is located at a certain path. This path will either be the value of `extended_with` if provided, or the value of `DEFAULT_EMAIL_TEMPLATE`. 

Finally, the `attachments` parameter is a list of one or more files that will be send along with this particular message. These attachments will be sent along with any static attachments that have been attached to the template itself through `Attachment`.

```py
from baseapp_message_templates.models import EmailTemplate


template = EmailTemplate.objects.get("Test Template")

recipients = ["john@test.com"]
context = {"content": "Hello."}
extended_with = "apps/base/templates/test-template.html"

template.send(recipients, context, True, extended_with)
```

### SmsTemplate Model

The `SmsTemplate` model has two fields:
* `name`: this name must be unique.
* `message`: this is a textfield and does not accept HTML

### Creating migrations for your template

Once you have installed the package you can simply create a migration to input your templates like so:
```py
from __future__ import unicode_literals

from django.db import migrations


def create_object(sms_template, name, message):
    sms_template.objects.create(
        name=name,
        message=message,
    )


def create_sms_templates(apps, schema_migration):
    sms_template = apps.get_model("baseapp_message_templates", "SmsTemplate")

    create_object(
        sms_template,
        "First Template",
        """
            Hello, {{ some_variable }}.
        """,
    )

    create_object(
        sms_template,
        "Second template",
        """
            Hello, {{ some_other_variable }}.
        """,
    )


class Migration(migrations.Migration):
    dependencies = [("some_app", "0002_some_previus_migration")]

    operations = [migrations.RunPython(create_sms_templates, migrations.RunPython.noop)]

```

OBS: make sure that the variables are the right ones that you will pass as context when getting the message.

### Get the template message
To get the template message you can simply use the util functions `get_sms_message` from `sms_utils` passing as first parameter the name of the template and the second parameter the context with your variables if needed.

```py
from baseapp_message_templates.sms_utils import get_sms_message

context = {"some_variable": "some_value"}

message = get_sms_message("First Template", context)
```
