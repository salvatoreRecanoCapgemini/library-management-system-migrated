

import logging
from app.services.loan_service import extend_loan_period

def extend_loan_period_controller(p_loan_id, p_extension_days=7):
    if not isinstance(p_loan_id, int) or p_loan_id <= 0:
        return {'error': 'Invalid loan ID'}
    if not isinstance(p_extension_days, int) or p_extension_days <= 0:
        return {'error': 'Invalid extension days'}

    try:
        extend_loan_period(p_loan_id, p_extension_days)
    except ValueError as e:
        logging.error(f'Error extending loan period: {str(e)}')
        return {'error': str(e)}
    except Exception as e:
        logging.error(f'Unexpected error extending loan period: {str(e)}')
        return {'error': 'An unexpected error occurred'}