from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
sayA = And(AKnight, AKnave)
knowledge0 = And(
    Implication(AKnight, sayA),
    Implication(AKnave, Not(sayA)),
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sayA = And(AKnave, BKnave)
knowledge1 = And(
    Implication(AKnight, sayA),
    Implication(AKnave,Not(sayA)),
    Or(AKnight,AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight,BKnave),
    Not(And(BKnight, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sayA = Or(And(AKnight, BKnight), And(AKnave, BKnave))
sayB = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    Implication(AKnight, sayA),
    Implication(AKnave, Not(sayA)),
    Implication(BKnight, sayB),
    Implication(BKnave, Not(sayB)),
    Or(sayA, sayB)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

sayA = Or(AKnight, AKnave)
sayBA = BKnave
sayB = CKnave
sayC = AKnight
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight,AKnave)),
    
    Or(BKnight,BKnave),
    Not(And(BKnight,BKnave)),
    
    Or(CKnight,CKnave),
    Not(And(CKnight, CKnave)),
    
    Implication(And(BKnight, AKnight), sayBA),
    Implication(And(BKnight, AKnave), Not(sayBA)),
    Implication(And(BKnave, AKnave), sayBA),
    Implication(And(BKnave,AKnight), Not(sayBA)),
    Implication(BKnight, sayB),
    Implication(BKnave, Not(sayB)),
    Implication(CKnight, sayC),
    Implication(CKnave, Not(sayC))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
