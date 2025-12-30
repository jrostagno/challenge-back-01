from fastapi import FastAPI, HTTPException

from app.models import DeliveryRequest, DeliveryResponse
from app.senders.email import MockEmailSender
from app.senders.push import MockPushSender
from app.senders.registry import SenderRegistry
from app.senders.sms import MockSmsSender

app = FastAPI(title="delivery-service", version="0.1.0")


def build_registry() -> SenderRegistry:
    reg = SenderRegistry()
    reg.register("email", MockEmailSender())
    reg.register("sms", MockSmsSender())
    reg.register("push", MockPushSender())
    return reg


registry = build_registry()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/deliver", response_model=DeliveryResponse)
async def deliver(req: DeliveryRequest):
    try:
        sender = registry.get(req.channel)
        return await sender.send(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}"
        ) from None
