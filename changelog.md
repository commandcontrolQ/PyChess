# Changelog

## Build 919.1 (19th September 2023)
- Added the ability to choose to play white, black, both or to let the AI play itself.
  - *In the next build, I am looking to add the ability to play again after a game is finished.*
- Sound files have been added to the repository but have not been implemented yet.
  - **They will likely be implemented in the next build.**
- Added a move log on the right hand side of the board (uses new notation *similar* to PGN).
  - *The old notation was removed and the new notation uses a overrided `__str__()` function.*
  - **Notation for checks, checkmates, and pawn promotions have yet to be implemented.**
- Changed the images used for the chess pieces (old images were from [*Wikipedia: Chess*](https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent), new images are from [*greenchess.net*](https://greenchess.net/info.php?item=downloads).

## Build 919 (19th September 2023)
- Implemented Alpha-Beta pruning into the NegaMax recursion function. Performance is slightly improved.
  - **The depth of the recursion is still kept at 2 moves.**
- Deprecated multiple functions (they are likely to be removed)
  - The line in the current `findBestMove()` function referenced in build 918.1 has been removed.
- Removed the old `findBestMove()` function
- Removed the ability to undo a move using the 'z' button due to it causing multiple issues.

## Build 918.1 (18th September 2023)
- Changed the way the AI works to use NegaMax recursion instead of MinMax recursion. **MinMax recursion is still implemented and can be used by uncommenting a line in the `findBestMove()` function.**
  - The AI does run slower than usual, *although it is not due to the depth*. This will be fixed in a later build.
- Fixed a critical bug where PyChess would crash after castling due to a bad implementation of the `getKingMoves()` function.

## Build 918 (18th September 2023)
- Fixed castling issue where castling rights would be lost after the third move when looking for the best AI move.
  - **This issue was caused by how assignment statements work in Python. A workaround is to use `copy.deepcopy()`.** For more information, see [*here*](https://tinyurl.com/copypython).

## Build 906 (6th September 2023)
- Added move highlighting
- Added animations for when moves are made
- Added reset function (press 'r')
- Fixed bug with castling where the king could castle with a non-existent rook as long as that rook never moved
- Added messages that pop up when the game ends
  - Fixed a bug where the user could still press 'z' or 'r' after the game ended.
  - **The previous issue from last build has persisted. While I don't recommend using the undo function, it will not be commented out.**

## Build 825 (25th August 2023)
- Added support for castling
  - **There is currently an issue where it is not possible to redo a castle. This is being worked on.**

## Build 713 (13th July 2023)
- Added basic pawn promotion (at the moment, you can only promote to a queen)
- Added en-passant support
- Move notation has been changed to try to mimic the PGN format
  - **This is known to be buggy, and therefore it is commented out by default.**

## Build 712 (12th July 2023)
- Added checks
- Added checkmates
- Added stalemates

## Build 704 (4th July 2023)
- Initial release
  - Added basic movement for all pieces
  - Added undo function (press 'z')
  - Added simple move notation (move notation is formatted as `xxyy` where xx is the starting coordinate and yy is the ending coordinate)
