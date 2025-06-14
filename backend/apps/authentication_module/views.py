import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.db import connection

def check_if_existing(username: str, email: str) -> str | None:
    query = """
        SELECT username, email
        FROM users
        WHERE username = %s OR email = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [username, email])
        results = cursor.fetchall()

    username_exists = False
    email_exists = False

    for db_username, db_email in results:
        if db_username == username:
            username_exists = True
        if db_email == email:
            email_exists = True

    # Username fields will be replaced with firstName, lastName
    if username_exists:
        return "Username already exists"
    if email_exists:
        return "Email already exists"

    return None  # No match found


@csrf_exempt
def register(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("REQUEST FAILED: Expected 'POST' request.")

    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'INVALID JSON'}, status=400)

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    missing_fields = [field for field in ['username', 'email', 'password'] if not data.get(field)]
    if missing_fields:
        return JsonResponse({'error': f"Missing fields: {', '.join(missing_fields)}."}, status=400)

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # TEMP: Ensure users table exists (for testing only)
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        try:
            # Check for existing username or email
            existing=check_if_existing(username, email)
            if existing:
                return JsonResponse({
                    'error': existing
                }, status=400)

            # Insert user
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                [username, email, hashed_password]
            )

            return JsonResponse({
                'message': 'User registered successfully!',
                # 'username': username,
                # 'email': email,
                # These were unaccounted for in the frontend response mechanism,
                # which is why I kept getting an error even though user details went through to database
                }, status=201)

        except Exception as e:
            return JsonResponse({'error': f"Database error: {str(e)}"}, status=500)


@csrf_exempt
def login(request):
    """Login route logic."""
    if request.method!='POST':
        return HttpResponseBadRequest(f"REQUEST FAILED: Expected 'POST' request.")

    try:
        data=json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({
            'error':'INVALID JSON FORMAT!'
        }, status=400)

    email=data.get('email')
    password=data.get('password')

    missing_fields=[field for field in ['email', 'password'] if not data.get(field)]
    if missing_fields:
        return JsonResponse({
            'error':'Some fields are required but missing'
        }, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT email FROM users WHERE email = %s""", [email])
            existing=cursor.fetchall()

        if not existing:
            return JsonResponse({
                'error':'Credentials not found!',
            }, status=400)

        # to verify_password() if matches hash from user credentials

        # Simulating temporary direct success if user in database- to reconfigure for tighter security, like two-factor security features
        return JsonResponse(data={
            'message':'User login successful!',
        }, status=200)

    except Exception as exc:
        return JsonResponse(data={
            'error':'An internal server error occurred while logging in. Please try again later.'
        }, status=500)