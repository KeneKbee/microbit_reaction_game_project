from microbit import *
import random

# ---------------------------------------------------------------------------------------------------------------------------

# Classes:

class Player:
    def __init__(self, pin: MicroBitTouchPin) -> None:
        self.letter = ''
        self.score = 0
        self.__pin = pin

    def getPin(self) -> MicroBitTouchPin:
        return self.__pin



class Game:
    def __init__(self, player1: Player, player2: Player):
        self.__letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.__running = False
        self.__player1 = player1
        self.__player2 = player2

    def start(self) -> None:
        self.__player1.letter = self.__letters[self.__choose_letter(self.__player1.getPin())]
        self.__player2.letter = self.__letters[self.__choose_letter(self.__player2.getPin())]

        display.show(Image.NO)
        sleep(1000)
        while(not self.__running):
            if(self.__player1.getPin().is_touched() and self.__player2.getPin().is_touched()):
                self.__running = True

        self.__blink(Image.YES, 20, 1500)
        sleep(1000)
        self.__play()

    def __play(self) -> None:
        while(self.__running):
            self.__countdown(3)
            wait_time = random.randint(500, 3000)
            cheated = self.__await(wait_time)
            if(cheated):
                continue
            display.show('!')
            sleep(1000)

    def __blink(self, char, repeats: int, blink_time: int) -> None:
        for i in range(repeats):
            if(i%2==0):
                display.clear()
            else:
                display.show(char)
            sleep(blink_time//repeats)
        display.clear()

    def __choose_letter(self, playerPin: MicroBitTouchPin) -> int:
        index = 0
        while(not playerPin.is_touched()):
            if(button_a.is_pressed()):
                index-=1
            elif(button_b.is_pressed()):
                index+=1

            if(index <= -1):
                index = len(self.__letters)-1
            elif(index >= len(self.__letters)):
                index=0
            display.show(self.__letters[index])
        self.__blink(self.__letters[index], 10, 750)
        return index

    def __countdown(self, seconds: int) -> None:
        for i in range(seconds):
            display.show(seconds-i)
            sleep(1000)
        display.clear()

    def __await(self, time: int) -> bool:
        for i in range(time):
            sleep(1)
            if(self.__player1.getPin().is_touched()):
                self.__player2.score += 1
                return True
            elif(self.__player2.getPin().is_touched()):
                self.__player2.score += 1
                return True
        return False


# ---------------------------------------------------------------------------------------------------------------------------


# main:

while True:
    game: Game = Game(Player(pin0), Player(pin1))

    game.start()