class Runners:
    """
    >>> r1 = Runners('Gerhard', 'g123@gmail.com', '<40')
    >>> r1.change_email('g456@gmail.com')
    >>> r1.email
    'g456@gmail.com'
    >>> r1.name
    'Gerhard'
    >>> r1.change_speed('<30')
    >>> r1.speed
    '<30'
    """
    name: str
    email: str
    speed: str

    def __init__(self, name: str, email: str, speed: str):
        self.name = name
        self.email = email
        self.speed = speed

    def change_email(self, new_email: str):
        self.email = new_email

    def change_speed(self, new_speed):
        self.speed = new_speed

    def get_speed(self) -> str:
        return self.speed


class RaceRegistry:
    """
    Registering a runner:
    >>> race = RaceRegistry()
    >>> race.register('Gerhard', 'under 40')
    >>> race.register('Tom', 'under 30')
    >>> race.register('Toni', 'under 20')
    >>> race.register('Margot', 'under 30')
    >>> race.edit('Gerhard', 'under 30')
    >>> race.get_speed_category('<30')
    [
    """

    def __init__(self):
        self._ = []
        self._20 = []
        self._40 = []
