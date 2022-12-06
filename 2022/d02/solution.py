# First column
# A - Rock
# B - Paper
# C - Scissors

# Second column
# X - Rock
# Y - Paper
# Z - Scissors

# The strategy is not intended to win every time, but to inconspicuously win the
# tournament with the most points.

# Score is the sum of scores for each round.
# The score fora single round is the score for the shape you selected:
# Rock - 1
# Paper - 2
# Scissors - 3
# Plus the score for the outcome of the round:
# Loss - 0
# Draw - 3
# Win - 6

TRANSLATE_MOVES = {"X": "R", "Y": "P", "Z": "S", "A": "R", "B": "P", "C": "S"}
SHAPE_SCORES = {"R": 1, "P": 2, "S": 3}
BEATS = {"R": "S", "P": "R", "S": "P"}
LOSES = {loser: winner for winner, loser in BEATS.items()}

DRAW = 3
WIN = 6

# Calculate the score of the given round based upon what you and your opponent
# play.
def calculateRoundScore(theyPlay: str, youPlay: str) -> int:
    score = SHAPE_SCORES[youPlay]

    # You only get points for the result of a round if it is a tie or a win.
    if theyPlay == youPlay:
        score += DRAW
    elif BEATS[youPlay] == theyPlay:
        score += WIN

    return score


# Calculate the score of the given strategy using the second column as what move
# to play.
def calculateMoveStrategyScore(strategy: list[tuple[str, str]]) -> int:
    return sum(
        [
            calculateRoundScore(TRANSLATE_MOVES[theyPlay], TRANSLATE_MOVES[youPlay])
            for theyPlay, youPlay in strategy
        ]
    )


def getShapeToPlay(theyPlay: str, result: str) -> str:
    if result == "X":
        return BEATS[theyPlay]
    elif result == "Y":
        return theyPlay
    else:
        return LOSES[theyPlay]


# Calculate the score of the given strategy using the second column as what
# result to get in the round.
def calculateResultStrategyScore(strategy: list[tuple[str, str]]) -> int:
    return sum(
        [
            calculateRoundScore(
                TRANSLATE_MOVES[theyPlay],
                getShapeToPlay(TRANSLATE_MOVES[theyPlay], result),
            )
            for theyPlay, result in strategy
        ]
    )
