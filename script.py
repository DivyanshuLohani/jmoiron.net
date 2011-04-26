#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net script/commands"""

from flaskext.script import Manager
from run import app, db

script = Manager(app)

@script.command
def flushdb():
    """Flush the database."""
    db.drop_collection('blog_post')
    db.drop_collection('stream_entry')
    db.drop_collection('stream_plugin')
    db.drop_collection('flatpage')
    db.drop_collection('tag')

@script.command
def create_indexes():
    """Create indexes on the mongo collections."""
    import pymongo
    db.stream_entries.create_index('source_tag')
    db.stream_entries.create_index([('timestamp', pymongo.DESCENDING)])
    db.blog_posts.create_index('tags')
    db.blog_posts.create_index([('timestamp', pymongo.DESCENDING)])
    db.tags.create_index('slug')

@script.command
def migratedb(dumpfile=None):
    """Run a migration from an SQL database."""
    from misc import migrate
    print 'Flushing current mongo database...'
    flushdb()
    if dumpfile:
        print 'Reloading database from "%s"...' % dumpfile
        migrate.loaddb(dumpfile)
    print 'Migrating stream objects...'
    m = migrate.Migrate()
    stream = m.stream()
    db['stream_entry'].insert(stream['entries'])
    db['stream_plugin'].insert(stream['plugins'])
    print 'Migrating blog posts...'
    blog = m.blog()
    db['tag'].insert(blog['tags'])
    db['blog_post'].insert(blog['posts'])
    print 'Creating indexes...'
    create_indexes()

@script.command
def rerender_entries(source_tag=None):
    """Rerender stream entries."""
    from stream.models import Entry
    if source_tag:
        entries = Entry.find({'source_tag': source_tag})
    else:
        entries = Entry.find()
    for e in entries:
        e.save()

if __name__ == '__main__':
    script.run()

