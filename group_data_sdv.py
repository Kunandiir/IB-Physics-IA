import pandas as pd


def process_physics_data(input_file, output_file):
    # Load the CSV file without assuming a header row
    # This ensures we capture all data points correctly
    df = pd.read_csv(input_file, header=None)

    # Column 2 (Index 1) is Distance (m)
    # Column 4 (Index 3) is Force
    # We select only these two columns
    df = df[[1, 2]].copy()
    df.columns = ["Distance", "Force"]

    # Convert values to numeric, turning any text (like headers) into NaN
    df["Distance"] = pd.to_numeric(df["Distance"], errors="coerce")
    df["Force"] = pd.to_numeric(df["Force"], errors="coerce")

    # Remove rows that couldn't be converted (like the original header row)
    df = df.dropna()

    # Group by Distance and calculate the Mean and Standard Deviation for Force
    result = df.groupby("Distance")["Force"].agg(["mean", "std"]).reset_index()

    # Rename columns for clarity
    result.columns = ["Distance (m)", "Mean Force", "Std Dev Force"]

    # Sort by Distance for better readability
    result = result.sort_values(by="Distance (m)")

    # Save the processed data to a new CSV file
    result.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

    return result


# Execute the processing

amps = ["0.05"]
coils = ["300"]


for coil in coils:
    for amp in amps:
        processed_df = process_physics_data(
            "/mnt/main_storage/Physics_Work_Backup/300 0.05.csv",
            f"/mnt/main_storage/Physics_Work_Backup/analisis_std/{coil} {amp}_processed_physics_data.csv",
        )

# Display the first few rows of the result
print(processed_df.head())
