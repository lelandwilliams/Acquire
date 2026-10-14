# TODO

## Environment / setup
- [x] Use `sys.executable` instead of hardcoded `"python"` when spawning subprocesses (`humanClient.py`, `concierge.py`, ...)
- [ ] Open `weights.gam` / `savegame.txt` via paths relative to `__file__`, then remove the `chdir` hack in `concierge.py`
- [x] Fix README run instructions (`mainWidgent.py` doesn't exist; use `./startgame.sh` or `uv run`)
- [ ] Replace `sys.path` hacks (`ui/acquireUI.py`, `ui/newgamedialog.py`, `demos/playTest.py`) with a proper package layout
- [ ] Update or remove `Classes.txt` (describes `mainWidget.py` / `acquire.py`, out of date)
- [x] Rename `master` branch to `main`
- [x] Inspect/Remove old branches

## Network / concierge
- [ ] `concierge.py`: remove old code
- [ ] `concierge.py`: write additional documentation
- [ ] `concierge.py`: change `newClient()` to handle requests from players looking for game servers
- [ ] `concierge.py`: change all prints to logger messages
- [ ] `humanClient.py`: connect to a remote concierge
- [ ] `humanClient.py`: handle disconnection while a game is still in session

## UI
- [ ] Make UI theme independent of system themee
- [ ] Change background of active player box
- [ ] Add instructions/prompts for human players
- [ ] Add delays with one-shot timers
- [ ] Show last player actions in player bar
- [ ] Show stocks owned in player bar
- [ ] Add mouseover animations to tiles and stocks when selecting
- [ ] Have a different shade of yellow on gridlines
- [ ] Highlight the board space when hovering over a piece
-- or highlight all possible moves and allow the player to choose by clicking on the board.
- [ ] Dont show stock prices when founding a company
- [ ] Add a corporation status box
- [ ] Add a 'Game Over' announcement at the bottom
- [ ] Default the Human player to 'Puny Human' but allow it to be set
- [ ] Ensure merging tile gets recolored once the merger is resolved before moving on to stock buying
- [ ] Include a sellall button in merger resolution dialog
- [ ] Add messages in UI listing robot actions, or have animations showing robot actions

## Testing
- [ ] Add a debug option to start a game from a saved position (e.g. just before the human's tile causes an equal-size merger), building on `model.py`'s `savegame.txt` save/load
- [ ] Test the "Choose the Surviving Corporation" dialog in a real game where the human's tile merges two equal-size corporations
