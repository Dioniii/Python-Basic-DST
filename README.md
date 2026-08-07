INDUSTRIAL WARFARE
A Pygame Zero Platformer
===========================================

## DESCRIPTION

Industrial Warfare is a side-view platformer built with Pygame Zero. The
player controls a robot character across tile-based levels, avoiding hazards,
fighting off patrolling enemies, collecting a key/chest, and reaching the
exit door to complete the mission.

## LIBRARIES USED

- Pygame Zero (pgzrun) -> game loop, screen drawing, input handling,
  sound playback, Actor/Rect helpers
- Rect (from pgzero.builtins) -> collision boxes for the player, enemies,
  bullets and level tiles (this is the only
  piece imported from the underlying Pygame
  library, as permitted by the task rules)
- pathlib (standard library) -> resolving the folder where level CSV files
  are stored

No other third-party libraries are used. The raw "pygame" library is never
imported directly, only the Pygame Zero wrapper and the allowed Rect class.

## HOW TO RUN

1. Make sure you have Python 3.8+ installed.
2. Install Pygame Zero:
   pip install pgzero
3. From the project folder, run the game with:
   pgzrun main.py
   (Do not run "python main.py" directly, Pygame Zero games are launched
   with the pgzrun command.)

## CONTROLS

- Left Arrow / Right Arrow : move
- Up Arrow : jump
- Space : shoot
- Esc : return to the main menu while playing
- R : restart the level after dying, or return to
  the menu after completing the mission

## PROJECT STRUCTURE

main.py - entry point, main menu (Start / Sound On-Off / Exit),
screen switching between menu and gameplay
gameplay.py - core game loop: player movement, gravity, shooting,
collisions, level loading/advancing, win/lose states
enemy.py - Enemy class, enemy patrol logic and animations, bullet
vs. enemy and player vs. enemy collision checks
platformer.py - tile map loader/renderer, reads level layers from CSV
files and builds solid, hazard, and exit collision areas
images/ - sprite sheets for the player, enemies, tiles and menu
levels/ - CSV tile layer data for each level
sounds/ - background music and sound effects

## GAMEPLAY / GAME DESIGN NOTES

- Two levels, each built from layered CSV tile maps (background, platforms,
  obstacles, scaffolding, doors, collectibles).
- Two distinct enemy types: robot enemies and zombie enemies. Each enemy
  patrols back and forth within a fixed left/right range on its own
  platform and cannot leave that range.
- Player and enemies both use frame-based sprite animation for walking/
  driving and for idling (idle bob/blink cycle), not just a single static
  or mirrored image.
- Hazard tiles (acid) and enemy contact both end the run with a "YOU DIED"
  state; reaching the exit door after picking up the level's key/chest
  advances to the next level, and finishing the last level triggers a
  "MISSION COMPLETE" state. Both endings are reachable without soft-locks.
- Background music loops continuously, with distinct sound effects for
  shooting, taking damage/dying, collecting the key/chest, opening doors,
  and completing the mission. The main menu's Sound button mutes/unmutes
  both music and effects.
