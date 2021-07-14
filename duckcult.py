# Duck Hunger Cowntdown
import time
from replit import db

hunger = db["hungerbar"]

while hunger != 0:
  hunger = db["hungerbar"]
  time.s(60)
  hunger = hunger - 1
  db["hunger"] = hunger