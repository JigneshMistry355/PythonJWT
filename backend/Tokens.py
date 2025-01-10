import jwt

def create_Token(payload):
    header = {"alg" : "HS256", "typ" : "JWT"}
    secret_key = "supersecretkey"
    algorithm = "HS256"
    token = jwt.encode(payload, secret_key, algorithm, headers=header)
    return token

def validate_Token(token):
    secret_key = "supersecretkey"
    algorithm = 'HS256'
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=[algorithm], verify=True)
        print("Login Successful")
        return decoded_payload
    except jwt.exceptions.ImmatureSignatureError:
        print("Invalid Token, Access Denied")
    except jwt.exceptions.ExpiredSignatureError:
        print("Token expired. Login again!")

def main():
    payload = {
        "sub" : 123546,
        "name" : "Jignesh Mistry",
        "iat" : 15124878
    }
    token = create_Token(payload)
    validate_Token(token)

    

if __name__ == '__main__':
    main()