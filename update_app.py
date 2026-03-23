import re, datetime, sys

# Trip route data
route = [
    {'city':'Las Vegas','start':'2026-03-08','end':'2026-03-10','tz':'America/Los_Angeles','tzLabel':'PT'},
    {'city':'Redmond','start':'2026-03-10','end':'2026-03-14','tz':'America/Los_Angeles','tzLabel':'PT'},
    {'city':'Atlanta','start':'2026-03-14','end':'2026-03-22','tz':'America/New_York','tzLabel':'EST'},
    {'city':'Berkeley','start':'2026-03-22','end':'2026-03-25','tz':'America/Los_Angeles','tzLabel':'PT',
     'hotel':'Holiday Inn Express Berkeley','hotelAddr':'1175 University Ave, Berkeley, CA 94702'},
    {'city':'San Francisco','start':'2026-03-25','end':'2026-03-27','tz':'America/Los_Angeles','tzLabel':'PT',
     'hotel':'TBD — near Moscone Center'},
]

today = datetime.date.today()
trip_start = datetime.date(2026, 3, 8)
trip_end = datetime.date(2026, 3, 27)

# Determine current city
current_city = None
day_of_trip = (today - trip_start).days + 1
total_days = (trip_end - trip_start).days

for leg in route:
    s = datetime.date.fromisoformat(leg['start'])
    e = datetime.date.fromisoformat(leg['end'])
    if s <= today < e:
        current_city = leg
        break

if today > trip_end:
    print("Trip completed! No updates needed.")
    sys.exit(0)

if today < trip_start:
    print(f"Trip hasn't started yet. Starts {trip_start}.")
    sys.exit(0)

print(f"Day {day_of_trip} of {total_days} — Currently in {current_city['city'] if current_city else 'transit'}")

# Read the HTML file
with open('Travel_App_Design.html', 'r') as f:
    html = f.read()

# Update the "Edit Trip" current city display
if current_city:
    html = re.sub(
        r'(id="epCurrentCity">)[^<]*(</span>)',
        rf'\g<1>{current_city["city"]}\2',
        html
    )
    html = re.sub(
        r'(id="epCurrentInfo">)[^<]*(</div>)',
        rf'\g<1>Day {day_of_trip} of {total_days} &bull; Mar 8&ndash;27\2',
        html
    )

# Write back
with open('Travel_App_Design.html', 'w') as f:
    f.write(html)

print("App updated successfully.")
