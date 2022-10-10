from enum import IntFlag


class ScopeOption(IntFlag):
    functionEnd = 1
    ifEnd = 2
    whileEnd = 3
    switchEnd = 4
    caseEnd = 5
    jumpEnd = 6
    ternaryEnd = 7
