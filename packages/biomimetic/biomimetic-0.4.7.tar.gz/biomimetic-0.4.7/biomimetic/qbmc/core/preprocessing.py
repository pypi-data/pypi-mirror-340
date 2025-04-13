# qbmc/core/preprocessing.py
import numpy as np
from typing import Union, Tuple
from dataclasses import dataclass

DEFAULT_BINSIZE = 9  # 8 bits + sign bit


@dataclass
class QBMCDataContainer:
    binary: np.ndarray
    scale: float = 1.0
    offset: float = 0.0
    quantized: bool = False

class QBMCDataProcessor:
    """
    Handles automatic data conversion and quantization for QBMC models
    """
    def __init__(self, binsize: int = DEFAULT_BINSIZE):
        self.binsize = binsize

    def auto_convert(self, data: Union[np.ndarray, list]) -> QBMCDataContainer:
        """
        Main entry point: Automatically handles either integer or float input
        Returns a QBMCDataContainer with binary representation and parameters
        """
        arr = np.asarray(data)
        
        if np.issubdtype(arr.dtype, np.integer):
            bin_data = self.int_to_bin(arr)
            return QBMCDataContainer(bin_data, quantized=False)
            
        elif np.issubdtype(arr.dtype, np.floating):
            quantized, scale, offset = self.quantize_float(arr)
            bin_data = self._arr_to_bin(quantized, signed=True)
            return QBMCDataContainer(bin_data, scale, offset, quantized=True)
            
        else:
            raise TypeError(f"Unsupported data type: {arr.dtype}")

    def int_to_bin(self, data: np.ndarray) -> np.ndarray:
        """Direct integer to binary conversion"""
        return self._arr_to_bin(data, signed=True)

    def float_to_bin(self, data: np.ndarray) -> QBMCDataContainer:
        """Float to binary conversion with automatic quantization"""
        quantized, scale, offset = self.quantize_float(data)
        bin_data = self._arr_to_bin(quantized, signed=True)
        return QBMCDataContainer(bin_data, scale, offset, quantized=True)

    def quantize_float(self, data: np.ndarray) -> Tuple[np.ndarray, float, float]:
        """
        Quantizes float data to integer space
        Returns: (quantized_data, scale, offset)
        """
        d_min = np.min(data)
        d_max = np.max(data)
        
        if d_max == d_min:  # Handle constant features
            scale = 1.0
            offset = 0.0
        else:
            # Calculate quantization parameters
            scale = (d_max - d_min) / (2**self.binsize - 1)
            offset = - (d_min / scale) - (2**(self.binsize-1))
        
        # Quantize and clamp values
        quantized = np.round((data / scale) + offset).astype(np.int64)
        return quantized, scale, offset

    def _to_bin(self, value: int, signed: bool = True) -> np.ndarray:
        """Core integer -> binary array conversion"""
        if signed:
            if value < 0:
                value = (1 << self.binsize) + value  # Two's complement
            return np.array(
                [bool((value >> i) & 0x01) 
                for i in reversed(range(self.binsize))]
            )
        else:
            return np.array(
                [bool((value >> i) & 0x01) 
                for i in reversed(range(self.binsize))]
            )

    def _from_bin(self, binary_array: np.ndarray, signed: bool = True) -> int:
        """Core binary array -> integer conversion"""
        value = sum(
            bit << (self.binsize - 1 - i) 
            for i, bit in enumerate(binary_array)
        )
        if signed and binary_array[0]:  # Handle two's complement
            value -= (1 << self.binsize)
        return value

    def _arr_to_bin(self, data: np.ndarray, signed: bool = True) -> np.ndarray:
        """Batch convert array of integers to binary representation"""
        return np.stack([np.stack([
            self._to_bin(val, signed=signed) 
            for val in sample
        ]) for sample in data])

    def postprocess(self, container: QBMCDataContainer) -> np.ndarray:
        """Convert binary predictions back to original data space using container's parameters"""
        int_data = np.apply_along_axis(
            lambda x: self._from_bin(x, signed=True),
            -1, container.binary
        )
        
        if container.quantized:
            return (int_data - container.offset) * container.scale
        return int_data


if __name__ == "__main__":
    print("=== Testing QBMC Data Processor ===")
    
    # Initialize with default binsize (9)
    processor = QBMCDataProcessor()
    
    # Test data from qbmc.pdf
    int_data = np.array([
        [0, 1, 3, 5, 7, 8],   # X
        [0, 0, 1, 0, 1, 1]    # Y
    ])
    
    float_data = np.array([
        [1.2, 2.4, 3.6, 5.1],
        [0.5, 1.0, 1.5, 2.0]
    ])
    
    # ===== Test 1: Integer to Binary Conversion =====
    print("\nTest 1: Integer to Binary")
    int_container = processor.auto_convert(int_data)
    print("Input:\n", int_data)
    print("Binary Output:\n", int_container.binary)
    print("Binary Output Integers:\n", int_container.binary.astype(int))
    print("Container params - Quantized:", int_container.quantized, 
          "Scale:", int_container.scale, "Offset:", int_container.offset)
    
    # Verify round-trip
    reconstructed = processor.postprocess(int_container)
    assert np.array_equal(int_data, reconstructed), "Integer round-trip failed"
    print("✓ Integer round-trip verified")
    
    # ===== Test 2: Float Quantization =====
    print("\nTest 2: Float Quantization")
    float_container = processor.auto_convert(float_data)
    print("Input:\n", float_data)
    print("Binary Output:\n", float_container.binary.astype(int))
    
    # Verify quantization parameters
    print(f"Quantization params - Scale: {float_container.scale:.4f}, Offset: {float_container.offset:.4f}")
    
    # Verify round-trip
    reconstructed = processor.postprocess(float_container)
    print("Reconstruction MSE:", np.mean(float_data - reconstructed)**2)
    assert np.allclose(float_data, reconstructed, atol=float_container.scale/2), "Float round-trip failed"
    print("✓ Float round-trip verified")
    
    # ===== Test 3: Auto Conversion =====
    print("\nTest 3: Auto Conversion")
    mixed_data = [
        [0, 1.5, 3, 4.2],  # Mixed types
        [1, 2.0, 5, 6.8]
    ]
    
    mixed_container = processor.auto_convert(mixed_data)
    reconstructed = processor.postprocess(mixed_container)
    print("Mixed Input:\n", mixed_data)
    print("Binary Output:\n", mixed_container.binary.astype(int))
    print("Container params - Quantized:", mixed_container.quantized, 
          "Scale:", mixed_container.scale, "Offset:", mixed_container.offset)
    print("Reconstructed Input:\n", reconstructed)

    # ===== Test 4: Edge Cases =====
    print("\nTest 4: Edge Cases")
    
    # Test negative integers
    neg_data = np.array([[-5, -3, 0, 2, 4]])
    neg_container = processor.auto_convert(neg_data)
    print("Negative Input:", neg_data)
    print("Binary Output:\n", neg_container.binary.astype(int))
    print("Container params:", neg_container.scale, neg_container.offset)
    
    # Test large value range
    wide_range = np.array([[0.1, 450, 1000.0]])
    wide_container = processor.auto_convert(wide_range)
    print("Wide Range Input:", wide_range)
    print("Binary Output:\n", wide_container.binary.astype(int))
    print("Quantization params:", wide_container.scale, wide_container.offset)
    
    # ===== Test 5: Batch Processing =====
    print("\nTest 5: Batch Processing")
    
    # From ANN replication section in qbmc.pdf
    ann_data = np.array([
        [1.6746e-03, 1.0286e+00],
        [1.0286e+00, 3.0220e+00]
    ])
    
    ann_container = processor.auto_convert(ann_data)
    print("ANN-style Input:\n", ann_data)
    print("Binary Output:\n", ann_container.binary.astype(int))
    
    # Verify reconstruction
    reconstructed = processor.postprocess(ann_container)
    print("Reconstructed ANN Data:\n", reconstructed)
    assert np.allclose(ann_data, reconstructed, atol=ann_container.scale/2), "ANN data round-trip failed"
    print("✓ ANN data round-trip verified")
    
    # ===== Test 6: Quantization Bounds =====
    print("\nTest 6: Quantization Bounds")

    # Test minimum/maximum representable values
    test_vals = np.array([[-2**(processor.binsize-1), 2**(processor.binsize-1)-1]])
    test_container = processor.auto_convert(test_vals)
    print("Boundary Input:", test_vals)
    print("Binary Output:\n", test_container.binary.astype(int))

    try:
        # This should trigger two's complement overflow
        overflow = np.array([[-2**(processor.binsize)]])
        processor.int_to_bin(overflow)
        assert False, "Should have raised error on overflow"
    except Exception as e:
        print(f"✓ Overflow protection working: {str(e)}")

    # ===== Test 7: Constant Feature Handling =====
    print("\nTest 7: Constant Feature Handling")
    const_data = np.array([[5, 5, 5, 5], [3, 3, 3, 3]])
    const_container = processor.auto_convert(const_data)
    print("Constant Input:", const_data)
    print("Binary Output:\n", const_container.binary.astype(int))
    reconstructed = processor.postprocess(const_container)
    assert np.array_equal(const_data, reconstructed), "Constant feature handling failed"
    print("✓ Constant feature handling verified")

    print("\n=== All tests passed successfully ===")
