from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    requires_model_validation = True

    def handle_noargs(self, **options):
        lines = []
        from django.db.models import get_models
        for model in get_models():
            lines.append("[%s] - %s objects" % (
                model.__name__, model._default_manager.count() or "0"))
        self.stderr.write("error: %s" % "\nerror: ".join(lines))
        return "\n".join(lines)
