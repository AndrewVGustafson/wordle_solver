// verify working
console.log("Editing js code...")


// Makes each tile flip simultaneously
flipTile = function(tile, index, array, guess) {
    const letter = tile.dataset.letter
  const key = keyboard.querySelector(`[data-key="${letter}"i]`)
  setTimeout(() => {
    tile.classList.add("flip")
  }, (index * 10) / 2)

  tile.addEventListener(
    "transitionend",
    () => {
      tile.classList.remove("flip")
      if (targetWord[index] === letter) {
        tile.dataset.state = "correct"
        key.classList.add("correct")
      } else if (targetWord.includes(letter)) {
        tile.dataset.state = "wrong-location"
        key.classList.add("wrong-location")
      } else {
        tile.dataset.state = "wrong"
        key.classList.add("wrong")
      }

      if (index === array.length - 1) {
        tile.addEventListener(
          "transitionend",
          () => {
            startInteraction()
            checkWinLose(guess, array)
          },
          { once: true }
        )
      }
    },
    { once: true }
  )
}

// adds reference to main scope
window.flipTile = flipTile

console.log("Finished.")