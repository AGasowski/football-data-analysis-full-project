class User:

    def __init__(self, age: int) -> None:
        self.age = age

    def is_majeur(self) -> bool:
        return self.age >= 18
