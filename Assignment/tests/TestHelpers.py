# Author: F.M. Ashfaq
# Student ID: 23472297
# Date: 2026-10-25
# Purpose: Provide simple pass checks and expected-error checks for test drivers.

def expectError(label, exception_type, operation):
    raised = False
    try:
        operation()
    except exception_type as error:
        print(f"PASS {label}: {error}")
        raised = True
    if not raised:
        raise AssertionError("Expected error was not raised: " + label)


def check(label, condition):
    if not condition:
        raise AssertionError("Failed: " + label)
    print("PASS", label)
