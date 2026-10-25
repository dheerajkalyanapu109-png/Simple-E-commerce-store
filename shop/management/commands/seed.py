from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Product
DATA = [
 ("Monstera Deliciosa", 799, 12, "#4f7a5a", "Split leaves that grow bolder with every new shoot. Bright, indirect light; water when the top 3 cm are dry."),
 ("Snake Plant", 499, 20, "#8da35c", "Nearly impossible to kill. Tolerates low light and missed waterings."),
 ("Fiddle Leaf Fig", 1499, 6, "#3e6b4b", "A tall statement plant that wants a bright window and a steady routine."),
 ("Pothos Trailing", 299, 30, "#6e9e6a", "Fast-growing vine for shelves and hanging pots. Forgiving and easy to propagate."),
 ("ZZ Plant", 649, 15, "#2f5a44", "Glossy, drought-tolerant stems. Thrives on neglect in dim rooms."),
 ("Peace Lily", 549, 10, "#5a8c7a", "White blooms in low light. Droops when thirsty, then bounces back within hours."),
]
class Command(BaseCommand):
    help = "Load sample products"
    def handle(self, *a, **k):
        for n, pr, st, c, d in DATA:
            Product.objects.update_or_create(slug=slugify(n), defaults=dict(name=n, price=pr, stock=st, color=c, description=d))
        self.stdout.write("Seeded products.")
