from microbit import *
import music
from random import randint, seed

# ---------------------------------------------------------------------------------------------------------------------------

# Classes:

class Player:
    def __init__(self, pin: MicroBitTouchPin) -> None:
        self.letter = ''
        self.__score = 0
        self.__pin = pin

    def get_pin(self) -> MicroBitTouchPin:
        return self.__pin

    def win(self) -> None:
        self.__score+=1
    
    def get_score(self) -> int:
        return self.__score
    
    def reset_score(self) -> None:
        self.__score = 0


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.__letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.__running = False
        self.__player1 = player1
        self.__player2 = player2
        self.__rounds = 5

    def start(self) -> None:
        self.__player1.letter = self.__letters[self.__choose_letter(self.__player1.get_pin())]
        self.__player2.letter = self.__letters[self.__choose_letter(self.__player2.get_pin())]

        seed(running_time())

        display.show(Image.NO)
        sleep(1000)
        while(not self.__running):
            if(self.__player1.get_pin().is_touched() and self.__player2.get_pin().is_touched()):
                self.__running = True

        self.__blink(Image.YES, 20, 1500)
        self.__play()

    def __play(self) -> None:
        rounds = 0
        while(self.__running):
            display.show(rounds+1)
            sleep(1000)
            display.clear()
            sleep(500)
            self.__countdown(3)
            cheated = self.__await()
            if(not cheated):
                self.__show()

            rounds+=1
            if(rounds >= self.__rounds):
                break
        
        self.__end_game()

    def __await(self) -> bool:
        wait_time = randint(300, 3000)
        for i in range(wait_time):
            sleep(1)
            if(self.__player1.get_pin().is_touched()):
                self.__player_win(self.__player2, -1)
                return True
            elif(self.__player2.get_pin().is_touched()):
                self.__player_win(self.__player1, -1)
                return True
        return False
    
    def __show(self) -> None:
        start_time = running_time()
        # TODO: sfx for showing
        display.show('!')
        while True:
            if(self.__player1.get_pin().is_touched()):
                self.__player_win(self.__player1, running_time() - start_time)
                break
            elif(self.__player2.get_pin().is_touched()):
                self.__player_win(self.__player2, running_time() - start_time)
                break
            sleep(1)

    def __end_game(self) -> None:
        winner = None
        loser = None

        if(self.__player1.get_score() > self.__player2.get_score()):
            winner = self.__player1
            loser = self.__player2
        else:
            winner = self.__player2
            loser = self.__player1
        
        display.scroll(winner.letter + " wins!")
        self.__blink(winner.get_score(), 20, 1500)
        display.scroll(loser.letter + "loses")
        self.__blink(loser.get_score(), 20, 1500)

        for count in range(7000):
            if(self.__player1.get_pin().is_touched() and self.__player2.get_pin().is_touched()):
                self.__reset()
                break
            sleep(1)

    def __reset(self) -> None:
        seed(running_time())
        self.__player1.reset_score()
        self.__player2.reset_score()
        self.__play()

    def __blink(self, char, repeats: int, blink_time: int) -> None:
        for i in range(repeats):
            if(i%2==0):
                display.clear()
            else:
                # TODO: sfx for blinking
                display.show(char)
            sleep(blink_time//repeats)
        display.clear()

    def __choose_letter(self, playerPin: MicroBitTouchPin) -> int:
        index = 0
        while(not playerPin.is_touched()):
            if(button_a.was_pressed()):
                # TODO: sfx for clicking
                index-=1
            elif(button_b.was_pressed()):
                # TODO: sfx for clicking
                index+=1

            if(index <= -1):
                index = len(self.__letters)-1
            elif(index >= len(self.__letters)):
                index=0
            display.show(self.__letters[index])

        # TODO: sfx for choosing
        self.__blink(self.__letters[index], 10, 750)
        return index

    def __countdown(self, seconds: int) -> None:
        for i in range(seconds):
            # TODO: sfx for counting down
            display.show(seconds-i)
            sleep(1000)
        display.clear()


    def __player_win(self, player: Player, milliseconds: int) -> None:
        player.win()

        # TODO: sfx for winning
        self.__blink(player.letter, 10, 750)
        if(milliseconds > -1):
            display.scroll(str(milliseconds)+"ms")
        self.__blink(player.get_score(), 10, 750)

        sleep(1000)

# ---------------------------------------------------------------------------------------------------------------------------


# main:

game: Game = Game(Player(pin0), Player(pin1))
game.start()
