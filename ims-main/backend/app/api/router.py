from fastapi import APIRouter

from app.api import shipment, auth, user, dashboard, inventory, product, partner, customer, inbound, outbound, snapshot, audit, settings, incoming, rma, bom, print, station, device_ledger, stocktake, inventory_adjustment, docs

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(dashboard.router)
api_router.include_router(inventory.router)
api_router.include_router(product.router)
api_router.include_router(partner.router)
api_router.include_router(customer.router)
api_router.include_router(inbound.router)
api_router.include_router(outbound.router)
api_router.include_router(snapshot.router)
api_router.include_router(audit.router)
api_router.include_router(settings.router)
api_router.include_router(incoming.router)
api_router.include_router(rma.router)
api_router.include_router(shipment.router)
api_router.include_router(bom.router)
api_router.include_router(bom.router_task)
api_router.include_router(print.router)

# 二期新增
api_router.include_router(station.router)
api_router.include_router(device_ledger.router)
api_router.include_router(stocktake.router)
api_router.include_router(inventory_adjustment.router)
api_router.include_router(docs.router)