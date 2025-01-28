import os
import subprocess

# Define the input and output folders
input_folder = r"C:\Users\verst\Desktop\ScrapedArticles"  # Update if needed
output_folder = r"C:\Users\verst\Desktop\RewrittenArticles"

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the instruction prompt
instruction = "Rewrite the following article in a less formal style and expand on the content, add some facts to it and relevant information:\n\n"

# Define categories and associated keywords
categories = {
    "Technology": ["AI", "technology", "software", "hardware"],
    "Health": ["health", "wellness", "medicine", "fitness"],
    "Finance": ["finance", "economy", "investment", "money"],
    "Lifestyle": ["lifestyle", "travel", "culture", "food"],
}

def assign_category(content):
    """Assign a category to an article based on its content."""
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in content.lower():
                return category
    return "Uncategorized"

# Process each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):  # Adjust if your file type is different
        input_path = os.path.join(input_folder, filename)

        # Remove underscores from filename for saving
        output_filename = filename.replace("_", "")
        output_path = os.path.join(output_folder, output_filename)

        try:
            # Read the file with UTF-8 encoding
            with open(input_path, 'r', encoding='utf-8', errors='replace') as file:
                content = file.read()

            # Combine the instruction with the article content
            prompt = instruction + content

            # Run the local AI to rewrite the content
            process = subprocess.Popen(
                ["ollama", "run", "dolphin-mistral"],  # Ensure this is the correct model name
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8"  # Ensure subprocess communication uses UTF-8
            )
            rewritten_content, error = process.communicate(input=prompt)

            if process.returncode == 0:
                # Assign a category based on the rewritten content
                category = assign_category(rewritten_content)

                # Save the rewritten content with category information
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(f"Category: {category}\n\n{rewritten_content}")
            else:
                print(f"Error rewriting {filename}: {error}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

print("Processing complete!")

# Run article_poster.py after the processing is complete
try:
    subprocess.run(["python", "article_poster.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Failed to run article_poster.py: {e}")
