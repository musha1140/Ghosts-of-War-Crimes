#!/bin/bash
# Instructions on how to append the Readme
# Variables
DATA_FILE="./data/processed_data/processed_data.csv"
README_FILE="README.md"

echo "Starting the data appender for verified sources."

# Function to add data to the dataset file
add_to_dataset() {
  echo "Adding data to $DATA_FILE..."

  read -p "Incident Type: " incident_type
  read -p "Date (YYYY-MM-DD): " date
  read -p "Location: " location
  read -p "Number of Victims: " victims
  read -p "Responsible Party: " responsible_party
  read -p "Latitude: " latitude
  read -p "Longitude: " longitude
  read -p "Source URL: " source

  echo -e "$incident_type,$date,$location,$victims,$responsible_party,$latitude,$longitude,$source" >> "$DATA_FILE"

  echo "Data added successfully!"
}

# Function to append verification examples to README
add_to_readme() {
  echo "Adding source verification example to $README_FILE..."

  read -p "Provide a brief description of the example: " description
  read -p "Enter the source URL: " source_url

  echo -e "\n#### Example of Verification\n\n- **Description:** $description\n- **Source:** [$source_url]($source_url)" >> "$README_FILE"

  echo "Example added successfully!"
}

# Menu
echo "Select an option:"
echo "1. Add data to the dataset file"
echo "2. Add a verification example to README"
echo "3. Exit"
read -p "Your choice: " choice

case $choice in
  1) add_to_dataset ;;
  2) add_to_readme ;;
  3) echo "Exiting..." && exit 0 ;;
  *) echo "Invalid choice. Exiting..." && exit 1 ;;
esac
