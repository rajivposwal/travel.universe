from flask import Flask, session
from bookticket import app, get_db

with app.test_request_context('/profile'):
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['user'] = 'admin'
        
        with get_db() as conn:
            conn.execute('''
                INSERT INTO bookings (booking_ref, user_id, service_type, price)
                VALUES ('TEST1', 3, 'Flight', 1000)
            ''')
            conn.commit()

        res = c.get('/profile')
        print('Status:', res.status_code)
        if res.status_code != 200:
            print('Error:', res.data.decode('utf-8')[:500])
