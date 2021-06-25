import numpy as np
import pandas as pd
import scipy.stats as st
import math
import random
import os
from pathlib import Path


#Implementation of the CTW Meta Variables Generator
"""
Name: CTW Basic Variables Generator
Description: This is a python script for the generation of realistic values for the Meta Variables of cable tree wiring (CTW) instances
The Meta Variables are:
-"numTwoSidedCables":           The number of two-sided cables in a CTW instance
-"numOneSidedCables":           The number of one-sided cables in a CTW instance
-"numSideCables":               The number of side-cables in a CTW instance (cables that have none of their both ends plugged into the central plug)
-"numHousings":                 The number of housings for a CTW instance
-"numDifferentHousingTypes":    The number of different housing types in a CTW instance
-"numFreeCentralCavs":          The number of cavities in the central plug in which no cable end is plugged in
-"numFreeNormalCavs":           The number of cavities in normal (non-central plug) housings in which no cable end is plugged in (sum of free cavities over all normal housings)


We use an additional variable throughout the generation process:
-"k":      The total number of insertion jobs in a CTW instance (= 2*numTwoSidedCables + numOneSidedCables)



Input:
1.  The generation process can be controlled by setting integer values for the parameters constK, constB, constO and constNumSideCables
    They set k, numTwoSidedCables, numOneSidedCables, numSideCables respectively to constant values for all meta variable records that are being generated
    If the parameters are set to -1 the values for the variables will be generated dynamically from suitable distributions.

2.  "outputPath": change this variable to the absolute path of where the output should be stored (e.g. "C:\\Users\\MyName\\Desktop\\my_filename.csv")

3. "numToGenerate": Set this to an non negative integer. It determines how many meta variable records are generated




Output:
A semicolon seperated csv file with "numToGenerate" number of meta variable records.

"""







#Parameters explanation
"""
Change the following parameters to control the generation
The default values for these input parameters are:
constK = -1         //Sets k to a constant value
constB = -1         //Sets numTwoSidedCables to a constant value
constO = -1         //Sets numOneSidedCables to a constant value
constNumSideCables = -1     //Sets numSideCables to a constant value
With all values set to default this script generates realistic values for the Meta Variables with varying values for numTwoSidedCables, numOneSidedCables and numSideCables.


"""

#Parameters
######################################################################
constK = -1
constB = -1
constO = -1
constNumSideCables = -1
outputPath = ""   #e.g. "C:\\Users\\Name\\Desktop\\meta_data.csv"
numToGenerate = 600

if (outputPath == ""):
    outputPath = Path(os.path.dirname(os.path.realpath(__file__)))
    outputPath = outputPath / "meta_data.csv"
######################################################################








# To guarantee that the input describes valid meta variables we check the min-max constraints (e.g. 0 <= bInput <= 99)
# as well as inter-relationships (e.g. numSideCablesInput < 0.8 * bInput)
# Additionally, when kInput != -1 it must be possible generate numSideCables and numOneSidedCables so that kInput = 2*numTwoSidedCables + numOneSidedCables
def validateInput(kInput:int, bInput:int, oInput:int, numSideCablesInput:int):
    #Check whether types are correct
    if(type(kInput) != int or type(bInput) != int or type(oInput) != int or type(numSideCablesInput) != int):
        raise Exception("At least one input variable is of a wrong type! kInput, bInput, oInput and numSideCablesInput have to be of type int")
    validateMinMaxConstraints(kInput, bInput, oInput, numSideCablesInput)
    validateRelations(kInput, bInput, oInput, numSideCablesInput)


def validateMinMaxConstraints(kInput:int, bInput:int, oInput:int, numSideCablesInput:int):
    #Variable min/max
    #K 1/198
    #B 0/99
    #O 0/20
    #numSideCables 0/63

    if(kInput != -1):
        if(kInput < 1 or kInput > 198):
            raise Exception("kInput is not in the valid range! (0 < kInput <= 198)")

    if(bInput != -1):
        if(bInput < 0 or bInput > 100):
            raise Exception("bInput is not in the valid range! (0 <= bInput <= 100)")
    
    if(oInput != -1):
        if(oInput < 0 or oInput > 20):
            raise Exception("oInput is not in the valid range! (0 <= oInput <= 20)")
    
    if(numSideCablesInput != -1):
        if(numSideCablesInput < 0 or numSideCablesInput > 65):
            raise Exception("numSideCablesInput is not in the valid range! (0 <= numSideCablesInput <= 65)")


def validateRelations(kInput:int, bInput:int, oInput:int, numSideCablesInput:int):

    if(kInput != -1 and bInput != -1 and oInput != -1):
        if(kInput != 2* bInput + oInput):
            raise Exception("kInput has to satisfy kInput = 2*bIntput + oInput")
    elif(kInput != -1 and bInput != -1):
        if(2*bInput > kInput):
            raise Exception("bInput is too large for the given kInput! It must satify: 2*bInput <= kInput")
    elif(kInput != -1 and oInput != -1):
        if(oInput > kInput):
            raise Exception("oInput cannot be larger than kInput!")
        if(((kInput-oInput) % 2) != 0):
            raise Exception("It must be ((kInput - bInput) mod 2) == 0 !")

    if(numSideCablesInput != -1 and bInput != -1):
        if(numSideCablesInput > bInput):
            raise Exception("numSideCablesInput cannot be greater than bInput")
    elif(numSideCablesInput != -1 and kInput != -1):
        if(oInput != -1):
            if(kInput < 2*numSideCablesInput + oInput):
                raise Exception("kInput must be smaller than 2*numSideCablesInput + oInput")
        else:
            if(kInput < 2*numSideCablesInput):
                raise Exception("kInput must be smaller than 2*numSideCablesInput")








def sampleInitialBdistribution(numToGenerate):
    b = []
    bBins = [i for i in range(0,41)]
    #The counts for B from 0 to 40 extracted from the cleaned Komax Set
    bWeights = [3, 3, 4, 8, 3, 2, 10, 2, 10, 5, 10, 1, 10, 7, 1, 5, 2, 4, 8, 3, 17, 3, 4, 5, 5, 9, 2, 5, 2, 7, 8, 4, 5, 1, 10, 9, 1, 3, 3, 5, 9]
    
    #in 10,5% of the time b is larger than 40 -> and we assume a uniform distribution
    #in the other 89,5% of the time b is smaller than 40 and we assume the distribution described by bWeights
    for i in range(0,numToGenerate):
        rnum = random.uniform(0, 1)
        if(rnum < 0.105):
            bVal = random.randint(41,99)
        else:
            bVal = random.choices(bBins, weights=bWeights)[0]
        b.append(bVal)

    return b



def sampleOneSidedGivenKInput(k):
    o=[]
    for i in range(0,len(k)):
        rnum = random.uniform(0, 1)
        #in round about 0.832 of the instances we have 0 one-sided cables //when k % 2 = 1 then we need an odd number of one-sided cables
        if(rnum < 0.8):
            if(k[i] % 2):
                o.append(1)
            else:
                o.append(0)
        else:
            val = st.exponpow.rvs(b=0.68, loc=2.00, scale=7.59, size=1)[0]
            val = round(val)
            if(val > 20):
                val = 20
            if(val > k[i]):
                val = k[i]
            elif ((k[i]-val) % 2):
                val -= 1
            o.append(val)
    return o


def sampleOneSidedGivenB(b):
    o=[]
    for i in range(0,len(b)):
        rnum = random.uniform(0, 1)
        #in round about 0.832 of the instances we have 0 one-sided cables
        if(rnum < 0.8 and b[i] != 0):
            o.append(0)
        else:
            val = st.lomax.rvs(c=5.09, loc=1.00, scale=18.29, size=1)[0]
            val = round(val)
            if(val > 20):
                val = 20
            if(b[i]< 4 and val > 10):
                val = 10
            if(b[i] + val > 99):
                val = 99 - b[i]
            o.append(val)

    return o













#Start sequential generation ##############################################################################################################################################

#First validate the input
validateInput(constK, constB, constO, constNumSideCables) #throws error with description of the cause if input parameters are invalid

#Compute B (numTwoSidedCables) and O (numOneSidedCables) Arrays as well as the helper variable K (K = 2*B + O)
if(constK != -1 and constB == -1):
    k = np.full((numToGenerate,), constK)
    if(constO == -1):
        o = sampleOneSidedGivenKInput(k)
    else:
        o = np.full((numToGenerate,), constO)
    b = []
    for i in range(0,numToGenerate):
        b.append(int((k[i]-o[i])/2))

elif(constK != -1 and constB != -1):
    k = np.full((numToGenerate,), constK)
    b = np.full((numToGenerate,), constB)
    oHelp = constK - 2*constB
    o = np.full((numToGenerate,), oHelp)

elif(constK == -1 and constB == -1):
    b = sampleInitialBdistribution(numToGenerate)
    if(constO == -1):
        o = sampleOneSidedGivenB(b)
    else:
        o = np.full((numToGenerate,), constO)
    k=[]
    for i in range(0,numToGenerate):
        k.append(2*b[i]+o[i])

elif(constK == -1 and constB != -1):
    b = np.full((numToGenerate,), constB)
    if(constO == -1):
        o = sampleOneSidedGivenB(b)
    else:
        o = np.full((numToGenerate,), constO)
    k=[]
    for i in range(0,numToGenerate):
        k.append(2*b[i]+o[i])



##############B DataFrame################
newBData = pd.DataFrame(b, columns=['numTwoSidedCables'])

print("==Succesfully generated numTwoSidedCables==")



##############O DataFrame################
newOData = pd.DataFrame(o, columns=['numOneSidedCables'])

print("==Succesfully generated numOneSidedCables==")









################numHousings###################
numHousings = []

def housingFromKWithNoise(k:int):
    housingVal = -1
    if(k < 20):
        noise = np.random.normal(scale=1.5)
        housingVal  = int(round(0.2*k + noise))
    elif(k < 71):
        noise = np.random.normal(scale=2.5)
        housingVal = int(round(0.2*k + noise))
    elif(k < 110):
        noise = np.random.normal(scale = 2.5)
        val = 10 + noise
        if(val <= 4.5):
            val = 5
        housingVal = int(round(val))
    else:
        noise = np.random.normal(scale=1.5)
        housingVal = int(round(10 + noise))
    if(housingVal <= 1):
        if(kVal > 6):
            housingVal = 2
        else:
            housingVal = 1
    return housingVal


for kVal in k:
    hVal = -1
    if(kVal == 1):
        hVal = 1
        numHousings.append(hVal)
        continue
    if(kVal < 5):
        hVal = random.randint(1,2)
        numHousings.append(hVal)
        continue
    hVal = housingFromKWithNoise(kVal)
    if(hVal > kVal * 0.5):
        hVal = math.floor(kVal * 0.5)
    if(hVal > 18):
        hVal = 18
    numHousings.append(hVal)


newHousingData = pd.DataFrame(numHousings, columns=['numHousings'])

print("==Succesfully generated numHousings==")



#################numSideCable###################
if(constNumSideCables != -1):
    numSideCables= np.full((numToGenerate,), constNumSideCables)

else:
    numSideCables = []

    for i in range(0,numToGenerate):
        if(numHousings[i] < 3): #numhousings < 3 -> no SideCables possible
            numSideCables.append(0)
            continue
        if(b[i] < 3):          #b < 3 -> no SideCables in the cleanedKomaxSet
            numSideCables.append(0)
            continue
        elif(b[i] < 9):
            rnum = random.uniform(0, 1)
            if(rnum < 0.94):         #with ~94% = 0 in cleanedKomaxSet
                numSideCables.append(0)
                continue
            else:
                numSideCables.append(1)
                continue
        elif(b[i] < 18):
            rnum = random.uniform(0, 1)
            if(rnum < 0.89):         #with ~89% = 0 in cleanedKomaxSet
                numSideCables.append(0)
                continue
            else:
                rnum = random.randint(1, 4)
                numSideCables.append(rnum)
                continue
        elif(b[i] < 35):
            rnum = random.uniform(0, 1) 
            if(rnum < 0.66):         #with 66% = 0 in cleanedKomaxSet
                numSideCables.append(0)
                continue
            else:
                rnum = random.randint(1, 16)
                if(rnum > 0.8*b[i]):
                    rnum = int(0.8*b[i])
                numSideCables.append(rnum)
                continue
            
        ######else when b >= 35 we have a linear relationship####### -> we sample with noise from this relationship
        val = -23.3 + 0.842 * b[i]

        val = int(round(val + np.random.normal(scale=10)))

        if(val > 63):
            val = random.randint(50,63)
        if(val > 0.8 * b[i]): # no instance in the cleaned Komax Set has more than 0.8*B  sideCables
            val = int(0.8*b[i])
            numSideCables.append(val)
            continue
        if((b[i] - val)> 95): #we have no central plug that can take more than 95 two sided cables
            val = b[i] - 95
            numSideCables.append(val)
            continue
        if(val < 0):
            val = random.randint(0,10)
            numSideCables.append(val)
            continue
        numSideCables.append(val)
###################################################################
newSideData = pd.DataFrame(numSideCables, columns=['numSideCables'])
###################################################################
print("==Succesfully generated numSideCables==")


#####################numHousingTypes###############################
numDifferentHousingTypes = []
for i in range(0,numToGenerate):
    if(b[i] > 37):
        noise = int(round(np.random.normal(scale=1)))
        val = noise + 3
        if(val < 2):
            val = 2
        if(numHousings[i] < val):
            val = numHousings[i]
        numDifferentHousingTypes.append(val)
        continue
    if(numHousings[i] < 3):
        randVal = random.randint(1, numHousings[i])
        numDifferentHousingTypes.append(randVal)
        continue
    if(numHousings[i] < 13):
        randVal = random.randint(2, numHousings[i])
        numDifferentHousingTypes.append(randVal)
        continue

    #here we have b[i] <= 37 and numHousings[i] >= 13
    rnum = random.uniform(0, 1)
    if(rnum < 0.9):
        noise = int(round(np.random.normal(scale=1)))
        randVal = noise + 8
        if(numHousings[i] < randVal):
            randVal = numHousings[i]
        numDifferentHousingTypes.append(randVal)
        continue
    else:
        randVal = random.randint(2,6)
        numDifferentHousingTypes.append(randVal)
########################################################################
newHTypesData = pd.DataFrame(numDifferentHousingTypes, columns=['numDifferentHousingTypes'])
########################################################################
print("==Successfully generated numDifferentHousingTypes==")



"""
#####################numWireTypes###################################

#completely random -> sample from distribution and cannot be bigger than number of cables used in cable tree
numWireTypes = []


for i in range(0,numToGenerate):
    rnum = random.uniform(0, 1)
    #in round about 0.832 of the instances we have 0 one-sided cables
    if(rnum < 0.66): #war 0.66
        numWireTypes.append(1)
        continue
    else:
        val = st.weibull_min.rvs(c=0.92, loc=2.00, scale=1.63, size=1)[0]
        val = int(round(val))
    totalNumCables = o[i] + b[i]
   
    if(val > totalNumCables):
        val = totalNumCables
        numWireTypes.append(val)
        continue
    if(val > 10):
        numWireTypes.append(10)
        continue
    if(val < 1): #is always false
        numWireTypes.append(1)
        continue
    
    numWireTypes.append(val)
########################################################################
newWTypesData = pd.DataFrame(numWireTypes, columns=['numWireTypes'])
########################################################################
print("10")
"""




#####################numFreeCentralCavs###################################
numFreeCentralCavs = []


for i in range(0,numToGenerate):
    if (k[i]<6):
        rnum = random.uniform(0, 1)
        if(rnum < 0.75):
            randVal = random.randint(0,19)
        else:
            randVal = random.randint(20,39)
    elif (k[i] < 70):
        randVal = random.randint(0, 47)
    elif (k[i] < 86):
        randVal = random.randint(0,19)
    else:
        randVal = random.randint(0,14)
    if(numDifferentHousingTypes[i] == 1 and randVal > 14):
        randVal = random.randint(0,14)
    elif(numDifferentHousingTypes[i] > 7 and randVal < 18):
        randVal = random.randint(18,47)

    if(numHousings[i] == 1):
        if(randVal + k[i] > 95):
            randVal = 95 - k[i]
            if(randVal < 0):
                raise Exception("Only one Housing and more than 95 insertion jobs not possible!!!!")
            if(randVal > 12):
                randVal = random.randint(0,10)
    elif (numHousings[i] > 10 and numHousings[i] < 14):
        if(randVal < 10):
            rnum = random.uniform(0, 1)
            if(rnum < 0.9):
                randVal = random.randint(10,40)
    else:
        if(randVal + (b[i]-numSideCables[i]) > 95):
            randVal = 95 - (b[i] - numSideCables[i])
            if(randVal < 0):
                raise Exception("Too many two sided cables connected to the central plug!!!!")
    
    numFreeCentralCavs.append(randVal)

newFreeCentralCavData = pd.DataFrame(numFreeCentralCavs, columns=['numFreeCentralCavs'])


print("==Succesfully generated numFreeCentralCavs==")


#####################numFreeSmallCavs#####################################
def maxFreeFromNumHousings(numHousings:int):
    if(numHousings == 1):
        return 0
    elif(numHousings == 2):
        return 15
    elif(numHousings > 2 and numHousings < 10):
        return int(15*numHousings - 11)
    elif(numHousings < 14 and numHousings > 10):
        return 85
    else:
        return 180

def maxFreeFromHousingTypes(numHousingTypes:int):
    if(numHousingTypes == 1):
        return 18
    elif(numHousingTypes > 3 and numHousingTypes < 8):
        return 55
    elif(numHousingTypes >= 8):
        return 20
    else:
        return 180

numFreeNormalCavs = []
for i in range(0,numToGenerate):
    neededSmallCavs = numSideCables[i] + b[i] + o[i] # = 2*numSideCables[i] + (b[i] - numSideCables[i]) + o[i]
    neededcentralCavs = b[i]-numSideCables[i] + numFreeCentralCavs[i]
    if(neededSmallCavs < 40):
        rnum = random.uniform(0, 1)
        if(rnum < 0.85):
            randVal = st.invgauss.rvs(mu=4.09, loc=-0.41, scale=1.51, size=1)[0]
            randVal = round(randVal)
            if(randVal > 20 or randVal < 0):
                randVal = random.randint(0,20)
        elif(rnum < 0.95):
            randVal = random.randint(21,40)
        else:
            randVal = random.randint(41,180)
    elif(neededSmallCavs < 66):
        randVal = random.randint(16,160)
    elif(neededSmallCavs < 120):
        randVal = random.randint(0,140)
    else: #zwischen 120 und 0
        randVal = random.randint(0,70)
    if(k[i] < 6 and randVal > 16):
        randVal = random.randint(0,16)
    numMaxFromNumH = maxFreeFromNumHousings(numHousings[i])
    numMaxFromHTypes = maxFreeFromHousingTypes(numDifferentHousingTypes[i])
    if(randVal > numMaxFromNumH):
        randVal = random.randint(0,numMaxFromNumH)
    if(randVal > numMaxFromHTypes):
        randVal = random.randint(0,numMaxFromHTypes)
    if(randVal + neededcentralCavs + neededSmallCavs > 260):
        randVal = 260 - neededcentralCavs - neededSmallCavs

    numFreeNormalCavs.append(randVal)

newFreeNormalCavData = pd.DataFrame(numFreeNormalCavs, columns=['numFreeNormalCavs'])


print("==Succesfully generated numFreeNormalCavs==")

newResult = pd.concat([newBData, newOData, newSideData, newHousingData, newHTypesData, newFreeCentralCavData, newFreeNormalCavData], axis=1)


newResult.to_csv(outputPath, sep=';', index=False)