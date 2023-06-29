import asyncio
import LinkedIn_Extractor
# Example usage
csv_file = 'companiesdata.csv'  # Provide the path to your CSV file

# Run the process_csv function asynchronously
output_file = asyncio.run(LinkedIn_Extractor.Run(csv_file))

if output_file:
    print(f"Output file '{output_file}' generated successfully.")
else:
    print("Error occurred during processing.")

