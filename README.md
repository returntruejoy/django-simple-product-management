# Simple Product Management System

A Django web app for uploading product data from Excel and moving items through a draft-to-approved workflow.

## Who It Is For
Operations or inventory staff who batch-upload product catalogs and approve records before publishing.

## Key Features
- Upload `.xlsx` files and validate required columns and values
- Create new product drafts or update existing products as drafts
- Highlight recently updated products after upload
- Approve individual draft products to move them to the approved list
- Search approved products by name or category
- Filter approved products by updated date range and control pagination

## Architecture Overview
- Framework: Django 4.2 (project: `config`, app: `products`)
- Data: `Product` model stored in SQLite (`db.sqlite3`)
- Import: `openpyxl` reads Excel files; rows are validated and saved in a transaction
- UI: Server-rendered templates (`templates/`) for drafts and approved lists
- Routes:
  - `/` draft upload + draft list
  - `/approved/` approved list + filters
  - `/approve/<product_id>/` approve a draft

## Getting Started (Local)
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run migrations:
   - `python manage.py migrate`
4. Start the dev server (standard Django command):
   - `python manage.py runserver`
5. Open:
   - `http://127.0.0.1:8000/` for drafts and upload
   - `http://127.0.0.1:8000/approved/` for approved products

## Deployment (PythonAnywhere)
See `DEPLOYMENT.md` for the checklist.

## Sample Data
- `sample_products.xlsx` for testing uploads.
