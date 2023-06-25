import requests

demo_email ="""
    Hi, 
    I'm the HR manager from GUCCI company with 1000 employees.
    We are looking for a vendor to provide us with T-shirts for our employees, 2 for each employee.
    We would like to have our company logo printed on the T-shirts.
    Can you please provide us with a quote?
    Thanks.
    Best regards,
    John
"""

test_url = "https://gmail-gpt-gyxz.onrender.com"
response = requests.post(
    test_url,
    json={
        "from_email": "markyan@foxmail.com",
        "content": demo_email
    }
).json()

print(response)