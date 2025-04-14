# SVDClassifier
This package provides the implementation for the SVD-based classifier developed in the [Autonomous Agent Learning Lab](https://oak.conncoll.edu/parker/research.html) at [Connecticut College](https://www.conncoll.edu/academics/majors-departments-programs/departments/computer-science/). This classifier is designed to be used with Evolutionary Strategies such as CMA-ES, Open-ES, and others due to it's reduced number of weights compared to a traditional convolutional neural network.

## Installation
To install SVDC, use pip:
```bash
pip install SVDClassifier
```

## Usage Example
The following is a simple example of using the SVDC classifier on a toy input:
```python
from  SVDC.SVDC  import  SVDC
import  numpy  as  np
# Example weight vector, if the length is wrong the correct length will be returned as an error
weights = [0.1] * 111
# Example 5x5 input
sensor_input_sample = np.random.rand(5, 5)
# Create the SVDC Classifier, weight sizes are calculated for you based on the input sample
model = SVDC(weights, output_size=4, layer_count=1, sensor_input_sample=sensor_input_sample)
# Run forward pass on example input
output = model.forward(sensor_input_sample)
print("Output:", output)
```
The SVDC classifier can be optimized with CMA-ES by the following:
```python
from SVDC.SVDC_CMA import SVDC_CMA
# Define fitnesss function
def fit_func(): ...
# Define the optimizer
optimizer = SVDC_CMA(
    starting_weights=starting_weights,
    output_size=desired_output_size,
    SVDC_layers=number_of_layers,
    fitness_function=fit_func,
    generations=total_generations_count,
    log_folder=folder_for_logs,
)
# Then run the optmizer and save the best result
result = optimizer.train(sample_input)
```
A more detailed example can be found in the examples folder.

## License
This project is licensed under the MIT License. View the license in [LICENSE.md](LICENSE.md)