import json

with open('mainbank.json', 'r') as f:
    users = json.load(f)

for user in users:
    bank = users[user]["bank"]
    bank += bank*0.069
    print(bank)
    users[user]["bank"] = bank
    with open('mainbank.json', 'w') as f:
        json.dump(users, f)