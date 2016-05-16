import datetime

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPFound
from .forms import EntryCreateForm
from .forms import EntryEditForm

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    Entry,
    )

this_id = 0 # the ID of an entry


@view_config(route_name='home', renderer='templates/list.jinja2')
def index_page(request):
    """
    Returns the dictionary of all the entries in the Entry database.
    """
    # Get all entries from the Entry database.
    entries = Entry.all()
    return {'entries': entries}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
# and update this view function:
def view(request):
    """
    Returns the dictionary of the entry for viewing.
    """
    global this_id
    # Get the id of the entry to be viewed.
    this_id = request.matchdict.get('id', -1)
    # Get the entry of the given id.
    entry = Entry.by_id(this_id)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(route_name='action', match_param='action=create', renderer='templates/edit.jinja2')
def create(request):
    """
    Creates a new entry and populates it to the Entry database.  If this is successful, the web browser will
    return back to the home page.  Otherwise, a dictionary of form and action will be returned.
    """
    entry = Entry()
    # Create a form for a new entry.
    form = EntryCreateForm(request.POST)

    if request.method == 'POST' and form.validate():

        # Populate the entry from the form.
        form.populate_obj(entry)
        # Add the new entry to the database session.
        DBSession.add(entry)

        return HTTPFound(location=request.route_url('home'))

    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='action', match_param='action=edit', renderer='templates/edit_entry.jinja2')
def update(request):
    # Use the global variable of the ID.
    global this_id

    # Get the Entry object corresponding to the given ID.
    entry = Entry.by_id(this_id)

    # Create an edit form object.
    form = EntryEditForm(request.POST)

    if request.method == 'POST' and form.validate():

        if entry is not None and form is not None:
            # Update the title attribute of the Entry object.
            entry.title = form.title.data
            # Update the body attribute of the Entry object.
            entry.body = form.body.data
            # Update the edited attribute of the Entry object.
            entry.edited = datetime.datetime.utcnow()

        return HTTPFound(location=request.route_url('detail', id=this_id))

    return {'form': form, 'action': request.matchdict.get('action')}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
