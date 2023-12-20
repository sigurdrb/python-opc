import asyncio

from asyncua import Client, ua

url = "opc.tcp://localhost:4840"
namespace = "CODESYSSPV3/3S/IecVarAccess"


async def main_client():

    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        node = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL_Modbus.Mb_Tank01_ManualDensity")
        var = await node.get_value()
        print(var)
        
        node2 = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL_Modbus.Tank_01_Active")
        await node2.write_value(True, ua.Boolean)




if __name__ == "__main__":
    asyncio.run(main_client())