"""Recent acceptance — a running score of how often somebody has been
taking the callouts we send them.

One of the three inputs to ranking. Sits between 0 and 1. Everyone
starts at NEUTRAL_SCORE when we take them on.

Answers the 2019 TODO that used to sit here: the score now eases back
toward NEUTRAL_SCORE on its own the longer it's been since it last
moved, so a bad stretch fades instead of sticking forever — see
DECAY_PER_DAY. A timeout is also no longer scored the same as an
active decline; see record_no_answer.
"""

import time

from config import (
    ACCEPTANCE_CREDIT,
    DECLINE_PENALTY,
    TIMEOUT_PENALTY,
    DECAY_PER_DAY,
    SCORE_FLOOR,
    SCORE_CEILING,
)

NEUTRAL_SCORE = 0.5
SECONDS_PER_DAY = 86400

# responder.id -> (score, last_updated_epoch_seconds)
_scores = {}


def recent_acceptance(responder):
    """This responder's score right now, decayed toward neutral for
    however long it's been since it last moved. Read by
    routing.score()."""
    return _decayed(responder)


def record_accepted(responder):
    """They took the callout. Score goes up."""
    _set(responder, _decayed(responder) + ACCEPTANCE_CREDIT)


def record_declined(responder):
    """They actively turned it down. Score goes down."""
    _set(responder, _decayed(responder) - DECLINE_PENALTY)


def record_no_answer(responder):
    """The offer timed out before they answered. We don't know if they
    ever saw it, so this costs less than an active decline."""
    _set(responder, _decayed(responder) - TIMEOUT_PENALTY)


def _decayed(responder):
    """The stored score, eased toward NEUTRAL_SCORE for the time
    that's passed since it last changed."""
    score, last_updated = _scores.get(responder.id, (NEUTRAL_SCORE, None))
    if last_updated is None:
        return score
    days_idle = (time.time() - last_updated) / SECONDS_PER_DAY
    closed = min(1.0, days_idle * DECAY_PER_DAY)
    return score + (NEUTRAL_SCORE - score) * closed


def _set(responder, value):
    clamped = max(SCORE_FLOOR, min(SCORE_CEILING, value))
    _scores[responder.id] = (clamped, time.time())
