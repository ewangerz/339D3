import csv
import os
import re
import random
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
    """Extracts the meet name from the <h1> tag of an HTML file."""
    parser = MeetNameParser()
    with open(html_file, 'r', encoding='utf-8') as file:
        parser.feed(file.read())
    return parser.meet_name

def csv_to_html(csv_filename, output_folder):
    # Derive the HTML filename by replacing the CSV extension with '.html' in the meets folder
    html_filename = os.path.join(output_folder, os.path.splitext(os.path.basename(csv_filename))[0] + '.html')

    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        # Ensure there are at least 5 rows for valid HTML generation
        if len(rows) < 5:
            print("CSV file must have at least 5 rows.")
            return

        # Extract values from the first five rows
        link_text = rows[0][0]
        h2_text = rows[1][0]
        link_url = rows[2][0]
        summary_text = rows[3][0]

        # Initialize HTML content
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{link_text}</title>
<link rel="stylesheet" href="../css/reset.css">
<link rel="stylesheet" href="../css/style.css">
<link rel="stylesheet" href="../css/enhancements.css"> <!-- Link to enhancements.css -->
<script src="../js/enhancements.js" defer></script> <!-- Link to enhancements.js -->
</head>
<body>
<a href="#main">Skip to Main Content</a>
<nav>
  <ul>
    <li><a href="index.html">Home Page</a></li>
    <li><a href="#summary">Summary</a></li>
    <li><a href="#team-results">Team Results</a></li>
    <li><a href="#individual-results">Individual Results</a></li>
    <li><a href="#gallery">Gallery</a></li>
  </ul>
</nav>
<header>
  <h1><a href="{link_url}">{link_text}</a></h1>
  <h2 tabindex="0">{h2_text}</h2>
</header>
<main id="main">

<section class="summary collapsible" id="summary">
  <button class="collapsible-button" onclick="toggleSection(this, 'summary')">Collapse</button>
  <h2 tabindex="0">Race Summary</h2>
  <div class="collapsible-content">{summary_text}</div>
</section>
"""

        # Start container for individual results
        html_content += """<section id="team-results" class="collapsible">\n
        <button class="collapsible-button" onclick="toggleSection(this, 'team-results')">Collapse</button>
        <h2 tabindex="0">Team Results</h2>
        <div class="collapsible-content">
        <table>\n"""

        table_start = True
        for row in rows[4:]:
            if len(row) == 3:
                if row[0] == "Place":
                    html_content += f"<tr><th>{row[0]}</th><th>{row[1]}</th><th>{row[2]}</th></tr>\n"
                else:
                    html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>\n"
            elif len(row) == 8 and row[5].strip().lower() == 'ann arbor skyline':
                if table_start:
                    table_start = False
                    html_content += "</table>\n</div>\n</section>\n<section id=\"individual-results\" class=\"collapsible\">\n<button class=\"collapsible-button\" onclick=\"toggleSection(this, 'individual-results')\">Collapse</button>\n<h2 tabindex=\"0\">Individual Results</h2>\n<div class=\"collapsible-content\">"

                place = row[0]
                grade = row[1]
                name = row[2]
                time = row[4]
                profile_pic = row[7]
                
                # Check if the profile image exists
                profile_img_path = os.path.join(os.getcwd(), "images", "profiles", profile_pic)
                if not os.path.isfile(profile_img_path):
                    print(f"Image not found for athlete '{name}'. Skipping entry.")
                    continue  # Skip if image is not found

                # Add the athlete div
                html_content += f"""
<div class="athlete">
<figure> 
    <img src="../images/profiles/{profile_pic}" width="200" alt="Profile picture of {name}" onclick="openModal(this.src)"> 
    <figcaption>{name}</figcaption>
</figure>
<dl>
    <dt>Place</dt><dd>{place}</dd>
    <dt>Time</dt><dd>{time}</dd>
    <dt>Grade</dt><dd>{grade}</dd>
</dl>
</div>
"""

        html_content += """</div></section>\n
        <section id="gallery" class="collapsible">
        <button class="collapsible-button" onclick="toggleSection(this, 'gallery')">Collapse</button>
        <h2 tabindex="0">Gallery</h2>
        <div class="collapsible-content">
        """

        html_content += create_meet_image_gallery(link_url)
        html_content += """
   </div>
   </section>
   </main>   
   <footer>
       <p>
       Skyline High School<br>
       <address>
       2552 North Maple Road<br>
       Ann Arbor, MI 48103<br><br>
       </address>
       <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
       Follow us on Instagram <a href="https://www.instagram.com/a2skylinexc/" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a> 
   </footer>

   <!-- Scroll-to-Top Button -->
   <button onclick="scrollToTop()" id="scrollTopBtn">Top</button>

</body>
</html>
"""

        # Save HTML content to a file in the meets folder
        with open(html_filename, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_content)
        print(f"HTML file '{html_filename}' created successfully.")

def process_meet_files():
    # Set the meets folder path
    meets_folder = os.path.join(os.getcwd(), "meets")
    csv_files = [f for f in os.listdir(meets_folder) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in folder: {meets_folder}")
        return

    for csv_file in csv_files:
        csv_file_path = os.path.join(meets_folder, csv_file)
        csv_to_html(csv_file_path, meets_folder)

# Step 1: Extract the meet ID from the URL
def extract_meet_id(url):
    match = re.search(r"/meet/(\d+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Meet ID not found in URL.")

# Step 2: Select random photos from the folder
def select_random_photos(folder_path, num_photos=25):
    all_files = os.listdir(folder_path)
    image_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    if len(image_files) < num_photos:
        return ""
    
    return random.sample(image_files, num_photos)

# Step 3: Generate HTML image tags
# Step 3: Generate HTML image tags
def generate_image_tags(image_files, folder_path):
    img_tags = []
    for img in image_files:
        img_path = os.path.join(folder_path, img)
        
        # Only include the image if the file exists
        if os.path.isfile(img_path):
            img_tags.append(f'<img src="../{img_path}" width="200" alt="" onclick="openModal(this.src)">')
        else:
            print(f"Image '{img}' not found, skipping in gallery.")
            
    return "\n".join(img_tags)

# Putting it all together
def create_meet_image_gallery(url):
    meet_id = extract_meet_id(url)
    folder_path = f'images/meets/{meet_id}/'
    
    if not os.path.exists(folder_path):
        return ""
    
    selected_photos = select_random_photos(folder_path)
    return generate_image_tags(selected_photos, folder_path)


if __name__ == "__main__":
    meets_folder = os.path.join(os.getcwd(), "meets")
    if not os.path.exists(meets_folder):
        print(f"Folder '{meets_folder}' does not exist.")
    else:
        process_meet_files()
