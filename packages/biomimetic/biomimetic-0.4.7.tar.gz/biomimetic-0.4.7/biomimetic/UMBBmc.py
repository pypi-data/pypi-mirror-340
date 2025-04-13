import numpy as np
from .UBBmc import UniversalBiasBiomimeticCell


class UniversalModeBiasBiomimeticCell(UniversalBiasBiomimeticCell):
    def __init__(Cell, index, inputNums, inputSize, memorySize, outputSize, outputNums, modeCount):
        super().__init__(index, inputNums, inputSize, memorySize, outputSize, outputNums)
        Cell.modeCount = modeCount
        Cell.currentMode = 0
        Cell.weightCube = np.zeros((modeCount, inputNums, memorySize, inputSize))

    def __str__(Cell):
        return f"UMBBmc({Cell.index}, {Cell.inputSize}, {Cell.memorySize}, {Cell.outputSize}, {Cell.activationFlags}, {Cell.fireFlags}, {Cell.inputNums}, {Cell.outputNums}, {Cell.modeCount})"

    def learn(Cell, weightCube: np.array):
        Cell.weightCube = np.array(weightCube)
        Cell.memorySize = weightCube.shape[1]

    def learnMode(Cell, weightSheets: np.array, modeIndex: int):
        Cell.weightCube[modeIndex] = np.array(weightSheets)

    def activate(Cell, inputValues: np.array, modeIndex: int):
        Cell.currentMode = modeIndex
        modeWeights = Cell.weightCube[Cell.currentMode]
        activationSheet = []
        for i in range(Cell.inputNums):
            matches = np.logical_not(np.logical_xor(modeWeights[i], inputValues[i])).all(axis=1)
            activationSheet.append(matches.astype(int))
            Cell.activationFlags[i] = np.any(matches)
        return np.array(activationSheet)


if __name__ == "__main__":
    # Test 1: Initialization
    cell = UniversalModeBiasBiomimeticCell(1, 2, 3, 4, 2, 3, 2)  # 2 inputs, 3 outputs, 2 modes
    print("Test 1: Initialization")
    print(cell)

    # Test 2: Learning for Modes
    print("\nTest 2: Learning for Modes")
    weightCube = [
        [[[1, 1, 1], [0, 1, 0], [1, 0, 1], [0, 0, 0]],  # Input 1, Mode 0
         [[1, 1, 0], [0, 0, 1], [0, 1, 1], [1, 0, 0]]],  # Input 2, Mode 0
        [[[1, 0, 0], [0, 1, 1], [1, 1, 1], [0, 0, 0]],  # Input 1, Mode 1
         [[0, 1, 0], [1, 0, 1], [1, 0, 0], [0, 1, 1]]],  # Input 2, Mode 1
    ]
    cell.learn(weightCube)
    print("Weight Cube After Learning:")
    print(cell.weightCube)

    # Test 3: Activation in Mode 0
    print("\nTest 3: Activation in Mode 0")
    activations = cell.activate([[1, 1, 1], [0, 0, 1]], modeIndex=0)
    print("Activations:", activations)
    print("Activation Flags:", cell.activationFlags)

    # Test 4: Fire with Activation and Bias (Mode 0)
    print("\nTest 4: Fire with Activation and Bias (Mode 0)")
    cell.output([[0, 1], [1, 0], [1, 1]])
    output = cell.fire(np.array([True, False, True]))
    print("Output Array:", output)

    # Test 5: Fire with Activation and No Bias (Mode 0)
    print("\nTest 5: Fire with Activation and No Bias (Mode 0)")
    output = cell.fire(np.array([True, True, True]))
    print("Output Array:", output)

    # Test 6: Activation in Mode 1
    print("\nTest 6: Activation in Mode 1")
    activations = cell.activate([[0, 1, 0], [1, 0, 0]], modeIndex=1)
    print("Activations:", activations)
    print("Activation Flags:", cell.activationFlags)

    # Test 7: Fire with Activation and Bias (Mode 1)
    print("\nTest 7: Fire with Activation and Bias (Mode 1)")
    cell.output([[0, 1], [1, 0], [1, 1]])
    output = cell.fire(np.array([True, False, False]))
    print("Output Array:", output)

    # Test 8: Fire with Activation and No Bias (Mode 1)
    print("\nTest 8: Fire with Activation and No Bias (Mode 1)")
    output = cell.fire(np.array([True, True, True]))
    print("Output Array:", output)
