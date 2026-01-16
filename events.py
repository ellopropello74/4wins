from event_bus import EventBus

# Initialize the global event bus.
bus = EventBus()


class MouseHoverEvent:

    def __init__(self, posx: int):
        self.posx = posx


class MouseClickEvent:

    def __init__(self, posx: int):
        self.posx = posx


class GameOver:


    def __init__(self, was_tie: bool = True, winner: str = None, winning_pieces: list = None):
        self.was_tie = was_tie
        self.winner = winner
        self.winning_pieces = winning_pieces


class PieceDropEvent:
    def __init__(self, side: str):
        self.side = side

