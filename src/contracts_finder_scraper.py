import os
import csv
import json
import time
import requests
from datetime import datetime, timedelta


def get_data(published_from, published_to):
    url = "https://www.contractsfinder.service.gov.uk/api/rest/2/search_notices/json"
    criteria = {
        "searchCriteria": {
            "types": ["Contract"],
            "statuses": ["Awarded"],
            "publishedFrom": published_from.strftime('%Y-%m-%d'),
            "publishedTo": published_to.strftime('%Y-%m-%d'),
        },
        "size": 1000
    }
    payload = json.dumps(criteria)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        print("Received 403 error. Waiting for 5 minutes before retrying...")
        time.sleep(300)
        return get_data(published_from, published_to)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print("Response content:")
        print(response.text)
        return None


def adjust_date_range(start_date, end_date):
    field_names = [
        'id', 'parentId', 'noticeIdentifier', 'title', 'description', 'cpvDescription',
        'cpvDescriptionExpanded', 'publishedDate', 'deadlineDate', 'awardedDate', 'awardedValue',
        'awardedSupplier', 'approachMarketDate', 'valueLow', 'valueHigh', 'postcode', 'coordinates',
        'isSubNotice', 'noticeType', 'noticeStatus', 'isSuitableForSme', 'isSuitableForVco',
        'awardedToSme', 'awardedToVcse', 'lastNotifableUpdate', 'organisationName', 'sector',
        'cpvCodes', 'cpvCodesExtended', 'region', 'regionText', 'start', 'end'
    ]
    current_from = start_date
    current_to = start_date + timedelta(days=30)
    csv_file = "data.csv"
    with open(os.path.join(os.getcwd(), '..', 'data', csv_file),
              'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        while current_to <= end_date:
            print(f"Fetching data from {current_from.strftime('%Y-%m-%d')} to "
                  f"{current_to.strftime('%Y-%m-%d')}")
            data = get_data(current_from, current_to)
            if data and (data['hitCount'] > 1000):
                current_to = current_from + timedelta(days=14)
                print(f"More than 1000 results. Adjusting range to fortnightly: "
                      f"{current_from.strftime('%Y-%m-%d')} to {current_to.strftime('%Y-%m-%d')}")
                data = get_data(current_from, current_to)
                if data and (data['hitCount'] > 1000):
                    current_to = current_from + timedelta(days=7)
                    print(f"More than 1000 results. Adjusting range to weekly: "
                          f"{current_from.strftime('%Y-%m-%d')} to {current_to.strftime('%Y-%m-%d')}")
                    data = get_data(current_from, current_to)
                    if data and (data['hitCount'] > 1000):
                        current_to = current_from + timedelta(days=1)
                        print(f"More than 1000 results. Adjusting range to daily: "
                              f"{current_from.strftime('%Y-%m-%d')} to {current_to.strftime('%Y-%m-%d')}")
                        data = get_data(current_from, current_to)
            if data and (data['hitCount'] <= 1000):
                print(f"Data fetched for range: {current_from.strftime('%Y-%m-%d')} to "
                      f"{current_to.strftime('%Y-%m-%d')}, Records: {data['hitCount']}")
                for item in data['noticeList']:
                    writer.writerow(item['item'])
            elif data['hitCount'] > 1000:
                print(f'Cripes, more than 1000 returns on: {current_from.strftime("%Y-%m-%d")} to '
                      f'{current_to.strftime("%Y-%m-%d")}, Records: {data["hitCount"]}')
                stop #if this happens, approach needs modifying into intra-day timestamps
            else:
                print(f"No data returned for range: {current_from.strftime('%Y-%m-%d')} to "
                      f"{current_to.strftime('%Y-%m-%d')}")
            current_from = current_to + timedelta(days=1)
            current_to = current_from + timedelta(days=30)


if __name__ == "__main__":
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2024, 5, 1)
    adjust_date_range(start_date, end_date)
