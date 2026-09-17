"""Tuning values for callout routing.

Everything in here changes who gets asked to take a job, so don't
change anything in here without telling Marcus.
"""

# How long a callout offer stays on a responder's phone before we give
# up on them and move to the next person on the list.
OFFER_TIMEOUT_SECONDS = 60           # was 90 until 4.2

# How much each input counts when we rank who to ask first. These are
# relative to each other; they don't need to add up to anything.
WEIGHT_PROXIMITY = 0.60              # was 0.45 until 4.2
WEIGHT_RECENT_ACCEPTANCE = 0.25      # was 0.40 until 4.2
WEIGHT_CAPABILITY_MATCH = 0.15       # unchanged since 4.0

# Points on and off the recent-acceptance score. Kept equal so that
# someone answering yes half the time holds steady at NEUTRAL_SCORE
# instead of drifting down — was 0.08/0.12 (a 60% breakeven) until the
# fix proposed 17 Sep 2026.
ACCEPTANCE_CREDIT = 0.10
DECLINE_PENALTY = 0.10

# A timeout isn't a confirmed active refusal, so it costs less than an
# explicit decline until we know otherwise.
TIMEOUT_PENALTY = 0.05

# How much of the gap back to NEUTRAL_SCORE closes per day of no
# activity. 0.05 means a stale score is back to neutral in about three
# weeks with no further offers either way.
DECAY_PER_DAY = 0.05

# The score never goes outside these.
SCORE_FLOOR = 0.0
SCORE_CEILING = 1.0

# Anyone further out than this scores zero on proximity.
PROXIMITY_HORIZON_MINUTES = 45
