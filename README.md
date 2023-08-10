# GSTGenius - GST Bill Invoice Generator and Printer

GSTGenius is a Django web application designed to streamline the process of creating GST bill invoices. This application provides a user-friendly interface for generating GST-compliant invoices and supports the printing of the generated invoices.

## Features

- **Invoice Creation**: Users can create GST bill invoices by entering relevant details such as client information, items, quantities, prices, and applicable taxes.

- **GST Compliance**: GSTGenius automatically calculates and applies the appropriate Goods and Services Tax (GST) based on the items and tax rates entered by the user.

- **Invoice Preview**: Users can preview the generated invoice before printing it.

- **Invoice Printing**: Once the invoice is generated and confirmed, users have the option to print the invoice directly from the application.
  
- **Invoice History**: Maintain a history of generated invoices for reference and retrieval.

## How it Works

1. **Invoice Information**: Users provide necessary details including client information, invoice number, items, quantities, prices, and tax rates.

2. **GST Calculation**: GSTGenius calculates the GST amounts based on the provided tax rates and adds them to the invoice total.

3. **Invoice Preview**: Users can preview the generated invoice to ensure accuracy and completeness.

4. **Printing**: Once satisfied with the invoice, users can initiate the printing process directly from the application.

## Getting Started

Follow these steps to use GSTGenius:

1. **Installation**: Clone the GSTGenius repository and install the required dependencies using `pip`:

    ```
    git clone https://github.com/your-username/GSTGenius.git
    cd GSTGenius
    pip install -r requirements.txt
    ```

2. **Database Setup**: Set up the database by running migrations:

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Run the Application**: Start the Django development server:

    ```
    python manage.py runserver
    ```

4. **Access the Web Interface**: Open a web browser and navigate to `http://127.0.0.1:8000` to access GSTGenius.

[![Screenshot-2023-08-10-170707.png](https://i.postimg.cc/fR4Wy7Pg/Screenshot-2023-08-10-170707.png)](https://postimg.cc/BXgfwF4x)

5. **Create Invoices**: Create new invoices by entering client and item details, and review the calculated GST amounts.

6. **Preview and Print**: Preview the invoice and print it directly from the application.

## Future Enhancements

GSTGenius has potential for further improvements:

- **Invoice Templates**: Provide customizable invoice templates with options for branding and styling.

- **Edit Invoices**: Allow users to edit already generated invoices.

GSTGenius simplifies the process of creating and managing GST-compliant invoices. By combining the power of Django with intuitive user interfaces, GSTGenius empowers users to generate, preview, and print professional invoices with ease.
