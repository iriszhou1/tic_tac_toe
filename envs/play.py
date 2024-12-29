from base_env import BaseEnv


def clean_move(move: str) -> tuple[int]:
    move = move[1:-1]
    move_lst = move.split(",")
    move_lst = [int(token.strip()) for token in move_lst]
    return move_lst[0], move_lst[1]


def main():
    env = BaseEnv()
    env.render()

    while not env.terminated:
        # Get next move
        move = input("Enter move as (x, y)! \n> Move: ")
        move = clean_move(move)

        # Take turn and display board
        env.take_turn(move)
        env.render()
        print()

    print("Thanks for playing!")


if __name__=="__main__":
    main()