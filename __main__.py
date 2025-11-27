from view.accueil_view import AccueilView

view = AccueilView()

with open("view/resources/banner.txt", mode="r", encoding="utf-8") as title:
    print(title.read())

while view:
    view.display_info()
    view = view.make_choice()

with open(
    "view/resources/exit.txt", mode="r", encoding="utf-8"
) as exit_message:
    print(exit_message.read())
