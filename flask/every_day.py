import gspread
import time
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('SanFrancisCOVID Master Spreadsheet')
zipcodes = ['94558', '94533', '95620', '95476', '94559', '94954', '94571', '94535', '94503', '94949', '94945', '94512', '94591', '94510', '94592', '94589', '94947', '94590', '94946', '94561', '94525', '94569', '94585', '94103', '94565', '94903', '94520', '94572', '94553', '94547', '94963', '94938', '94502', '94509', '94960', '94513', '94109', '94521', '94930', '94973', '94933', '94598', '94564', '94801', '94519', '94806', '94901', '94531', '94803', '94601', '94523', '94518', '94904', '94115', '94549', '94517', '94805', '94804', '94939', '94964', '94530', '94925', '94596', '94708', '94105', '94941', '94563', '94720', '94707', '94514', '94970', '94706', '94710', '94104', '94595', '94709', '94703', '94704', '94507', '94702', '94965', '94556', '94920', '94118', '94705', '94611', '94618', '94609', '94550', '94608', '94528', '94526', '94506', '94130', '94607', '94123', '94610', '94583', '94602', '94612', '94546', '94133', '94129', '94606', '94111', '94619', '94121', '94102', '94552', '94501', '94108', '94605', '94613', '94117', '94122', '94621', '94114', '94107', '94110', '94588', '94131', '94603', '94116', '94124', '94127', '94577', '94132', '94112', '94134', '94568', '94578', '94015', '94005', '94014', '94579', '94580', '94541', '94566', '94542', '94544', '94044', '94545', '94586', '94080', '94587', '94066', '94128', '94401', '94019', '94030', '94555', '94038', '94010', '94536', '94539', '94402', '94404', '94403', '94538', '94560', '94065', '94063', '94027', '94002', '94070', '95134', '95002', '94062', '94089', '94301', '94025', '94303', '95035', '95140', '94061', '94043', '94304', '94305', '94035', '94306', '94028', '94040', '94022', '94085', '94086', '94024', '94087']

from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("data.sfgov.org", None)
client = Socrata("data.sfgov.org","UUweTGjGMbvHnq8oHSqyc3Bqf")

# ,userame="isabellahochschild@gmail.com", password="Sydney10!"

running_total = {"count":0,"deaths":0,"acs_population":0}

def update_data():
    for zip in zipcodes:
        try:
            new_worksheet = spreadsheet.worksheet(zip)
            if len(new_worksheet.get_all_values()) == 4:
                results = client.get("tpyr-dvnc", id=zip)
                if results:
                    results = results[0]
                    results["count"] = float(results["count"].strip().split(".")[0])
                    if new_worksheet.acell('B1').value:
                        results["delta"] = results["count"] - float(new_worksheet.acell('B2').value.strip())
                    else:
                        results["delta"] = "-"
                    if "deaths" not in results:
                        results["deaths"] = 0.0
                    if "count" not in results:
                        results["count"] = 0.0
                        results["rate"] = 0.0
                    if "last_updated_at" in results:
                        results["datetime"] = datetime.strptime(results["last_updated_at"],"%Y-%m-%dT%H:%M:%S.%f")
                        results["date"] = results["datetime"].isoformat()
                    new_worksheet.append_row([results['date'],results['count'],results['rate'],float(results['rate'])/100,results['deaths'],results["delta"],results['acs_population'],results['last_updated_at'],results['area_type'],results['id']])
                    new_worksheet.update('B2', results['count'])
                    new_worksheet.update('C2', results['rate'])
                    new_worksheet.update('D2', float(results['rate'])/100)
                    new_worksheet.update('E2', results['deaths'])
                    new_worksheet.update('F2', results['delta'])
                    new_worksheet.update('G2', results['acs_population'])
                    new_worksheet.update('H2', results['last_updated_at'])
                    new_worksheet.update('I2', results['area_type'])
                    new_worksheet.update('J2', results['id'])
                    new_worksheet.format('A1:J1', {'textFormat': {'bold': True}})
                    new_worksheet.format('A1:A', {'textFormat': {'bold': True}})
                    running_total["count"] = running_total["count"] + float(results['count'])
                    running_total["deaths"] = running_total["deaths"] + float(results['deaths'])
                    running_total["acs_population"] = running_total["acs_population"] + float(results['acs_population'])
                    time.sleep(50)
            sheet = spreadsheet.worksheet("Master")
            running_total["delta"] = running_total["count"] - float(sheet.acell('B2').value.strip())
            results = running_total
            new_worksheet = sheet
            new_worksheet.update('B2', results['count'])
            new_worksheet.update('C2', results['rate'])
            new_worksheet.update('D2', float(results['rate'])/100)
            new_worksheet.update('E2', results['deaths'])
            new_worksheet.update('F2', results['delta'])
            new_worksheet.update('G2', results['acs_population'])
            new_worksheet.update('H2', results['last_updated_at'])
            new_worksheet.append_row([results['date'],results['count'],results['rate'],float(results['rate'])/100,results['deaths'],results["delta"],results['acs_population'],results['last_updated_at']])
            sheet.format('A1:A', {'textFormat': {'bold': True}})
        except Exception as e:
            print(zip)
            print(e)