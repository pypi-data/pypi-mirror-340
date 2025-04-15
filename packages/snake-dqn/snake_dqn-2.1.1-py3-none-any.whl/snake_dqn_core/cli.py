from ..snake_dqn_core import *
import argparse

def main():
    parser = argparse.ArgumentParser(prog="sdqn")
    subparsers = parser.add_subparsers(dest="command", required=True)

    model_choices = ["dqn", "doubling_dqn", "dueling_dqn", "hybrid_dqn", "rainbow_dqn"]

    # train
    train_code = subparsers.add_parser("train", help="Train a model")
    train_code.add_argument("--model", type=str, choices=model_choices, required=True)
    train_code.add_argument("--episodes", type=int, default=1000)
    train_code.add_argument("--modelpath", type=str, default="")
    train_code.add_argument("--render", action="store_true")

    # play
    play_code = subparsers.add_parser("play", help="Play a model")
    play_code.add_argument("--model", type=str, choices=model_choices, required=True)
    play_code.add_argument("--modelpath", type=str, default="")
    play_code.add_argument("--episodes", type=int, default=5)

    args = parser.parse_args()

    train_funcs = {
        "dqn": train_dqn,
        "doubling_dqn": train_doubling_dqn,
        "dueling_dqn": train_dueling_dqn,
        "hybrid_dqn": train_hybrid_dqn,
        "rainbow_dqn": train_rainbow_dqn,
    }

    play_funcs = {
        "dqn": play_dqn_model,
        "doubling_dqn": play_doubling_dqn_model,
        "dueling_dqn": play_dueling_dqn_model,
        "hybrid_dqn": play_hybrid_dqn_model,
        "rainbow_dqn": play_rainbow_dqn_model,
    }

    if args.command == "train":
        env = SnakeGameEnv(render_mode=args.render)
        train_funcs[args.model](env, args.episodes, args.episodes, args.modelpath or None)

    elif args.command == "play":
        play_funcs[args.model](args.modelpath, args.episodes)
