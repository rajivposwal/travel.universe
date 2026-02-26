"""
bookticket.py  –  ASRS Travel v4.0
Clean, DB-backed, multi-modal ticket booking system
"""

from flask import (Flask, render_template, request, jsonify,
                   session, redirect, url_for, flash, get_flashed_messages)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3, random, math, os, json

app = Flask(__name__)
app.secret_key = 'kayenaat_travel_2026_secure'

DB_PATH     = os.path.join(os.path.dirname(__file__), "airports.db")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# ── Login Required Decorator ─────────────────────────────
from functools import wraps

def login_required(f):
    """Redirect guests to /login; API routes return 401 JSON."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            # API / JSON requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
               request.accept_mimetypes.best == 'application/json':
                return jsonify({'error': 'login_required',
                                'message': 'Please sign in to continue.'}), 401
            # Save intended destination & redirect to login
            session['next'] = request.url
            flash('Please sign in to book or order.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ────────────────────────────────────────────────────────
#  DB Helpers
# ────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def lookup_city(name: str):
    """Return airport row as dict with lat/lon aliases, or None."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM airports WHERE city_lower = ?",
            (name.strip().lower(),)
        ).fetchone()
    if not row:
        return None
    d = dict(row)
    # Alias DB column names → short keys used throughout the code
    d['lat'] = d.get('latitude',  20.0)
    d['lon'] = d.get('longitude', 77.0)
    return d

def all_cities():
    """Return sorted list of city names for autocomplete."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT city FROM airports ORDER BY city"
        ).fetchall()
    return [r["city"] for r in rows]

def all_trains():
    """Return all train records from DB as list of dicts."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT name, category, speed_kmph, description FROM trains ORDER BY id"
        ).fetchall()
    return [dict(r) for r in rows]

# ────────────────────────────────────────────────────────
#  Carriers / Operators
# ────────────────────────────────────────────────────────
AIRLINES = ["IndiGo", "Air India", "SpiceJet", "Vistara", "Akasa Air", "GoFirst"]
BUS_OPS  = [
    "Volt Travels", "Orange Sector", "Highway Nova", "ZipBus", "Urban Link",
    "KSRTC Premium", "MSRTC Shivneri", "VRL Travels", "KPN Travels",
    "SRM Travels", "Kallada Travels", "Parveen Travels", "Neeta Tours & Travels",
    "Kesineni Travels (KRL)", "Eagle Travels", "SVR Travels", "Orange Travels",
    "Dolphin Travel House", "IntrCity SmartBus", "RedBus Travels", "Pinkbus",
    "National Express / NTHO", "M S Jogeshwari Enterprises", "BTP Buses",
    "Maru Travels", "PMR Express", "Kerala State Road Transport Corporation (KSRTC)",
    "State RTCs"
]
HOTELS   = ["The Almond Sands", "Aqueous Retreat", "Heritage Pods",
            "The Velvet Sector", "Skyline Grand", "Quantum Plaza"]
# Full verified Unsplash hotel photo URLs (no broken partial IDs)
HOTEL_IMGS = [
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1455053288096-09b8d5ef8c73?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1625244724120-1fd1d34d00f6?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1561501900-3701fa6a0864?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=600&q=80",
]

# (OTP system removed — password-based auth used instead)

# ────────────────────────────────────────────────────────
#  Utilities
# ────────────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dl = math.radians(lat2 - lat1)
    dL = math.radians(lon2 - lon1)
    a  = (math.sin(dl/2)**2
          + math.cos(math.radians(lat1))
          * math.cos(math.radians(lat2))
          * math.sin(dL/2)**2)
    return max(1, int(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))))

def rand_time():
    return f"{random.randint(0,23):02d}:{random.choice(['00','15','30','45'])}"

# ────────────────────────────────────────────────────────
#  Routes
# ────────────────────────────────────────────────────────
@app.route("/")
def index():
    cities          = all_cities()
    just_logged_in  = session.pop('just_logged_in', False)
    return render_template("bookticket.html",
                           logged_in      = ('user' in session),
                           user_name      = session.get('user', ''),
                           avatar_color   = session.get('avatar_color', '#ff9f1c'),
                           just_logged_in = just_logged_in,
                           cities         = cities)

@app.route("/login")
def login():
    if 'user' in session:
        return redirect(url_for('index'))
    tab = request.args.get('tab', 'login')
    next_url = session.pop('next', None)
    return render_template("login.html", tab=tab, next_url=next_url)

# ── Register ───────────────────────────────────────────
@app.route("/auth/register", methods=['POST'])
def auth_register():
    username = request.form.get('username', '').strip()
    email    = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm  = request.form.get('confirm_password', '')

    # Validation
    if not username or len(username) < 3:
        flash('Username must be at least 3 characters.', 'error')
        return redirect(url_for('login') + '?tab=register')
    if '@' not in email:
        flash('Please enter a valid email address.', 'error')
        return redirect(url_for('login') + '?tab=register')
    if len(password) < 6:
        flash('Password must be at least 6 characters.', 'error')
        return redirect(url_for('login') + '?tab=register')
    if password != confirm:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('login') + '?tab=register')

    pw_hash = generate_password_hash(password)
    colors  = ['#ff9f1c','#2ec4b6','#e71d36','#7209b7','#3a86ff']
    color   = random.choice(colors)

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO users (username, email, password_hash, avatar_color, auth_provider) "
                "VALUES (?, ?, ?, ?, 'email')",
                (username, email, pw_hash, color)
            )
            conn.commit()
        session['user']         = username
        session['email']        = email
        session['avatar_color'] = color
        session['just_logged_in'] = True
        next_url = session.pop('next', None)
        if next_url:
            return redirect(next_url)
        if 'search' in session:
            return redirect(url_for('results'))
        return redirect(url_for('index'))
    except Exception as e:
        if 'UNIQUE' in str(e):
            if 'username' in str(e):
                flash('That username is already taken. Try another.', 'error')
            else:
                flash('An account with this email already exists. Sign in instead.', 'error')
        else:
            flash('Something went wrong. Please try again.', 'error')
        return redirect(url_for('login') + '?tab=register')

# ── Email / Password Login ──────────────────────────────
@app.route("/auth/login", methods=['POST'])
def auth_login():
    identifier = request.form.get('identifier', '').strip()
    password   = request.form.get('password', '')

    if not identifier or not password:
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('login'))

    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ? OR username = ?",
            (identifier.lower(), identifier)
        ).fetchone()

    if not row:
        flash('No account found with that email or username.', 'error')
        return redirect(url_for('login'))

    user = dict(row)
    if not user['password_hash'] or not check_password_hash(user['password_hash'], password):
        flash('Incorrect password. Please try again.', 'error')
        return redirect(url_for('login'))

    session['user']         = user['username']
    session['email']        = user['email']
    session['avatar_color'] = user.get('avatar_color', '#ff9f1c')
    session['just_logged_in'] = True
    next_url = session.pop('next', None)
    if next_url:
        return redirect(next_url)
    if 'search' in session:
        return redirect(url_for('results'))
    return redirect(url_for('index'))

# ── Google / Gmail Auth (Simulated) ────────────────────
@app.route("/auth/google")
def auth_google():
    email    = request.args.get('email', '').strip().lower()
    name     = request.args.get('name',  'Traveler')
    if not email or '@' not in email:
        flash('Invalid Gmail address.', 'error')
        return redirect(url_for('login'))

    colors = ['#ff9f1c','#2ec4b6','#e71d36','#7209b7','#3a86ff']
    avatar = random.choice(colors)

    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()

        if not row:
            # Auto-create account via Gmail
            conn.execute(
                "INSERT OR IGNORE INTO users (username, email, avatar_color, auth_provider) "
                "VALUES (?, ?, ?, 'google')",
                (name, email, avatar)
            )
            conn.commit()
        else:
            # Use existing user's data
            user = dict(row)
            name   = user.get('username', name)
            avatar = user.get('avatar_color', avatar)

    session['user']           = name
    session['email']          = email
    session['avatar_color']   = avatar
    session['just_logged_in'] = True
    if 'search' in session:
        return redirect(url_for('results'))
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

# ── Forgot Password — Step 1: Send OTP ─────────────────
@app.route("/auth/forgot-password", methods=['POST'])
def forgot_password():
    mobile = request.form.get('mobile', '').strip()
    if not mobile or not mobile.isdigit() or len(mobile) != 10:
        return jsonify({'success': False, 'message': 'Please enter a valid 10-digit mobile number.'})

    # In production, send real SMS. Here we generate & return OTP for demo.
    otp = str(random.randint(100000, 999999))
    # Store in session for verification
    session['otp']        = otp
    session['otp_mobile'] = mobile

    # For demo: return OTP in response (in production, send via SMS API)
    return jsonify({'success': True, 'otp': otp,
                    'message': f'OTP sent to +91-XXXXXX{mobile[-4:]} (demo: {otp})'})

# ── Forgot Password — Step 2: Verify OTP ───────────────
@app.route("/auth/verify-otp", methods=['POST'])
def verify_otp():
    entered = request.form.get('otp', '').strip()
    stored  = session.get('otp', '')
    if not stored:
        return jsonify({'success': False, 'message': 'OTP expired. Please request a new one.'})
    if entered != stored:
        return jsonify({'success': False, 'message': 'Incorrect OTP. Please try again.'})
    session['otp_verified'] = True
    return jsonify({'success': True, 'message': 'OTP verified!'})

# ── Forgot Password — Step 3: Reset Password ───────────
@app.route("/auth/reset-password", methods=['POST'])
def reset_password():
    if not session.get('otp_verified'):
        return jsonify({'success': False, 'message': 'Please verify OTP first.'})

    new_pw  = request.form.get('new_password', '')
    confirm = request.form.get('confirm_password', '')

    if len(new_pw) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters.'})
    if new_pw != confirm:
        return jsonify({'success': False, 'message': 'Passwords do not match.'})

    # Clear OTP session
    session.pop('otp', None)
    session.pop('otp_mobile', None)
    session.pop('otp_verified', None)

    # In production: look up user by phone and update password_hash.
    # Here OTP verification is the security gate; return success for demo.
    return jsonify({'success': True, 'message': 'Password reset successful! You can now sign in.'})


# ── City Autocomplete API ───────────────────────────────
@app.route("/api/cities")
def api_cities():
    q     = request.args.get('q', '').lower()
    query = "SELECT city, state, iata_code FROM airports WHERE city_lower LIKE ? ORDER BY city LIMIT 10"
    with get_db() as conn:
        rows = conn.execute(query, (f"{q}%",)).fetchall()
    return jsonify([dict(r) for r in rows])

# ── Food API ────────────────────────────────────────────
@app.route("/api/food")
def api_food():
    """Return food items filtered by category, type, search query."""
    cat    = request.args.get('category', '')
    ftype  = request.args.get('type', '')
    search = request.args.get('q', '').strip().lower()

    query = "SELECT * FROM food_items WHERE 1=1"
    params = []
    if cat:
        query += " AND category = ?"
        params.append(cat)
    if ftype:
        query += " AND type = ?"
        params.append(ftype)
    if search:
        query += " AND lower(name) LIKE ?"
        params.append(f"%{search}%")
    query += " ORDER BY category, subcategory, name"

    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
    return jsonify([dict(r) for r in rows])

# ── Food Page ────────────────────────────────────────────
@app.route("/food")
@login_required
def food():
    # Fetch all food items grouped
    with get_db() as conn:
        all_food = [dict(r) for r in conn.execute(
            "SELECT * FROM food_items ORDER BY category, subcategory, name"
        ).fetchall()]

    # Group by category → subcategory
    from collections import defaultdict
    grouped = defaultdict(lambda: defaultdict(list))
    for item in all_food:
        grouped[item['category']][item['subcategory']].append(item)

    # Convert to regular dicts for Jinja
    grouped = {cat: dict(subs) for cat, subs in grouped.items()}

    return render_template("food.html",
        logged_in    = True,
        user_name    = session.get('user', ''),
        avatar_color = session.get('avatar_color', '#ff9f1c'),
        grouped      = grouped,
        total        = len(all_food),
    )

# ── Search ─────────────────────────────────────────────
@app.route("/search", methods=['POST'])
@login_required
def search():
    session['search'] = {
        'type':        request.form.get('travel_type', 'Flight'),
        'source':      request.form.get('source', '').strip(),
        'destination': request.form.get('destination', '').strip(),
        'date':        request.form.get('date', ''),
    }
    return redirect(url_for('results'))

# ── Results ────────────────────────────────────────────
@app.route("/results")
@login_required
def results():
    s = session.get('search')
    if not s:
        return redirect(url_for('index'))

    t_type = s['type']
    src    = s['source']
    dst    = s['destination']
    date   = s['date']

    # ── City validation (Flights only) ──────────────────
    if t_type == 'Flight':
        sd = lookup_city(src)
        dd = lookup_city(dst)

        if not sd:
            return render_template("no_service.html",
                                   city=src, reason="source",
                                   cities=all_cities())
        if not dd:
            return render_template("no_service.html",
                                   city=dst, reason="destination",
                                   cities=all_cities())
        if sd['city_lower'] == dd['city_lower']:
            return render_template("no_service.html",
                                   city=src, reason="same",
                                   cities=all_cities())

        dist    = haversine(sd['lat'], sd['lon'], dd['lat'], dd['lon'])
        s_info  = sd
        d_info  = dd
        src_disp = sd['city']
        dst_disp = dd['city']

    else:
        # Non-flight: use DB lookup if available, else sensible defaults
        _sd = lookup_city(src)
        _dd = lookup_city(dst)
        sd = _sd if _sd else {"lat": 20.0, "lon": 77.0, "city": src.title(),
                              "famous": "", "local_food": "", "best_time": ""}
        dd = _dd if _dd else {"lat": 19.0, "lon": 72.0, "city": dst.title(),
                              "famous": "", "local_food": "", "best_time": ""}
        dist     = haversine(sd['lat'], sd['lon'], dd['lat'], dd['lon'])
        s_info   = sd
        d_info   = dd
        src_disp = sd['city']
        dst_disp = dd['city']

    # ── Generate results ─────────────────────────────────
    items = []

    if t_type == 'Flight':
        for _ in range(12):
            price = int(dist * random.uniform(4.5, 9.0) + 1000)
            items.append({
                "id":        f"FL-{random.randint(100,999)}",
                "name":      random.choice(AIRLINES),
                "departure": rand_time(),
                "arrival":   rand_time(),
                "duration":  f"{max(1, dist//800)}h {random.randint(5,55)}m",
                "price":     price,
                "tag":       f"Gate {random.choice(['A','B','C','D'])}{random.randint(1,25)}",
                "class":     random.choice(["Economy", "Business", "First Class"]),
            })

    elif t_type == 'Train':
        trains_db = all_trains()          # load all 20 from DB
        for _ in range(10):
            train   = random.choice(trains_db)
            speed   = train['speed_kmph']
            dur_h   = max(1, round(dist / speed))
            dur_m   = random.choice([0, 15, 30, 45])
            # Price inversely proportional to speed (faster = pricier)
            price   = int(dist * random.uniform(0.8, 2.8) * (speed / 100) + 200)
            items.append({
                "id":        f"TRN-{random.randint(10000,99999)}",
                "name":      train['name'],
                "departure": rand_time(),
                "arrival":   rand_time(),
                "duration":  f"{dur_h}h {dur_m}m",
                "price":     price,
                "tag":       f"PF {random.randint(1,15)} · {train['category']}",
                "class":     random.choice(["Sleeper (SL)", "3A AC", "2A AC", "1A AC", "Chair Car"]),
            })

    elif t_type == 'Bus':
        for _ in range(10):
            price = int(dist * random.uniform(0.6, 1.2) + 120)
            items.append({
                "id":        f"BUS-{random.randint(100,999)}",
                "name":      random.choice(BUS_OPS),
                "departure": rand_time(),
                "arrival":   rand_time(),
                "duration":  f"{max(6, dist//50)}h",
                "price":     price,
                "tag":       f"Bay {random.randint(1,20)}",
                "class":     random.choice(["AC Sleeper", "Volvo AC", "Non-AC Semi-Sleeper"]),
            })

    elif t_type == 'Hotel':
        for i in range(10):
            items.append({
                "id":       f"HTL-{i+1:02d}",
                "name":     random.choice(HOTELS),
                "meta":     random.choice(["Deluxe Suite", "Premium Room",
                                           "Heritage Vista", "Ocean View"]),
                "price":    random.randint(2500, 9500),
                "rating":   round(random.uniform(4.1, 5.0), 1),
                "amenities":random.sample(["Free WiFi", "Pool", "Spa",
                                           "Breakfast", "Gym", "Parking"], 3),
                "img":      random.choice(HOTEL_IMGS),
            })

    return render_template("results.html",
                           travel_type =t_type,
                           source      =src_disp,
                           destination =dst_disp,
                           date        =date,
                           distance    =dist,
                           items       =items,
                           s_coords    =(round(s_info['lat'],4), round(s_info['lon'],4)),
                           d_coords    =(round(d_info['lat'],4), round(d_info['lon'],4)),
                           place       =d_info)

# ── Booking page ───────────────────────────────────────
@app.route("/book")
@login_required
def book():
    return render_template("booking.html",
        type         = request.args.get('type',  'Flight'),
        name         = request.args.get('name',  'Unknown'),
        item_id      = request.args.get('id',    ''),
        dep          = request.args.get('dep',   '--:--'),
        arr          = request.args.get('arr',   '--:--'),
        date         = request.args.get('date',  'Unknown Date'),
        price        = int(request.args.get('price', 0)),
        src          = request.args.get('src',   '--'),
        dst          = request.args.get('dst',   '--'),
        cls          = request.args.get('cls',   '--'),
        rating       = request.args.get('rating','--'),
        session_user = session.get('user', 'Traveler'),
    )

# ── Deals dashboard ────────────────────────────────────
@app.route("/deals")
@login_required
def deals():

    city_pairs = [
        ("Delhi","Mumbai"), ("Mumbai","Goa"), ("Bangalore","Chennai"),
        ("Jaipur","Agra"),  ("Kolkata","Hyderabad"), ("Pune","Delhi"),
    ]
    items = []

    for src, dst in random.sample(city_pairs, 3):
        sd = lookup_city(src); dd = lookup_city(dst)
        if sd and dd:
            dist = haversine(sd['lat'],sd['lon'],dd['lat'],dd['lon'])
            items.append({"category":"Flight","from":src,"to":dst,
                           "carrier":random.choice(AIRLINES),
                           "dep":rand_time(),"arr":rand_time(),
                           "dur":f"{max(1,dist//800)}h",
                           "price":int(dist*random.uniform(5,9)+1000)})

    trains_db = all_trains()
    for src, dst in random.sample(city_pairs, 3):
        sd = lookup_city(src); dd = lookup_city(dst)
        if sd and dd:
            dist  = haversine(sd['lat'],sd['lon'],dd['lat'],dd['lon'])
            train = random.choice(trains_db)
            dur_h = max(1, round(dist / train['speed_kmph']))
            items.append({"category":"Train","from":src,"to":dst,
                           "carrier": train['name'],
                           "dep":rand_time(),"arr":rand_time(),
                           "dur":f"{dur_h}h",
                           "price":int(dist*random.uniform(1,2.2)+300)})

    for src, dst in random.sample(city_pairs, 3):
        sd = lookup_city(src); dd = lookup_city(dst)
        if sd and dd:
            dist = haversine(sd['lat'],sd['lon'],dd['lat'],dd['lon'])
            items.append({"category":"Bus","from":src,"to":dst,
                           "carrier":random.choice(BUS_OPS),
                           "dep":rand_time(),"arr":rand_time(),
                           "dur":f"{max(6,dist//50)}h",
                           "price":int(dist*random.uniform(0.7,1.2)+150)})

    for _ in range(6):
        items.append({"category":"Hotel",
                       "name":random.choice(HOTELS),
                       "meta":random.choice(["Deluxe Suite","Premium Room","Heritage Vista"]),
                       "price":random.randint(2500,9000),
                       "rating":round(random.uniform(4.2,5.0),1),
                       "amenities":random.sample(["WiFi","Pool","Spa","Breakfast"],2),
                       "img": random.choice(HOTEL_IMGS)})

    random.shuffle(items)
    return render_template("deals.html", user_name=session['user'], items=items)

# ── Budget Hotels directory ────────────────────────────
@app.route("/hotels")
@login_required
def hotels():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM hotels ORDER BY rating DESC"
        ).fetchall()
    hotels_list = [dict(r) for r in rows]
    return render_template("hotels.html",
                           hotels    = hotels_list,
                           logged_in = True,
                           user_name = session.get('user', ''))

# ────────# ── User Profile ────────────────────────────────────────
@app.route("/profile")
@login_required
def profile():
    username = session['user']
    with get_db() as conn:
        user = dict(conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone())
        bookings = [dict(r) for r in conn.execute(
            "SELECT * FROM bookings WHERE user_id = ? ORDER BY booked_at DESC",
            (user['id'],)
        ).fetchall()]

    # stats
    total_spent = sum(b['price'] for b in bookings)
    by_type = {}
    for b in bookings:
        by_type[b['service_type']] = by_type.get(b['service_type'], 0) + 1

    return render_template("profile.html",
        user         = user,
        bookings     = bookings,
        total_spent  = total_spent,
        by_type      = by_type,
        avatar_color = session.get('avatar_color', '#ff9f1c'),
    )


@app.route("/profile/update", methods=['POST'])
@login_required
def profile_update():
    username = session['user']
    phone    = request.form.get('phone', '').strip()
    with get_db() as conn:
        conn.execute("UPDATE users SET phone = ? WHERE username = ?",
                     (phone, username))
        conn.commit()
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('profile'))


@app.route("/profile/upload-photo", methods=['POST'])
@login_required
def upload_photo():
    username = session['user']
    file = request.files.get('photo')
    if not file or file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected.'})
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Only PNG, JPG, GIF, WEBP allowed.'})

    ext      = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(f"avatar_{username}.{ext}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    with get_db() as conn:
        conn.execute("UPDATE users SET profile_photo = ? WHERE username = ?",
                     (filename, username))
        conn.commit()

    photo_url = url_for('static', filename=f'uploads/{filename}')
    return jsonify({'success': True, 'url': photo_url})


# ── Booking Management (User Area) ────────────────────────
@app.route("/booking/<booking_ref>")
@login_required
def manage_booking(booking_ref):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM bookings WHERE booking_ref = ? AND user_id = (SELECT id FROM users WHERE username = ?)",
            (booking_ref, session['user'])
        ).fetchone()
        if not row:
            flash("Booking not found.", "error")
            return redirect(url_for('profile'))
        b = dict(row)
    return render_template("manage_booking.html", b=b)

@app.route("/booking/<booking_ref>/cancel", methods=['GET', 'POST'])
@login_required
def cancel_booking(booking_ref):
    username = session['user']
    with get_db() as conn:
        user = dict(conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone())
        row = conn.execute("SELECT * FROM bookings WHERE booking_ref = ? AND user_id = ?", (booking_ref, user['id'])).fetchone()
        if not row:
            flash("Booking not found.", "error")
            return redirect(url_for('profile'))
        b = dict(row)

    if request.method == 'POST':
        with get_db() as conn:
            conn.execute("UPDATE bookings SET status = 'Cancelled' WHERE booking_ref = ? AND user_id = ?", (booking_ref, user['id']))
            conn.commit()
        flash("Booking cancelled successfully.", "success")
        return redirect(url_for('manage_booking', booking_ref=booking_ref))

    deduction = int(b['price'] * 0.20)
    refund = b['price'] - deduction
    return render_template("cancel_booking.html", b=b, deduction=deduction, refund=refund)

@app.route("/booking/<booking_ref>/ticket")
@login_required
def download_ticket(booking_ref):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM bookings WHERE booking_ref = ? AND user_id = (SELECT id FROM users WHERE username = ?)",
            (booking_ref, session['user'])
        ).fetchone()
        if not row:
            flash("Booking not found.", "error")
            return redirect(url_for('profile'))
        b = dict(row)
    if b['service_type'] == 'Hotel':
        return render_template("welcome_card.html", b=b, user_name=session['user'])
    return render_template("ticket.html", b=b, user_name=session['user'])

@app.route("/booking/<booking_ref>/payment")
@login_required
def payment_details(booking_ref):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM bookings WHERE booking_ref = ? AND user_id = (SELECT id FROM users WHERE username = ?)",
            (booking_ref, session['user'])
        ).fetchone()
        if not row:
            flash("Booking not found.", "error")
            return redirect(url_for('profile'))
        b = dict(row)
    return render_template("payment_details.html", b=b, user_name=session['user'])


# ── Save Booking (called from booking.html after payment) ──
@app.route("/api/book/save", methods=['POST'])
@login_required
def save_booking():
    data = request.get_json(force=True)
    username = session['user']
    with get_db() as conn:
        user = conn.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if not user:
            return jsonify({'success': False, 'message': 'User not found.'})

        try:
            conn.execute("ALTER TABLE bookings ADD COLUMN traveler_names TEXT")
        except:
            pass

        try:
            conn.execute("""
                INSERT OR IGNORE INTO bookings
                (booking_ref, user_id, service_type, item_name,
                 from_city, to_city, travel_date, seat_room,
                 passengers, traveler_names, class_type, price, pay_method, status)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                data.get('booking_ref',''),
                user['id'],
                data.get('service_type',''),
                data.get('item_name',''),
                data.get('from_city',''),
                data.get('to_city',''),
                data.get('travel_date',''),
                data.get('seat_room',''),
                data.get('passengers', 1),
                data.get('traveler_names', ''),
                data.get('class_type',''),
                int(data.get('price', 0)),
                data.get('pay_method','UPI'),
                data.get('status', 'Confirmed')       # ← now dynamic
            ))
            conn.commit()
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    return jsonify({'success': True})


# ── Update booking status (Payment Pending → Confirmed) ──
@app.route("/api/book/update-status", methods=['POST'])
@login_required
def update_booking_status():
    data = request.get_json(force=True)
    booking_ref = data.get('booking_ref', '')
    new_status  = data.get('status', 'Confirmed')
    username    = session['user']
    with get_db() as conn:
        user = conn.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if not user:
            return jsonify({'success': False, 'message': 'User not found.'})
        conn.execute("""
            UPDATE bookings SET status = ?
            WHERE booking_ref = ? AND user_id = ?
        """, (new_status, booking_ref, user['id']))
        conn.commit()
    return jsonify({'success': True})


if __name__ == "__main__":
    app.run(debug=True)
