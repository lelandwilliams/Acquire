# Acquire
An implementation of the Sid Sackson 3M Classic for purposes of exploring Artificial Intelligence

## Running
Requires [uv](https://docs.astral.sh/uv/). Clone the master branch and run:

```sh
./startgame.sh
```

or equivalently `cd ui && uv run python acquireUI.py`. On first run, uv will fetch Python 3.14 and the dependencies (PyQt5, pandas) into a local `.venv`.

The new-game dialog lets you choose your opponents: a random agent (`randomClient`) or one of the reflex agents (`reflexAgent2`–`4`). It also has a standalone mode that runs many bot-only games and records the game traces.

## Background
Acquire is a long-time favorite board game of mine. When I'm hosting a game night, I find this game to be a good one to teach persons new to gaming as the rules are simple, and the goal (make money) is more concrete than victory point schemes, and the game has suspense, and a sense of history.

I thought that coming up with an AI for the game could be very interesting, as good play
requires interpreting other players' actions, and understanding the board. The latter,
in particular, seems like a good place for the use of Neural Nets. I'd love it if a good AI could
teach me to play better, not just by making me work harder for the win, but by determining a strategy and communicating it in human terms.

Of course, it is more fun to see how an agent performs by playing against it, and it didn't seem
that the UI for this would be too complex: just a grid for the playing board, a place to show player holdings,
and a message area for prompts. I'm much more interested in the view as a tool for
imagining the developments under the hood than a wow-inspiring UI.

## Architecture
The game runs client-server over WebSockets, so human and AI players take part in exactly the same way,
and games can be played with or without a human at the table.

- **Model and rules**: `model.py` holds the game state (public `state` plus private `hands`); `rules.py` provides `new_game()`, `getActions()` and `succ()`.
- **Server side**: `concierge.py` launches game servers (`gameServer.py`) and the players for them; `GM.py` is the game master client that runs the game and records its history.
- **Clients**: `randomClient.py` is the base class for all players and chooses randomly; agents override its `chooseXXX()` methods. `humanClient.py` connects the GUI in `ui/`.
- **Agents**: `reflexAgent*.py` are hand-built and learned reflex agents using features from `featureExtractor.py`; `reflexAgent4` loads learned weights from `weights.gam`. `minimax.py` and `alphabeta.py` are search experiments over `rules.py`.
- **Data and training**: `exampleMaker.py` / `statsBuilders.py` run batches of bot games; `train.py` and `data_builder.py` turn game traces into training data. Results live in `data/`.
- **Older code**: `network/`, `controller.py`, `acquire_model.py`, `randomAI.py` and `robotFactory.py` are from an earlier version of the networking and model, superseded by the files above.

## Status
The game is playable through the GUI against random and reflex agents, and bot-only games can be run in bulk to generate training data.
See [TODO.md](TODO.md) for planned work.
