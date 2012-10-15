# MAPC's Development Database

A database that tracks development projects.

Features:

* Project search
* Project forms
* Tastypie Data API
* Comments

MAPC Project team: Tim Reardon, Meghna, Dutta, Rob Goodspeed, Christian Spanring 

## Dependencies

A PostgreSQL/PostGIS database is required for data storage and GeoDjango functionality. To create one, execute:

    $ createdb developmentdatabase -T template_postgis

Python dependencies can be installed through the pip requirements file:

    $ pip install -r requirements.txt

---

Copyright 2012 MAPC