# django-json2model
create django models dynamically from json data structures

# instructions
add the following apps to INSTALLED_APPS:
INSTALLED_APPS += (
    'mutant',
    'mutant.contrib.boolean',
    'mutant.contrib.temporal',
    'mutant.contrib.file',
    'mutant.contrib.numeric',
    'mutant.contrib.text',
    'mutant.contrib.web',
    'mutant.contrib.related',
)

set APP_LABEL_DYNAMIC_MODELS in settings.py to the app that you want the dynamic models to be placed in. Defaulting to json2model.

add the app json2model in INSTALLED_APPS as last.



