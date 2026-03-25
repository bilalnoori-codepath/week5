"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
]

SAMPLE_POSTS += [
    "Not gonna lie, this is kinda mid 😬",
    "I'm so exhausted but I finally got it done! 🎉",
    "lowkey dreading tomorrow but it is what it is 🙃",
    "just got ghosted lol why am I even surprised 💀",
    "okay the food was actually bussin no cap 🔥",
    "I absolutely love sitting in traffic for two hours 🙃",
    "feel like crying but also kinda fine?? idk man",
]

TRUE_LABELS += [
    "negative",   # "Not gonna lie, this is kinda mid 😬"
    "mixed",      # "I'm so exhausted but I finally got it done! 🎉"
    "mixed",      # "lowkey dreading tomorrow but it is what it is 🙃"
    "negative",   # "just got ghosted lol why am I even surprised 💀"
    "positive",   # "okay the food was actually bussin no cap 🔥"
    "negative",   # "I absolutely love sitting in traffic for two hours 🙃" (sarcasm)
    "mixed",      # "feel like crying but also kinda fine?? idk man"
]

# Stress-test posts: sarcasm, double negation, faint positivity, and slang the word list won't know
SAMPLE_POSTS += [
    "oh great, another Monday 🙄",
    "not gonna say it was bad but I definitely didn't have fun",
    "it's not the worst thing ever I guess",
    "that presentation slapped fr fr 🔥",
]

TRUE_LABELS += [
    "negative",   # "oh great, another Monday 🙄" — sarcasm, 'great' used ironically
    "negative",   # "not gonna say it was bad but I definitely didn't have fun" — double negation still lands negative
    "mixed",      # "it's not the worst thing ever I guess" — lukewarm, double-negative softens it
    "positive",   # "that presentation slapped fr fr 🔥" — enthusiastic praise, pure slang
]
