from datetime import datetime
from typing import Optional


def _format_date_for_input(date_value: Optional[str]) -> Optional[str]:
        """
        Convert incoming date (expected YYYY-MM-DD) to DD/MM/YYYY for the FBI form inputs.
        """
        if not date_value:
            return None
        try:
            parsed = datetime.strptime(date_value, "%Y-%m-%d")
            return parsed.strftime("%d/%m/%Y")
        except ValueError:
            #logger.warning(f"Invalid date format for FBI sync: {date_value}") #TODO
            return None