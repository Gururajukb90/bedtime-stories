#!/usr/bin/env python3
"""Deterministic bedtime story generator (no APIs, no secrets).

Writes stories/YYYY-MM-DD.md using the Europe/Brussels local date.
The same date always produces the same story; themes rotate daily.

Usage: python scripts/generate_story.py [YYYY-MM-DD]
"""
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# --- Customize here -------------------------------------------------------
MIN_WORDS, MAX_WORDS = 120, 220  # allowed story length (body + moral)

# (hero, friend, place) - add more entries to add variety.
SETTINGS = [
    ("Milo the little rabbit", "Pip the sparrow", "a meadow full of daisies"),
    ("Luna the baby owl", "Fern the hedgehog", "a quiet pine forest"),
    ("Benny the small bear", "Dot the ladybug", "a sunny hill by the river"),
    ("Tilly the young turtle", "Odo the duck", "a sparkling pond"),
    ("Coco the kitten", "Wink the firefly", "a cosy garden"),
]

# (theme, what happens in the middle, moral) - add more to rotate more morals.
THEMES = [
    ("Sharing",
     "found one big, juicy berry and only one. {hero} thought for a moment, "
     "then cut the berry in two and gave half to {friend}. They both smiled "
     "as sweet juice tickled their noses",
     "Sharing makes happy things even happier."),
    ("Kindness",
     "saw {friend} sitting alone and looking sad. {hero} sat close, gave a "
     "warm hug, and said, \"I am here.\" Soon {friend} was giggling again",
     "A kind heart can turn a sad day into a happy one."),
    ("Honesty",
     "accidentally knocked over a basket of acorns. {hero} felt a little "
     "scared, but told {friend} the truth. {friend} said, \"Thank you for "
     "telling me. Let us fix it together,\" and they did",
     "Telling the truth is brave, and it makes our hearts feel light."),
    ("Patience",
     "planted a tiny seed and wanted it to grow right away. {friend} "
     "whispered, \"Good things take time.\" So they waited, watered the seed, "
     "and one morning a bright flower popped up",
     "Good things come to those who wait."),
    ("Courage",
     "heard a rustle in the dark and felt wobbly inside. {hero} took a deep "
     "breath and looked. It was only a friendly breeze dancing in the leaves, "
     "and {friend} laughed with relief",
     "Being brave means trying even when we feel a little scared."),
    ("Gratitude",
     "ate a yummy snack that {friend} had made. {hero} said, \"Thank you, "
     "this is lovely!\" and {friend} beamed from ear to ear",
     "Saying thank you fills everyone's heart with sunshine."),
    ("Teamwork",
     "tried to roll a big round pebble up the path but it was too heavy. "
     "{friend} came to help, and together they pushed it all the way to the "
     "top with a happy cheer",
     "Together we can do things that are too big to do alone."),
]


def build_story(day: date) -> str:
    """Return the markdown story for a given date (rotates by day number)."""
    n = day.toordinal()
    hero, friend, place = SETTINGS[n % len(SETTINGS)]
    theme, middle, moral = THEMES[n % len(THEMES)]
    middle = middle.format(hero=hero, friend=friend)

    paragraphs = [
        f"Once upon a time, {hero} lived near {place}. The sun was sinking "
        f"low, the sky turned soft pink, and everything felt calm and cosy. "
        f"{hero} loved evenings like this, when the whole world slowed down.",
        f"On this special evening, {hero} went for a little walk with "
        f"{friend}. Along the way, {hero} {middle}. It was a small moment, "
        f"but it felt very big and very warm.",
        f"As the first stars began to twinkle, {hero} and {friend} waved "
        f"goodnight. {hero} walked home slowly, feeling happy and proud. "
        f"A soft blanket was waiting, and a gentle breeze hummed a lullaby. "
        f"{hero} yawned a big, sleepy yawn, snuggled in tight, closed "
        f"both eyes, and drifted off to a peaceful sleep.",
        "The end. Sweet dreams.",
    ]
    title = f"{theme} Under the Stars: The Story of {hero.split(' the ')[0]}"
    body = "\n\n".join(paragraphs)
    words = len((body + " " + moral).split())
    if not MIN_WORDS <= words <= MAX_WORDS:
        raise ValueError(f"Story has {words} words; expected {MIN_WORDS}-{MAX_WORDS}")
    return f"# {title}\n\n{body}\n\nMoral: {moral}\n"


def main() -> None:
    if len(sys.argv) > 1:
        day = date.fromisoformat(sys.argv[1])
    else:
        # Always use the Belgium calendar date, regardless of runner timezone.
        day = datetime.now(ZoneInfo("Europe/Brussels")).date()
    out = Path(__file__).resolve().parent.parent / "stories" / f"{day.isoformat()}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(build_story(day), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
