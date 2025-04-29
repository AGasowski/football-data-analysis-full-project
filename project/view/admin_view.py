from project.model.user import User
from project.view.abstract_view import AbstractView
from InquirerPy import prompt


class AdminView(AbstractView):

    def __init__(self):
        super().__init__()
        self.questions = [
            {
                "type": "input",
                "name": "question age",
                "message": "Quel age avez vous ?",
            }
        ]

    def make_choice(self):
        answers = prompt(self.questions)
        user = User(answers["question age"])
        print(
            f"Oh vous êtes admin et avez {user.age} ans, notre application n'est pas terminée revenez plus tard"
        )
        from project.view.accueil_view import AccueilView

        return AccueilView()

    def display_info(self):
        print("Quelques information sur vous !")
