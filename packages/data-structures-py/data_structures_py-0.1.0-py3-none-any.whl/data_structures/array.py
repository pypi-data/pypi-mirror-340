import numpy as np

class MyArray(np.ndarray):
    """
    A enhanced array class built on numpy.ndarray with additional methods.
    
    Attributes:
        Inherits all attributes from numpy.ndarray
    """
    
    def __new__(cls, input_array):
        """
        Create a new MyArray instance.
        
        Args:
            input_array: Input data that can be converted to an array.
            
        Returns:
            MyArray instance
        """
        obj = np.asarray(input_array).view(cls)
        return obj
    
    def __array_finalize__(self, obj):
        """Finalize the array creation."""
        if obj is None:
            return
    
    def sum(self):
        """Return the sum of array elements."""
        return np.sum(self)
    
    def mean(self):
        """Return the mean of array elements."""
        return np.mean(self)
    
    def shape(self):
        """Return the shape of the array."""
        return self.shape
    
    def reshape(self, new_shape):
        """
        Reshape the array.
        
        Args:
            new_shape: New shape for the array
            
        Returns:
            Reshaped MyArray
        """
        return self.reshape(new_shape)
    
    def max(self):
        """Return the maximum value in the array."""
        return np.max(self)
    
    def min(self):
        """Return the minimum value in the array."""
        return np.min(self)
    
    def sort(self, axis=-1):
        """
        Sort the array.
        
        Args:
            axis: Axis along which to sort
            
        Returns:
            Sorted MyArray
        """
        return np.sort(self, axis=axis)