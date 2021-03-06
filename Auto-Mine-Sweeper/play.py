import time
import logging
from termcolor import colored
from game import MineGame, STATUS, OPERATION
from auto import MineBot

HEADING = colored("""
     ___  ___   _   __   _   _____        _____   _          __  _____   _____   _____   _____   _____   
    /   |/   | | | |  \ | | | ____|      /  ___/ | |        / / | ____| | ____| |  _  \ | ____| |  _  \  
   / /|   /| | | | |   \| | | |__        | |___  | |  __   / /  | |__   | |__   | |_| | | |__   | |_| |  
  / / |__/ | | | | | |\   | |  __|       \___  \ | | /  | / /   |  __|  |  __|  |  ___/ |  __|  |  _  /  
 / /       | | | | | | \  | | |___        ___| | | |/   |/ /    | |___  | |___  | |     | |___  | | \ \  
/_/        |_| |_| |_|  \_| |_____|      /_____/ |___/|___/     |_____| |_____| |_|     |_____| |_|  \_\ 
""", 'yellow')

GAME = MineGame()
BOT = MineBot()
INTERVAL = 0.10
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('main')


def play_manual() -> list:
    # Play a game manually
    move = input('Input row and column position to uncover or mark:\n'
                 'e.g., `1 3 5` as to uncover grid[3][5];\n'
                 '`2 4 6` as to mark grid[4][6])\n'
                 'Press `ctrl + c` to quit.\n> ').strip().split()
    move = OPERATION(int(move[0])), int(move[1]), int(move[2])
    return [move]


def play_auto() -> list:
    # Play a game by auto
    move_list = BOT.analyze(GAME)
    return move_list


def main():
    # 2 modes of playing
    play_modes = {
        'man': play_manual,
        'auto': play_auto
    }
    # Start game
    print(HEADING)
    while True:
        try:
            command = input('Starting a new game...\n'
                            'Input rows, columns, mines and interact type:\n'
                            '(`auto` = automatic play, `man` = manual play)\n'
                            'e.g., `20 30 25 man`, `10 10 10 auto`\n'
                            'Press `ctrl + c` to quit.\n> ').strip().split()
            assert len(command) == 4
            mode = command[3]
            params = list(map(int, command[:3]))
            assert mode in play_modes
            play = play_modes[mode]
            GAME.start(*params)
            GAME.show()
            # Continuously playing
            while GAME.status == STATUS.RUNNING:
                # Generate a sequence of operations
                try:
                    move_list = play()
                    for move in move_list:
                        GAME.move(*move)
                        GAME.show()
                        time.sleep(INTERVAL)
                        # Game is over
                        if GAME.status != STATUS.RUNNING:
                            logger.info('Last move: {}'.format(move))
                            break
                except (IndexError, ValueError, AssertionError):
                    logger.warning('Illegal move.')
                except KeyboardInterrupt:
                    logger.info('Quit this game...')
                    break
        except AssertionError:
            logger.warning('Illegal paramaters. Input again.')
        except KeyboardInterrupt:
            logger.info('Have a nice day:)')
            break


if __name__ == '__main__':
    main()
