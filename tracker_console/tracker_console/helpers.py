
def get_token():
    with open("./tracker_console/token", "r") as file:
        token = file.readline()
    return token
