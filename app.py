from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import csv
from datetime import datetime

app = Flask(__name__)

# Directory to store results
RESULTS_FILE = os.path.join('results', f'results.csv')

# Directory to store images
IMAGE_DIRECTORY = 'images'
def load_images(directory):
    """Load the image files from the specified directory."""
    if os.path.exists("static/" + directory):
        return os.listdir("static/" + directory)
    return []

# Ensure the results directory and file exist
os.makedirs('results', exist_ok=True)
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['timestamp', 'task', 'image_dir', 'positive_images', 'negative_images'])

@app.route('/', methods=['GET', 'POST'])
def index():

    global IMAGE_DIRECTORY
    images = load_images(IMAGE_DIRECTORY)

    if request.method == 'POST':

        if 'change_dir' in request.form:
            # Handle directory change
            new_directory = request.form.get('image_directory')
            IMAGE_DIRECTORY = new_directory
            images = load_images(IMAGE_DIRECTORY)
            # Render the index.html template
            return render_template('index.html', images=images, current_directory=IMAGE_DIRECTORY)

        # Get the task and selected images from the form
        task = request.form.get('task')
        positive_images = request.form.getlist('images')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save the results to a CSV file
        with open(RESULTS_FILE, 'a', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            negative_images = [img for img in images if img not in positive_images]
            writer.writerow([timestamp, task, IMAGE_DIRECTORY, ",".join(positive_images), ",".join(negative_images)])

        # # Redirect to the result page with selected images
        # return redirect(url_for('result', images=",".join(positive_images), task=task, timestamp=timestamp))

    # Render the index.html template
    return render_template('index.html', images=images, current_directory=IMAGE_DIRECTORY)

@app.route('/download')
def download_csv():
    return send_file(RESULTS_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
