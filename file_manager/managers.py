from django.db.models import QuerySet


class FileManger(QuerySet):

    def order_by_type(self):

        return sorted(self, key=lambda q: q.type)
