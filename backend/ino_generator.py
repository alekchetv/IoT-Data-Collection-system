from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import json
from models import sensor_list
from sensors.repository import SensorTypeREPO
import asyncio
from devices.schemas import Device
from config import VITE_IP_HOST
import codecs
from sensors.schemas import Sensor


env = Environment(
    loader=FileSystemLoader(".")
)


async def json_pin_generate(device: Device):
    file = codecs.open("sensors.json", "r", "utf_8_sig")
    content = file.read()
    sensor_list = json.loads(content)
    dic_sen = {
        "Углекислый газ": "pin_number1",
        "Инфракрасный": "pin_number2",
        "Температура": "pin_number3",
        "Влажность": "pin_number3",
        "Угарный газ": "pin_number4",
        "Пары спирта": "pin_number5",
        "Расстояние": "pin_number6",
    }

    template = env.get_template("sensors.json")
    print(device.sensors)
    types_in_query = []
    tmp_dic_pins = {}
    for sensor in device.sensors:
        print(sensor)
        for sensor_code in sensor_list:
            type = await SensorTypeREPO.find_by_id(sensor.sensor_type)
            if sensor_code["sensor_name"] == type.sensor_name:
                tmp_dic_pins[dic_sen[type.sensor_name]] = sensor.pin
                types_in_query.append(type.sensor_name)
                print(types_in_query)
    print(tmp_dic_pins)
    rendered_page = template.render(**tmp_dic_pins)
    with open('sensors_with_pins.json', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    # With Pins
    code_glob_list = []
    code_setup_list = []
    code_loop_list = []
    file = codecs.open("sensors_with_pins.json", "r", "utf_8_sig")
    content = file.read()
    sensor_list = json.loads(content)
    for type in types_in_query:
        for sensor in sensor_list:
            if sensor["sensor_name"] == type:
                code_glob_list.append(sensor["code"]["glob"])
                code_setup_list.append(sensor["code"]["setup"])
                code_loop_list.append(sensor["code"]["loop"])
    print(code_loop_list)
    # main.cpp generating ...
    template = env.get_template("code_sample.txt")
    rendered_page = template.render(
        code_glob_list=code_glob_list, code_setup_list=code_setup_list, code_loop_list=code_loop_list)
    with open('./pio_diplom/src/main.cpp', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    cpp_upload(device.ip_address)


def cpp_upload(ip_address: str):
    template = env.get_template("upload_script.bat")
    rendered_page = template.render(ip_address=ip_address)
    with open('upload_script_ip.bat', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    os.system('start upload_script_ip.bat')


async def script():
    db = await SensorTypeREPO.find_all()
    db_sensors = []
    for model in db:
        db_sensors.append(model.sensor_name)
    sensors = ["Температура", "Влажность", "Угарный газ",
               "Расстояние", "Пары спирта", "Инфракрасный", "Углекислый газ"]
    for sensor in sensors:
        if sensor not in db_sensors:
            await SensorTypeREPO.add(sensor_name=sensor)
