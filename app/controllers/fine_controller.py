

from app.services.fine_service import FineService
from decimal import Decimal

class FineController:
    def process_fine_payment(self, p_fine_id: int, p_amount_paid: Decimal):
        fine_service = FineService()
        fine_service.process_fine_payment(p_fine_id, p_amount_paid)