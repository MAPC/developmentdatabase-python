FROM django:python2-onbuild

RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin vim

COPY ./libgeos.py /usr/local/lib/python2.7/site-packages/django/contrib/gis/geos/libgeos.py

CMD ['manage.py', 'runserver']