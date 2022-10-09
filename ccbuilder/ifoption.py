from enum import IntFlag


class IfOption(IntFlag):
    ifStmt = 1
    elseIfStmt = 2
    whileStmt = 3
    caseStmt = 4
    ternaryIfStmt = 5
    doWhileStmt = 6
    forStmt = 7
    # switchStmt = 8
    # elseStmt = 9
