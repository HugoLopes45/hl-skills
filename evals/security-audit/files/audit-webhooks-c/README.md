# checkout

Checkout backend. The payment provider reports payment results as signed events; a `payment.succeeded` event marks
the order paid and releases it for shipping. Production runs `gunicorn -c gunicorn.conf.py app.routes:app`.

The edge gateway terminates TLS, checks the provider's signature on `/internal/payment-events` and forwards verified events to this service. Its configuration lives in the platform repository.
