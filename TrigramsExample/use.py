import pickle
import random
  
chain = pickle.load(open("chain.p", "rb"))
  
new_review = []
sword1 = "BEGIN"
sword2 = "NOW"
  
while True:
    sword1, sword2 = sword2, random.choice(chain[(sword1, sword2)])
    if sword2 == "END":
        break
    new_review.append(sword2)
  
print (' '.join(new_review))