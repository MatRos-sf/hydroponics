from random import choice, randint, uniform

from django.contrib.auth.models import User
from faker import Faker

from hydroponics_manager.models import HydroponicsType, HydroponicSystem, Measurement

PASSWORD = "luna"
FAKER = Faker()


def get_random_num(a: int, b: int, r: int = 1) -> float:
    return round(uniform(a, b), r)


def run():
    """
    Creates 10 users and assigns HydroponicSystems with random names, descriptions and types. Then, it generates random
    measurements.
    If you want to run this script use the command:
    python3 manage.py runscript fill_db
    """
    system_type = [i[0] for i in HydroponicsType.choices]

    for i in range(10):
        user = User.objects.create_user(username=f"user_{i}", password=PASSWORD)
        hs = HydroponicSystem.objects.create(
            name=FAKER.word(),
            description=FAKER.sentence(),
            system_type=choice(system_type),
            owner=user,
        )
        for _ in range((i + 1) * 2):
            Measurement.objects.create(
                hydroponic_system=hs,
                ph=get_random_num(0, 14, 1),
                water_temperature=get_random_num(0, 100, 1),
                tds=get_random_num(0, 100, 1),
            )

    print("Done")
