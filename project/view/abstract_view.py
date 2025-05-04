from abc import ABC, abstractmethod


class AbstractView(ABC):
    def __init__(self):
        self.style = {
            "separator": "ffffff",
            "questionmark": "000000",
            "selected": "00BFFF",
            "pointer": "ffffff",
            "instruction": "ffffff",
            "answer": "008000",
            "question": "FF7F50",
        }

    @abstractmethod
    def display_info(self):
        pass

    @abstractmethod
    def make_choice(self):
        pass
