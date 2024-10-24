"""Run this file to run either the manual or automatic wordle solver."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from solvers.auto_solver import AutoSolver
from solvers.manual_solver import ManualSolver

RUN_AUTO: bool = False

def main() -> None:
    """Runs either manual or automatic wordle solver, depending on `RUN_AUTO`."""
    if RUN_AUTO:
        options = Options()
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(options=options)
        url = 'https://speedle.rahuljk.com/'

        auto_solver = AutoSolver(driver, url)
        auto_solver.solve(starting_words=["slant"], replay_forever=True)

    else:
        solver = ManualSolver()
        solver.run_solver()


if __name__ == "__main__":
    main()
