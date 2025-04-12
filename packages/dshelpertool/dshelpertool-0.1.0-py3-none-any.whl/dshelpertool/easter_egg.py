def fortune_cookie():
    """
    Prints a random data-related quote or joke.
    Good for a break.
    """
    import random
    fortunes = [
        "The best model is the one that ships.",
        "Correlation is not causation — unless you're explaining your code.",
        "90% of Data Science is cleaning the same 3 columns.",
        "Today’s feature is tomorrow’s bug.",
        "You have too many features. Trust me."
    ]
    print(f"🥠 {random.choice(fortunes)}")