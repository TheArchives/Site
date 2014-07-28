__author__ = 'Gareth Coles'

import datetime
from pymongo.collection import ObjectId


class Type(object):
    def __init__(self, *args):
        self.types = args

    def validate(self, obj):
        for typ in self.types:
            if obj is typ or isinstance(obj, typ):
                return True
        return False


INFO = {
    "version": Type(int),  # For updates
    "base_url": Type(unicode),  # For relative URL paths and such
    "name": Type(unicode),  # The site's name
    "logo": Type(unicode),  # URL to the site logo
}

POST = {
    "id": Type(long),  # Sequential numerical post IDs
    "markdown": Type(unicode),  # Raw Markdown for editing
    "html": Type(unicode),  # Converted HTML, plus tokens
    "posted_by": Type(ObjectId),  # Who posted the post
    "posted_date": Type(datetime.datetime),  # When it was posted
    "edited": Type(bool),  # Whether it has been edited
    "edited_by": Type(ObjectId, None),  # Who edited the post
    "edited_date": Type(datetime.datetime, None),  # When it was edited
    "key": Type(unicode),  # Unique key for URL slugs
    "tags": Type(list),  # List of tags for filtering
    "views": Type(long)  # Number of /FULL PAGE/ post views
}

TAG = {
    "name": Type(unicode),  # Tag name
    "colour": Type(unicode)  # Display colour for tag
}

USER = {
    "id": Type(long),  # Sequential numerical user IDs
    "name": Type(unicode),  # Publicly displayed name
    "username": Type(unicode),  # Login username
    "password": Type(unicode),  # Hashed and salted password
    "salt": Type(unicode),  # Password salt
    "email": Type(unicode),  # Contact email address (for password resets, etc)
    "admin": Type(bool)  # If not an admin, can only post/edit own articles
}

PAGE = {
    "id": Type(long),  # Sequential numerical page IDs
    "markdown": Type(unicode),  # Raw Markdown for editing
    "html": Type(unicode),  # Converted HTML, plus tokens
    "posted_by": Type(ObjectId),  # Who posted the page
    "posted_date": Type(datetime.datetime),  # When it was posted
    "views": Type(long)  # Number of /FULL PAGE/ post views
}

URL = {
    "id": Type(long),  # Sequential numerical URL IDs
    "key": Type(unicode, None),  # Slug for URL redirection (None if not used)
    "target": Type(unicode),  # Full URL to redirect to
    "redirects": Type(long)  # Number of redirects in total
}

TOKEN = {  # Custom tokens only here
    "name": Type(unicode),  # The name of the token
    "code": Type(unicode)  # The token's raw Python code
}

BLOCK = {  # Blocks are switchable sections that can be placed in templates
    "name": Type(unicode),  # Name of the block
    "location": Type(unicode),  # What part of the template to add this to
    "markdown": Type(unicode),  # Raw Markdown for editing
    "html": Type(unicode)  # Converted HTML, plus tokens
}

schemas = {
    "info": INFO,  # Application info
    "posts": POST,  # Each post/article
    "tags": TAG,  # All of our custom tags
    "users": USER,  # All users
    "pages": PAGE,  # Static pages (aside from tags)
    "urls": URL,  # URL redirection that tracks number of clicks
    "tokens": TOKEN,  # Custom tokens - for dynamic content, and otherwise
    "blocks": BLOCK  # Content blocks for placement in template sections
}
