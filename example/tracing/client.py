import uuid
import asyncio
import logging

from grpclib.client import Channel
from grpclib.events import listen, SendRequest

from helloworld.helloworld_pb2 import HelloRequest
from helloworld.helloworld_grpc import GreeterStub


log = logging.getLogger(__name__)


async def send_request(event: SendRequest):
    request_id = event.payload['x-request-id'] = str(uuid.uuid4())
    log.info('Generated Request ID: %s', request_id)


async def main():
    loop = asyncio.get_event_loop()
    channel = Channel('127.0.0.1', 50051, loop=loop)
    listen(channel, SendRequest, send_request)

    stub = GreeterStub(channel)
    response = await stub.SayHello(HelloRequest(name='World'))
    print(response.message)

    channel.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
