# Mapping to translate input encoded moves to a common representation (R, P, S).
TRANSLATE_MOVES = {"X": "R", "Y": "P", "Z": "S", "A": "R", "B": "P", "C": "S"}
SHAPE_SCORES = {"R": 1, "P": 2, "S": 3}

# Inverse mappings of what shapes beat/lose to other shapes.
BEATS = {"R": "S", "P": "R", "S": "P"}
LOSES_TO = {loser: winner for winner, loser in BEATS.items()}

# Point values for drawing/winning, losing gets no points.
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


# Determine the shape to play in order to achieve the given result depending on
# what they opponent plays.
def getShapeToPlay(theyPlay: str, result: str) -> str:
    if result == "X":
        return BEATS[theyPlay]
    elif result == "Y":
        return theyPlay
    else:
        return LOSES_TO[theyPlay]


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
