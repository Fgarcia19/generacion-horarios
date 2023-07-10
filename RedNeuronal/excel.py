import pandas as pd
import numpy as np

# Create a 3D NumPy array
def np_to_excel(name,my_matrix):

    # Convert each list to a string
    str_matrix = np.array([[str(lst) for lst in row] for row in my_matrix])

    # Flatten the 2D string matrix
    flat_matrix = str_matrix.reshape((-1, str_matrix.shape[-1]))

    # Convert the flattened matrix to a pandas DataFrame
    df = pd.DataFrame(flat_matrix)

    # Export the DataFrame to an Excel file
    df.to_excel(name+'output.xlsx', index=False)
    print("DONE")
