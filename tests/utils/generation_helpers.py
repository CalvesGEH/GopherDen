import random, string

def randomword(max_length, min_length=1):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(random.randint(min_length, max_length)))

def random_sentence():
    return ' '.join([randomword(10) for i in range(1, random.randint(5, 10))])

def random_person():
    # Open up tests/data/fake_people.csv and grab a random person.
    with open('tests/data/fake_people.csv', 'r') as f:
        lines = f.readlines()
        user = lines[random.randint(0, len(lines)-1)].strip(" \n").split(',')
        return {
            "first_name": user[0],
            "last_name": user[1],
            "email": f"{user[0]}.{user[1]}@{randomword(10,5)}.{randomword(3)}",
        }
    
def random_chore():
    # Open up tests/data/fake_chores.txt and grab a random chore.
    with open('tests/data/fake_chores.txt', 'r') as f:
        lines = f.readlines()
        chore = lines[random.randint(0, len(lines)-1)].strip(" \n").split('|')
        return {
            "name": chore[0],
            "description": chore[1],
            "total_time_minutes": chore[2],
            "frequency_days": chore[3],
        }
    
def random_tool():
    # Open up tests/data/fake_tools.txt and grab a random tool.
    with open('tests/data/fake_tools.txt', 'r') as f:
        lines = f.readlines()
        tool = lines[random.randint(0, len(lines)-1)].strip(" \n").split('|')
        return {
            "name": tool[0],
            "description": tool[1],
        }