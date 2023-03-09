import aiohttp
from datetime import datetime

baseUrl = "https://myflameboss.com/api/v4/"

class FlameBoss:

    def __init__(self, username=None, token=None, deviceId=None):
        if username is not None:
            self.header = {
                "X-API-TOKEN": token,
                "X-API-USERNAME": username,
                "X-API-VERSION": "4"
            }
            self.deviceId = deviceId
        else:
            self.header = {}
            self.deviceId = None
        
    async def getCurrentCookData(self):
        async with aiohttp.ClientSession(headers=self.header) as session:
            response = await session.get(f"{baseUrl}/cooks")
            currentCookId = (await response.json())["cooks"][0]["id"]

            response = await session.get(f"{baseUrl}/cooks/{currentCookId}")

            cookData = await response.json()
            currentStats = cookData["data"][cookData["data_cnt"]-1]

            currentStats["title"] = cookData["title"]

            if cookData["online"] is False:
                currentStats["probe_name_0"] = None
                currentStats["probe_name_1"] = None
                currentStats["probe_name_2"] = None
                currentStats["probe_name_3"] = None
                currentStats["online"] = cookData["online"]

                currentStats["sec"] = None

                currentStats["set_temp"] = None
                currentStats["pit_temp"] = None
                currentStats["meat_temp1"] = None
                currentStats["meat_temp2"] = None
                currentStats["meat_temp3"] = None

                currentStats["fan_dc"] = None
            else:
                currentStats["probe_name_0"] = cookData["probe_name_0"]
                currentStats["probe_name_1"] = cookData["probe_name_1"]
                currentStats["probe_name_2"] = cookData["probe_name_2"]
                currentStats["probe_name_3"] = cookData["probe_name_3"]
                currentStats["online"] = cookData["online"]

                currentStats["sec"] = datetime.fromtimestamp(currentStats["sec"])

                currentStats["set_temp"] = self.FixTemp(currentStats["set_temp"])
                currentStats["pit_temp"] = self.FixTemp(currentStats["pit_temp"])
                currentStats["meat_temp1"] = self.FixTemp(currentStats["meat_temp1"])
                currentStats["meat_temp2"] = self.FixTemp(currentStats["meat_temp2"])
                currentStats["meat_temp3"] = self.FixTemp(currentStats["meat_temp3"])

                currentStats["fan_dc"] = round(currentStats["fan_dc"] / 100)

            return currentStats

    async def setPitTargetTemp(self, temp: int):
        async with aiohttp.ClientSession(headers=self.header) as session:
            data = {
                "temp_tdc": round((temp - 32) / .18)
            }
            response = await session.post(f"https://myflameboss.com/api/v1/devices/{self.deviceId}/set_set_temp", data=data)
            return

    async def getToken(self, username, password):
        async with aiohttp.ClientSession() as session:
            data = {
                "session[login]": username,
                "session[password]": password,
            }
            response = await session.post(f"{baseUrl}/sessions", data=data)

            tokenData = await response.json()

            self.header = {
                "X-API-TOKEN": tokenData["auth_token"],
                "X-API-USERNAME": username,
                "X-API-VERSION": "4"
            }

            return tokenData

    async def getDeviceId(self):
        async with aiohttp.ClientSession() as session:
            
            response = await session.get(f"{baseUrl}/devices",headers=self.header)
            deviceData = await response.json()

            self.deviceId = deviceData["ip_devices"][0]["id"]

            return self.deviceId

    def FixTemp(self, temp):
        correctedTemp = round(.18 * temp + 32)
        if (correctedTemp < 0):
            return None
        else:
            return correctedTemp