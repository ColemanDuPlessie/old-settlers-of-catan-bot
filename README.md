An old Settlers of Catan bot I made several years ago. Gameplay is decent, UI is clunky.

Since I wrote this before I began using git for most projects (big mistake, I should have started sooner!) there is unfortunately no version here; I uploaded this after the fact.

This project is really quite old (made in 2020); it is certainly not representative of my current ability as a programmer.

## Setup

To try it yourself, run SettlersGame.py. It will open a window with several settings for setup (e.g. which bots you play against). The defaults are generally good, though if you have a smaller computer screen, you should turn "Screen Size" down. You can also change Player 4 from "NOBODY" to one of the available bots (they are roughly sorted from smartest to dumbest) if you want a 4-player game instead of 3-player.

After modifying these settings, just click play and it'll generate the board. This should take no more than 10-20 seconds at most. After that, the game is played with the mouse only. The rest of this explanation focuses on the UI of this implementation (I made some questionable decisions when I designed it ~4 years ago) and assumes that you already understand the rules of Settlers (if not, see the [official rules](https://www.catan.com/sites/default/files/2021-06/catan_base_rules_2020_200707.pdf))

## Player Cards

Player information is easily available on "player cards" to the left of the screen. Each player card contains many pieces of information. In normal reading order, they are:

- Number of resource cards in hand
- Points (first player to 10 points wins!)
- Number of development cards in hand
- Roads (max of 15) and an indicator of longest road
- Settlements (max of 5)
- Cities (max of 4)
- Soldiers played and an indicator of largest army
- Player/bot name

## Gameplay

At the beginning of the game, players set up their starting settlements and roads. Your opponents will do this automatically. When it is your turn, there will be a white dot at each legal placement location, which you can click to place a settlement. You can see what the game is currently waiting for you to do by looking in the top-left, to the right of the player cards (this is true at all stages of the game).

During normal gameplay, the dice(top left of the screen) will be rolled automatically at the start of each player's turn. Resources will accrue in your hand in the bottom right. Each color corresponds to one resource (dark green = wood, red = brick, light green = sheep, yellow = wheat, gray = ore).

#### Trading

When it is a bot's turn, it will automatically propose trades with you and other bots. You can see all trade offers made and accept or reject them to the right of the board (though if you're winning, the bot may be willing to trade, just not with you). If you get tired of seeing the bot ask you for resources you don't have, click the green box labeled "view trades you cannot accept" to toggle seeing these trades.

On your turn, you may make trades immediately after rolling the dice and collecting resources (which is automatic). To offer cards from your hand, click them (click them again to deselect them), and to request cards from your opponents, use the five resource selectors above your hand. Once you have selected what you want, click "offer." If you can complete the trade entirely by using the bank (using 4:1 trades and harbor trades), you will. Otherwise, each opponent will see your trade offer and will accept or reject it. You can then decide who to trade with by clicking the checkmark corresponding to one of the players who accepted your trade (or clicking "no" to cancel the trade). When you are done, click "done" to move on to building.

#### Building

Bots build automatically during their turns. On your turn, after trading, there will be a button visible for each item you can build (road, settlement, city, development card). This means there may be no buttons visible if you can't build anything (e.g. you don't have enough resources, you have no space for a settlement, you have no settlements to upgrade to cities). Click the button to automatically spend the necessary resources. For roads, settlements, and cities, you then must choose where the item will be placed. Development cards will be visible on the right of the screen. They cannot be played the turn they are purchased. On subsequent turns, you can click a development card twice to play it.

## Troubleshooting

If the game seems stuck or you're unsure what to do, check the text in the top left (to the immediate right of the player cards and dice); it will tell you what action the game is waiting on.

If the game crashes after hitting play but before showing you the board, try running it again, but increase the slider marked "Balance Precision."
