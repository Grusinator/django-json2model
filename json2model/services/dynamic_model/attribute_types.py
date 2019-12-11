from datetime import datetime

import mutant.contrib.boolean.models
import mutant.contrib.file.models
import mutant.contrib.numeric.models
import mutant.contrib.temporal.models
import mutant.contrib.text.models
from django.contrib.sessions.backends import file

ATTRIBUTE_TYPES = {
    str: mutant.contrib.text.models.TextFieldDefinition,
    float: mutant.contrib.numeric.models.FloatFieldDefinition,
    bool: mutant.contrib.boolean.models.NullBooleanFieldDefinition,
    int: mutant.contrib.numeric.models.BigIntegerFieldDefinition,
    file: mutant.contrib.file.models.FilePathFieldDefinition,
    datetime: mutant.contrib.temporal.models.DateTimeFieldDefinition,
    # ('varchar', mutant.contrib.text.models.CharFieldDefinition),
    #
    # ('integer', mutant.contrib.numeric.models.BigIntegerFieldDefinition),
    # ('small_integer', mutant.contrib.numeric.models.SmallIntegerFieldDefinition),
    # ('float', mutant.contrib.numeric.models.FloatFieldDefinition),
    #
    # ('null_boolean', mutant.contrib.boolean.models.NullBooleanFieldDefinition),
    # ('boolean', mutant.contrib.boolean.models.BooleanFieldDefinition),
    #
    # ('file', mutant.contrib.file.models.FilePathFieldDefinition),
    #
    # ('foreign_key', mutant.contrib.related.models.ForeignKeyDefinition),
    # ('one_to_one', mutant.contrib.related.models.OneToOneFieldDefinition),
    # ('many_to_many', mutant.contrib.related.models.ManyToManyFieldDefinition),
    #
    # ('ip_generic', mutant.contrib.web.models.GenericIPAddressFieldDefinition),
    # ('ip', mutant.contrib.web.models.IPAddressFieldDefinition),
    # ('email', mutant.contrib.web.models.EmailFieldDefinition),
    # ('url', mutant.contrib.web.models.URLFieldDefinition),
    #
    # ('date', mutant.contrib.temporal.models.DateFieldDefinition),
    # ('time', mutant.contrib.temporal.models.TimeFieldDefinition),
    # ('datetime', mutant.contrib.temporal.models.DateTimeFieldDefinition),
}
