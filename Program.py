from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your-secret-key-here' 

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',  
    'password': 'jaihind!',  
    'database': 'car_prediction'
}

def create_tables_and_insert(brand, model, manufacturing_date, fuel, mileage, transmission):
    """Create normalized tables and insert car data"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create brands table
        create_brands_table = """
        CREATE TABLE IF NOT EXISTS brands (
            brand_id INT AUTO_INCREMENT PRIMARY KEY,
            brand_name VARCHAR(50)
        )
        """
        cursor.execute(create_brands_table)
        
        # Create models table
        create_models_table = """
        CREATE TABLE IF NOT EXISTS models (
            model_id INT AUTO_INCREMENT PRIMARY KEY,
            model_name VARCHAR(50),
            brand_id INT,
            fuel_type VARCHAR(20),
            transmission VARCHAR(20),
            FOREIGN KEY (brand_id) REFERENCES brands (brand_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
        cursor.execute(create_models_table)
        
        # Create car_data table
        create_car_data_table = """
        CREATE TABLE IF NOT EXISTS car_data (
            car_id INT AUTO_INCREMENT PRIMARY KEY,
            model_id INT,
            manufacturing_year DATE,
            mileage FLOAT,
            price DECIMAL(10, 2),
            estimated_life_km INT,
            sold_date DATE,
            validity_years INT,
            sell_recommended BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (model_id) REFERENCES models (model_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
        cursor.execute(create_car_data_table)
        
        # Insert or get brand_id
        cursor.execute("SELECT brand_id FROM brands WHERE brand_name = %s", (brand,))
        brand_result = cursor.fetchone()
        
        if brand_result:
            brand_id = brand_result[0]
        else:
            cursor.execute("INSERT INTO brands (brand_name) VALUES (%s)", (brand,))
            brand_id = cursor.lastrowid
        
        # Insert or get model_id
        cursor.execute("""
            SELECT model_id FROM models 
            WHERE model_name = %s AND brand_id = %s AND fuel_type = %s AND transmission = %s
        """, (model, brand_id, fuel, transmission))
        model_result = cursor.fetchone()
        
        if model_result:
            model_id = model_result[0]
        else:
            cursor.execute("""
                INSERT INTO models (model_name, brand_id, fuel_type, transmission) 
                VALUES (%s, %s, %s, %s)
            """, (model, brand_id, fuel, transmission))
            model_id = cursor.lastrowid
        
        # Insert car data
        cursor.execute("""
            INSERT INTO car_data (model_id, manufacturing_year, mileage)
            VALUES (%s, %s, %s)
        """, (model_id, manufacturing_date, mileage))
        
        car_id = cursor.lastrowid
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"✅ Data successfully inserted into normalized database with car_id: {car_id}")
        return car_id
        
    except Error as e:
        print(f"❌ Database error: {e}")
        return None


@app.route("/")
def index():
    return render_template("Form.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        brand = request.form.get("brand")
        model = request.form.get("model").upper()  # Convert model to uppercase
        year_date = request.form.get("year")
        fuel = request.form.get("fuel")
        mileage = request.form.get("mileage")
        transmission = request.form.get("transmission")

        
        if not all([brand, model, year_date, fuel, mileage, transmission]):
            flash("Please fill in all required fields.", "error")
            return render_template("Form.html")

        try:
            # Validate date format and keep as full date for database
            from datetime import datetime
            datetime.strptime(year_date, '%Y-%m-%d')  # Validate format
            manufacturing_date = year_date  # Keep full date
        except ValueError:
            flash("Invalid date format. Please select a valid manufacturing date.", "error")
            return render_template("Form.html")

        try:
            mileage_float = float(mileage)
        except ValueError:
            flash("Invalid mileage value. Please enter a valid number.", "error")
            return render_template("Form.html")

        car_id = create_tables_and_insert(brand, model, manufacturing_date, fuel, mileage_float, transmission)
        
        if car_id:
            # Extract year for display
            display_year = manufacturing_date.split('-')[0]
            print(f"=== Car Data Inserted Successfully ===")
            print(f"Car ID: {car_id}")
            print(f"Brand: {brand}")
            print(f"Model: {model}")
            print(f"Manufacturing Date: {manufacturing_date}")
            print(f"Fuel Type: {fuel}")
            print(f"Mileage: {mileage_float} km")
            print(f"Transmission: {transmission}")
            print(f"=====================================")
            
            return render_template("Form.html", success=True, alert_message="Data submitted successfully", data={
                'brand': brand, 'model': model, 'year': display_year, 
                'fuel': fuel, 'mileage': mileage, 'transmission': transmission
            })
        else:
            flash("Failed to save data to database. Please try again.", "error")
            return render_template("Form.html")

    except Exception as e:
        print(f"Error processing form: {e}")
        flash("An error occurred while processing your request.", "error")
        return render_template("Form.html")


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
