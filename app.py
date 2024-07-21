import ewelink, time
from ewelink import Client, DeviceOffline
import paho.mqtt.client as mqtt

import os
from dotenv import load_dotenv

load_dotenv()

mqtt_hostname = os.getenv("MQTT_HOSTNAME")
mqtt_port = os.getenv("MQTT_PORT")
mqtt_user = os.getenv("MQTT_USER")
mqtt_password = os.getenv("MQTT_PASSWORD")
ewelink_user = os.getenv("EWELINK_USER")
ewelink_password= os.getenv("EWELINK_PASSWORD")
ewelink_device_id = os.getenv("EWELINK_DEVICE_ID")

@ewelink.login(ewelink_password, ewelink_user,region="eu")
async def main(client: Client):
    print(client.region)
    print(client.user.info)
    print(client.devices)
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id="ewelink")
    mqttc.username_pw_set(username=mqtt_user,password=mqtt_password)
    mqttc.connect(mqtt_hostname, int(mqtt_port), 60)
    mqttc.loop_start()

    while True:
        await client.update()
        device = client.get_device(ewelink_device_id) #single channel device
        msg_humid = mqttc.publish("ewelink/THR320D/humidity", device.params.get("currentHumidity"), qos=1)
        msg_temp = mqttc.publish("ewelink/THR320D/temperature", device.params.get("currentTemperature"), qos=1)
        msg_switch = mqttc.publish("ewelink/THR320D/switch", device.state.value , qos=1)

        time.sleep(15)
        msg_humid.wait_for_publish(5)
        msg_temp.wait_for_publish(5)
        msg_switch.wait_for_publish(5)