import jwt

header = {
    "alg" : "HS256",
    "typ" : "JWT"
}

payload = {
    "sub" : 123546,
    "name" : "Jignesh Mistry",
    "iat" : 15124878
}

secret = "JigPass"

encodedJWT = jwt.encode(payload, secret, algorithm="HS256", headers=header)

print("Encoded\n", encodedJWT)

decodedJWT = jwt.decode(encodedJWT, secret, algorithms=["HS256"])

print("DEcoded\n", decodedJWT)

try:
    decodedJWT = jwt.decode(encodedJWT, secret, algorithms=['HS256'], verify=True)
    print("Verfied Decoded\n",decodedJWT)
except jwt.exceptions.ImmatureSignatureError:
    print("invalid signature")


# Here are the top three important drawbacks of JWT:

# 1. Stateless Nature: While JWT’s statelessness is a plus, it can also be a drawback. Revoking tokens (e.g., when a user logs out or change password) can be challenging since JWTs are self-contained.

# 2. Security Risks with Stored Tokens: Storing JWTs on the client side can pose security risks if they are compromised.

# 3. Token Size: JWT tokens can grow in size if you include a lot of information in the payload, potentially increasing bandwidth usage.