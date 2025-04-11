import numpy as np
from idtxl.bivariate_te import BivariateTE
from idtxl.data import Data
from idtxl.visualise_graph import plot_network
import matplotlib.pyplot as plt
import pandas as pd

# Generate test data using the built-in MUTE model
data = Data()
data.generate_mute_data(n_samples=1000, n_replications=5)

# Initialize the analysis
network_analysis = BivariateTE()

# Set up the analysis settings
settings = {
    "cmi_estimator": "JidtGaussianCMI",
    "max_lag_sources": 10,
    "min_lag_sources": 1,
    "verbose": True,
    "n_perm_max_seq": 1000,
    "n_perm_omnibus": 1000,
    "alpha_omnibus": 0.05,
    "alpha_max_seq": 0.05,
    "local_values": True  # This is important to get all TE values
}

# Run the analysis
results = network_analysis.analyse_network(settings=settings, data=data)

# Create a DataFrame to store all TE values
n_sensors = data.n_processes
n_lags = 10

# Initialize DataFrame with all combinations of source, target, and lags
rows = []
for source in range(n_sensors):
    for target in range(n_sensors):
        if source != target:  # Skip self-interactions
            for lag in range(1, n_lags + 1):
                rows.append({
                    'source': source,
                    'target': target,
                    'lag': lag,
                    'TE': np.nan  # Initialize with NaN
                })

df = pd.DataFrame(rows)

# Fill in the TE values
for target in range(n_sensors):
    target_results = results.get_single_target(target, fdr=False)
    
    if target_results is None:
        continue
        
    # Get all source variables and their lags
    source_vars = target_results.get('selected_vars_sources', [])
    if not source_vars:
        continue
        
    # Fill in TE values for each source and lag
    for var_idx, (source, lag) in enumerate(source_vars):
        if source != target:  # Skip self-interactions
            te_value = target_results['selected_sources_te'][var_idx]
            # Update the corresponding row in the DataFrame
            mask = (df['source'] == source) & (df['target'] == target) & (df['lag'] == lag)
            df.loc[mask, 'TE'] = te_value

# Save to CSV
# df.to_csv('transfer_entropy_results.csv', index=False)

# Print results to console
print("\nTransfer Entropy Results:")
print("------------------------")
results.print_edge_list(weights="max_te_lag", fdr=False)

# Plot the network
plot_network(results=results, weights="max_te_lag", fdr=False)
plt.show()

# Print a summary of the CSV file
print("\nCSV file summary:")
print("----------------")
print(f"Total rows: {len(df)}")
print(f"Number of significant TE values: {df['TE'].notna().sum()}")
print("\nFirst few rows of the CSV:")
print(df.head())
