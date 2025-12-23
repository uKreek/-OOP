import math

PI = math.pi


class Angle:
    """Класс для работы с углами"""

    def __init__(self, value=0.0, radians=None, degrees=None):
        """
        Создание угла. Можно задать:
        - напрямую значение в радианах: Angle(1.57)
        - через именованные параметры: Angle(radians=1.57) или Angle(degrees=90)
        """
        if radians is not None:
            self._radians = float(radians)
        elif degrees is not None:
            self._radians = math.radians(float(degrees))
        else:
            self._radians = float(value)

    @property
    def _normal_ang(self):
        """Нормализация угла в диапазон [0, 2*pi)"""
        return self._radians % (2 * PI)

    @property
    def radians(self):
        return self._radians

    @property
    def degrees(self):
        return self._radians

    @radians.setter
    def radians(self, value):
        self._radians = float(value)

    @degrees.setter
    def radians(self, value):
        self._radians = float(math.radians(value))

    def __eq__(self, other):
        '''сравнение углов в радианах'''
        if isinstance(other, Angle):
            return math.isclose(self._normal_ang, other._normal_ang, rel_tol=1e-9)

    def __int__(self):
        return int(self._radians)

    def __float__(self):
        return float(self._radians)

    def __lt__(self, other):
        '''less than'''
        if isinstance(other, Angle):
            return self._normal_ang < other._normal_ang

    def __le__(self, other):
        '''less or equal'''
        if isinstance(other, Angle):
            return self._normal_ang <= other._normal_ang

    def __gt__(self, other):
        '''greater than'''
        if isinstance(other, Angle):
            return self._normal_ang > other._normal_ang

    def __ge__(self, other):
        '''great or equal'''
        if isinstance(other, Angle):
            return self._normal_ang >= other._normal_ang

    def __add__(self, other):
        if isinstance(other, Angle):
            return self._radians + other._radians
        return self._radians + other

    def __sub__(self, other):
        if isinstance(other, Angle):
            return self._radians - other._radians
        return self._radians - other

    def __mul__(self, other):
        return self._radians * other

    def __truediv__(self, other):
        return self._radians / other

    def __str__(self):
        return f'{self._radians:.4f}'

    def __repr__(self):
        return f"Angle(radians={self._radians})"



class AngleRange:
    def __init__(self, start, end, start_inclusive=True, end_inclusive=True):
        """
        Создание промежутка углов.
        start, end: начальный и конечный углы (Angle, float или int)
        start_inclusive, end_inclusive: включающие ли границы
        """
        self.start = self._to_angle(start)
        self.end = self._to_angle(end)
        self.start_inclusive = start_inclusive
        self.end_inclusive = end_inclusive

    def _to_angle(self, value):
        """Преобразование в Angle"""
        if isinstance(value, Angle):
            return value
        elif isinstance(value, (int, float)):
            return Angle(value)
        else:
            raise TypeError("Значение должно быть Angle, int или float")

    def __eq__(self, other):
        if not isinstance(other, AngleRange):
            return False
        return (self.start == other.start and
                self.end == other.end and
                self.start_inclusive == other.start_inclusive and
                self.end_inclusive == other.end_inclusive)

    def __str__(self):
        start_bracket = "[" if self.start_inclusive else "("
        end_bracket = "]" if self.end_inclusive else ")"
        return f"{start_bracket}{self.start} - {self.end}{end_bracket}"

    def __repr__(self):
        start_bracket = "[" if self.start_inclusive else "("
        end_bracket = "]" if self.end_inclusive else ")"
        return f"AngleRange({start_bracket}{self.start._radians:.6f}, {self.end._radians:.6f}{end_bracket})"


    def __abs__(self):
        """Длина промежутка в радианах"""
        start_rad = self.start.radians
        end_rad = self.end.radians

        if end_rad >= start_rad:
            return end_rad - start_rad
        else:
            return (2 * PI - start_rad) + end_rad

    def __contains__(self, item):
        if isinstance(item, Angle):
            angle = item.radians
        elif isinstance(item, (int, float)):
            angle = Angle(item).radians
        elif isinstance(item, AngleRange):
            return self._contains_range(item)
        else:
            return False

        start_rad = self.start.radians
        end_rad = self.end.radians

        if start_rad <= end_rad:
            # Нормальный случай
            left_ok = angle > start_rad or (angle == start_rad and self.start_inclusive)
            right_ok = angle < end_rad or (angle == end_rad and self.end_inclusive)
            return left_ok and right_ok
        else:
            # Промежуток пересекает 0
            left_ok = angle >= start_rad or (angle == start_rad and self.start_inclusive)
            right_ok = angle <= end_rad or (angle == end_rad and self.end_inclusive)
            return left_ok or right_ok

    def _contains_range(self, other):
        """Проверка вхождения одного промежутка в другой"""
        # Упрощенная проверка - проверяем что обе границы другого промежутка содержатся в текущем
        return other.start in self and other.end in self

    def __add__(self, other):
        """Объединение промежутков"""
        if not isinstance(other, AngleRange):
            return NotImplemented

        # Упрощенная реализация - возвращаем список промежутков
        if self._can_merge(other):
            start = min(self.start, other.start, key=lambda x: x.radians)
            end = max(self.end, other.end, key=lambda x: x.radians)
            return [AngleRange(start, end)]
        else:
            return [self, other]

    def __sub__(self, other):
        """Разность промежутков"""
        if not isinstance(other, AngleRange):
            return NotImplemented

        # Упрощенная реализация
        if other in self:
            start_bracket = False if other.start_inclusive else True
            end_bracket = False if other.end_inclusive else True
            # Если другой промежуток полностью внутри текущего
            return [AngleRange(self.start, other.start, end_inclusive=start_bracket), AngleRange(other.end, self.end, start_inclusive=end_bracket)]
        else:
            return [self]

    def _can_merge(self, other):
        """Проверка возможности объединения промежутков"""
        return (other.start in self or other.end in self or
                self.start in other or self.end in other)


