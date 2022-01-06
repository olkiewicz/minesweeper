from minesweeper import Minesweeper, Action

if __name__ == '__main__':
    print(f'Welcome to Minesweeper!\n"-": not discovered; " " empty, discovered; "T" check as mine; "X" field has X mines around')
    minesweeper = Minesweeper(8)
    print(minesweeper.__str__().replace('0', '-'))
    action_x = int(input('Please enter x position of your next action:\n'))
    action_y = int(input('Please enter y position of your next action:\n'))
    print('Your first action is discovering.\n')
    minesweeper.first_action(action_x, action_y)

    while not minesweeper.game_over:
        print(minesweeper)
        action_x = int(input('Please enter x position of your next action:\n'))
        action_y = int(input('Please enter y position of your next action:\n'))

        choice = int(input('Enter 1 for check as mine.\nEnter 2 for discover:\n'))
        minesweeper.action(action_x, action_y, Action(choice))

