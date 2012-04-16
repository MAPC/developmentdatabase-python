from django.core.management.base import NoArgsCommand, CommandError

from projects.models import Project


class Command(NoArgsCommand):
    help = "Shortcut for calling project.save()"
    
    def handle(self, **options):
        try:
            projects = Project.objects.all()
        except: 
                raise CommandError("An Error occurred.")

        for project in projects:
            project.save()

        self.stdout.write('Successfully updated all projects.\n')

            