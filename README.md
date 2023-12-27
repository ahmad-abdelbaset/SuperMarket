# Supermarket Management System

## Overview

The Supermarket Management System is a Python application built with the Tkinter library and utilizes a MySQL 8.1 database. This program is designed to assist in the management of small supermarkets. It offers a user-friendly interface for handling product pricing, barcode scanning, and comprehensive user and product management.

## Features

### Login

- Upon running the program, users are prompted with a login window.
- Users must enter a valid username and password to access the system.

![image](https://github.com/ahmad-abdelbaset/SuperMarket/assets/27960593/df5db856-8790-460e-9101-805c44c7e1ed)



### Features

![image](https://github.com/ahmad-abdelbaset/SuperMarket/assets/27960593/e36e183d-3afa-4ce5-8787-22f89ca29649)


#### Low Permissions

1. **Check Price:**
   - Users can scan product barcodes to check their prices.


![image](https://github.com/ahmad-abdelbaset/SuperMarket/assets/27960593/d4862103-b7e2-4751-a59a-f7776b40614c)



2. **Sum Products Prices:**
   - Users can scan multiple product barcodes to calculate and display the total price.

![image](https://github.com/ahmad-abdelbaset/SuperMarket/assets/27960593/67c48a98-27ab-4a45-96ee-f6e354cc8efb)


#### High Permissions

In addition to low permission features, high-level users can access:

3. **Admin Settings:**
   - **Edit Users:**
     - Add new users.
     - Change passwords for existing users.
     - Change permissions for users (high to low or vice versa).

   - **Edit Products:**
     - Add new products.
     - Edit existing product information, including:
       - Barcode
       - Product description
       - Selling and buying prices
       - Expiration date
       - Current quantity
     - Delete products.
     - Search for specific products.
     
     Note: If a product has a quantity of 40 and 10 units are sold, the quantity will be automatically updated.

![image](https://github.com/ahmad-abdelbaset/SuperMarket/assets/27960593/d10e5030-b497-47d5-8dc9-0cd600a9c710)
![image](https://github.com/ahmad-abdelbaset/SuperMarket/assets/27960593/4cca245e-6fc2-4bcd-abf3-90231b21d6cc)
![image](https://github.com/ahmad-abdelbaset/SuperMarket/assets/27960593/3aa317b4-395f-4bb5-b900-f0a9d4be06a6)


### MySQL Automatic Startup

- The program automatically starts the MySQL 8.1 database if it is stopped.

## Installation

1. Ensure your system is running Windows 10.
2. Obtain the program as an .exe file.
3. Install MySQL on your PC.
4. Create a database called `supermarkets`.
5. Restore the database using the provided backup file:
    ```bash
    cd path/to/project
    mysql -u root -p supermarket < supermarket_backup.sql
    ```

## License

This program is protected by copyright, and it is not allowed to be sold or used without explicit permission from the author, Ahmad Abdelbaset.

## Contact Information

For any issues or inquiries, please contact the author via email: ahmad.abdelbaset@outlook.com.
