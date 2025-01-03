'''
Purpose: Matching game is a game that I've created which takes user input by allowing them to click on a card which flips to display a number, and they continue to do so till they've clicked on all the cards that contain the same number. After they do so, a winning screen appears. 
Author: Radhika Radhika
Creation Date: 20/5/2022
'''

# import functions
import pgzrun
import random

# screen size
WIDTH = 210
HEIGHT = 210

# all the variables used in the game
card = [Rect((10,10), (40, 40)), Rect((60,10), (40, 40)), Rect((110,10), (40, 40)), Rect((160,10), (40, 40)), Rect((10,60), (40, 40)), Rect((60,60), (40, 40)), Rect((110,60), (40, 40)), Rect((160,60), (40, 40))] # size and position of the rectangles
cardNumber = [] # stores the card numbers
cardThatWasChosen = [0, 0, 0, 0, 0, 0, 0, 0] # changes value to '1' when that card index is chosen by user
timer = 0 # counts down to 0
cardsFliped = 0 # stores how many cards are currently flipped
whatCardWasClickedAgain = [] # stores what cardIndex was clicked right before new click (to check if the same card isn't clicked twice)
areTheCardNumbersSimilar = [] # stores cardNumber to check if they're similar or not for matched or comparsion 
matches = 0 # stores the number of matches made
matchedAlready = [] # stores if a cardNumber has been matched already
comparsions = 0 # stores the number of comparsions made
gameOver = False # if the game is over or not
startButton = False # start button -> allows to play the game
button1 = Rect((70, 110), (70, 25)) # start button position and size
changeColor = False # when hovered over, change color

# entering random numbers into the card
while len(cardNumber) != 8:
  number = random.randint(1, 4)
  if cardNumber.count(number) < 2: # if that random number isn't on the list more than 2 times
    cardNumber.append(number)

# draw function
def draw():
  screen.fill((0, 0, 0))

  if startButton == False: # until the user doesn't click on the button
    screen.draw.text("Matching Game", (25, 80), color="white", fontsize=30)
    if changeColor == True: # the mouse is within the button boundary, change colour
      screen.draw.rect(button1, (111, 192, 176))
      screen.draw.text("START", center=button1.center, color="white", fontsize=20)
    else: # else change colour
      screen.draw.filled_rect(button1, (111, 192, 176))
      screen.draw.text("START", center=button1.center, color="black", fontsize=20)
  else: # if the user does click on it, change the screen to the card screen
    screen.clear()
    for i in range(0, len(card)):
      if cardThatWasChosen[i] > 0: # if the card was clicked on
        
        if cardsFliped <= 2 and cardNumber[i] not in matchedAlready: # if there aren't more than 2 cards flipped and cards haven't been matched already
          screen.draw.text(str(cardNumber[i]), center = card[i].center, color="white", fontsize=25)
          screen.draw.rect(card[i], (111, 192, 176))
        else:  
          if cardThatWasChosen[i] != 1: # if the card wasn't clicked, flip it back
            screen.draw.filled_rect(card[i], (111, 192, 176))
          else: # or else, turn it black because they have been matched already
            screen.draw.filled_rect(card[i], (0, 0, 0))
          
      else: # draws all the card at the start of the game because everything is false
        screen.draw.filled_rect(card[i], (111, 192, 176))
  
      # draws the comparsions and matches on the screen
      screen.draw.text("Comparsion: " + str(comparsions), (10, 130), color="white", fontsize=30)
      screen.draw.text("Matches: " + str(matches), (10, 160), color="white", fontsize=30)
      
      if gameOver: # if the game is over, clear the screen and draw 'winner' on screen
        screen.clear()
        screen.draw.text("WINNER!", (30, 90), color="YELLOW", fontsize=50)
          
# all the logic function
def update(dt):
  
  global cardsFliped, timer, cardThatWasChosen, matches, areTheCardNumbersSimilar, comparsions, matchedAlready, whatCardWasClickedAgain, gameOver
  
  if cardsFliped >= 2: # if there are 2 cards flipped on the screen, start timer
    timer -= dt
    
    if timer <= 0: # if the timer is at 0
      for i in range(0, 10): # play the sound after the cards have been flipped
        for j in range(0, 10):
          print("\a", end = "\r")
        
      if areTheCardNumbersSimilar[0] == areTheCardNumbersSimilar[1]: # if the first cardNumber same as the second, increment matches and add that number to the matchedAlready so that they appear black
        matches += 1
        matchedAlready.append(areTheCardNumbersSimilar[0])
        
      else: # otherwise, it is a comparsion
        comparsions += 1
      areTheCardNumbersSimilar.clear() # clean the list because the current flip was checked and decided on
      whatCardWasClickedAgain.clear() # also clean whatever the first card that was clicked on
      cardsFliped = 0 # changes value to 0 because all cards are flipped back
      timer = 0 
      
      for i in range(0, len(card)): # if the card hasn't been matched already, turn that card back to 0 (helped out for the draw function)
        if cardNumber[i] not in matchedAlready:
          cardThatWasChosen[i] = 0

    if len(matchedAlready) >= 4: # if there are 4 matches, the game is over
      gameOver = True

# function to go to when the card has been pressed on and needs to be flipped
def card_flipping_action(num): 
  global cardThatWasChosen, cardsFliped, timer, areTheCardNumbersSimilar, whatCardWasClickedAgain
  
  cardThatWasChosen[num] = 1 # flip the card
  print("\a", end = "\r") # play a sound that the card was flipped
  cardsFliped += 1 # store that a card on the screen is flipped
  timer += 0.4 # set timer to 4 seconds
  areTheCardNumbersSimilar.append(cardNumber[num]) # store the cardNumber value for when we'll check if they're similar
  whatCardWasClickedAgain.append(card[num]) # store the first card for when we'll check if that card wasn't clicked on again

# when the user picks their card
def on_mouse_up(pos, button):
  global startButton
  
  if button1.collidepoint(pos): # if the button is clicked, make it true
    startButton = True
    
  if startButton:
    for i in range(0, len(card)): 
      if cardsFliped != 2: # checks if the screen hasn't flipped more than 2 cards
        if card[i] not in whatCardWasClickedAgain: # checks if the card hasn't been pressed on earlier in this turn
          if cardNumber[i] not in matchedAlready: # checks if the cards haven't been matched already
            if card[i].collidepoint(pos): # checks if the user has clicked on the card
              card_flipping_action(i) # flip the card!

def on_mouse_move(pos): # tracks the mouse movement
  global changeColor
  if button1.collidepoint(pos): # if the mouse ever collides with the button
    changeColor = True
  else:
    changeColor = False

# game loop 
pgzrun.go()
