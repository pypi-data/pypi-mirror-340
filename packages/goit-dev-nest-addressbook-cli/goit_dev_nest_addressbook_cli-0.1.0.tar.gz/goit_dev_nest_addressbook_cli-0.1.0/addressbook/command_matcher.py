import difflib

KNOWN_COMMANDS = [
    "add", "change", "phone", "all", 
    "add-birthday", "show-birthday", 
    "birthdays", "hello", "exit", "close"
]

def match_command(user_input: str, threshold=0.7):
    input_clean = user_input.strip().lower()
    closest = difflib.get_close_matches(input_clean, KNOWN_COMMANDS, n=1, cutoff=threshold)
    return closest[0] if closest else None