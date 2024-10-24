from time import sleep
from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from utils import get_from_file, purge

class AutoSolver:
    def __init__(self, driver: webdriver.Chrome, url: str) -> None:

        self.driver = driver
        self.driver.get(url)
        self.actions = ActionChains(self.driver)

        self.words = get_from_file.get_dict_data()
        self.purged_words = self.words
        self.starting_words = None
        self.guess = None

        self.start_button_id = "startButton"
        self.play_again_button_id = "playAgainButton"
        self.guess_grid_id = "guess-grid"
        self.start_button = self.driver.find_element(By.ID, self.start_button_id)
        self.play_again_button = self.driver.find_element(By.ID, self.play_again_button_id)


    def solve(self, replay_forever: bool = False, guessing_interval: float = 1.45, starting_words: list = ["tales"], better_guess_cutoff: int = 3) -> None:
        self.starting_words = purge.get_starting_words(starting_words)
        self.purged_words = self.words

        self.start_button = self.driver.find_element(By.ID, self.start_button_id)
        self.play_again_button = self.driver.find_element(By.ID, self.play_again_button_id)

        self.click_available_element(self.start_button, self.start_button_id)

        for i in range(6):
            if starting_words[i]:
                self.guess = starting_words[i]

            if self.play_again_button.is_displayed():
                break

            print(f"Guess: {self.guess}, Words Remaining: {len(self.purged_words)}\n")

            self.send_word(self.guess)
            sleep(guessing_interval)
            self.guess = self.get_guess(i, better_guess_cutoff)

            if self.purged_words == 1:
                break

        self.click_available_element(self.play_again_button, self.play_again_button_id)
        if replay_forever:
            self.solve(replay_forever=True, guessing_interval=guessing_interval, starting_words=starting_words)


    def get_guess(self, row: int, better_guess_cutoff: int) -> str:
        tile_data = self.get_tiles_data()
        self.purged_words = purge.filter_words(tile_data, self.purged_words)
        if row <= better_guess_cutoff:
            return purge.better_guess(self.purged_words)
        else:
            return self.purged_words[0]

    def send_word(self, guess: str) -> None:
        self.actions.send_keys(guess + Keys.ENTER)
        self.actions.perform()

    def click_available_element(self, element: WebElement, element_id: str) -> None:
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        element.click()

    def get_tiles_data(self) -> dict[str, Any]:
        tile_elements = self.driver.find_elements(By.CLASS_NAME, "tile")

        tiles_data = {
            "wrong": "",
            "wrong-location": [],
            "correct": []
        }

        for tile in tile_elements:
            letter = tile.text.lower()
            if not letter:
                continue

            data_state = tile.get_attribute("data-state")
            pos = tile_elements.index(tile) % 5
            block = (letter, pos)

            if data_state != "wrong":
                tiles_data[data_state].append(block)
            else:
                tiles_data["wrong"] += letter

        return tiles_data

if __name__ == "__main__":
    STARTING_WORDS = ["cones", "trial"]
    BETTER_GUESS_CUTOFF = 3
    GUESSING_INTERVAL = 1.45

    driver = webdriver.Chrome(options=Options().add_argument('--log-level=3'))
    URL = 'https://speedle.rahuljk.com/'

    auto_solver = AutoSolver(driver, URL)
    auto_solver.solve(starting_words=STARTING_WORDS, replay_forever=True)
