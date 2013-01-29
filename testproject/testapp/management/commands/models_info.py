from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        content_types = ContentType.objects.all()
        for ct_type in content_types:
            if ct_type.model_class():
                str_built = "[%s] - %s objects\n" % (
                    ct_type.model,
                    ct_type.model_class().objects.count())
                self.stdout.write(str_built)
                self.stderr.write("error: %s" % str_built)
