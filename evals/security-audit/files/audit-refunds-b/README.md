# orders

Order API for the storefront. Customers can turn a paid order into store credit, which they spend on later orders.
Production runs `gunicorn -c gunicorn.conf.py app.routes:app` against PostgreSQL.
