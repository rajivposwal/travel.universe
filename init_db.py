"""
init_db.py  -  ASRS Travel
Run this ONCE to create / recreate airports.db (airports + hotels tables)
"""

import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "airports.db")

# ─────────────────────────────────────────────────────────────────
#  Airport Cities
# ─────────────────────────────────────────────────────────────────
CITIES = [
    # (name, state, airport_code, lat, lon, famous, food, best_time)
    ("Visakhapatnam","Andhra Pradesh","VTZ",17.7042,83.2985,"RK Beach & Steel City","Pulihora & Pesarattu","Oct-Mar"),
    ("Vijayawada",   "Andhra Pradesh","VGA",16.5062,80.6480,"Kanaka Durga Temple","Punugulu & Bamboo Chicken","Oct-Feb"),
    ("Tirupati",     "Andhra Pradesh","TIR",13.6288,79.4192,"Tirumala Venkateswara Temple","Tirupati Laddu","Sep-Feb"),
    ("Rajahmundry",  "Andhra Pradesh","RJA",17.1143,81.8181,"Godavari Ghats","Kakinada Kaja","Nov-Feb"),
    ("Kadapa",       "Andhra Pradesh","CDP",14.4673,78.8242,"Pushpagiri Ruins","Rayalaseema Spicy Curry","Oct-Feb"),
    ("Kurnool",      "Andhra Pradesh","KJB",15.8281,78.0373,"Belum Caves","Kurnool Biryani","Oct-Feb"),
    ("Itanagar",     "Arunachal Pradesh","HGI",27.0844,93.6053,"Ita Fort & Ganga Lake","Apong Rice Beer","Oct-Apr"),
    ("Pasighat",     "Arunachal Pradesh","IXT",28.0660,95.3360,"Siang River","Bamboo Shoots Curry","Oct-Mar"),
    ("Guwahati",     "Assam","GAU",26.1445,91.7362,"Kamakhya Temple","Masor Tenga fish curry","Oct-Apr"),
    ("Dibrugarh",    "Assam","DIB",27.4839,95.0169,"Brahmaputra Tea Gardens","Pitha & Til Pitha","Oct-Mar"),
    ("Jorhat",       "Assam","JRH",26.7315,94.1754,"Majuli River Island","Assamese Thali","Oct-Mar"),
    ("Silchar",      "Assam","IXS",24.9129,92.9787,"Barak Valley","Aloo Pitika","Oct-Mar"),
    ("Tezpur",       "Assam","TEZ",26.7084,92.7842,"Agnigarh Hill","Assam Tea","Oct-Mar"),
    ("North Lakhimpur","Assam","IXI",27.2991,94.0979,"Subansiri River","Jolpan breakfast","Oct-Mar"),
    ("Patna",        "Bihar","PAT",25.5941,85.1376,"Golghar & Patna Sahib","Litti Chokha","Oct-Mar"),
    ("Gaya",         "Bihar","GAY",24.7955,84.9994,"Bodh Gaya (UNESCO)","Thekua sweets","Oct-Mar"),
    ("Darbhanga",    "Bihar","DBR",26.1542,85.8918,"Darbhanga Fort","Makhana Kheer","Oct-Mar"),
    ("Raipur",       "Chhattisgarh","RPR",21.2514,81.6296,"Chitrakote Falls","Farra & Chila","Oct-Mar"),
    ("Bilaspur",     "Chhattisgarh","PAB",22.0755,82.1392,"Achanakmar Tiger Reserve","Muthia","Oct-Mar"),
    ("Jagdalpur",    "Chhattisgarh","JGB",19.0748,82.0388,"Bastar Dussehra","Basi with chutney","Oct-Mar"),
    ("Delhi",        "Delhi","DEL",28.6139,77.2090,"Red Fort & Qutub Minar","Paranthas & Butter Chicken","Oct-Mar"),
    ("Goa",          "Goa","GOI",15.3800,73.8314,"Baga & Palolem Beaches","Fish Curry & Bebinca","Nov-Feb"),
    ("Ahmedabad",    "Gujarat","AMD",23.0225,72.5714,"Sabarmati Ashram & Old City","Dhokla & Fafda","Oct-Mar"),
    ("Surat",        "Gujarat","STV",21.1702,72.8311,"Diamond & Textile Hub","Surat Undhiyu","Oct-Mar"),
    ("Vadodara",     "Gujarat","BDQ",22.3072,73.1812,"Laxmi Vilas Palace","Surti Locho","Oct-Mar"),
    ("Rajkot",       "Gujarat","RAJ",22.3039,70.8022,"Watson Museum","Gharis sweets","Oct-Mar"),
    ("Bhavnagar",    "Gujarat","BHU",21.7645,72.1519,"Palitana Jain Temples","Sev Khamani","Oct-Mar"),
    ("Jamnagar",     "Gujarat","JGA",22.4707,70.0577,"Lakhota Lake","Gathiya & Jalebi","Oct-Mar"),
    ("Porbandar",    "Gujarat","PBD",21.6422,69.6093,"Gandhi Birthplace","Rotlo & Gota","Oct-Mar"),
    ("Kandla",       "Gujarat","IXY",23.1129,70.1002,"Kandla Port","Kathiyawadi Thali","Oct-Mar"),
    ("Hisar",        "Haryana","HSS",29.1492,75.7217,"Agroha Dham","Bajra Khichdi","Oct-Mar"),
    ("Shimla",       "Himachal Pradesh","SLV",31.1048,77.1734,"Ridge & Mall Road","Dham & Sidu","Apr-Jun, Sep-Oct"),
    ("Kangra",       "Himachal Pradesh","DHM",32.1024,76.2673,"Kangra Fort & Dharamshala","Chha Gosht","Mar-Jun"),
    ("Kullu",        "Himachal Pradesh","KUU",31.8580,77.1498,"Rohtang Pass & Solang Valley","Siddu & Babru","Apr-Jun"),
    ("Srinagar",     "Jammu & Kashmir","SXR",34.0837,74.7973,"Dal Lake & Mughal Gardens","Rogan Josh & Wazwan","Apr-Oct"),
    ("Jammu",        "Jammu & Kashmir","IXJ",32.7266,74.8570,"Vaishno Devi Shrine","Rajma Chawal","Oct-Mar"),
    ("Ranchi",       "Jharkhand","IXR",23.3441,85.3096,"Hundru Falls","Rugda mushroom curry","Oct-Mar"),
    ("Deoghar",      "Jharkhand","DGH",24.4823,86.6941,"Baidyanath Jyotirlinga","Tilkut","Oct-Mar"),
    ("Bengaluru",    "Karnataka","BLR",12.9716,77.5946,"Lalbagh & Vidhana Soudha","Masala Dosa & Rava Idli","Sep-Mar"),
    ("Mangaluru",    "Karnataka","IXE",12.8703,74.8926,"Panambur Beach","Mangalore Fish Curry","Oct-Feb"),
    ("Mysuru",       "Karnataka","MYQ",12.2958,76.6394,"Mysore Palace","Mysore Pak & Masala Dosa","Oct-Mar"),
    ("Hubballi",     "Karnataka","HBX",15.3647,75.1240,"Nrupatunga Betta","Jolada Rotti","Oct-Mar"),
    ("Belagavi",     "Karnataka","IXG",15.8497,74.5162,"Kittur Fort","Kunda & Dharwad Peda","Oct-Mar"),
    ("Kalaburagi",   "Karnataka","GBI",17.3291,76.8200,"Sharana Basaveshwara Temple","Jolada Rotti","Oct-Mar"),
    ("Thiruvananthapuram","Kerala","TRV",8.5241,76.9366,"Padmanabhaswamy Temple & Kovalam","Appam with Stew","Sep-Mar"),
    ("Kochi",        "Kerala","COK",9.9312,76.2673,"Backwaters & Fort Kochi","Appam & Fish Molee","Sep-Mar"),
    ("Kozhikode",    "Kerala","CCJ",11.2588,75.7804,"Beypore & Kappad Beach","Biryani & Halwa","Sep-Mar"),
    ("Kannur",       "Kerala","CNN",11.8745,75.3704,"Kannur Fort & Beaches","Kerala Sadya","Sep-Mar"),
    ("Bhopal",       "Madhya Pradesh","BHO",23.2599,77.4126,"Bhojpur Temple & Upper Lake","Poha Jalebi","Oct-Mar"),
    ("Indore",       "Madhya Pradesh","IDR",22.7196,75.8577,"Rajwada Palace & Sarafa Market","Poha & Sabudana Khichdi","Oct-Mar"),
    ("Jabalpur",     "Madhya Pradesh","JLR",23.1815,79.9864,"Bhedaghat Marble Rocks","Dal Bafla","Oct-Mar"),
    ("Gwalior",      "Madhya Pradesh","GWL",26.2183,78.1828,"Gwalior Fort","Bedai & Kachori","Oct-Mar"),
    ("Khajuraho",    "Madhya Pradesh","HJR",24.8318,79.9199,"Khajuraho Temples (UNESCO)","Bundelkhandi Thali","Oct-Mar"),
    ("Mumbai",       "Maharashtra","BOM",19.0760,72.8777,"Gateway of India & Marine Drive","Vada Pav & Pav Bhaji","Oct-Feb"),
    ("Pune",         "Maharashtra","PNQ",18.5204,73.8567,"Shaniwar Wada & Osho Ashram","Misal Pav","Oct-Feb"),
    ("Nagpur",       "Maharashtra","NAG",21.1458,79.0882,"Deekshabhoomi & Ramtek Fort","Saoji Mutton Curry","Oct-Feb"),
    ("Nashik",       "Maharashtra","ISK",19.9975,73.7898,"Sula Vineyards & Trimbakeshwar","Misal Pav","Oct-Mar"),
    ("Aurangabad",   "Maharashtra","IXU",19.8762,75.3433,"Ajanta & Ellora Caves (UNESCO)","Naan Qalia","Oct-Mar"),
    ("Shirdi",       "Maharashtra","SAG",19.7547,74.4779,"Sai Baba Temple","Puran Poli","Oct-Mar"),
    ("Kolhapur",     "Maharashtra","KLH",16.7050,74.2433,"Kolhapur Palace","Kolhapuri Chicken & Tambda Rassa","Oct-Mar"),
    ("Solapur",      "Maharashtra","SSE",17.6869,75.9064,"Siddheshwar Temple","Shengdana Chutney","Oct-Mar"),
    ("Imphal",       "Manipur","IMF",24.7650,93.9010,"Kangla Fort & Loktak Lake","Eromba & Singju","Oct-Mar"),
    ("Shillong",     "Meghalaya","SHL",25.5788,91.8933,"Living Root Bridges & Cherrapunji","Jadoh & Tungrymbai","Oct-May"),
    ("Aizawl",       "Mizoram","AJL",23.7271,92.7176,"Blue Mountain & Durtlang Hills","Bai & Sawhchiar","Oct-Mar"),
    ("Dimapur",      "Nagaland","DMU",25.8830,93.7712,"Hornbill Festival & Ruins","Smoked Pork with Bamboo Shoots","Oct-May"),
    ("Bhubaneswar",  "Odisha","BBI",20.2961,85.8245,"Lingaraj Temple & Konark Sun Temple","Dalma & Chhena Poda","Oct-Mar"),
    ("Jharsuguda",   "Odisha","JRG",21.9148,84.0476,"Hirakud Dam","Pitha","Oct-Mar"),
    ("Amritsar",     "Punjab","ATQ",31.6340,74.8723,"Golden Temple","Amritsari Kulcha & Lassi","Oct-Mar"),
    ("Chandigarh",   "Punjab","IXC",30.7333,76.7794,"Rock Garden & Sukhna Lake","Chole Bhature","Sep-Mar"),
    ("Ludhiana",     "Punjab","LUH",30.9010,75.8573,"Punjab Agricultural University","Tandoori Chicken","Oct-Mar"),
    ("Jaipur",       "Rajasthan","JAI",26.9124,75.7873,"Amber Fort & City Palace","Dal Bati Churma","Oct-Mar"),
    ("Jodhpur",      "Rajasthan","JDH",26.2389,73.0243,"Mehrangarh Fort & Blue City","Mirchi Vada & Mawa Kachori","Oct-Mar"),
    ("Udaipur",      "Rajasthan","UDR",24.5854,73.7125,"City Palace & Pichola Lake","Dal Baati","Oct-Mar"),
    ("Jaisalmer",    "Rajasthan","JSA",26.9157,70.9083,"Jaisalmer Fort & Sam Sand Dunes","Ker Sangri","Oct-Mar"),
    ("Bikaner",      "Rajasthan","BKB",28.0229,73.3119,"Junagarh Fort","Bikaneri Bhujia","Oct-Mar"),
    ("Kota",         "Rajasthan","KTU",25.1802,75.8330,"Chambal River & Kota Barrage","Kota Kachori","Oct-Mar"),
    ("Gangtok",      "Sikkim","GTK",27.3289,88.6065,"Rumtek Monastery & Nathula Pass","Thukpa & Momos","Mar-May, Sep-Nov"),
    ("Chennai",      "Tamil Nadu","MAA",13.0827,80.2707,"Marina Beach & Kapaleeshwarar","Idli Sambar & Filter Coffee","Nov-Feb"),
    ("Coimbatore",   "Tamil Nadu","CJB",11.0168,76.9558,"Anamalai Tiger Reserve","Coimbatore Idiyappam","Oct-Mar"),
    ("Madurai",      "Tamil Nadu","IXM",9.9252,78.1198,"Meenakshi Amman Temple","Jigarthanda & Parotta","Oct-Mar"),
    ("Trichy",       "Tamil Nadu","TRZ",10.7905,78.7047,"Rockfort Temple","Kavuni Arisi","Oct-Mar"),
    ("Salem",        "Tamil Nadu","SXV",11.6675,78.1460,"Yercaud Hills","Salem Biryani","Oct-Mar"),
    ("Tuticorin",    "Tamil Nadu","TCR",8.7642,78.0865,"Coral Islands","Seafood & Kozhukattai","Oct-Mar"),
    ("Hyderabad",    "Telangana","HYD",17.3850,78.4867,"Charminar & Golconda Fort","Biryani & Haleem","Oct-Mar"),
    ("Agartala",     "Tripura","IXA",23.8315,91.2868,"Ujjayanta Palace","Mui Borok","Oct-Mar"),
    ("Lucknow",      "Uttar Pradesh","LKO",26.8467,80.9462,"Bara Imambara & Rumi Darwaza","Galouti Kebab & Biryani","Oct-Mar"),
    ("Varanasi",     "Uttar Pradesh","VNS",25.3176,82.9739,"Ghats on Ganga & Kashi Vishwanath","Banarasi Paan & Kachori Sabzi","Oct-Mar"),
    ("Prayagraj",    "Uttar Pradesh","IXD",25.4358,81.8463,"Sangam & Kumbh Mela","Aloo Puri","Oct-Mar"),
    ("Kanpur",       "Uttar Pradesh","KNU",26.4499,80.3319,"Green Park Stadium","Thaggu Ke Laddu","Oct-Mar"),
    ("Gorakhpur",    "Uttar Pradesh","GOP",26.7606,83.3732,"Gorakhnath Temple","Gorakhpur Litti","Oct-Mar"),
    ("Bareilly",     "Uttar Pradesh","BEK",28.3670,79.4304,"Alakhnath Temple","Bareilly Bhaat","Oct-Mar"),
    ("Dehradun",     "Uttarakhand","DED",30.3165,78.0322,"Robber's Cave & Mussoorie","Aloo Ke Gutke","Mar-Jun"),
    ("Pantnagar",    "Uttarakhand","PGH",29.0334,79.4734,"Corbett National Park","Bal Mithai","Oct-Jun"),
    ("Kolkata",      "West Bengal","CCU",22.5726,88.3639,"Victoria Memorial & Howrah Bridge","Rosogolla & Kati Roll","Oct-Mar"),
    ("Bagdogra",     "West Bengal","IXB",26.6812,88.3285,"Darjeeling & Gangtok Gateway","Momos & Darjeeling Tea","Mar-May, Sep-Nov"),
]

# ─────────────────────────────────────────────────────────────────
#  Curated Budget Hotels  (real hotels, manually verified)
#  img: high-quality Unsplash photo IDs matching property aesthetic
# ─────────────────────────────────────────────────────────────────
HOTELS = [
    # id, name, city, state, area, price_min, price_max,
    # stars, rating, reviews, category, tag,
    # amenities (comma-sep), highlights (comma-sep),
    # img_unsplash_id, chain, description

    # ── Delhi & North India ───────────────────────────────
    (1,"Hotel Ajanta","Delhi","Delhi","Paharganj",1800,3500,
     3,4.2,2840,"Budget","Great Value",
     "Free WiFi,AC,Hot Water,TV,Room Service",
     "Free airport pickup available,Near New Delhi Railway Station,Street food hub nearby",
     "1450389481","Independent",
     "A well-loved Paharganj favourite with consistently great reviews. Free airport pickup makes it the ultimate hassle-free arrival option for budget travellers."),

    (2,"Hotel Tara Palace","Delhi","Delhi","Chandni Chowk",1500,2800,
     2,4.0,1650,"Budget","Heritage Area",
     "Free WiFi,AC,TV,Daily Housekeeping",
     "Walking distance to Chandni Chowk market,Near Red Fort & Jama Masjid,Excellent local food access",
     "1529679813","Independent",
     "An affordable haven steps away from historic Old Delhi. Perfect base for exploring Red Fort, Chandni Chowk, and Jama Masjid without spending a fortune."),

    (3,"Hotel City Star","Delhi","Delhi","Paharganj",1200,2500,
     2,3.9,980,"Budget","Central Location",
     "Free WiFi,AC,TV,24h Front Desk",
     "Central Paharganj location,Easy metro access,Close to Connaught Place",
     "1466335316","Independent",
     "Centrally positioned in the heart of Paharganj, this reliable budget option keeps you connected to Delhi's transit network and dozens of affordable eateries."),

    (4,"Hotel Seven Inn","Delhi","Delhi","Karol Bagh",2200,4000,
     3,4.1,720,"Budget","Good Amenities",
     "Free WiFi,AC,TV,Parking,Breakfast Available",
     "Well-connected by metro,Near Karol Bagh market,Multiple dining options",
     "1528360619","Independent",
     "A clean and comfortable budget stay in Karol Bagh. Check recent reviews for the latest updates on amenities. Great value for money in the Indian capital."),

    # ── Rajasthan ─────────────────────────────────────────
    (5,"Shahi Palace Hotel","Jaisalmer","Rajasthan","Fort Area",2500,5500,
     3,4.5,1820,"Boutique","Fort District",
     "Free WiFi,Rooftop Restaurant,AC,Desert View,Room Service",
     "Inside the historic Jaisalmer Fort,Rooftop sunset views,Authentic Rajasthani decor",
     "1499658961","Independent",
     "A jewel inside Jaisalmer's legendary golden fort. Rooftop dining with panoramic desert and fort views make this one of the most atmospheric budget stays in all of Rajasthan."),

    (6,"Hotel Oasis Haveli","Jaisalmer","Rajasthan","Fort Periphery",1800,4000,
     3,4.3,1120,"Boutique","Haveli Style",
     "Free WiFi,Rooftop Terrace,AC,Heritage Decor,Tour Desk",
     "Cozy haveli-style architecture,Traditional blue pottery decor,Close to sunset point",
     "1542621168","Independent",
     "Experience a classic Rajasthani haveli at a budget price. Intricately carved stone jharokhas, a peaceful courtyard, and warm hospitality make this a travellers' favourite."),

    # ── South India ───────────────────────────────────────
    (7,"Roopa Elite","Mysuru","Karnataka","City Centre",1800,3800,
     3,4.4,3100,"Value","City Centre",
     "Free WiFi,AC,TV,Hot Water,Parking,Restaurant",
     "Walking distance to Mysore Palace,Lots of diner choice,Great for solo & family travelers",
     "1455053288","Independent",
     "One of Mysore's most positively reviewed budget hotels. Ideally positioned near the famous Mysore Palace for sightseeing and within walking reach of the best local restaurants."),

    (8,"Hotel Udechee Huts","Dharamshala","Himachal Pradesh","McLeod Ganj",1500,3500,
     2,4.2,860,"Boutique","Mountain View",
     "Free WiFi,Mountain Views,Hot Water,Valley Terrace,Homely Atmosphere",
     "Panoramic Himalayan views,Bohemian McLeod Ganj atmosphere,Nearby Dalai Lama Temple",
     "1485105977","Independent",
     "A charming boutique stay tucked into the hills of McLeod Ganj. Wake up to stunning Himalayan views, sip chai on a terrace overlooking the valley, and explore the vibrant Tibetan culture below."),

    (9,"IKON by Annapoorna","Coimbatore","Tamil Nadu","RS Puram",2500,4500,
     3,4.3,1450,"Value","Modern Design",
     "Free WiFi,AC,Smart TV,Rooftop Pool,Restaurant,Gym",
     "Stylish modern interiors,Rooftop pool for guests,Famous Annapoorna restaurant chain",
     "1519088490","Chain",
     "Stylish and affordable, IKON brings a premium feel to Coimbatore's budget hotel scene. The affiliation with the legendary Annapoorna restaurant guarantees exceptional dining on-site."),

    (10,"Holiday Inn Express Pune","Pune","Maharashtra","Hinjewadi",6500,9500,
     4,4.4,2200,"Value","IHG Brand",
     "Free WiFi,AC,Smart TV,Gym,Business Centre,Breakfast Included",
     "IHG loyalty points eligible,Near Rajiv Gandhi IT Park,Shuttle to city centre",
     "1582719123","IHG",
     "An IHG brand property often available under Rs 10,000 during off-peak periods. Global quality standards, breakfast included, and proximity to Pune's IT corridor make it a favourite for business travellers."),

    # ── Central & Other Cities ────────────────────────────
    (11,"Hotel The Grand Indore","Indore","Madhya Pradesh","Vijay Nagar",3000,6000,
     3,4.5,2650,"Value","Highly Rated",
     "Free WiFi,AC,TV,Restaurant,Bar,Parking,Room Service",
     "Consistently high ratings,Great Indore street food nearby,Near Sarafa Night Market",
     "1536940076","Independent",
     "Indore's most celebrated mid-range hotel, The Grand consistently tops guest satisfaction charts. Its location is a gateway to the world-famous Sarafa night food market."),

    (12,"Hotel Yash Residency","Chhanera","Madhya Pradesh","City Centre",1000,2200,
     2,3.8,410,"Budget","Budget Essential",
     "Free WiFi,AC,TV,Hot Water",
     "Very economical option,Clean and basic amenities,Good connectivity",
     "1556760027","Independent",
     "An extremely affordable choice for travellers passing through Madhya Pradesh. Clean, functional, and easy on the wallet — perfect for one-night stopovers."),

    (13,"Hotel Yatri Nivas","Hyderabad","Telangana","Secunderabad",1800,3500,
     3,4.0,1180,"Budget","City Access",
     "Free WiFi,AC,TV,Hot Water,24h Front Desk,Restaurant",
     "Close to Secunderabad Railway Station,Near Hussain Sagar Lake,Easy access to Charminar",
     "1587300817","Independent",
     "A reliable performer in Hyderabad's budget segment, Yatri Nivas provides solid value near the twin cities' junction point. The biryani places within walking distance are legendary."),

    (14,"Hotel Vishnu Residency","Visakhapatnam","Andhra Pradesh","Beach Road",1200,2500,
     2,3.7,520,"Budget","Coastal Access",
     "Free WiFi,AC,TV,Hot Water",
     "Close to RK Beach,Very competitively priced,Good for port city visits",
     "1549740102","Independent",
     "A very low-cost option near the beautiful Visakhapatnam coastline. We recommend reviewing recent guest feedback before booking to confirm current facilities."),

    # ── Premium Budget Chains ─────────────────────────────
    (15,"Ginger Hotels","Delhi","Delhi","Multiple Locations",2500,5000,
     3,4.2,8500,"Chain","Pan-India Chain",
     "Free WiFi,AC,TV,Gym,Breakfast Available,Parking",
     "Reliable quality across all properties,Loyalty rewards program,50+ properties across India",
     "1542621040","Ginger (IHCL)",
     "India's most trusted budget hotel chain by IHCL (Tata group). Reliable, consistent, and available in 50+ cities. Perfect for frequent business and leisure travellers wanting guaranteed quality."),

    (16,"FabHotel Prime","Mumbai","Maharashtra","Andheri",2800,5500,
     3,4.1,6200,"Chain","Budget Brand",
     "Free WiFi,AC,TV,Hot Water,24h Front Desk",
     "Standardised clean properties,Good urban locations,Easy online booking",
     "1582719123","FabHotels",
     "FabHotels offers standardised, clean, and comfortable stays in Mumbai's Andheri belt — perfect for anyone visiting the business district, film studios, or connecting via the international airport."),

    (17,"OYO Townhouse","Bangalore","Karnataka","Koramangala",2000,4500,
     3,4.0,4800,"Chain","Modern Stay",
     "Free WiFi,AC,Smart TV,Hot Water,Work Desk",
     "Modern interiors,Good for business travelers,Koramangala dining & nightlife",
     "1536940076","OYO",
     "OYO Townhouse in Koramangala combines modern design with affordability. Bangalore's hippest neighbourhood is right outside your door, with hundreds of cafes, pubs, and coworking spaces."),

    (18,"Treebo Trend Hotel","Jaipur","Rajasthan","C-Scheme",2200,4000,
     3,4.2,1340,"Chain","Verified Quality",
     "Free WiFi,AC,TV,Hot Water,Breakfast Included",
     "Breakfast included,Standardised clean rooms,Near Jaipur city centre",
     "1499658961","Treebo",
     "Treebo brings verified quality standards to Jaipur's budget market. Breakfast included, consistent cleanliness, and proximity to the Pink City's sights make it an outstanding value proposition."),
]


# ─────────────────────────────────────────────────────────────────
#  Init Function
# ─────────────────────────────────────────────────────────────────
def init():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    # ── Airports table ──────────────────────────────────────────
    cur.execute("DROP TABLE IF EXISTS airports")
    cur.execute("""
        CREATE TABLE airports (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            city         TEXT NOT NULL,
            city_lower   TEXT NOT NULL UNIQUE,
            state        TEXT NOT NULL,
            iata_code    TEXT NOT NULL,
            latitude     REAL NOT NULL,
            longitude    REAL NOT NULL,
            famous       TEXT,
            local_food   TEXT,
            best_time    TEXT
        )
    """)
    for row in CITIES:
        city, state, iata, lat, lon, famous, food, time = row
        cur.execute("""
            INSERT INTO airports
            (city, city_lower, state, iata_code, latitude, longitude, famous, local_food, best_time)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (city, city.lower(), state, iata, lat, lon, famous, food, time))

    # ── Hotels table ────────────────────────────────────────────
    cur.execute("DROP TABLE IF EXISTS hotels")
    cur.execute("""
        CREATE TABLE hotels (
            id              INTEGER PRIMARY KEY,
            name            TEXT NOT NULL,
            city            TEXT NOT NULL,
            state           TEXT NOT NULL,
            area            TEXT,
            price_min       INTEGER NOT NULL,
            price_max       INTEGER NOT NULL,
            stars           INTEGER DEFAULT 3,
            rating          REAL DEFAULT 4.0,
            reviews         INTEGER DEFAULT 100,
            category        TEXT DEFAULT 'Budget',
            tag             TEXT,
            amenities       TEXT,
            highlights      TEXT,
            img_unsplash_id TEXT,
            chain           TEXT,
            description     TEXT
        )
    """)
    for h in HOTELS:
        cur.execute("""
            INSERT INTO hotels
            (id,name,city,state,area,price_min,price_max,stars,rating,reviews,
             category,tag,amenities,highlights,img_unsplash_id,chain,description)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, h)

    # ── Users table (IF NOT EXISTS — preserves existing accounts) ──
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT NOT NULL UNIQUE,
            email         TEXT NOT NULL UNIQUE,
            password_hash TEXT,
            avatar_color  TEXT DEFAULT '#ff9f1c',
            auth_provider TEXT DEFAULT 'email',
            profile_photo TEXT,
            phone         TEXT,
            created_at    TEXT DEFAULT (datetime('now'))
        )
    """)
    # migrate existing users table with new columns if needed
    try: cur.execute("ALTER TABLE users ADD COLUMN profile_photo TEXT")
    except: pass
    try: cur.execute("ALTER TABLE users ADD COLUMN phone TEXT")
    except: pass

    # ── Bookings table (IF NOT EXISTS) ──────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_ref  TEXT NOT NULL UNIQUE,
            user_id      INTEGER NOT NULL,
            service_type TEXT NOT NULL,
            item_name    TEXT,
            from_city    TEXT,
            to_city      TEXT,
            travel_date  TEXT,
            seat_room    TEXT,
            passengers   INTEGER DEFAULT 1,
            class_type   TEXT,
            price        INTEGER DEFAULT 0,
            pay_method   TEXT DEFAULT 'UPI',
            status       TEXT DEFAULT 'Confirmed',
            booked_at    TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ── Trains table ─────────────────────────────────────────────
    cur.execute("DROP TABLE IF EXISTS trains")
    cur.execute("""
        CREATE TABLE trains (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            category    TEXT NOT NULL,
            speed_kmph  INTEGER DEFAULT 100,
            description TEXT
        )
    """)

    TRAINS_DATA = [
        # ── Category 1: Premium & High-Speed ─────────────────────
        ("Vande Bharat Express",   "Premium",       160,
         "India's fastest semi-high-speed train with on-board Wi-Fi, automatic doors and push-pull technology."),
        ("Rajdhani Express",       "Premium",       130,
         "Flagship express connecting state capitals to New Delhi with fully air-conditioned coaches and meals included."),
        ("Shatabdi Express",       "Premium",       150,
         "Premium day-time intercity express known for punctuality, AC chair-car comfort and hot catering."),
        ("Duronto Express",        "Premium",       130,
         "Non-stop long-distance express directly linking major city pairs without intermediate halts."),
        ("Gatimaan Express",       "Premium",       160,
         "India's first semi-high-speed train, running between Delhi and Agra at 160 km/h."),
        ("Tejas Express",          "Premium",       130,
         "India's first corporate-run train with automatic doors, LED lighting, WiFi and on-board entertainment."),

        # ── Category 2: Long-Distance Express ────────────────────
        ("Superfast Express",      "Long-Distance", 110,
         "Priority express trains covering long distances faster than ordinary mail trains with limited stops."),
        ("Mail Express",           "Long-Distance",  90,
         "Historic category of long-distance trains that originally carried mail along with passengers."),
        ("Express",                "Long-Distance",  75,
         "Standard long-distance trains connecting cities and towns with moderate stops en route."),
        ("Sampark Kranti Express", "Long-Distance", 110,
         "Connects state capitals and major cities to New Delhi, passing through multiple important junctions."),
        ("Humsafar Express",       "Long-Distance", 110,
         "Fully air-conditioned third-class (3A) trains with bio-toilets, GPS tracking and CCTV."),
        ("Garib Rath Express",     "Long-Distance", 110,
         "Air-conditioned economy trains designed to provide affordable AC travel to common passengers."),
        ("Antyodaya Express",      "Long-Distance",  80,
         "High-capacity unreserved superfast trains catering to daily-wage workers and weaker sections."),
        ("Yuva Express",           "Long-Distance", 100,
         "Low-cost trains with reserved seats targeting youth and budget long-distance travellers."),

        # ── Category 3: Intercity & Short-Distance ───────────────
        ("Intercity Express",      "Intercity",      80,
         "Connects nearby cities and towns within a state, typically completing journeys within a single day."),
        ("Jan Shatabdi Express",   "Intercity",     100,
         "Economy version of Shatabdi, offering day-time intercity connectivity at affordable fares."),
        ("Jan Sadharan Express",   "Intercity",      75,
         "General un-reserved class trains providing low-cost transport for everyday commuters."),
        ("MEMU Express",           "Intercity",      80,
         "Mainline Electric Multiple Unit trains — electric-powered suburban and intercity services."),
        ("DEMU Express",           "Intercity",      70,
         "Diesel Electric Multiple Unit trains operating on non-electrified rural and semi-urban routes."),
        ("Passenger Express",      "Intercity",      50,
         "Slow passenger trains stopping at every station — the lifeline for rural and remote communities."),
    ]

    for t in TRAINS_DATA:
        cur.execute(
            "INSERT INTO trains (name, category, speed_kmph, description) VALUES (?,?,?,?)", t
        )

    # ── Food Items table ─────────────────────────────────────────
    cur.execute("DROP TABLE IF EXISTS food_items")
    cur.execute("""
        CREATE TABLE food_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            category    TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            type        TEXT NOT NULL DEFAULT 'Veg',
            price_min   INTEGER NOT NULL,
            price_max   INTEGER NOT NULL,
            emoji       TEXT DEFAULT '🍽️',
            description TEXT
        )
    """)

    # (name, category, subcategory, type, price_min, price_max, emoji, description)
    FOOD_ITEMS = [
        # ── Continental Pastas & Mains ─────────────────────────────────────
        ("Veg Alfredo Pasta",             "Continental","Pastas & Mains","Veg",    405, 405, "🍝","Creamy Alfredo sauce with fresh vegetables and penne."),
        ("Veg Arrabiata Pasta",           "Continental","Pastas & Mains","Veg",    455, 455, "🍝","Spicy tomato Arrabiata sauce tossed with penne."),
        ("Veg Pink Sauce Pasta",          "Continental","Pastas & Mains","Veg",    455, 455, "🍝","Velvety pink sauce blending cream and tomato with veggies."),
        ("Spaghetti Aglio Olio (Veg)",    "Continental","Pastas & Mains","Veg",    475, 475, "🍝","Classic Italian olive oil and garlic spaghetti."),
        ("Penne Arrabbiata",              "Continental","Pastas & Mains","Veg",    229, 229, "🍝","Bold spicy tomato sauce with penne pasta."),
        ("Creamy Mushroom Pasta",         "Continental","Pastas & Mains","Veg",    239, 239, "🍝","Sautéed mushrooms in rich creamy white sauce."),
        ("Non-Veg Alfredo",               "Continental","Pastas & Mains","Non-Veg",475, 475, "🍝","Creamy Alfredo pasta loaded with grilled chicken."),
        ("Non-Veg Arrabiata",             "Continental","Pastas & Mains","Non-Veg",475, 475, "🍝","Spicy Arrabiata pasta with succulent chicken pieces."),
        ("Non-Veg Pink Sauce Pasta",      "Continental","Pastas & Mains","Non-Veg",475, 475, "🍝","Pink sauce pasta with chicken and herbs."),
        ("Spaghetti Aglio Olio (Chicken)","Continental","Pastas & Mains","Non-Veg",525, 525, "🍝","Aglio Olio with tender grilled chicken strips."),
        ("Spaghetti Aglio Olio (Prawns)", "Continental","Pastas & Mains","Non-Veg",575, 575, "🍝","Classic Aglio Olio elevated with juicy prawns."),
        ("Cheesy Chicken Pasta",          "Continental","Pastas & Mains","Non-Veg",269, 269, "🍝","Loaded cheesy pasta with chicken chunks."),
        ("Moroccan Spaghetti Meatballs",  "Continental","Pastas & Mains","Non-Veg",269, 269, "🍝","Morocco-spiced meatballs in tomato spaghetti."),
        ("Peri-Peri Chicken Steak Bowl",  "Continental","Pastas & Mains","Non-Veg",269, 269, "🍗","Grilled chicken with fiery peri-peri sauce over rice."),
        ("Signature Piri-Piri Steak",     "Continental","Pastas & Mains","Non-Veg",399, 399, "🥩","Char-grilled Piri-Piri spiced signature steak."),
        # Expanded Continental Mains
        ("Pesto Pasta (Veg)",             "Continental","Pastas & Mains","Veg",    445, 445, "🍝","Fresh basil pesto tossed with farfalle and cherry tomatoes."),
        ("Herb Pasta (Veg)",              "Continental","Pastas & Mains","Veg",    395, 395, "🍝","Light Italian herb and olive oil pasta."),
        ("Arrabiata Prawns Pasta",        "Continental","Pastas & Mains","Non-Veg",549, 549, "🍝","Spicy arrabiata with sautéed king prawns."),
        ("Pesto Chicken Pasta",           "Continental","Pastas & Mains","Non-Veg",499, 499, "🍝","Grilled chicken in fresh basil pesto."),
        ("Grilled Chicken Steak",         "Continental","Pastas & Mains","Non-Veg",449, 449, "🥩","Herb-marinated chicken breast, char-grilled to perfection."),
        ("Grilled Vegetable Steak",       "Continental","Pastas & Mains","Veg",    349, 349, "🥩","Platter of seasoned grilled seasonal vegetables."),
        ("Fish & Chips",                  "Continental","Pastas & Mains","Non-Veg",399, 399, "🐟","Beer-battered crispy fish fillet with golden fries."),

        # ── Continental Snacks — Veg ───────────────────────────────────────
        ("French Fries",                  "Continental","Snacks","Veg",    110, 139, "🍟","Crispy golden fries tossed in seasoning."),
        ("Fried Potato Wedges",           "Continental","Snacks","Veg",    189, 189, "🍟","Thick potato wedges seasoned and fried."),
        ("Garlic Bread with Cheese",      "Continental","Snacks","Veg",    189, 189, "🧀","Toasted garlic bread smothered in molten cheese."),
        ("Cheese French Fries",           "Continental","Snacks","Veg",    189, 189, "🍟","Fries topped with luscious cheese sauce."),
        ("Sweet Corn Cheese Nuggets",     "Continental","Snacks","Veg",    189, 189, "🌽","Crunchy nuggets packed with sweet corn and cheese."),
        ("Jalapeño Cheese Poppers",       "Continental","Snacks","Veg",    209, 209, "🌶️","Crispy jalapeño shells filled with cream cheese."),
        ("Mushroom Duplex",               "Continental","Snacks","Veg",    229, 229, "🍄","Double-stacked grilled mushroom sandwich."),
        ("Stuffed Garlic Bread",          "Continental","Snacks","Veg",    239, 239, "🥖","Garlic bread stuffed with cheese and herbs."),
        # Expanded Veg Snacks
        ("Onion Rings",                   "Continental","Snacks","Veg",    159, 159, "🧅","Beer-battered crispy onion rings."),
        ("Mozzarella Sticks",             "Continental","Snacks","Veg",    219, 219, "🧀","Golden fried mozzarella with marinara dip."),
        ("Loaded Nachos",                 "Continental","Snacks","Veg",    249, 249, "🌮","Nachos loaded with salsa, guacamole and cheese."),
        ("Bruschetta (Veg)",              "Continental","Snacks","Veg",    189, 189, "🍅","Toasted bread with olive oil, tomato and basil."),
        ("Corn & Cheese Toast",           "Continental","Snacks","Veg",    179, 179, "🌽","Cheesy corn on crispy toast."),

        # ── Continental Snacks — Non-Veg ──────────────────────────────────
        ("Chicken Stuffed Garlic Bread",  "Continental","Snacks","Non-Veg",239, 239, "🍗","Garlic bread stuffed with spiced chicken and cheese."),
        ("Chicken Bruschettas",           "Continental","Snacks","Non-Veg",239, 239, "🍗","Toasted bread with chicken, tomato and herbs."),
        ("Chicken Cheese Jalapeño Poppers","Continental","Snacks","Non-Veg",239, 239, "🌶️","Spicy poppers filled with chicken and cheese."),
        ("Chicken Nuggets",               "Continental","Snacks","Non-Veg",239, 239, "🍗","Crispy fried chicken nuggets with dipping sauce."),
        # Expanded Non-Veg Snacks
        ("BBQ Chicken Wings",             "Continental","Snacks","Non-Veg",299, 299, "🍗","Smoky BBQ glazed wings, 6 pieces."),
        ("Fish Fingers",                  "Continental","Snacks","Non-Veg",259, 259, "🐟","Golden crumbed fish fingers with tartar sauce."),
        ("Prawn Tempura",                 "Continental","Snacks","Non-Veg",329, 329, "🍤","Light crispy Japanese-style prawn tempura."),

        # ── Indian Snacks — Veg ───────────────────────────────────────────
        ("Masala Papad",                  "Indian","Snacks Veg",  "Veg",    50,  50,  "🫓","Roasted papad topped with spiced onion-tomato mix."),
        ("Peanut Masala",                 "Indian","Snacks Veg",  "Veg",    105, 105, "🥜","Crunchy peanuts tossed with spices and lemon."),
        ("Vegetable Pakora (8 pcs)",      "Indian","Snacks Veg",  "Veg",    120, 120, "🧅","Crispy mix-vegetable fritters served with chutney."),
        ("Paneer Pakora (8 pcs)",         "Indian","Snacks Veg",  "Veg",    220, 220, "🧀","Golden fried paneer fritters with mint chutney."),
        ("Paneer Tikka (6 pcs)",          "Indian","Snacks Veg",  "Veg",    240, 240, "🔥","Tandoor-charred paneer cubes with bell peppers."),
        # Expanded Veg Indian Snacks
        ("Samosa (2 pcs)",                "Indian","Snacks Veg",  "Veg",    50,  50,  "🥟","Crispy pastry stuffed with spiced potato and peas."),
        ("Dhokla",                        "Indian","Snacks Veg",  "Veg",    89,  89,  "🟡","Steamed Gujarati chickpea cake, soft and tangy."),
        ("Aloo Tikki (4 pcs)",            "Indian","Snacks Veg",  "Veg",    99,  99,  "🥔","Pan-fried spiced potato patties."),
        ("Dahi Puri (6 pcs)",             "Indian","Snacks Veg",  "Veg",    119, 119, "💫","Crispy puris filled with potato, yogurt and chutneys."),
        ("Pav Bhaji",                     "Indian","Snacks Veg",  "Veg",    149, 149, "🍞","Mumbai-style spiced vegetable mash with buttered pav."),
        ("Corn Chaat",                    "Indian","Snacks Veg",  "Veg",    99,  99,  "🌽","Sweet corn tossed with spices, lemon and coriander."),
        ("Masala Corn",                   "Indian","Snacks Veg",  "Veg",    89,  89,  "🌽","Steamed corn cobs with butter and masala."),
        ("Veg Cutlet (4 pcs)",            "Indian","Snacks Veg",  "Veg",    129, 129, "🥕","Mixed vegetable cutlets, pan-fried golden."),
        ("Kachori (2 pcs)",               "Indian","Snacks Veg",  "Veg",    60,  60,  "🥟","Flaky pastry stuffed with spiced lentil filling."),

        # ── Indian Starters — Non-Veg ─────────────────────────────────────
        ("Egg Pakora (8 pcs)",            "Indian","Starters Non-Veg","Non-Veg",175, 175, "🥚","Boiled egg fritters in spiced besan batter."),
        ("Chicken Pakora (8 pcs)",        "Indian","Starters Non-Veg","Non-Veg",220, 220, "🍗","Juicy chicken pieces in crispy besan coating."),
        ("Chicken Tikka (6 pcs)",         "Indian","Starters Non-Veg","Non-Veg",275, 275, "🔥","Marinated chicken pieces char-grilled in tandoor."),
        ("Chicken Reshmi Kebab (6 pcs)",  "Indian","Starters Non-Veg","Non-Veg",290, 290, "🍢","Silky smooth minced chicken kebabs."),
        ("Tandoori Chicken (Half)",       "Indian","Starters Non-Veg","Non-Veg",290, 290, "🔥","Classic tandoori-roasted half chicken with mint chutney."),
        ("Fish Tikka (6 pcs)",            "Indian","Starters Non-Veg","Non-Veg",310, 310, "🐟","Marinated fish cubes charred in the tandoor."),
        # Expanded Non-Veg Indian Starters
        ("Seekh Kebab (6 pcs)",           "Indian","Starters Non-Veg","Non-Veg",299, 299, "🍢","Spiced minced lamb skewers, grilled in tandoor."),
        ("Tangri Kebab (4 pcs)",          "Indian","Starters Non-Veg","Non-Veg",299, 299, "🍗","Drumstick kebab marinated overnight and tandoor-roasted."),
        ("Prawn Tikka (8 pcs)",           "Indian","Starters Non-Veg","Non-Veg",349, 349, "🍤","Juicy tiger prawns marinated and grilled."),
        ("Egg Bhurji",                    "Indian","Starters Non-Veg","Non-Veg",119, 119, "🥚","Spiced scrambled eggs tempered with onion and tomato."),
        ("Chicken 65",                    "Indian","Starters Non-Veg","Non-Veg",259, 259, "🌶️","South Indian deep-fried spicy chicken."),
        ("Mutton Seekh Kebab (6 pcs)",    "Indian","Starters Non-Veg","Non-Veg",349, 349, "🍢","Minced mutton kebabs with aromatic spices."),

        # ── Indian Curries — Veg ──────────────────────────────────────────
        ("Dal Makhani",                   "Indian","Curries Veg",  "Veg",    190, 190, "🫘","Slow-cooked black lentils in rich buttery tomato gravy."),
        ("Paneer Butter Masala",          "Indian","Curries Veg",  "Veg",    190, 190, "🧀","Paneer cubes in velvety tomato-cream gravy."),
        ("Matar Paneer",                  "Indian","Curries Veg",  "Veg",    215, 215, "🧀","Cottage cheese and green peas in spiced tomato gravy."),
        ("Palak Paneer",                  "Indian","Curries Veg",  "Veg",    215, 215, "🥬","Paneer cubes in smooth spinach and spice sauce."),
        # Expanded Veg Curries
        ("Shahi Paneer",                  "Indian","Curries Veg",  "Veg",    235, 235, "👑","Royal paneer in rich almond-cashew cream gravy."),
        ("Kadai Paneer",                  "Indian","Curries Veg",  "Veg",    225, 225, "🧀","Paneer with bell peppers in tangy kadai masala."),
        ("Dal Tadka",                     "Indian","Curries Veg",  "Veg",    165, 165, "🫘","Yellow lentils tempered with cumin and ghee."),
        ("Chana Masala",                  "Indian","Curries Veg",  "Veg",    175, 175, "🫘","Punjabi spiced chickpea curry."),
        ("Aloo Matar",                    "Indian","Curries Veg",  "Veg",    175, 175, "🥔","Potato and peas in North Indian tomato gravy."),
        ("Rajma Masala",                  "Indian","Curries Veg",  "Veg",    185, 185, "🫘","Kidney beans slow-cooked in robust masala."),
        ("Baingan Bharta",                "Indian","Curries Veg",  "Veg",    185, 185, "🍆","Flame-roasted mashed eggplant with spices."),
        ("Mix Vegetable Curry",           "Indian","Curries Veg",  "Veg",    185, 185, "🥕","Seasonal vegetables in North Indian masala gravy."),
        ("Navratan Korma",                "Indian","Curries Veg",  "Veg",    225, 225, "👑","Nine-gem vegetable curry in mild cream korma sauce."),
        ("Gatte ki Sabzi",                "Indian","Curries Veg",  "Veg",    195, 195, "🫙","Rajasthani gram flour dumplings in spiced yogurt gravy."),

        # ── Indian Curries — Non-Veg ──────────────────────────────────────
        ("Egg Curry",                     "Indian","Curries Non-Veg","Non-Veg",115, 115, "🥚","Boiled eggs in spiced North Indian onion-tomato gravy."),
        ("Chicken Butter Masala",         "Indian","Curries Non-Veg","Non-Veg",230, 230, "🍗","Tender chicken in buttery tomato-cream sauce."),
        ("Kadai Chicken",                 "Indian","Curries Non-Veg","Non-Veg",260, 260, "🍗","Chicken with capsicum in flavorful kadai masala."),
        ("Mutton Rogan Josh",             "Indian","Curries Non-Veg","Non-Veg",295, 295, "🐑","Kashmiri slow-cooked mutton in aromatic whole spices."),
        # Expanded Non-Veg Curries
        ("Chicken Handi",                 "Indian","Curries Non-Veg","Non-Veg",265, 265, "🍗","Chicken slow-cooked in clay pot with aromatic spices."),
        ("Mutton Keema",                  "Indian","Curries Non-Veg","Non-Veg",285, 285, "🐑","Minced mutton with peas in rich masala."),
        ("Fish Masala",                   "Indian","Curries Non-Veg","Non-Veg",275, 275, "🐟","Fish fillets in spicy South Indian coconut-tomato gravy."),
        ("Prawn Masala",                  "Indian","Curries Non-Veg","Non-Veg",299, 299, "🍤","Prawns in tangy Goan-style masala."),
        ("Chicken Chettinad",             "Indian","Curries Non-Veg","Non-Veg",275, 275, "🌶️","Fiery South Indian Chettinad chicken curry."),
        ("Chicken Saag",                  "Indian","Curries Non-Veg","Non-Veg",255, 255, "🥬","Chicken pieces in spiced spinach gravy."),

        # ── Rice & Biryani ────────────────────────────────────────────────
        ("Veg Pulao",                     "Indian","Rice & Biryani","Veg",    155, 155, "🍚","Fragrant basmati rice cooked with mixed vegetables and spices."),
        ("Egg Biryani",                   "Indian","Rice & Biryani","Non-Veg",175, 175, "🍚","Layered dum biryani with boiled eggs and saffron."),
        ("Chicken Biryani",               "Indian","Rice & Biryani","Non-Veg",240, 240, "🍚","Classic Hyderabadi dum chicken biryani."),
        ("Mutton Biryani",                "Indian","Rice & Biryani","Non-Veg",290, 290, "🍚","Slow-cooked Lucknowi mutton biryani."),
        # Expanded
        ("Veg Biryani",                   "Indian","Rice & Biryani","Veg",    185, 185, "🍚","Aromatic vegetable dum biryani with caramelized onions."),
        ("Jeera Rice",                    "Indian","Rice & Biryani","Veg",    99,  99,  "🍚","Basmati rice tempered with toasted cumin."),
        ("Kolkata Chicken Biryani",       "Indian","Rice & Biryani","Non-Veg",265, 265, "🍚","Kolkata-style biryani with potato, egg and chicken."),
        ("Prawn Biryani",                 "Indian","Rice & Biryani","Non-Veg",319, 319, "🍚","Coastal prawn biryani with coconut and aromatics."),
        ("Paneer Biryani",                "Indian","Rice & Biryani","Veg",    215, 215, "🍚","Fragrant paneer biryani with saffron and rose water."),
        ("Curd Rice",                     "Indian","Rice & Biryani","Veg",    119, 119, "🍚","South Indian cooling curd rice tempered with mustard."),

        # ── Indian Breads ─────────────────────────────────────────────────
        ("Tandoori Roti",                 "Indian","Breads",       "Veg",    45,  65,  "🫓","Whole wheat flatbread baked directly in tandoor."),
        ("Plain Naan",                    "Indian","Breads",       "Veg",    65,  85,  "🫓","Soft leavened flatbread baked in tandoor."),
        ("Butter Naan",                   "Indian","Breads",       "Veg",    75,  95,  "🫓","Tender naan brushed generously with butter."),
        ("Garlic Naan",                   "Indian","Breads",       "Veg",    85,  105, "🧄","Naan topped with garlic and fresh coriander."),
        ("Lachha Paratha",                "Indian","Breads",       "Veg",    105, 105, "🫓","Multi-layered crispy whole-wheat paratha."),
        ("Pudina Paratha",                "Indian","Breads",       "Veg",    55,  85,  "🫓","Flaky paratha infused with fresh mint leaves."),
        ("Cheese Naan",                   "Indian","Breads",       "Veg",    95,  120, "🧀","Naan stuffed with melted cheese."),
        ("Roomali Roti",                  "Indian","Breads",       "Veg",    60,  90,  "🫓","Paper-thin handkerchief bread, very soft."),
        ("Stuffed Paratha",               "Indian","Breads",       "Veg",    95,  95,  "🫓","Paratha stuffed with spiced potato or paneer."),
        ("Missi Roti",                    "Indian","Breads",       "Veg",    65,  65,  "🫓","Chickpea flour roti with ajwain and spices."),
        ("Kulcha",                        "Indian","Breads",       "Veg",    75,  75,  "🫓","Amritsari leavened bread baked in tandoor."),

        # ── Non-Veg Combo Meals ────────────────────────────────────────────
        # 🐔 Chicken + Bread Combos
        ("Butter Chicken + Butter Naan",         "Indian","Combo Meals","Non-Veg", 400, 550, "🍗","Classic butter chicken served with soft butter naan — a match made in heaven."),
        ("Chicken Tikka Masala + Garlic Naan",   "Indian","Combo Meals","Non-Veg", 410, 500, "🍗","Smoky tikka masala with fragrant garlic naan."),
        ("Chicken Curry + Tandoori Roti",         "Indian","Combo Meals","Non-Veg", 395, 450, "🍗","Home-style chicken curry with crisp tandoori roti."),
        ("Chicken Korma + Plain Naan",            "Indian","Combo Meals","Non-Veg", 425, 500, "🍗","Mild creamy korma with soft plain naan."),
        ("Kadhai Chicken + Roomali Roti",         "Indian","Combo Meals","Non-Veg", 405, 480, "🍗","Bold kadhai chicken with paper-thin roomali roti."),
        # 🐑 Mutton + Bread Combos
        ("Mutton Curry + Tandoori Roti",          "Indian","Combo Meals","Non-Veg", 485, 550, "🐑","Slow-cooked mutton curry with whole-wheat tandoori roti."),
        ("Rogan Josh + Butter Naan",              "Indian","Combo Meals","Non-Veg", 495, 600, "🐑","Kashmiri Rogan Josh with buttery naan."),
        ("Keema Matar + Garlic Naan",             "Indian","Combo Meals","Non-Veg", 475, 550, "🐑","Minced mutton with peas, served with garlic naan."),
        # 🐟 Fish & Prawn + Bread Combos
        ("Fish Curry + Tandoori Roti",            "Indian","Combo Meals","Non-Veg", 465, 550, "🐟","Coastal spiced fish curry with hot tandoori roti."),
        ("Prawn Masala + Butter Naan",            "Indian","Combo Meals","Non-Veg", 525, 620, "🍤","Goan-style prawn masala with soft butter naan."),
        ("Goan Fish Curry + Naan",                "Indian","Combo Meals","Non-Veg", 485, 580, "🐟","Tangy Goan coconut fish curry with plain naan."),

        # ── Desserts ──────────────────────────────────────────────────────
        ("Double Chocolate Cake",         "Desserts","Cakes & Pastries","Veg",89,  89,  "🎂","Rich double-chocolate layer cake with ganache."),
        ("Butterscotch Mousse Cup",       "Desserts","Cakes & Pastries","Veg",99,  99,  "🍮","Silky butterscotch mousse in a chilled cup."),
        ("Classic Rabdi Gulab Jamun",     "Desserts","Indian Sweets",  "Veg",89,  89,  "🍯","Soft gulab jamuns in thick saffron rabdi."),
        ("Ice Cream Vanilla",             "Desserts","Ice Creams",     "Veg",60,  60,  "🍨","Classic creamy vanilla ice cream scoop."),
        ("Gulab Jamun (2 pcs)",           "Desserts","Indian Sweets",  "Veg",40,  40,  "🍯","Soft milk-solid balls soaked in rose sugar syrup."),
        ("Rasgulla (2 pcs)",              "Desserts","Indian Sweets",  "Veg",40,  40,  "⚪","Spongy cottage cheese balls in light sugar syrup."),
        # Expanded Desserts
        ("Cheesecake Slice",              "Desserts","Cakes & Pastries","Veg",149, 149, "🍰","Velvety New York cheesecake on biscuit crust."),
        ("Brownie with Ice Cream",        "Desserts","Cakes & Pastries","Veg",119, 119, "🍫","Warm fudge brownie topped with vanilla ice cream."),
        ("Chocolate Mousse Cup",          "Desserts","Cakes & Pastries","Veg",99,  99,  "🍫","Light airy dark chocolate mousse."),
        ("Kulfi (Stick)",                 "Desserts","Ice Creams",     "Veg",60,  60,  "🍦","Traditional Indian ice cream in pistachio or mango."),
        ("Mango Ice Cream",               "Desserts","Ice Creams",     "Veg",79,  79,  "🥭","Fresh Alphonso mango ice cream scoop."),
        ("Chocolate Ice Cream",           "Desserts","Ice Creams",     "Veg",69,  69,  "🍫","Rich dark chocolate ice cream."),
        ("Rasmalai (2 pcs)",              "Desserts","Indian Sweets",  "Veg",69,  69,  "🍮","Spongy paneer in chilled saffron rabdi."),
        ("Jalebi (100g)",                 "Desserts","Indian Sweets",  "Veg",49,  49,  "🌀","Crispy spiral fried batter in sugar syrup."),
        ("Kheer",                         "Desserts","Indian Sweets",  "Veg",89,  89,  "🍚","Creamy rice pudding with cardamom and dry fruits."),
        ("Gajar Ka Halwa",                "Desserts","Indian Sweets",  "Veg",99,  99,  "🥕","Slow-cooked carrot halwa with ghee and nuts."),
        ("Malpua with Rabdi",             "Desserts","Indian Sweets",  "Veg",99,  99,  "🥞","Fried sugar-soaked pancakes with chilled rabdi."),
        ("Falooda",                       "Desserts","Special Drinks", "Veg",119, 119, "🥤","Rose falooda with ice cream, basil seeds and vermicelli."),
    ]

    for item in FOOD_ITEMS:
        cur.execute(
            "INSERT INTO food_items (name, category, subcategory, type, price_min, price_max, emoji, description) "
            "VALUES (?,?,?,?,?,?,?,?)", item
        )

    conn.commit()
    total_hotels = len(HOTELS)
    total_cities = len(CITIES)
    total_trains = len(TRAINS_DATA)
    total_food   = len(FOOD_ITEMS)
    print(f"airports.db created: {total_cities} cities, {total_hotels} hotels, "
          f"{total_trains} trains, {total_food} food items, users table ready.")
    conn.close()


if __name__ == "__main__":
    init()
