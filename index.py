import os
from html.parser import HTMLParser

# Custom HTML parser to extract the <h1> tag content
class MeetNameParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meet_name = None
        self.in_h1 = False

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_h1 and not self.meet_name:
            self.meet_name = data.strip()

def extract_meet_name(html_file):
    """Extracts the meet name from the <h1> tag of an HTML file, if it exists."""
    parser = MeetNameParser()
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            parser.feed(file.read())
    except FileNotFoundError:
        print(f"File {html_file} not found.")
        return None
    return parser.meet_name

def generate_homepage(meets_folder, output_file="index.html"):
    # Step 1: Get all the meet HTML files
    meet_files = [f for f in os.listdir(meets_folder) if f.endswith('.html')]

    # Step 2: Generate the homepage HTML with inline CSS
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cross Country Meets</title>
        <link rel="stylesheet" href="../css/homepage.css">
    </head>
    <body>

    <header>
        <h1>Cross Country Meets Homepage</h1>
        <p>Explore all the cross-country meets below.</p>
    </header>

    <main>
    <section id="meets-list">
    <h2 tabindex="0">Available Meets</h2>
    <div class="meet-boxes">
    """

    # Step 3: Add each meet as a boxed item with its extracted name and link
    for meet_file in meet_files:
        meet_file_path = os.path.join(meets_folder, meet_file)
        
        # Extract the actual meet name from the HTML file
        meet_name = extract_meet_name(meet_file_path)
        
        # Only add the meet if a valid meet name was found
        if meet_name:
            # Fallback to the file name if no meet name was found in the <h1> tag
            meet_name = meet_name or os.path.splitext(meet_file)[0].replace("-", " ").title()
            
            # Create a meet box with a link to the meet file
            html_content += f"""
            <div class="meet-box">
                <h3>{meet_name}</h3>
                <a href="{meet_file}">View Meet Details</a>
            </div>
            """
        else:
            print(f"Skipping {meet_file}: No valid <h1> tag found.")

    # Step 4: Close the HTML structure
    html_content += """
    </div>
    </section>

    <footer>
        <p>Skyline Cross Country </p>
    </footer>

    </body>
    </html>
    """

    # Step 5: Write the HTML content to the homepage file
    homepage_path = os.path.join(meets_folder, output_file)
    with open(homepage_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"Homepage created successfully at: {homepage_path}")

def create_meet_homepage():
    # Define the meets folder path
    meets_folder = os.path.join(os.getcwd(), "meets")

    # Check if the meets folder exists
    if not os.path.exists(meets_folder):
        print(f"Meets folder '{meets_folder}' does not exist.")
        return

    # Call the function to generate the homepage
    generate_homepage(meets_folder)

if __name__ == "__main__":
    create_meet_homepage()
