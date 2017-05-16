import requests
import glob
import json
import unicodecsv as csv
from collections import Counter
from hashlib import md5

URL = "https://publicapi.fcc.gov/ecfs/filings"

# As of 10 May 2017 at 9:56 PM EST - good enough    
# API zero indexes offset
MAX_OFFSET = 1596215
STEP = 5000
MAX_STEP = (MAX_OFFSET/STEP)*STEP
START_OFFSET = 1375000

# See API docs: https://www.fcc.gov/ecfs/public-api-docs.html
# raise Exception("Please edit the file and insert a data.gov API key and then comment this out.")
parameters = {
    "api_key": "Fk8mHdyRvWCk3VLlBiElqpPUGCCDWtlbNYVzBBIZ",
    "q": "",
    "proceedings.name": "17-108",
    "sort": "date_received,DESC",
    "limit": STEP,
    "offset": START_OFFSET
}

# Cycle through in chunks of 5000
for offset in range(START_OFFSET, MAX_STEP+1, STEP):
    parameters['offset'] = offset
    
    print parameters        
    resp = requests.get(URL, params=parameters)
    data = resp.json() # Check if it's JSON

    fn = "chunk.fcc-ecfs-17-108-%s-%s.json" % (offset, offset + parameters['limit'])
    with open(fn, 'w') as f: f.write(resp.content)

# Combine
raw_filings = []
for i, fn in enumerate(glob.glob("chunk*.json")):
    print "Loading %s" % fn
    raw_filings.append(json.load(open(fn))['filings'])

# Sanity check
assert sum(len(j['filings']) for j in raw_filings) == MAX_OFFSET

# Assemble all filings into one giant list
filings = reduce(list.__add__, [ record['filings'] for record in raw_filings ])
assert len(filings) == MAX_OFFSET

# Checked for false positives manually
Counter( [hash(f['text_data']) for f in filings])

# These are the spam message, with and without newlines respectively
keep_hashes = [-9181624845762270155, 799472478102808580] 
filings = [ record for record in filings if hash(record['text_data']) in keep_hashes]

# Also remove the couple of filings which have more than one filer
filings = [ record for record in filings if len(record['filers']) == 1 ]

# Load zip codes for geocoding
with open('zipcodes.csv') as f:       
    r = csv.reader(f)   
    zips = list(r)
    zips = {row[0]: (float(row[1]), float(row[2])) for row in list(zips)[1:]}

# Now let's create a giant spreadsheet of these...
export = []
for record in filings:
    keep = {}

    # Address fields
    addr_fields = (u'address_line_1', u'address_line_2', u'city', u'state', u'zip_code', u'zip4')
    for field in addr_fields:
        keep[field] = record['addressentity'].get(field)

    # Get international address if they have it
    if record.get('internationaladdressentity'):
        keep['internationaladdress'] = record.get('internationaladdressentity').get('addresstext')
    else:    
        keep['internationaladdress'] = None
    
    # Name
    keep['filer_name'] = record['filers'][0]['name']
    
    # Text hash
    keep['text_data_hash'] = md5(record['text_data']).hexdigest()
    
    # Date fields
    date_fields = ('date_disseminated', 'date_received', 'date_submission')
    for field in date_fields:
        keep[field] = record.get(field).replace("Z","")
    
    # Other fields
    fields = ('confirmation_number', 'contact_email', 'id_submission')
    for field in fields:
        keep[field] = "_%s" % record.get(field)
    
    # Geocoding
    zipcode = record['addressentity'].get('zip_code')

    if zipcode:
        # Never store zipcodes as integers, folks
        if len(zipcode) == 4:
            zipcode = '0%s' % zipcode
            keep['zip_code'] = zipcode
            
        elif len(zipcode) == 3:
            zipcode = '00%s' % zipcode        
            keep['zip_code'] = zipcode
            
        
        if zipcode in zips:
            lat, lng = zips.get( zipcode )
        else:
            lat, lng = 0,0    
    else:
        lat, lng = 0, 0

    keep['zip_lat'] = lat
    keep['zip_lng'] = lng
    keep['zip_code'] = zipcode
    
    export.append(keep)

header = ['id_submission', 'confirmation_number', 
         'filer_name',
         'text_data_hash',
         'date_disseminated', 'date_received', 'date_submission',
         'contact_email',
         u'address_line_1', u'address_line_2', 
         u'city', u'state', u'zip_code', u'zip4', 
         'internationaladdress', 'zip_lat', 'zip_lng']
         
with open("fcc-filings-17-108--may15.csv", "w+") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(export)
    