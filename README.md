# CTWMetaVariablesGenerator
**Description:** This is a python script for the generation of realistic values for the meta variables of cable tree wiring (CTW) instances

The meta variables are:
- "numTwoSidedCables":           The number of two-sided cables in a CTW instance
- "numOneSidedCables":           The number of one-sided cables in a CTW instance
- "numSideCables":               The number of side-cables in a CTW instance (two-sided cables that have none of their both ends plugged into the central plug)
- "numHousings":                 The number of housings for a CTW instance
- "numDifferentHousingTypes":    The number of different housing types in a CTW instance
- "numFreeCentralCavs":          The number of cavities in the central plug in which no cable end is plugged in
- "numFreeNormalCavs":           The number of cavities in normal (non-central plug) housings in which no cable end is plugged in (sum of free cavities over all normal housings)


We use an additional variable throughout the generation process:
- "k":      The total number of insertion jobs in a CTW instance (= 2*numTwoSidedCables + numOneSidedCables)

## Installation

The script relies on the following packages:
- numpy (`pip install numpy`)
- pandas (`pip install pandas`)
- scipy (`pip install scipy`)

## Input/Output

Several parameters can be changed in the source code.

**Input:**
1.  The generation process can be controlled by setting integer values for the parameters constK, constB, constO and constNumSideCables in the source code
    They set k, numTwoSidedCables, numOneSidedCables, numSideCables respectively to constant values for all meta variable records that are being generated
    If the parameters are set to -1 the values for the variables will be generated dynamically from suitable distributions.

2.  "outputPath": change this variable to the absolute path of where the output should be stored (e.g. "C:\\Users\\MyName\\Desktop\\my_filename.csv")

3. "numToGenerate": Set this to an non negative integer. It determines how many meta variable records are generated




**Output:**
A semicolon seperated CSV file with "numToGenerate" number of meta variable records.
