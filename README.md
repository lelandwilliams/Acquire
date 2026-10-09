# Acquire
A Python implementation of Sid Sackson's classic board game *Acquire*, built as a testbed for game-playing AI.

Acquire is a game of hotel-chain mergers and stock speculation. The rules fit on a single page, but strong play means reading the board, anticipating mergers, and inferring what your opponents are holding. That combination of simple rules and deep strategy makes it an ideal target for AI research. The long-term goal is an agent that not only wins, but discovers strategy and can explain it in human terms.

## Features
- **Playable GUI** (PyQt5): play a full game against AI opponents.
- **Client-server architecture over WebSockets**: human and AI players connect the same way, so games run identically with or without a human at the table.
- **Pluggable agents**: a random baseline, a family of reflex agents (including one with learned feature weights), and minimax / alpha-beta search.
- **Self-play at scale**: run large batches of bot-only games and record complete game traces for training and analysis.

## Quick start
Requires [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/lelandwilliams/Acquire.git
cd Acquire
./startgame.sh
```

On first run, uv fetches Python 3.14 and the dependencies (PyQt5, pandas) into a local `.venv`. To launch manually: `cd ui && uv run python acquireUI.py`.

From the new-game dialog, choose your opponents (`randomClient`, `reflexAgent2`–`4`), set a seed, or switch to standalone mode to run bot-only games in bulk.

## Architecture
| Layer | Files | Role |
|---|---|---|
| Model and rules | `model.py`, `rules.py` | Game state (public `state` plus private `hands`); `new_game()`, `getActions()`, `succ()` |
| Server | `concierge.py`, `gameServer.py`, `GM.py` | Concierge launches game servers and players; the GM runs each game and records its history |
| Clients | `randomClient.py`, `humanClient.py`, `ui/` | `RandomClient` is the base for every player; agents override its `chooseXXX()` methods; `HumanClient` drives the GUI |
| Agents | `reflexAgent*.py`, `featureExtractor.py`, `minimax.py`, `alphabeta.py` | Feature-based reflex agents (`reflexAgent4` loads learned weights from `weights.gam`) and tree search |
| Data and training | `exampleMaker.py`, `statsBuilders.py`, `train.py`, `data_builder.py`, `data/` | Batch self-play, game-trace reconstruction, and training-data generation |

`network/`, `controller.py`, `acquire_model.py`, `randomAI.py` and `robotFactory.py` are legacy code from an earlier version of the networking and model layers.

## Roadmap
Planned work includes richer UI feedback (active-player highlighting, recent actions, stock holdings), remote play through the concierge, and stronger learned agents. See [TODO.md](TODO.md).
