# checkout

Checkout backend. The payment provider reports payment results as signed events; a `payment.succeeded` event marks
the order paid and releases it for shipping. Production runs `gunicorn -c gunicorn.conf.py app.routes:app`.
