# webhook_server.py (Webhook Server)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class WebhookRegistration(BaseModel):
    new_URL: str
    event: str

event_urls = {'purchase': []}
data_file = "webhook_data.json"

# Load existing webhook data from file
try:
    with open(data_file, "r") as f:
        event_urls = json.load(f)
except FileNotFoundError:
    pass

@app.post("/register_webhook")
async def register_webhook(registration: WebhookRegistration):
    new_url = registration.new_URL
    event = registration.event

    if event not in event_urls:
        raise HTTPException(status_code=400, detail="Event does not exist")

    if new_url in event_urls[event]:
        raise HTTPException(status_code=400, detail="URL already registered for the event")

    event_urls[event].append(new_url)

    # Save updated webhook data to file
    with open(data_file, "w") as f:
        json.dump(event_urls, f)

    return {"message": "Webhook registration successful"}

@app.post("/unregister_webhook")
async def unregister_webhook(registration: WebhookRegistration):
    url_to_remove = registration.new_URL
    event = registration.event

    if event not in event_urls:
        raise HTTPException(status_code=400, detail="Event does not exist")

    if url_to_remove not in event_urls[event]:
        raise HTTPException(status_code=400, detail="URL not registered for the event")

    event_urls[event].remove(url_to_remove)

    # Save updated webhook data to file
    with open(data_file, "w") as f:
        json.dump(event_urls, f)

    return {"message": "Webhook unregistration successful"}

@app.post("/ping")
async def demo_purchase(product: dict):
    if not product:
        raise HTTPException(status_code=400, detail="Product information is required")

    urls = event_urls.get('purchase', [])
    for url in urls:
        requests.post(url, json=product)
    return {"message": "Demo purchase event triggered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
