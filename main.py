from fastapi import FastAPI, Request
from mangum import Mangum
import os
import boto3

app = FastAPI()

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

lambda_client = boto3.client('lambda', region_name='us-west-1')

@app.get("/", include_in_schema=False)
async def verify_webhook(request: Request):
    """
    Endpoint to verify the WhatsApp webhook.
    """
    mode = request.query_params.get("hub.mode")
    challenge = request.query_params.get("hub.challenge")
    verify_token = request.query_params.get("hub.verify_token")

    if mode == "subscribe" and challenge:
        if verify_token == VERIFY_TOKEN:
            return int(challenge)
        else:
            return "Verification token mismatch", 403
    return "Hello world", 200

@app.post("/", include_in_schema=False)
async def handle_webhook(request: Request):
    """
    Endpoint to handle incoming WhatsApp messages.
    """
    data = await request.json()
    # Process the incoming message data
    print(data)
    return "OK", 200
    pass




handler = Mangum(app)