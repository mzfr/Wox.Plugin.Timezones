import copy
import os
from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

from wox import Wox, WoxAPI

TIMEZONES = {"pst": "US/Pacific", "ct": "US/Central", "ist": "Asia/Kolkata"}

RESULT_TEMPLATE = {
    "Title": "{}",
    "SubTitle": "copyToClipboard",
    "IcoPath": "Images/clock.png",
    "JsonRPCAction": {
        "method": "copyToClipboard",
        "parameters": ["{}"],
        "dontHideAfterAction": False,
    },
}


class TimeZone(Wox):
    def query(self, query):
        """Take a given time we do the following
        1. Replace the timezone of time with the first_zone/from_zone
        2. Replace the year to current year
            - we can even hardcode 2023 for quite sometime
        3. Then update the astimezone to to_zone
        4. Return strftime('%I:%M %p') of the time we get from Step-3
        """
        results = []

        try:
            time, indication, first_zone, _, second_zone = query.strip().split(" ")

            if len(time.split(":")) > 1:
                time_obj = datetime.strptime(time + indication, "%I:%M%p")
            else:
                time_obj = datetime.strptime(time + indication, "%I%p")

            fzone = TIMEZONES[first_zone.lower()]
            szone = TIMEZONES[second_zone.lower()]

            converted_time = (
                time_obj.replace(tzinfo=ZoneInfo(fzone))
                .replace(year=2023)
                .astimezone(ZoneInfo(szone))
                .strftime("%I:%M %p")
            )

            self.add_item(results, converted_time)

        except Exception as err:
            self.add_item(results, err)

        return results

    def add_item(self, results: List[dict], converted_time):

        template = copy.deepcopy(RESULT_TEMPLATE)
        template["Title"] = template["Title"].format(converted_time)
        template["JsonRPCAction"]["parameters"][0] = str(converted_time)
        results.append(template)

    def copyToClipboard(self, value):
        os.system("echo | set /p nul=" + value.strip() + "| clip")


if __name__ == "__main__":
    TimeZone()
