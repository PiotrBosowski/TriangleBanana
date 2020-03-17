from exception import IllegalCarError


class Car:
    def __init__(self, pax_count, car_mass, gear_count):
        if pax_count < 1 or pax_count > 5:
            raise IllegalCarError("Number of passengers must fit in <1, 5> range.")
        if car_mass > 2000:
            raise IllegalCarError("Car mass cannot exceed 2000 kg.")
        self._pax_count = pax_count
        self._car_mass = car_mass
        self._gear_count = gear_count
        self._calculate_total_mass()

    @property
    def car_mass(self):
        return self._car_mass

    @car_mass.setter
    def car_mass(self, new_value):
        if new_value > 2000:
            raise IllegalCarError("Car mass cannot exceed 2000 kg.")
        self._car_mass = new_value
        self._calculate_total_mass()

    @property
    def pax_count(self):
        return self._pax_count

    @pax_count.setter
    def pax_count(self, new_value):
        if new_value < 1 or new_value > 5:
            raise IllegalCarError('Invalid pax_count value')
        self._pax_count = new_value
        self._calculate_total_mass()

    @property
    def total_mass(self):
        return self._total_mass

    def _calculate_total_mass(self):
        self._total_mass = self._car_mass + 70 * self._pax_count


car = Car(3, 1700, 5)
# car = Car(3, 2010, 5)  # IllegalCarError
# car = Car(7, 1999, 5)  # IllegalCarError
print(car.total_mass)  # 1910

# car.car_mass = 2100  # IllegalCarError
car.car_mass = 1900
print(car.total_mass)  # 2110

# car.pax_count = 7  # IllegalCarError
car.pax_count = 1
print(car.total_mass)  # 1970

# car.total_mass = 100  # Error
