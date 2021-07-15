# Duck Hunger Cowntdown
import time
from replit import db

db["hungerbar"] = 100

hunger = db["hungerbar"]

while hunger != 0:
  hunger = db["hungerbar"]
  time.sleep(5)
  hunger = hunger - 1
  db["hungerbar"] = hunger
  print(hunger)