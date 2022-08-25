import csv
from lib2to3.pytree import Base
from pathlib import Path

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent.parent


class Command(BaseCommand):
    help = "Импорт ингредиентов в базу данных"

    def handle(self, **kwargs):
        with open(
            f"{PROJECT_DIR}\\data\\ingredients.csv", "r", newline="", encoding="UTF-8"
        ) as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                Ingredient.objects.get_or_create(name=row[0], measurement_unit=row[1])
                print(" ".join(row), "---------> success")
