"""games models"""
from datetime import datetime

from sqlalchemy.orm import validates

from mastermind_be.database import db


# game table
class Game(db.Model):
    """ Games table """

    __tablename__ = 'games'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    player1_name = db.Column(
        db.Text,
        nullable=False
    )

    player1_guesses_count = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    player2_name = db.Column(
        db.Text,
        nullable=False
    )

    player2_guesses_count = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # TODO: SET enums for status. ONGOING, WIN, LOSS
    status = db.Column(
        db.Text,
        # SQLAlchemyEnum(GameStatusEnum, name='game_status_enum'),
        nullable=False,
        default="ONGOING"
    )

    winner = db.Column(
        db.Text,
        nullable=True,
    )

    spaces = db.Column(
        db.Integer,
        db.CheckConstraint('spaces >= 4 AND spaces <= 7'),
        nullable=False
    )

    @validates("spaces")
    def validate_spaces(self, key, value):
        """validates number of spaces is between 4 and 7"""

        parsed_value = int(value)
        if 4 > parsed_value > 7:
            raise ValueError("Number to guess must be between 4 and 7")
        return parsed_value

    number_to_guess = db.Column(
        db.Integer,
        nullable=False
    )

    # TODO: ADD MULTIPLAYER FUNCTIONALITY.
    players_count = db.Column(
        db.Integer,
        nullable=False,
        default=2
    )

    computer_opponent = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    attempts = db.Relationship("Attempt", back_populates="game", uselist=True)

    # attempts = db.Column(
    #     db.Integer,
    #     nullable=False,
    #     default=0
    # )

    def serialize(self):
        """returns self"""

        return {
            "id": self.id,
            "number_to_guess": self.number_to_guess,
            "spaces": self.spaces,
            "player1_name": self.player1_name,
            "player2_name": self.player2_name,
            "winner": self.winner,
            "status": self.status,
            "date_created": self.date_created,
            "attempts": self.attempts
        }

    @classmethod
    def create_game(cls, number_to_guess, spaces, player1_name, player2_name):
        """Instantiates a game with a number to guess"""

        game = Game(
            number_to_guess=number_to_guess,
            spaces=spaces,
            player1_name=player1_name,
            player2_name=player2_name
        )

        db.session.add(game)
        db.session.commit()

        return game

    @staticmethod
    def player1_increment_guess(game):
        """Static Method to Increment player1 guesses on a game."""

        game.player1_guesses_count += 1
        db.session.commit()

        return game

    @staticmethod
    def player2_increment_guess(game):
        """Static Method to Increment player2 guesses on a game."""

        game.player2_guesses_count += 1
        db.session.commit()

        return game

    @staticmethod
    def set_status_completed(game):
        """Sets the game status to completed"""

        game.status = "COMPLETED"
        db.session.commit()

        return game

    @staticmethod
    def set_winner_user1(game):
        """Sets the winner to user1"""

        game.winner = "user1"
        db.session.commit()

        return game

    @staticmethod
    def set_winner_user2(game):
        """Sets the winner to user2"""

        game.winner = "user2"
        db.session.commit()

        return game

# user table


