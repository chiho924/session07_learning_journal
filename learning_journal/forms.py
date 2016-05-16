from wtforms import (
    Form,
    TextField,
    TextAreaField,
    validators,
    HiddenField,
)

from .models import (
    DBSession,
    MyModel,
    Entry,
    )

strip_filter = lambda x: x.strip() if x else None


class EntryCreateForm(Form):
    """
    This class is the form that allows the user to enter a new entry.  It is inherited from
    Form.
    """

    # This is the TextAreaField that allows the user to enter the title of Entry.  The minimum character of
    # the content in this TextAreaField is 1, and the maximum character is 255.
    title = TextAreaField(
        'Entry title',
        [validators.Length(min=1, max=255)],
        filters=[strip_filter]
    )
    # The is the TextAreaField that allows the user to enter the body of Entry.  The minimum character of the
    # content in this TextAreaField is 1.
    body = TextAreaField(
        'Entry body',
        [validators.Length(min=1)],
        filters=[strip_filter]
    )


class EntryEditForm(EntryCreateForm):
    """
    This class is the form that allows the user to edit the database entry.  It is inherited from
    EntryCreateForm.
    """
    pass
