import json
from colorama import Fore, Style

from utils import get_from_file, purge

class ManualSolver:
    def __init__(self):
        self.words = get_from_file.get_dict_data()
        self.purged_words = self.words
        self.g, self.y, self.l, self.r = Fore.GREEN, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLACK_EX, Fore.RED

    def run_solver(self):
        print(f"Welcome to the {self.g}W{Fore.YELLOW}o{self.l}r{self.g}d{Fore.YELLOW}l{self.l}e{Fore.RESET} Solver!")
        try:
            while True:
                self.do_selection()
        except KeyboardInterrupt:
            print(Fore.WHITE + "Bye bye.\n" + Style.RESET_ALL)
            exit()
        # except Exception as e:
        #     print(Style.RESET_ALL, e)

    def get_selection(self) -> str:
        prompt = f"""{self.g}Select an option:
    {self.g}[W]{self.y} Wrong letters
    {self.g}[L]{self.y} Wrong Location Letters
    {self.g}[C]{self.y} Correct Letters
    {self.g}[G]{self.y} Get Available Words
    {self.g}[GG]{self.y} Get Optimized Guess Words
    {self.g}[E]{self.y} End Game
    {self.g}[N]{self.y} New Game
    {self.g}[S]{self.y} Save/Load Options{Fore.GREEN}
        """
        return input(prompt).lower()

    def do_selection(self):
        match self.get_selection():
            case 'w':
                wrong_letters = self.get_wrong()
                self.purged_words = purge.purge_wrong(wrong_letters, self.purged_words)

            case 'l':
                wrong_location_letters = self.get_wrong_location()
                self.purged_words = purge.purge_wrong_location(wrong_location_letters, self.purged_words)

            case 'c':
                correct_letters = self.get_correct()
                self.purged_words = purge.purge_correct(correct_letters, self.purged_words)

            case 'g':
                print("Please choose from one of the following words:")
                print(*self.purged_words, "\n")

            case 'gg':
                print("Please choose from one of the following words:")
                optimized_words = purge.better_guesses(self.purged_words)
                print(*optimized_words, "\n")

            case 'e':
                print(Fore.WHITE + "Bye bye.\n" + Style.RESET_ALL)
                exit()

            case 'n':
                print(self.r + "Resetting words...\n" + self.g)
                self.purged_words = self.words

            case 's':
                self.save_load_dialogue(self.purged_words)

            case _:
                print(Fore.RED + "Enter from one of the options...\n" + Fore.RESET)
                return

    def save_load_dialogue(self, words) -> None:
        """_summary_

        Args:
            words (_type_): _description_
        """
        selection = input("[S] Save Current Game [L] Load Last Played Game [R] Return to Game\n\n").lower()
        match selection:
            case "s":
                self.save_game(words)
            case 'l':
                self.load_game()
            case 'r':
                return
            case _:
                print("Enter from one of the options...\n")
                self.save_load_dialogue(words)


    def save_game(self, words: list) -> None:
        with open("wordle_save", 'w', encoding="utf-8") as file:
            json.dump(words, file, indent=4)

    def load_game(self) -> None:
        try:
            print("Getting save data...")
            with open("wordle_save", 'r', encoding="utf-8") as file:
                self.purged_words = json.load(file)
            print(self.g + "Loaded Save Data!\n" + self.g)

        except FileNotFoundError:
            print(self.r + "There is no save data.\n" + self.g)
            self.save_load_dialogue(self.purged_words)

    def get_wrong(self) -> list[str]:
        wrong_letters = input("\nEnter each incorrect letter, not seperated by a space:  ie. 'xyz'\n")
        wrong_letters = list(wrong_letters)
        return wrong_letters

    def get_wrong_location(self) -> list[tuple[str, int]]:
        wrong_location_letters = input("\nEnter each letter and the position it's not in, seperated by a space: ie. 'a1 b2 c3'\n")
        wrong_location_letters = wrong_location_letters.split(" ")
        try:
            wrong_location_letters = [(letter[0], int(letter[1]) - 1) for letter in wrong_location_letters]
        except (IndexError, ValueError):
            print(self.r + "Invalid Input." + self.g)
            self.get_wrong_location()
        return wrong_location_letters

    def get_correct(self) -> list[tuple[str, int]]:
        correct_letters = input("\nEnter each letter and the position it's in, seperated by a space: ie. 'a1 b2 c3'\n")
        correct_letters = correct_letters.split(" ")
        try:
            correct_letters = [(letter[0], int(letter[1]) - 1) for letter in correct_letters]
        except (IndexError, ValueError):
            print(self.r + "Invalid Input." + self.g)
            self.get_wrong_location()
        return correct_letters


if __name__ == "__main__":
    solver = ManualSolver()
    solver.run_solver()
