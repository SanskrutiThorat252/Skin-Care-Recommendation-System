from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# PostgreSQL database connection
conn = psycopg2.connect(
    dbname="product_skincare",
    user="postgres",          # Change if needed
    password="root",          # Change if needed
    host="localhost",
    port="5432"
)

@app.route('/')
def home():
    return render_template("home.html", theme_colors={
        'background': '#E5D9F2',
        'primary': '#A594F9',
        'secondary': '#CDC1FF',
        'light': '#F5EFFF',
        'accent': '#A594F9'
    })

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file part"

        image = request.files['image']
        if image.filename == '':
            return "No selected file"

        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        # Simulate prediction using filename
        if 'oily' in filename.lower():
            skin_type = 'Oily'
        elif 'dry' in filename.lower():
            skin_type = 'Dry'
        elif 'sensitive' in filename.lower():
            skin_type = 'Sensitive'
        else:
            skin_type = 'Oily'  # default fallback

        # Fetch recommended products
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT "Name", "Price", "Type Product", "Image", "Link"
            FROM skincare_products
            WHERE "{skin_type}" IS NOT NULL AND "{skin_type}" != ''
            ORDER BY "{skin_type}"::float DESC
            LIMIT 10
        """)
        results = cursor.fetchall()
        cursor.close()

        products = [
            {
                'name': row[0],
                'price': parse_price(row[1]),
                'type': row[2],
                'image': row[3],
                'link': row[4],
                'skin_type': skin_type
            }
            for row in results
        ]

        return render_template("recommendations.html", products=products)

    return render_template("upload.html")

@app.route('/recommendations')
def recommendations():
    skin_type = 'Oily'  # default skin type

    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT "Name", "Price", "Type Product", "Image", "Link"
        FROM skincare_products
        WHERE "{skin_type}" IS NOT NULL AND "{skin_type}" != ''
        ORDER BY "{skin_type}"::float DESC
        LIMIT 10
    """)
    results = cursor.fetchall()
    cursor.close()

    products = [
        {
            'name': row[0],
            'price': parse_price(row[1]),
            'type': row[2],
            'image': row[3],
            'link': row[4],
            'skin_type': skin_type
        }
        for row in results
    ]

    return render_template("recommendations.html", products=products)

@app.route('/about')
def about():
    return render_template("about.html")

# Utility function to clean price string
def parse_price(price_str):
    if not price_str:
        return 0.0
    try:
        cleaned = str(price_str).replace('Rp', '').replace('.', '').replace(',', '.').strip()
        return float(cleaned)
    except:
        return 0.0

if __name__ == '__main__':
    app.run(debug=True)
