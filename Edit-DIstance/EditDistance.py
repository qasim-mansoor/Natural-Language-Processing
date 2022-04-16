from tokenize import String


city = input("Enter city name: ")
city = city.strip().lower()

exact = False

f = open("cities.txt", "r")

lowest_score = None
lowest_name = None

def recursiveEditDistance(source, target, slen, tlen):
    if slen == 0:
        return tlen
    if tlen == 0:
        return slen
    if source[slen - 1] == target[tlen - 1]:
        return recursiveEditDistance(source, target, slen - 1, tlen - 1)
    
    return min(recursiveEditDistance(source, target, slen, tlen - 1) + 1,
              recursiveEditDistance(source, target, slen - 1, tlen) + 1,
                recursiveEditDistance(source, target, slen - 1, tlen - 1) + 2)


for line in f:
    target = line.strip().lower()

    score = recursiveEditDistance(city, target, len(city), len(target))
    if(score == 0):
        exact = True
        break
    
    
    if(lowest_score == None or score < lowest_score):
        lowest_score = score
        lowest_name = target


if(exact):
    print(city + " is a city in Pakistan.")
else:
    print("Did you mean: " + lowest_name)
    

    