import os
import pandas as pd

from pathlib import Path

def combine_csv_to_excel(input_folder: str, output_file: str) -> None:
    """
    Combines all CSV files from the input folder into a single Excel file,
    with each CSV as a separate sheet.
    """
    input_path = Path(input_folder)
    output_path = Path(output_file)

    # Ensure the input directory exists
    if not input_path.exists():
        print(f"Input directory does not exist: {input_folder}")
        return

    # Create the output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Get all CSV files
    csv_files = list(input_path.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {input_folder}")
        return

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for csv_file in csv_files:
            sheet_name = csv_file.stem.replace('_deployment_resource_info', '')[:31]  # Max sheet name length
            try:
                df = pd.read_csv(csv_file)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            except Exception as e:
                print(f"Failed to process {csv_file.name}: {e}")

    print(f"Excel file created at: {output_path}")

def main():
    input_folder = r"C:\temp\reports"
    output_file = os.path.join(input_folder, "custom_usage.xlsx")

    combine_csv_to_excel(input_folder, output_file)

if __name__ == "__main__":
    main()
