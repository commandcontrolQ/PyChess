# Changelog

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

## Build 704 (4th July 2023?)
- Initial release
  - Added basic movement for all pieces
  - Added undo function (press 'z')
  - Added simple move notation (move notation is formatted as `xxyy` where xx is the starting coordinate and yy is the ending coordinate)
