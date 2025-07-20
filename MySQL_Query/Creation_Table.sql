-- 1. Brands Table
CREATE TABLE IF NOT EXISTS brands (
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(50)
);

-- 2. Models Table
CREATE TABLE IF NOT EXISTS models (
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(50),
    brand_id INT,
    fuel_type VARCHAR(20),
    transmission VARCHAR(20),
    FOREIGN KEY (brand_id) REFERENCES brands (brand_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 3. Car Data Table (mileage is here)

CREATE TABLE IF NOT EXISTS car_data (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    model_id INT,
    manufacturing_year INT,
    mileage FLOAT,
    sold_date DATE,
    FOREIGN KEY (model_id) REFERENCES models (model_id) ON DELETE CASCADE
);

-- 4. Car Predictions Table
CREATE TABLE IF NOT EXISTS
 car_predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT,
    predicted_price DECIMAL(10, 2),
    predicted_validity_years INT,
    sell_recommended BOOLEAN,
    FOREIGN KEY (car_id) REFERENCES car_data (car_id) ON DELETE CASCADE
);