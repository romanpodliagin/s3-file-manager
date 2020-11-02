from django.db.models import QuerySet


class FileManger(QuerySet):

    def first_dirs(self):

        return sorted(self, key=lambda q: q.type)
