from datetime import datetime, timedelta


async def certificate_id():
    return 'ETC' + str(datetime.utcnow()) + str(datetime.utcnow() + timedelta(minutes=120))
