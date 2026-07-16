import os
import argparse
import pandas as pd
import glob

def extract_pxp_data(folder_path):
    # Find all Excel files in the target folder
    search_pattern = os.path.join(folder_path, '*.xlsx')
    excel_files = glob.glob(search_pattern)
    
    if not excel_files:
        print(f"No Excel files found in the directory: {folder_path}")
        return

    consolidated_data = []
    print(f"Found {len(excel_files)} files. Starting extraction...")

    for file in excel_files:
        print(f"Processing: {os.path.basename(file)}")
        try:
            # Read the Excel file without headers
            df = pd.read_excel(file, header=None)
            
            # 1. Month [4th row -> index 3, column 0]
            month_val = df.iloc[3, 0] if pd.notna(df.iloc[3, 0]) else df.iloc[2, 0] 
            
            # 2. Plant name [Extract from filename]
            file_name = os.path.basename(file)
            plant_name = file_name.split()[2] # Grabs the 3rd word, e.g., "Marwar"
            
            # 3. Application [2nd row -> index 1, column 0]
            application_val = df.iloc[1, 0] if pd.notna(df.iloc[1, 0]) else df.iloc[0, 0]

            # --- STEP 4a: Build a Tag Dictionary from the Header Section ---
            # Tags are listed vertically in rows 7-25 (indices 6-24)
            tags_dict = {}
            for i in range(6, 25):
                # Left side tags (Columns A & B)
                num_str1 = str(df.iloc[i, 0]).replace(":", "").strip()
                name1 = str(df.iloc[i, 1]).strip()
                if num_str1.isdigit() and name1 != "nan":
                    tags_dict[int(num_str1)] = name1
                
                # Right side tags (Columns L & M)
                num_str2 = str(df.iloc[i, 11]).replace(":", "").strip()
                name2 = str(df.iloc[i, 12]).strip()
                if num_str2.isdigit() and name2 != "nan":
                    tags_dict[int(num_str2)] = name2

            # --- STEP 4b & 5: Map tags to data columns and extract values ---
            # The Tag Numbers (1, 2, 3...) map to the columns on Row 27 (index 26)
            for col_idx in range(2, df.shape[1]):
                
                # Get the tag number from row 27
                tag_number_raw = df.iloc[26, col_idx]
                
                # Check if it's a valid tag number
                if pd.notna(tag_number_raw) and str(tag_number_raw).strip().isdigit():
                    tag_id = int(str(tag_number_raw).strip())
                    
                    # Look up the actual Tag Name using our dictionary
                    tag_name = tags_dict.get(tag_id)
                    
                    # Extract Min (67th row -> index 66)
                    min_val = df.iloc[66, col_idx]
                    
                    # Extract Max (64th row -> index 63)
                    max_val = df.iloc[63, col_idx]
                    
                    # Extract Std Dev (84th row -> index 83)
                    std_dev = df.iloc[83, col_idx]
                    
                    # Append to our master list
                    consolidated_data.append({
                        "Plant Name": plant_name,
                        "Month": month_val,
                        "Application": application_val,
                        "Tag Name": tag_name,
                        "Min": min_val,
                        "Max": max_val,
                        "Standard Deviation": std_dev
                    })
                
        except Exception as e:
            print(f"Error processing {os.path.basename(file)}: {e}")

    # Convert to DataFrame and Export
    if consolidated_data:
        final_df = pd.DataFrame(consolidated_data)
        output_filename = "Consolidated_PXP_Report.xlsx"
        final_df.to_excel(output_filename, index=False)
        print(f"\nSuccess! Consolidated data saved to '{output_filename}'.")
        print(f"Total rows extracted: {len(final_df)}")
    else:
        print("\nFailed to extract any data. Please check if the row indexes match your file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and consolidate PXP Excel reports.")
    parser.add_argument("folder", type=str, help="Path to the folder containing the Excel files.")
    args = parser.parse_args()
    
    extract_pxp_data(args.folder)