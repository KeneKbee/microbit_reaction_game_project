from microbit import *
from random import randint

# ---------------------------------------------------------------------------------------------------------------------------

# Classes:

class Player:
    def __init__(self, pin: MicroBitTouchPin) -> None:
        self.letter = ''
        self.__score = 0
        self.__pin = pin

    def getPin(self) -> MicroBitTouchPin:
        return self.__pin

    def win(self) -> None:
        self.__score+=1
    
    def getScore(self) -> int:
        return self.__score


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.__letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.__running = False
        self.__player1 = player1
        self.__player2 = player2
        self.__rounds = 5

    def start(self) -> None:
        self.__player1.letter = self.__letters[self.__choose_letter(self.__player1.getPin())]
        self.__player2.letter = self.__letters[self.__choose_letter(self.__player2.getPin())]

        display.show(Image.NO)
        sleep(1000)
        while(not self.__running):
            if(self.__player1.getPin().is_touched() and self.__player2.getPin().is_touched()):
                self.__running = True

        self.__blink(Image.YES, 20, 1500)
        self.__play()

    def __play(self) -> None:
        rounds = 0
        while(self.__running):
            self.__countdown(3)
            cheated = self.__await()
            if(cheated):
                continue
            else:
                self.__show()

            rounds+=1
            if(rounds >= self.__rounds):
                break
        
        self.__end_game()

    def __await(self) -> bool:
        for i in range(randint(500, 3000)):
            sleep(1)
            if(self.__player1.getPin().is_touched()):
                self.__player_win(2, -1)
                return True
            elif(self.__player2.getPin().is_touched()):
                self.__player_win(1, -1)
                return True
        return False
    
    def __show(self) -> None:
        milliseconds = 0
        display.show('!')
        while True:
            if(self.__player1.getPin().is_touched()):
                self.__player_win(1, milliseconds)
                break
            elif(self.__player2.getPin().is_touched()):
                self.__player_win(2, milliseconds)
                break

            milliseconds+=1

    def __end_game(self) -> None:
        pass

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
            if(button_a.was_pressed()):
                index-=1
            elif(button_b.was_pressed()):
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


    def __player_win(self, player: int, milliseconds: int) -> None:
        tmp_player = None

        if(player == 1):
            tmp_player = self.__player1
        elif(player == 2):
            tmp_player = self.__player2
        
        if(tmp_player == None):
            pass

        tmp_player.win()
        self.__blink(tmp_player.letter, 10, 750)
        if(milliseconds > -1):
            display.scroll(str(milliseconds)+"ms")
        self.__blink(tmp_player.getScore(), 10, 750)

        if(player == 1):
            self.__player1 = tmp_player
        elif(player == 2):
            self.__player2 = tmp_player

# ---------------------------------------------------------------------------------------------------------------------------


# main:

game: Game = Game(Player(pin0), Player(pin1))
game.start()