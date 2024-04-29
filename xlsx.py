
def read_excel_file(file_path):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def main():
    # Replace 'your_file.xlsx' with the path to your Excel file
    file_path = 'base.xlsx'

    # Read the Excel file
    df = read_excel_file(file_path)

    # If DataFrame is successfully loaded, print the first few rows
    if df is not None:
        print("Contents of the Excel file:")
        print(df.head())  # Display the first few rows of the DataFrame
    

if __name__ == "__main__":
    main()
