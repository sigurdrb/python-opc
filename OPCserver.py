import asyncio
import logging

from asyncua import Server, ua, Client
from asyncua.common.methods import uamethod


url = "opc.tcp://localhost:4840"
namespace = "CODESYSSPV3/3S/IecVarAccess"


@uamethod
def func(parent, value):
    return value * 2


async def server():
    _logger = logging.getLogger(__name__)
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://127.0.0.15:4840")

    # set up our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, "MyObject")
    myvar = await myobj.add_variable(idx, "MyVariable", 6.7)
    myvar2 = await myobj.add_variable(idx, "MyVariable2", 10000)
    # Set MyVariable to be non writable by clients
    await myvar.set_writable(False)
    await myvar2.set_writable(True)
    await server.nodes.objects.add_method(
        ua.NodeId("ServerMethod", idx),
        ua.QualifiedName("ServerMethod", idx),
        func,
        [ua.VariantType.Int64],
        [ua.VariantType.Int64],
    )
    _logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1)
            new_val = await myvar.get_value() + 0.1
            _logger.info("Set value of %s to %.1f", myvar, new_val)
            await myvar.write_value(new_val)



async def client():

    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        node = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.PLC_PRG.c")
        var = await node.get_value()
        print(var)
        
        node2 = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.PLC_PRG.a")
        await node2.write_value(11, ua.Int16)

async def main():
    results = await asyncio.gather(server(), client())



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
