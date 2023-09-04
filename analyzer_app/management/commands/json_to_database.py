from django.core.management.base import BaseCommand
import json
from ...models import StockData
from datetime import datetime

class Command(BaseCommand):
    help = 'Import JSON data into the database'

    def handle(self, *args, **options):
        with open('D:/python/django/full_stack_test/stock_market_analyzer/analyzer_app/stock_market_data.json', 'r') as file:
            data = json.load(file)[:4000]
            for item in data:
                stockData = StockData(
                    date=datetime.strptime(item['date'], '%Y-%m-%d').date(),
                    trade_code=item['trade_code'],
                    high=float(item['high'].replace(',', '')),
                    low=float(item['low'].replace(',', '')),
                    open=float(item['open'].replace(',', '')),
                    close=float(item['close'].replace(',', '')),
                    volume=int(item['volume'].replace(',', ''))
                )
                stockData.save()
        
        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))