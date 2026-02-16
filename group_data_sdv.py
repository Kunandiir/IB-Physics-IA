import pandas as pd


def process_physics_data(input_file, output_file):
    df = pd.read_csv(input_file, header=None)

    df = df[[1, 2]].copy()
    df.columns = ["Distance", "Force"]

    df["Distance"] = pd.to_numeric(df["Distance"], errors="coerce")
    df["Force"] = pd.to_numeric(df["Force"], errors="coerce")

    # Remove rows that couldn't be converted 
    df = df.dropna()

    # Group by Distance and calculate the Mean and Standard Deviation for Force
    result = df.groupby("Distance")["Force"].agg(["mean", "std"]).reset_index()

    result.columns = ["Distance (m)", "Mean Force", "Std Dev Force"]

    result = result.sort_values(by="Distance (m)")


    result.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

    return result



amps = ["0.05"]
coils = ["300"]


for coil in coils:
    for amp in amps:
        processed_df = process_physics_data(
            "/mnt/main_storage/Physics_Work_Backup/300 0.05.csv",
            f"/mnt/main_storage/Physics_Work_Backup/analisis_std/{coil} {amp}_processed_physics_data.csv",
        )

print(processed_df.head())
