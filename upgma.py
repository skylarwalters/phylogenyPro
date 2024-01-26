# UPGMA

# ----------------------- importing packages -----------------------
import sys
import graphviz

# -------------------------- parsing files -------------------------
file = open(sys.argv[1])
output = open(sys.argv[2], 'w')

lines = file.readlines()
speciesSet = set()
graph = graphviz.Graph(name="my-tree", filename=sys.argv[2])

if lines == '' or lines == ' ' or lines == '\n' or lines == '\n':
    print('')
    graph.save(filename=sys.argv[2])

else:        
    # DATA STRUCTURES!!!
    #   pairs: maps string to distance
    #   strings: maps string to list of strings
    #   heights: maps cluster to height
    #   condensed: maps condensed names
    pairs = {}
    strings = {}
    heights = {}
    condensed = {}


    #  ------------ create dictionary (use to populate matrix) -----------

    # generate dictionary with distances
    for line in lines:
        s1 = ''
        s2 = ''
        num = ''
        i = 0
        if s1 == '':
            while line[i] != ' ':
                s1 += line[i]
                i += 1

        while line[i] == ' ':
            i += 1

        if s2 == '':
            while line[i] != ' ':
                s2 += line[i]
                i += 1
        
        while line[i] == ' ':
            i += 1
        
        while i < len(line):
            num += line[i]
            i += 1
        
        if num[len(num) - 1] == '\n':
            num = num[:len(num) - 1]

        # create dictionary
        if s1 < s2:
            pairs['(' + s1 + ',' + s2 + ')'] = float(num)
            strings['(' + s1 + ',' + s2 + ')'] = [s1, s2]
            condensed['(' + s1 + ',' + s2 + ')'] = s1 + s2
        else:
            pairs['(' + s2 + ',' + s1 + ')'] = float(num)
            strings['(' + s2 + ',' + s1 + ')'] = [s2, s1]
            condensed['(' + s2 + ',' + s1 + ')'] = s2 + s1
    
        speciesSet.add(s1)
        speciesSet.add(s2)


    # convert speciesSet to a list
    speciesSet = sorted(list(speciesSet))

    # ---------------------------- file writing ---------------------------

    # add species in speciesSet to tree
    for species in speciesSet:
        # add each item to a height of 0
        heights[species] = 0
        condensed[species] = species
    

    # ---------------------------- adjust vals!!! -----------------------

    # convert to a string with () around it
    def stringIt(one, two):
        if one > two:
            return '(' + two + ',' + one + ')'
        else:
            return '(' + one + ',' + two + ')'
    
    # return the minimum pair of pairs 
    def findMinPair(grouping):
        prevMin = float('inf')
        retPair = ''
        for item in grouping:
            if grouping[item] == prevMin:
                # if the current pair comes lexicographically before the
                # current min
                if item < retPair:
                    prevMin = grouping[item]
                    retPair = item
                    
            if grouping[item] < prevMin:
                prevMin = grouping[item]
                retPair = item
        return retPair

    # computes distances between species 1 and 2
    def calcDist(dict, target, s1, s2):
        dist1 = dict[stringIt(target, s1)]
        dist2 = dict[stringIt(target, s2)]

        dict.pop(stringIt(target, s1))
        dict.pop(stringIt(target, s2))

        return ((dist1 + dist2) / 2)

    # condense form of output
    def condense(s1):
        s1 = ''.join(s for s in s1 if (s != '(' and s != ')' and s!=','))
        return s1

    # create edge between species 1 and 2
    def addEdge(s1, s1h, s2, s2h, h):
        # take in two items you are clustering, create edge from 
        # ab to a and b

        if s1 > s2:
            both = condense(s2 + s1) + str(h)
        else: 
            both = condense(s1 + s2) + str(h)
        graph.edge(both, condense(s1) + str(s1h))
        graph.edge(both, condense(s2) + str(s2h))

    # output list of pairs
    output = []

    while len(pairs) >= 1:
        if len(pairs.keys()) == 1:
            output += pairs.keys()
            #print(pairs.keys())
        #find min key value in pairs
        minPair = findMinPair(pairs)
        pairs.pop(minPair)

        # set s1 and s2 to the individual strings
        s1 = strings[minPair][0]
        s2 = strings[minPair][1]
        
        heights[minPair] = max(heights[s1], heights[s2]) + 1

        # add Edge in graph for s1, s2
        addEdge(s1, str(heights[s1]), s2, str(heights[s2]), heights[minPair])

        speciesSet.remove(s1)
        speciesSet.remove(s2)

        #for each remaining species, calculate new distance
        for species in speciesSet:

            newDist = calcDist(pairs, species, s1, s2)
            
            pairs[stringIt(species, minPair)] = newDist
            strings[stringIt(species, minPair)] = sorted([species, minPair])

        
        speciesSet.append(minPair)

    # save graph in system
    graph.save(filename=sys.argv[2])

    # create output string
    out = ''

    for item in output:
        out += str(item)

    #print output string to terminal
    print(out)