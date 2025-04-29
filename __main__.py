from project.view.accueil_view import AccueilView

view = AccueilView()

with open("resources/banner.txt", mode="r", encoding="utf-8") as title:
    print(title.read())

while view:
    view.display_info()
    view = view.make_choice()

with open("resources/exit.txt", mode="r", encoding="utf-8") as exit_message:
    print(exit_message.read())
