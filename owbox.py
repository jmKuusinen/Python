'''@Author jmKuusinen'''

import pyautogui # Install pip package first [pip install pyautogui]
import time

''' SHORT SCRIPT TO AUTOMATE LOOTBOX-OPENING IN OVERWATCH 
    Replace numberOfBoxes variable with the amount of lootboxes you have left'''

pyautogui.FAILSAFE = True # Moving cursor to upper left corner acts as killswitch

numberOfBoxes = 84 # Number of lootboxes to open

time.sleep(3) # Wait for animation


pyautogui.moveTo(1017,1307, duration=0.2) # Moves cursor to correct spot
while boxNo <= 84: # Opens boxes as long as user specified
    pyautogui.click()
    time.sleep(8)
    boxNo = boxNo -1