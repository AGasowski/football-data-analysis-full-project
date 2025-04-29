from project.view.abstract_view import AbstractView
from InquirerPy import prompt


class AccueilView(AbstractView):

    def __init__(self):
        super().__init__()
        self.questions = [
            {
                "type": "list",
                "name": "Menu principal",
                "message": "Que souhaitez vous faire ? ",
                "choices": [
                    "S'identifier en tant qu'admin",
                    "S'identifier en tant qu'utilisateur",
                    "Quitter l'appli",
                ],
            }
        ]

    def make_choice(self):
        answers = prompt(self.questions)
        if answers["Menu principal"] == "S'identifier en tant qu'admin":
            from project.view.admin_view import AdminView

            next_view = AdminView()
        elif (
            answers["Menu principal"] == "S'identifier en tant qu'utilisateur"
        ):
            from project.view.user_view import UserView

            next_view = UserView()
        elif answers["Menu principal"] == "Quitter l'appli":
            next_view = None
        else:
            next_view = AccueilView()

        return next_view

    def display_info(self):
        print(" MAIN MENU ".center(80, "="))
