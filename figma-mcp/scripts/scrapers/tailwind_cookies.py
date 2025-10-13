#!/usr/bin/env python3
"""
Tailwind UI cookies for authenticated scraping
IMPORTANT: Keep this file secure and do not commit to git!
"""

TAILWIND_COOKIES = [
    {
        'name': 'tailwind_plus_session',
        'value': 'eyJpdiI6ImEvK1Zld1NNVWp1Tm5EYUZPQkl0cGc9PSIsInZhbHVlIjoieG5URnF3VnVQbFJuRkhMTUNZeTQyLzJYN3hzdmJQcWtlVWZEZDQzNmN0NFl3ZG1UYW9CbGp6bnFvWklaY3Q1aWlzVFNYVEdkNmh6bkpMVC9DTXBzRGdsK2xPNE9uTE9iMm1HaWVIMGRrZlFockhEUVlpUVQwM3ZDdXM0Y09hV0QiLCJtYWMiOiIyYTNmZDZhMmI2ZWRmYjNkYWRmMGMyZGI3NzNhMzUzYmQzNzlmNmI0MzhjMTUxMTMxZWJkOWM3NmY0N2Q4NWM4IiwidGFnIjoiIn0=',
        'domain': '.tailwindui.com',
        'path': '/',
        'httpOnly': True,
        'secure': True,
        'sameSite': 'Lax'
    }
]