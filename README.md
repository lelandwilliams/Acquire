# Acquire
An implementation of the Sid Sackson 3M Classic for purposes of exploring Artificial Intelligence
## Background
Acquire is a long-time favorite board game of mine. When I'm hosting a game night, I find this game to be a good one to teach persons new to gaming as the rules are simple, and the goal (make money) is more concrete than victory point schemes, and the game has suspense, and a sense of history.

I thought that coming up with an AI for the game could be very interesting, as good play 
requires interpreting other player's actions, and understaning the board. The latter, 
in particular, seems like a good place for the use of Neural Nets. I'd love it if a good AI could 
teach me to play better, not just by making me work harder for the win, but by determining a strategy and communicating it in human terms.

I've written this program with hopefully enough
seperation between model, view, and controller that once the AI is developed, it can train against
itself.
Of course, it is more fun to see how an agent performs by playing against it, and it didn't seem
that the UI for this wouldn't
be too complex: just a grid for the playing board, and a place to show player holdings,
and a message area place prompts I'm much more interested in the view as a tool for 
imagining the developments under the hood than a wow-inspiring UI.

The model was a piece of cake. For now, development has focused on building the view and controller in
parallel, with the 'AI' only making random choices, which is enough to test M-V-C interaction.

## Status
The UI is nearly complete, and is generally playable, albeit only against agents that choose their 
actions randomly. However, the close integration of view and controller that greatly helped me 
to get the UI up and running is now in the way, 
and I am writing working to seperate them, allowing them to communicate via network sockets. 
This way the view will have it's own event loop, which is necesary to add animations and other visual 
enhancements; likewise the controller will have it's own loop, and can broadcast game event 
notifications to all clients, human and AI, in the same way. Once this
is done I want to explore the construction of a variety of agents, particularly neural nets, and 
experiment with using GAs to train them.

