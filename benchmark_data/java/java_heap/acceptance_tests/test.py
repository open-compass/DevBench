from subprocess import run
import sys
import os
import re
from collections import Counter

def check_format(s):
    # Define the patterns for each heap operation
    patterns = [
        r"Fibonacci Heap Insertion Time: \d+ms",
        r"Leftist Heap Insertion Time: \d+ms",
        r"Fibonacci Heap Deletion Time: \d+ms",
        r"Leftist Heap Deletion Time: \d+ms",
        r"Fibonacci Heap Merge Time: \d+ms",
        r"Leftist Heap Merge Time: \d+ms"
    ]

    # Split the string into lines
    lines = s.strip().split('\n')

    # Count occurrences of each pattern
    pattern_counts = Counter()

    for line in lines:
        # Check if the line matches any of the patterns
        for pattern in patterns:
            if re.match(pattern, line):
                pattern_counts[pattern] += 1
                break
        else:
            # If the line doesn't match any pattern, return False
            return False

    # Check if each pattern appears exactly once
    return all(count == 1 for count in pattern_counts.values())

run("./gradlew clean", shell=True)
run("./gradlew build jar", shell=True)
ret = run("java -jar build/libs/java_heap-1.0-SNAPSHOT.jar 10000", shell=True, capture_output=True, text=True)


if ret.returncode == 0:
    if not check_format(ret.stdout):
        print("test failed.")
        sys.exit(1)
    else:
        print("test passed.")
        sys.exit(0)

else:
    print("test failed.")
    sys.exit(1)

