# SVDC/SVDC.py

import torch
import torch.nn.functional as F
import numpy as np

class SVDC:
    """
    Deep SVDC class for performing a multi-layer SVD-based transformation on an input matrix.
    
    The SVDC transformation is applied repeatedly for a specified layer count. Each layer computes:
        term1 = w4[0] * (w1 @ Sigma @ Vt)
        term2 = w4[1] * (U @ w2)
        term3 = w4[2] * (w3 @ Vt)
    and sums them to form y.
    
    In SVDC layers, output of the previous layer is passed as the sensor input to the next SVDC layer.
    In the final layer, y is passed to the non-linear function f(y) via the FyFuncCoordinator.
    
    The chromosome for a layer is expected to have the following structure:
        - w1: shape (n, n)
        - w2: shape (n, n)
        - w3: shape (n, n)
        - w4: shape (3,)
        - fy_w: shape (n^2 + 2*layer_output)
    
    For SVDC layers, layer_output is set to n (so that the output is square).
    For the final layer linear, layer_output is the provided output_size.
    
    Total chromosome length per layer is:
      4*n^2 + 3 + 2 * (n  or output_size)
    
    The full deep chromosome is a merge of per-layer chromosomes.
    """

    def __init__(self,
                 chromosome: list,
                 output_size: int,
                 layer_count: int,
                 sensor_input_sample: np.ndarray,
                 verbose: bool = False):
        """
        Setup the deep SVDC.
        
        Parameters:
            chromosome (list): The full chromosome vector
            output_size (int): The output size for the final layer
            layer_count (int): The number of SVDC layers
            verbose (bool): If True, prints intermediate shapes and debugging info
        """
        self.chromosome = torch.tensor(chromosome, dtype=torch.float32)
        self.output_size = output_size
        self.num_layers = layer_count
        self.verbose = verbose
        self.target_dim = calculate_target_dim(sensor_input_sample)
        blocks = self.split_chromosome(self.target_dim)

        expected_length = calculate_expected_size(
            layerCount=self.num_layers,
            inputDimension=self.target_dim,
            outputSize=self.output_size)
        
        if self.chromosome.shape[0] != expected_length:
            raise ValueError(f"Expected overall chromosome length {expected_length}, but got {self.chromosome.shape[0]}.")
        
        self.weights = []
        for i, block in enumerate(blocks):
            is_final = (i == len(blocks) - 1)
            w = self.chromosome_to_weights(self.target_dim, is_final, block)
            self.weights.append(w)

    def adjust_to_square(self,
                         matrix: torch.Tensor,
                         target_dim: int) -> torch.Tensor:
        """
        Adjusts a 2D tensor to be square of size (target_dim, target_dim) by using 0 padding
        """
        rows, cols = matrix.shape
        
        if rows < target_dim:
            pad_rows = target_dim - rows
            matrix = F.pad(matrix, (0, 0, 0, pad_rows), mode="constant", value=0)
        
        if cols < target_dim:
            pad_cols = target_dim - cols
            matrix = F.pad(matrix, (0, pad_cols, 0, 0), mode="constant", value=0)
        
        return matrix

    def chromosome_to_weights(self,
                              target_dim: int,
                              isFinalLayer: bool,
                              block: torch.Tensor) -> tuple:
        """
        Converts a block of weights to weight matrices for one SVDC layer.
        
        As SVDC layers are chained together, the output of one layer is the input to the next.
        The final layer has a different weights size.
        We need the specify if this is the final layer or not to determine the size of fy_w.
        """
        n = target_dim
        size_w1 = n * n
        size_w2 = n * n
        size_w3 = n * n
        size_w4 = 3

        if isFinalLayer:
            size_fy = n * n + 2 * self.output_size
        else:
            size_fy = n * n + 2 * n 
        
        expected_length = size_w1 + size_w2 + size_w3 + size_w4 + size_fy
        
        if block.shape[0] != expected_length:
            raise ValueError(f"Expected block length {expected_length}, but got {block.shape[0]}.")
        
        w1 = block[0: size_w1].view(n, n)
        w2 = block[size_w1: size_w1 + size_w2].view(n, n)
        w3 = block[size_w1 + size_w2: size_w1 + size_w2 + size_w3].view(n, n)
        w4 = block[size_w1 + size_w2 + size_w3: size_w1 + size_w2 + size_w3 + size_w4].view(3)
        fy_w = block[size_w1 + size_w2 + size_w3 + size_w4:].view(-1)
        
        return w1, w2, w3, w4, fy_w

    def split_chromosome(self,
                         target_dim: int) -> list:
        """
        Splits the full chromosome into blocks for each layer.

        As the SVDC is mutli-layered, we need to split the chromosome we got
        from the optimizer into blocks for each layer.
        """
        blocks = []
        offset = 0
        for layer in range(self.num_layers):
            if layer == self.num_layers - 1:
                block_length = 4 * (target_dim ** 2) + 3 + 2 * self.output_size
            else:
                block_length = 4 * (target_dim ** 2) + 3 + 2 * target_dim
            block = self.chromosome[offset:offset + block_length]
            if block.shape[0] != block_length:
                raise ValueError(f"Expected block length {block_length} for layer {layer}, but got {block.shape[0]}.")
            blocks.append(block)
            offset += block_length
            if self.verbose:
                print(f"Layer {layer} block shape: {block.shape}")
        return blocks

    def forward(self,
                sensor_input: np.ndarray) -> np.ndarray:
        """
        Performs a forward pass of the deep SVDC transformation.

        Parameters
            sensor_input (np.ndarray): The input matrix from the system.
        
        Steps:
          1. Determine the target square dimension (n) from the sensor input.
          2. Adjust the input to a square matrix of size (n, n).
          3. Compute the full SVD of the input.
          4. Extract the current layer's weights from the chromosome.
          5. Compute three terms:
                term1 = w4[0] * (w1 @ Sigma @ Vt)
                term2 = w4[1] * (U @ w2)
                term3 = w4[2] * (w3 @ Vt)
          6. Sum the terms to get y.
          7. If this is the final layer apply the non-linear function f(y) via FyFuncCoordinator.
             Otherwise, pass y as input to the next layer.
        """
        if self.verbose:
            print("Calculated target dimension:", self.target_dim)

        input_matrix = torch.tensor(sensor_input, dtype=torch.float32)
        if input_matrix.ndim != 2: raise ValueError("sensor_input must be a 2D array.")
        if self.verbose:
            print("Original input shape:", input_matrix.shape)

        current_matrix = self.adjust_to_square(input_matrix, self.target_dim)

        if self.verbose:
            print("Adjusted input shape:", current_matrix.shape)

        for i, weights in enumerate(self.weights):
            is_final = (i == len(self.weights) - 1)
            U_np, S_np, Vt_np = np.linalg.svd(current_matrix.numpy(), full_matrices=False)
            U = torch.tensor(U_np, dtype=torch.float32)
            S = torch.tensor(S_np, dtype=torch.float32)
            Vt = torch.tensor(Vt_np, dtype=torch.float32)
            Sigma = torch.diag(S)
            if self.verbose:
                print("U shape:", U.shape)
                print("Sigma shape:", Sigma.shape)
                print("Vt shape:", Vt.shape)
            w1, w2, w3, w4, fy_w = weights
            if self.verbose:
                print("w1 shape:", w1.shape)
                print("w2 shape:", w2.shape)
                print("w3 shape:", w3.shape)
                print("w4:", w4)
                print("fy_w shape:", fy_w.shape)
            term1 = w4[0] * (w1 @ Sigma @ Vt)
            term2 = w4[1] * (U @ w2)
            term3 = w4[2] * (w3 @ Vt)
            if self.verbose:
                print("term1 shape:", term1.shape)
                print("term2 shape:", term2.shape)
                print("term3 shape:", term3.shape)
            y = term1 + term2 + term3
            if not is_final:
                current_matrix = y
            else:
                fy_func = FyFuncCoordinator(inputX=self.target_dim,
                                            inputY=self.target_dim,
                                            output=self.output_size)
                output = fy_func.fy(y, fy_w)
                return output.detach().numpy()

class FyFuncCoordinator:
    """
    Manages the final non-linear function fy.
    """
    def __init__(self,
                 inputX: int,
                 inputY: int,
                 output: int):
        """
        Takes the number of columns, rows of the input and the desired output shape.
        """
        self.inputX = inputX
        self.inputY = inputY
        self.output = output

    def get_w_size(self) -> int:
        """
        Returns the size of the weight vector required by the fy function.
        """
        return self.inputX * self.inputY + self.output * 2

    def fy_simple(self,
                  x: torch.Tensor,
                  w: torch.Tensor) -> torch.Tensor:
        """
        Splits the weight vector into a weight vector A and (scale, bias) pairs.
        For each (scale, bias) pair, computes:
            output = scale * dot(A, x.flatten()) + bias
        and returns the output vector.
        """
        expected_size = self.get_w_size()
        if w.shape[0] != expected_size:
            raise ValueError(f"Expected weight vector of size {expected_size}, got {w.shape[0]}")
        A = w[: self.inputX * self.inputY]
        B = w[self.inputX * self.inputY:].view(-1, 2)
        outputs = []
        for s, b in B:
            outputs.append(s * torch.dot(A, x.flatten()) + b)
        return torch.tensor(outputs)

    def fy(self,
           x: torch.Tensor,
           w: torch.Tensor,
           option: str = "default") -> torch.Tensor:
        """
        Calls the non-linear function. We can add additional function options
        """
        if option == "default":
            return self.fy_simple(x, w)
        
def calculate_target_dim(sensor_input: np.ndarray) -> int:
    """
    Calculates the dimension of the square matrix required to fit the sensor input.
    The target dimension is the maximum of the input's rows and columns.

    For example,
    If we have a sensor input of shape (3, 5), the target dimension is 5.
    If the input is (6, 4), the target dimension is 6.
    If the input is (3, 3), the target dimension is 3. etc.
    """
    if sensor_input.ndim != 2:
        raise ValueError("Sensor input must be a 2D array.")
    rows, cols = sensor_input.shape
    return max(rows, cols)

def calculate_expected_size(layerCount, inputDimension, outputSize):
    """
    Calculates the expected length of a chromosome in the SVDC algorithm
    depending on the SVDC layer count, input dimension, and output size
    """
    layerSizes = []
    for i in range(layerCount):
        is_final = (i == layerCount - 1)
        layer_output = outputSize if is_final else inputDimension
        layer_len = 4 * (inputDimension ** 2) + 3 + 2 * layer_output
        layerSizes.append(layer_len)
    expected_length = sum(layerSizes)
    return expected_length
