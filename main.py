import datetime
import time
from amazon_seller import ReportSeller
from amazon_seller_token import AccessTokenSeller
from get_report import Report
from get_token import AccessToken
from google_sheet import GoogleSheet
from config import REFRESH_TOKEN


# Set date ranges
start_date = str(datetime.datetime.now() - datetime.timedelta(days=2))[:10]
end_date = str(datetime.datetime.now() - datetime.timedelta(days=2))[:10]
date30d = str(datetime.datetime.now() - datetime.timedelta(days=31))[:10]

# -------------------Amazon Advertising Report-----------------------------------
# Get Amazon Advertising access token
ACCESS_TOKEN = AccessToken(REFRESH_TOKEN).get_access_token()
amazon_report = Report(ACCESS_TOKEN)

# Create id report for yesterday
id = amazon_report.get_report_id(start_date, end_date)

# Create report link
link = amazon_report.get_link_report()

# Download file
download_report = amazon_report.download_report(link,start_date)

# Read file
read_report = amazon_report.read_report(start_date)

# Add report for yesterday to Google Sheet
google_report = GoogleSheet()
for i in read_report:
    amazon_report.iterate_report(i)
    google_report.add_row(amazon_report.date_report, amazon_report.impressions, amazon_report.clicks,
                          amazon_report.cost, amazon_report.purchases30d)

# Delete file for yesterday
delete_file = amazon_report.delete_file(start_date)


# Update the report for the period today - 30 days to delete invalid clicks
# Delete rows date 30 days ago
google_report.delete_row(date30d)

# Create id report 30d
id_30d = amazon_report.get_report_id(date30d, date30d)

# Create report link 30d
link30d = amazon_report.get_link_report()

# Download file 30d
download_report30d = amazon_report.download_report(link30d, date30d)

# Read file 30d
read_report30d = amazon_report.read_report(date30d)

# Add report for day 30 days ago to Google Sheet
for i in read_report30d:
    amazon_report.iterate_report(i)
    google_report.add_row(amazon_report.date_report, amazon_report.impressions, amazon_report.clicks,
                          amazon_report.cost, amazon_report.purchases30d)

# Delete file for day 30 days ago
delete_file30d = amazon_report.delete_file(date30d)


# -------------------Amazon Seller Report-----------------------------------
google_sheet_seller = GoogleSheet()
ACCESS_TOKEN_SELLER = AccessTokenSeller().get_access_token()

report_seller = ReportSeller(ACCESS_TOKEN_SELLER)

# Create id report Seller Center
report_seller.get_report_id()

# Create document id report Seller Center
doc_id = report_seller.get_link_report_document_id()

# Create link report Seller Center
link = report_seller.get_report_by_document_id()

# Download report Seller Center
report_seller.download_report(link)

# Read report Seller Center
read_report = report_seller.read_report()

# Get traffic parametrs Seller Center
report_seller.iterate_report_by_day(read_report['salesAndTrafficByDate'][0])

# Add traffic parametrs Seller Center to Google Sheet
google_sheet_seller.add_row_seller_traffic(report_seller.date_report,report_seller.units_ordered,
                                           report_seller.total_order_items,	report_seller.units_refunded,
                                           report_seller.ordered_product_sales_amount,
                                           report_seller.shipped_product_sales_amount, report_seller.browser_page_views,
                                           report_seller.browser_sessions,report_seller.mobile_app_page_views,
                                           report_seller.mobile_app_sessions)

# Add asin parametrs Seller Center to Google Sheet
for index in read_report['salesAndTrafficByAsin']:
    report_seller.iterate_report_by_asin(index)
    google_sheet_seller.add_row_seller_asin(report_seller.date_report, report_seller.parent_asin,
                                            report_seller.child_asin, report_seller.total_order_items_asin,
                                            report_seller.units_ordered_asin, report_seller.browser_page_views_asin,
                                            report_seller.browser_sessions_asin)
    time.sleep(1)

# Delete file Seller Center
report_seller.delete_file()


