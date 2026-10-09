# TODO

## Environment / setup
- [ ] Use `sys.executable` instead of hardcoded `"python"` when spawning subprocesses (`humanClient.py`, `concierge.py`, ...)
- [x] Fix README run instructions (`mainWidgent.py` doesn't exist; use `./startgame.sh` or `uv run`)
- [ ] Replace `sys.path` hacks (`ui/acquireUI.py`, `ui/newgamedialog.py`, `demos/playTest.py`) with a proper package layout
- [ ] Update or remove `Classes.txt` (describes `mainWidget.py` / `acquire.py`, out of date)
- [ ] Rename Master branch to `Main`
- [ ] Inspect/Remove old branches

## Network / concierge
- [ ] `concierge.py`: remove old code
- [ ] `concierge.py`: write additional documentation
- [ ] `concierge.py`: change `newClient()` to handle requests from players looking for game servers
- [ ] `concierge.py`: change all prints to logger messages
- [ ] `humanClient.py`: connect to a remote concierge
- [ ] `humanClient.py`: handle disconnection while a game is still in session

## UI
- [ ] Change background of active player box
- [ ] Add instructions/prompts for human players
- [ ] Add delays with one-shot timers
- [ ] Show last player actions in player bar
- [ ] Show stocks owned in player bar
- [ ] Add mouseover animations to tiles and stocks when selecting
