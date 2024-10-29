import csv
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    # Read data from CSV file
    data = []
    with open('data.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)

    # HTML template for displaying data
    html_template = '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSV Data Display</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h2 class="text-center">CSV Data Display</h2>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>House</th>
                        <th>Gold</th>
                        <th>Silver</th>
                        <th>Bronze</th>
                        <th>Name</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in data %}
                    <tr>
                        <td>{{ row.rank }}</td>
                        <td>{{ row.house }}</td>
                        <td>{{ row.gold }}</td>
                        <td>{{ row.silver }}</td>
                        <td>{{ row.bronze }}</td>
                        <td>{{ row.name }}</td>
                        <td>{{ row.total }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    '''

    return render_template_string(html_template, data=data)

if __name__ == '__main__':
    app.run(debug=True)
