from datetime import datetime

import schedule
import time

from sql_app import crud
from sql_app.database import SessionLocal


class VerifyDateChange:

    @staticmethod
    def is_opportunity_expired():
        db = SessionLocal()
        try:
            db_opportunity = crud.get_opportunity(db, 0, 100)
            for opportunity in db_opportunity:
                now = datetime.today()
                opportunity_end_date = datetime.strptime(opportunity.endDate, '%d/%m/%Y')
                if opportunity_end_date < now and opportunity.isactive is True:
                    crud.update_active_status(db, opportunity, False)

        except Exception as e:
            print("Error: ", e.__str__())

    @staticmethod
    def verify_change_date():
        schedule.every().day.at("00:00").do(VerifyDateChange.is_opportunity_expired)

        while 1:
            schedule.run_pending()
            time.sleep(3600)
