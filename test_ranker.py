from creator import Creator
from ai.ranker import Ranker


c1 = Creator(username="Creator A")
c1.ai_score = 68

c2 = Creator(username="Creator B")
c2.ai_score = 91

c3 = Creator(username="Creator C")
c3.ai_score = 54


creators = [c1, c2, c3]

creators = Ranker.rank(creators)

for creator in creators:
    print(f"{creator.username} -> {creator.ai_score}")