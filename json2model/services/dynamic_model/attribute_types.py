from datetime import datetime

from django.contrib.sessions.backends import file
from mutant.contrib.boolean.models import NullBooleanFieldDefinition
from mutant.contrib.file.models import FilePathFieldDefinition
from mutant.contrib.numeric.models import FloatFieldDefinition, BigIntegerFieldDefinition
from mutant.contrib.temporal.models import DateTimeFieldDefinition
from mutant.contrib.text.models import TextFieldDefinition

ATTRIBUTE_TYPES = {
    str: TextFieldDefinition,
    float: FloatFieldDefinition,
    bool: NullBooleanFieldDefinition,
    int: BigIntegerFieldDefinition,
    file: FilePathFieldDefinition,
    datetime: DateTimeFieldDefinition,
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
