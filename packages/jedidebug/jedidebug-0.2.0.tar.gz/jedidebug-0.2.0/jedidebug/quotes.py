"""
Contains the database of Star Wars quotes for JediDebug.
"""

# General debugging quotes
GENERAL_QUOTES = [
    "Do or do not. There is no try. But seriously, try adding some print statements.",
    "The Force is strong with this one. The bug? Not so much.",
    "In my experience, there's no such thing as luck. But there is such a thing as a well-placed debugger.",
    "Your focus determines your reality. Focus on line 42, perhaps?",
    "The ability to destroy a planet is insignificant next to the power of fixing this bug.",
    "These aren't the bugs you're looking for. Look elsewhere in your code.",
    "You will find that many of the bugs we encounter depend greatly on our own point of view.",
    "Judge me by my code size, do you? And well you should not.",
    "Patience you must have, my young developer.",
    "Always pass on what you have learned. Especially about this bug.",
    "I find your lack of comments disturbing.",
    "The greatest teacher, failure is.",
    "Never tell me the odds of fixing this on the first try!",
    "Stay on target... stay on target!",
    "This is the way... to debug your code.",
    "Difficult to see. Always in motion is the future of this code.",
    "Help me debugger, you're my only hope.",
    "I've got a bad feeling about this variable.",
    "Fear is the path to the dark side. Fear leads to anger. Anger leads to hate. Hate leads to spaghetti code.",
    "You must unlearn what you have learned. Try a different approach.",
    "No! Try not. Do. Or do not. There is no try. But really, just keep debugging.",
    "May the Force be with your debugging efforts.",
    "The dark side clouds everything. Impossible to see, this bug is.",
    "Luminous beings are we, not this crude exception.",
    "Remember, a Jedi can feel the Force flowing through clean code."
]

# Quotes for specific error types
ERROR_QUOTES = {
    # Syntax errors
    'syntax': [
        "Your syntax is not complete. Much to learn, you still have.",
        "Powerful you have become, the dark side of syntax I sense in you.",
        "The syntax error is strong in this one.",
        "Your indentation betrays you. Your spacing has made you not powerful.",
        "Difficult to see. Always in motion are the brackets.",
    ],
    
    # Logic errors
    'logic': [
        "Trust your feelings, not your logic. Your algorithm is flawed.",
        "I sense a disturbance in your logic flow.",
        "This logic error will be the last mistake you ever make.",
        "You were the chosen one! You were supposed to bring balance to the logic, not destroy it!",
        "Be mindful of your thoughts. They betray your logical errors.",
    ],
    
    # Runtime errors
    'runtime': [
        "Size matters not. Look at your runtime errors. Judge them by their size, do you?",
        "The runtime will be with you, always. Especially when you don't want it to be.",
        "At runtime, the code becomes more powerful than you could possibly imagine.",
        "Happens at runtime. It does.",
        "Attachment leads to jealousy. The shadow of runtime errors, that is.",
    ],
    
    # Memory errors
    'memory': [
        "Memory leaks lead to suffering.",
        "Impossible to see, the memory allocation is.",
        "The garbage collector is your ally, and a powerful ally it is.",
        "The memory errors are easily startled, but they'll soon be back, and in greater numbers.",
        "Your memory management skills determine your commitment to the dark side.",
    ],
    
    # Input/Output errors
    'io': [
        "Be careful not to choke on your IO operations, Director.",
        "The file does not exist. Search your feelings, you know it to be true.",
        "Perhaps the archives are incomplete. Check your file paths.",
        "The file you seek is not complete.",
        "If an item does not appear in our records, it does not exist. Check your file system.",
    ],

    # Final encouraging words
    'encouragement': [
        "Trust your instincts, young Padawan. The solution is near.",
        "Strong in the Force you are. Fix this bug, you will.",
        "A Jedi uses the Force for knowledge and defense, never for despair. Keep debugging.",
        "You can do this. The Force will be with you, always.",
        "When gone am I, the last of the Jedi will you be. The Force is strong with you.",
    ]
}

# Combined quotes from all categories
ALL_QUOTES = GENERAL_QUOTES + sum(ERROR_QUOTES.values(), [])

# Error type to quote category mapping 
ERROR_TYPE_MAP = {
    'SyntaxError': 'syntax',
    'IndentationError': 'syntax',
    'TabError': 'syntax',
    
    'ValueError': 'logic',
    'TypeError': 'logic',
    'AssertionError': 'logic',
    'AttributeError': 'logic',
    
    'RuntimeError': 'runtime',
    'RecursionError': 'runtime',
    'TimeoutError': 'runtime',
    'StopIteration': 'runtime',
    
    'MemoryError': 'memory',
    'BufferError': 'memory',
    
    'FileNotFoundError': 'io',
    'PermissionError': 'io',
    'FileExistsError': 'io',
    'IsADirectoryError': 'io',
    'IOError': 'io',
}