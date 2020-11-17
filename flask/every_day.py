from sodapy import Socrata
from datetime import datetime

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.sfgov.org", None)



# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.sfgov.org,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")


results = client.get("tpyr-dvnc", id=zipcode_id, limit=2000)