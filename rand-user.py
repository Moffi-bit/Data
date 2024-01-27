import requests
import os

"""
Collect a variety of data from: https://randomuser.me/api/
"""


def send_requests():
    resp_contents = []
    url = "https://randomuser.me/api/"

    for _ in range(1000):
        resp = requests.get(url)

        if resp.status_code == 200:
            print("Successfully connected to server...")

            resp_contents.append(resp.json())

    return resp_contents


def organize_requests(resps, path):
    names = ""
    streets = ""
    cities = ""
    states = ""
    countries = ""
    emails = ""
    usernames = ""
    passwords = ""
    phones = ""
    dates = ""
    coordinates = ""

    for content in resps:
        content = content["results"][0]
        name = content["name"]
        location = content["location"]
        street = location["street"]
        login = content["login"]
        coord = location["coordinates"] 

        names = add_data_to_list(names, name["first"] + " " + name["last"])
        streets = add_data_to_list(streets, str(street["number"]) + " " + street["name"])
        cities = add_data_to_list(cities, location["city"])
        states = add_data_to_list(states, location["state"])
        countries = add_data_to_list(countries, location["country"])
        emails = add_data_to_list(emails,  content["email"])
        usernames = add_data_to_list(usernames, login["username"])
        passwords = add_data_to_list(passwords, login["password"])
        phones = add_data_to_list(phones, content["phone"])
        dates = add_data_to_list(dates, content["registered"]["date"])
        coordinates = add_data_to_list(coordinates, coord["latitude"] + ", " + coord["longitude"])

    write_data_txt(names, path + "names")
    write_data_txt(streets, path + "streets")
    write_data_txt(cities, path + "cities")
    write_data_txt(states, path + "states")
    write_data_txt(countries, path + "countries")
    write_data_txt(emails, path + "emails")
    write_data_txt(usernames, path + "usernames")
    write_data_txt(passwords, path + "passwords")
    write_data_txt(phones, path + "phones")
    write_data_txt(dates, path + "dates")
    write_data_txt(coordinates, path + "coordinates")

def write_data_txt(data, path):
    with open(path + ".txt", "a", encoding="utf-8") as f:
        f.write(data)

def add_data_to_list(data, new_data):
    if new_data not in data:
        data += new_data + "\n"
    
    return data

def main():
    ROOT = "./txts/people/"

    if not os.path.exists("./txts/"):
        os.mkdir("./txts/")

    if not os.path.exists(ROOT):
        os.mkdir(ROOT)

    resps = send_requests()
    organize_requests(resps, ROOT)

    print("Done!")


if __name__ == "__main__":
    main()
