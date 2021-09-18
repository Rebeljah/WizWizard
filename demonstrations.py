import pywizlight as pwz
import asyncio as aio
import time
import random

from home_model import Home

SCENES = {v.lower(): k for k, v in pwz.SCENES.items()}


def turn_all_on(lights):
    for light in lights:
        aio.run(light.turn_on())


def all_cozy(lights, brightness):
    for light in lights:
        aio.run(light.turn_on(pwz.PilotBuilder(
            brightness=brightness, scene=SCENES['Cozy'])
        ))


def red_alert(lights):
    light: pwz.wizlight
    while True:
        for light in lights:
            aio.run(light.updateState())
            if light.status:
                aio.run(light.turn_off())
            else:
                builder = pwz.PilotBuilder(brightness=255, rgb=(255, 0, 0))
                aio.run(light.turn_on(builder))
        time.sleep(0.75)


def party(lights):
    while True:
        for light in lights:
            rgb = tuple(random.randint(0, 255) for _ in range(3))
            builder = pwz.PilotBuilder(rgb=rgb)
            aio.run(light.set_state(builder))
            time.sleep(5)


def simple_cl_interface():
    def choose_scene(lights):
        for light in lights:
            aio.run(light.turn_on())

        while True:
            print("Choose a scene by entering its number or name (case insensitive)")
            for scene_name, scene_number in SCENES.items():
                print(f"{scene_number}...{scene_name:^15}")

            scene_numbers = tuple(str(n) for n in SCENES.values())
            scene_names = tuple(SCENES.keys())
            valid_responses = scene_names + scene_numbers
            prompt = "Enter choice (0 to return) -> "
            while (user_resp := input(prompt).lower()) not in valid_responses:
                if user_resp == '0':
                    return
                print(f"{user_resp} is an invalid choice, check your spelling")

            if user_resp.isdigit():
                scene_id = int(user_resp)
            else:
                scene_id = SCENES[user_resp.lower()]

            builder = pwz.PilotBuilder(scene=scene_id, state=True)
            for light in lights:
                aio.run(light.set_state(builder))

    def set_brightness(lights):
        while True:
            prompt = "Enter brightness (-1 to return) -> "
            while (not (user_resp := input(prompt)).isdigit()) or int(user_resp) not in range(266):
                if user_resp == '-1':
                    return
                print(f"{user_resp} is invalid input, enter a number from 0-255")
            else:
                brightness = int(user_resp)

            builder = pwz.PilotBuilder(brightness=brightness)
            for light in lights:
                aio.run(light.set_state(builder))

    def choose_room(home):
        rooms = home.rooms
        print("Choose a room by entering its number")
        for order, room in enumerate(rooms, start=1):
            print(f"{order}...{room.name:^15}")

        room_numbers = tuple(str(n) for n in range(1, len(rooms) + 1))
        prompt = "Enter choice (0 to return) -> "
        while (user_resp := input(prompt).lower()) not in room_numbers:
            if user_resp == '0':
                return
            print(f"{user_resp} is an invalid choice, check your spelling")

        if user_resp.isdigit():
            return rooms[int(user_resp) - 1]

    home_model = Home.from_save('3827676')
    room = choose_room(home_model)
    lights = room.lights
    while True:
        choose_scene(lights)
        set_brightness(lights)


simple_cl_interface()
