
def get_token():
    with open("./console/token", "r") as file:
        token = file.readline()
    return token
