#!/usr/bin/env python
import csv

NAME = "name"
URL = "url"
FROM_PLAYER = "from #player"
TO_PLAYER = "to #player"
DURATION = "duration (mins)"
COMPLEXITY = "complexity"

# there are duplicates in output final_result.txt of the parser
game_name_set = set()

game_data = []
with open("final_result.txt") as f:
    counter = 0
    for line in f:
        counter += 1
        if counter == 1: # game_href='/gamepanel?game=grosstarock'
            game_href = line.split("=", 1)[1].replace("'", "")
            game_url = f'https://boardgamearena.com{game_href}'.strip()
            game_name = line.split("=")[2][:-2]

            if game_name in game_name_set:
                # game_name is seen, skipping
                next(f)
                next(f)
                next(f)
                counter = 0
                continue
            else:
                game_name_set.add(game_name)

        elif counter == 2: # number_of_players=' 2 - 4 '
            number_of_players = line.split("=")[1].strip().replace("'", "").split("-")
            if len(number_of_players) == 2:
                number_of_players_from, number_of_players_to = number_of_players
            else:
                assert len(number_of_players) == 1

                # example: number_of_players=[' 2,3,4,6 ']
                if "," in number_of_players[0]:
                    players_range = number_of_players[0].split(",")
                    number_of_players_from = players_range[0]
                    number_of_players_to = players_range[-1]
                else:
                    number_of_players_from = number_of_players[0]
                    number_of_players_to = number_of_players[0]

            number_of_players_from = int(number_of_players_from)
            number_of_players_to = int(number_of_players_to)
        elif counter == 3: # average_duration='\xa0 11 mn '
            duration_in_minutes = line.strip().split(" ")[1]

            # make sure the duration is always in minutes
            assert line.strip().split(" ")[2] == "mn"
        elif counter == 4: # complexity='Complexity: 3 / 5'
            complexity = line.strip().split(" ")[1]

            # reset counter
            counter = 0
            game_data.append(
                {
                    NAME: game_name,
                    URL: game_url,
                    FROM_PLAYER: number_of_players_from,
                    TO_PLAYER: number_of_players_to,
                    DURATION: duration_in_minutes,
                    COMPLEXITY:complexity,
                }
            )
        else:
            assert False

with open("output.csv", "w") as csvfile:
    fieldnames = [NAME, URL, FROM_PLAYER, TO_PLAYER, DURATION, COMPLEXITY]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in game_data:
        writer.writerow(row)
