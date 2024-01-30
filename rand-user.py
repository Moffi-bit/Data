import requests
import os
import argparse

"""
Collect a variety of data from: https://randomuser.me/api/
"""

def send_requests(n):
    resp_contents = []
    url = "https://randomuser.me/api/"

    for _ in range(n):
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
    csv_lines = "name,street,city,state,country,email,username,password,phone,date,coordinates\n"

    for content in resps:
        content = content["results"][0]
        name = content["name"]
        location = content["location"]
        street = location["street"]
        login = content["login"]
        coord = location["coordinates"] 

        name_content = name["first"] + " " + name["last"]
        street_content = str(street["number"]) + " " + street["name"]
        city_content = location["city"]
        state_content = location["state"]
        country_content = location["country"]
        email_content = content["email"]
        username_content = login["username"]
        password_content = login["password"]
        phone_content = content["phone"]
        date_content = content["registered"]["date"]
        coord_content = coord["latitude"] + "$" + coord["longitude"]

        names = handle_data(names, name_content)
        streets = handle_data(streets, street_content)
        cities = handle_data(cities, city_content)
        states = handle_data(states, state_content)
        countries = handle_data(countries, country_content)
        emails = handle_data(emails, email_content)
        usernames = handle_data(usernames, username_content)
        passwords = handle_data(passwords, password_content)
        phones = handle_data(phones, phone_content)
        dates = handle_data(dates, date_content)
        coordinates = handle_data(coordinates, coord_content)

        csv_lines += "{},{},{},{},{},{},{},{},{},{},{}\n".format(name_content, street_content, city_content, state_content, country_content, email_content, username_content, password_content, phone_content, date_content, coord_content)

    write_data(names, path + "names")
    write_data(streets, path + "streets")
    write_data(cities, path + "cities")
    write_data(states, path + "states")
    write_data(countries, path + "countries")
    write_data(emails, path + "emails")
    write_data(usernames, path + "usernames")
    write_data(passwords, path + "passwords")
    write_data(phones, path + "phones")
    write_data(dates, path + "dates")
    write_data(coordinates, path + "coordinates")

    global ending
    ending = "csv"

    path = create_folders_needed()

    write_data(csv_lines, path + "people")

def write_data(data, path):
    with open(path + "." + ending, "a", encoding="utf-8") as f:
        f.write(data)

def handle_data(data, new_data):
    if new_data not in data:
        data += new_data + "\n"
    
    return data

def create_folders_needed():
    root = f"./{ending}s/"

    if not os.path.exists(root):
        os.mkdir(root)

    root += "people/"

    if not os.path.exists(root):
        os.mkdir(root)
    
    return root

def main():
    path = create_folders_needed()

    resps = send_requests(args.num)
    organize_requests(resps, path)

    print("Done!")


if __name__ == "__main__":
    ending = "txt"

    parser = argparse.ArgumentParser(description='Collect dummy data for "people".')
    parser.add_argument('-n', '--num', type=int, help='the amount of people dummy data you want')
    args = parser.parse_args()
    
    main()
