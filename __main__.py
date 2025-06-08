def main():
    from sys import exit
    from os import getenv
    from json import JSONDecodeError, load, dumps, loads
    from dotenv import load_dotenv
    from requests import request
    from time import sleep

    load_dotenv()
    token = getenv("DISCORD_ACTIVITY_TOKEN")
    if not token:
        print("Error: DISCORD_ACTIVITY_TOKEN environment variable is not set.")
        exit(1)
    discordsays = getenv("DISCORD_SAYS_URL")
    if not discordsays:
        print("Error: DISCORD_SAYS_URL environment variable is not set.")
        exit(1)

    #trim discordsays to only the domain
    discordsays = discordsays.rstrip('/')
    if not discordsays.startswith("https://"):
        discordsays = "https://" + discordsays
    if not discordsays.__contains__(".discordsays.com"):
        print("Error: discordsays is not a valid Discord Says URL.")
    elif (not discordsays.endswith(".discordsays.com")) and discordsays.__contains__(".discordsays.com"):
        discordsays = discordsays.split(".discordsays.com", 1)[0]
        discordsays = f"{discordsays}.discordsays.com"

    playlist = getenv("PLAYLIST")
    if not (playlist == "chill" or playlist == "sleepy" or playlist == "jazzy"):
        print("Invalid playlist. Please set the PLAYLIST environment variable to 'chill', 'sleepy', or 'jazzy'.")
        exit(1)
    try:
        SONGS= int(getenv("SONGS"))
    except ValueError:
        print("Error: SONGS environment variable is not a valid integer.")
        exit(1)
    if SONGS < 0:
        print("Error: SONGS environment variable must be greater than or the same as 0.")
        exit(1)

    #you might think why is it called startat?
    #Good question.
    startat = getenv("START_WITH")

    try: loadExisting = bool(getenv("LOAD_EXISTING_JSON"))
    except ValueError:
        print("Error: LOAD_EXISTING_JSON environment variable is not a valid boolean.")
        exit(1)

    allJsons = {}

    if loadExisting:
        try:
            with open(f"{playlist}.json", "r") as infile:
                allJsons = load(infile)
        except FileNotFoundError:
            print(f"{playlist}.json not found, starting from scratch.")
            allJsons = {}
        except JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            exit(1)
    else:
        allJsons = {}






    payload = ""
    headers = {
         "authorization": f"{token}"
    }
    for i in range(int(startat), int(SONGS) + int(startat)):
        print(i)
        url = f"{discordsays}/.proxy/functions/apiProxy/lofi/playlist/{playlist}/track/{i}"
        response = request("GET", url, data=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            requestJson = loads(dumps(data))
            t = f"{requestJson["track"]['title']} - {requestJson['track']['artist']}"
            allJsons[t] = requestJson["track"]
            print(t)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        sleep(1)

    json_object = dumps(allJsons, indent=4, ensure_ascii=False)


    with open(f"{playlist}.json", "w") as outfile:
        try:
            outfile.write(json_object)
        except UnicodeError as e:
            print(f"Unicode error: {e}")
            print("Not much we can do here so can you just copy and paste this to the file? Thanks!\n------------------------------------")
            print(json_object)
        except:
            print(f"An unexpected error occurred while writing to {playlist}.json.")
            print("--------------------------------------------------")
            print(json_object)
            exit(1)



if __name__ == '__main__':
    main()