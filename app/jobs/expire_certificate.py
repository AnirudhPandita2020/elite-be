import datetime
from typing import List

from sqlalchemy.orm import Session

from app.service.certificate_service import fetch_latest_certificate_for_all_trucks
from app.service.truck_service import fetch_truckIds_of_site
from app.utils.env_utils import setting


async def check_expire_certificate_of_trucks(db: Session) -> List:
    truck_list = []
    for site in setting.allowed_sites:
        truck_data = await fetch_truckIds_of_site(site, db)
        for trucks in truck_data:
            latest_certificates = await fetch_latest_certificate_for_all_trucks(trucks.truck_id, db)
            certificate_data = {
                'trailer_number': trucks.trailer_number,
                'data': []
            }
            for certificates in latest_certificates:
                certificate_date = certificates[1]
                expiring_date = certificate_date - datetime.date.today()
                if 1 <= expiring_date.days <= 15:
                    certificate_data['data'].append({
                        'type': certificates[0],
                        'validity': f'expires after {expiring_date.days} days'
                    })
                elif expiring_date.days <= 0:
                    certificate_data['data'].append({
                        'type': certificates[0],
                        'validity': f'expired {-1 * expiring_date.days} days before'
                    })

            if len(certificate_data['data']) == 0:
                continue

            truck_list.append(certificate_data)

    return truck_list
