# Acquire
An implementation of the Sid Sackson 3M Classic for purposes of exploring Artificial Intelligence
## Background
Acquire is a favorite of mine. When I'm hosting a game night, I find this game to be a good one to teachpersons new to gaming, as the rules are simple, and the goal (make money) is more concrete than victory point schemes, and the game has suspense, and a sense of history.

I thought that coming up with an AI for the game could be very interesting, as good play 
requires interpreting other player's actions, and understaning the board. The latter, 
in particular, seems like a good place for the use of Neural Nets. Perhaps a good AI could 
teach me to play better!

Also, AI's are more fun when you interact with them. I've written this program with hopefully enough
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
The UI is nearly complete. I think I have only one or two more dialogs to write, and then it 
is playable enough, albeit only against agents that choose their actions randomly. Once this
is done I want to explore the construction of neural nets, and possibly experiment with GAs to 
train them.

