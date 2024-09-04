from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import csv
from datetime import datetime

app = Flask(__name__)

# Directory to store results
RESULTS_FILE = os.path.join('data', 'results.csv')

# List of 100 images for a 6x5 grid
images = [f'img{i:02}.png' for i in range(1, 101)]

# Ensure the results directory and file exist
os.makedirs('data', exist_ok=True)
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Username', 'Timestamp', 'Selected Photos'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the username and selected photos from the form
        username = request.form.get('username')
        selected_photos = request.form.getlist('photo')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save the results to a CSV file
        with open(RESULTS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, timestamp, ", ".join(selected_photos)])

        # Redirect to the result page with selected photos
        return redirect(url_for('result', photos=",".join(selected_photos), username=username, timestamp=timestamp))

    # Render the index.html template
    return render_template('index.html', images=images)

@app.route('/result')
def result():
    # Get the selected photos, username, and timestamp from the query parameters
    selected_photos = request.args.get('photos').split(',')
    username = request.args.get('username')
    timestamp = request.args.get('timestamp')

    # Render the result.html template
    return render_template('result.html', photos=selected_photos, username=username, timestamp=timestamp)

@app.route('/download')
def download_csv():
    return send_file(RESULTS_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
