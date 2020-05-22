""" Validate the HXL knowledge base

Requires Python3.

Usage:

    python validate-base.py

Started 2020-05-22 by David Megginson

"""

import json, logging, sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Validate")

# Requires Python3 or higher
if sys.version_info < (3, ):
    raise Exception("Requires Python3 or higher")

def validate (data):
    """ Validate a JSON knowledge base

    @param data: the data structure to validate
    @returns: the number of errors logged (0 means no errors)
    """

    error_count = 0
    linked = set()

    def check (key, question, history=[]):
        """ Recursively check the whole tree """

        nonlocal error_count, linked

        linked.add(key)

        # Check for circular references
        if key in history:
            logger.error("Circular reference for question %s: %s", key, str(history + [key]))
            error_count += 1

        # Check each option
        for option in question["options"]:
            if "dest" in option:
                # non-terminal node: check linked question recursively
                newkey = option["dest"]
                if newkey in data:
                    check(newkey, data[newkey], history + [key])
                else:
                    logger.error("Destination question %s (from %s) does not exist", newkey, key)
                    error_count += 1

    if "top" in data:
        # Start at the top node
        check("top", data["top"], [])
    else:
        logger.error("No question marked \"top\" in data")
        error_count += 1

    # check for orphans
    orphans = set(data.keys()).difference(linked)
    for orphan in orphans:
        logger.error("Question \"%s\" is unreachable", orphan)
        error_count += 1

    return error_count
                    
        
#
# If run from the command line
#
if __name__ == "__main__":
# TODO: specify file on command line
    with open("hxl-knowledge-base.json", "r") as input:
        error_count = validate(json.load(input))
        if error_count > 0:
            logger.warning("%d error%s", error_count, ("" if error_count == 1 else "s"))
            sys.exit(1)
        else:
            sys.exit(0)
