django-ssiexport
----

[![Test Status](https://travis-ci.org/mauler/django-ssiexport.png?branch=master)](https://travis-ci.org/mauler/django-ssiexport)

[![Code Health](https://landscape.io/github/mauler/django-ssiexport/master/landscape.png)](https://landscape.io/github/mauler/django-ssiexport/master)

[![Latest PyPI version](https://pypip.in/v/django-ssiexport/badge.png)](https://crate.io/packages/django-ssiexport/)

[![Number of PyPI downloads](https://pypip.in/d/django-ssiexport/badge.png)](https://crate.io/packages/django-ssiexport/)


## Ideal usage (First use after installation)

1. ssiexport_all

2. ssiexport_templates

    After an update, like git pull.

3. signals checking for changes on Models

    Changes urls on the whole system that is related to the object.

4. cron running checking for changed queryset

5. After each regenerated url, generate a cron task the crawl the url searching
for other urls (like pagination).


## Export techniques

[ ] URL model instance on delete, remove htmls.

[ ] queryset serialization

[ ] model signals
    [ ] create
    [ ] update
    [ ] remove

[ ] crawling (for pagination)

[ ] templating editing (md5hash change)

[ ] cron

### Model signals

[ ] Create

    If the instance is on the queryset, then export the
    instance get_absolute_url.

[ ] Change

    If the instance is on the queryset, re-export the get_absolute_url.

[ ] Remove

    Remove all urls related to that object.
