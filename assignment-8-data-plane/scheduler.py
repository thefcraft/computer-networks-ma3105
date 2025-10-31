from typing import NamedTuple, Literal,  AsyncIterator, Callable, Awaitable
from enum import IntEnum
import heapq
import asyncio

class Priority(IntEnum):
    HIGH = 0
    MEDIUM = 1
    LOW = 2

class Packet(NamedTuple):
    priority: Priority
    source_ip: str
    dest_ip: str
    payload: str
    
async def fifo_scheduler(packets: AsyncIterator[Packet | None], pkt_reader_callback: Callable[[Packet], Awaitable[None]], maxsize: int = 1024):
    """This function simulates a First-Come, First-Served (FCFS/FIFO) scheduler."""
    pkt_queue: asyncio.Queue[Packet | None] = asyncio.Queue(maxsize=maxsize)
    async def enque_task_fn():
        async for pkt in packets:
            if pkt is None: 
                return await pkt_queue.put(None)
            try:
                pkt_queue.put_nowait(pkt)
            except asyncio.QueueFull:
                print("WARNING!: queue overflow.")
        return await pkt_queue.put(None)
    async def deque_task_fn():
        while (pkt := await pkt_queue.get()) is not None:
            await pkt_reader_callback(pkt)
        
    await asyncio.gather(
        enque_task_fn(),
        deque_task_fn()
    )

async def priority_scheduler(packets: AsyncIterator[Packet | None], pkt_reader_callback: Callable[[Packet], Awaitable[None]], maxsize: int = 1024):
    """This function simulates a Priority Scheduler."""
    pkt_heap: list[Packet] = []
    pkt_wait: asyncio.Queue[Literal[True] | None] = asyncio.Queue(maxsize=maxsize)
    async def enque_task_fn():
        async for pkt in packets:
            if pkt is None: 
                return await pkt_wait.put(None)
            try:
                pkt_wait.put_nowait(True)
                heapq.heappush(pkt_heap, pkt) # Insert packet into the heap with priority
            except asyncio.QueueFull:
                print("WARNING!: heap overflow.")
        return await pkt_wait.put(None)
                
    async def deque_task_fn():
        while True:
            if await pkt_wait.get() is None: break
            pkt = heapq.heappop(pkt_heap)
            await pkt_reader_callback(pkt)

    await asyncio.gather(
        enque_task_fn(),
        deque_task_fn()
    )


async def scheduler_fill_first(packets: list[Packet], 
                               scheduler: Callable[[AsyncIterator[Packet | None], Callable[[Packet], Awaitable[None]]], Awaitable[None]]) -> list[Packet]:
    fill_event = asyncio.Event()
    async def packet_stream():
        for pkt in packets:
            yield pkt
        fill_event.set()
    result: list[Packet] = []
    async def pkt_reader_callback(pkt: Packet):
        await fill_event.wait() # wait for stream to end
        result.append(pkt)
    await scheduler(packet_stream(), pkt_reader_callback)
    return result

async def main():
    packets = [
        Packet(source_ip="192.168.1.1", dest_ip="192.168.2.1", payload="Data Packet 1", priority=Priority.LOW),
        Packet(source_ip="192.168.1.2", dest_ip="192.168.2.2", payload="Data Packet 2", priority=Priority.LOW),
        Packet(source_ip="192.168.3.1", dest_ip="192.168.4.1", payload="VOIP Packet 1", priority=Priority.HIGH),
        Packet(source_ip="192.168.5.1", dest_ip="192.168.6.1", payload="Video Packet 1", priority=Priority.MEDIUM),
        Packet(source_ip="192.168.7.1", dest_ip="192.168.8.1", payload="VOIP Packet 2", priority=Priority.HIGH),
    ]
    
            
    print("Running FIFO Scheduler:")
    for pkt in await scheduler_fill_first(packets, fifo_scheduler):
        print(pkt)
    
    print("\nRunning Priority Scheduler:")
    for pkt in await scheduler_fill_first(packets, priority_scheduler):
        print(pkt)
        

if __name__ == "__main__":
    # asyncio.run(main())
    # quit()

    import unittest

    class TestScheduler(unittest.TestCase):
        def setUp(self):
            self.packets = [
                Packet(source_ip="192.168.1.1", dest_ip="192.168.2.1", payload="Data Packet 1", priority=Priority.LOW),
                Packet(source_ip="192.168.1.2", dest_ip="192.168.2.2", payload="Data Packet 2", priority=Priority.LOW),
                Packet(source_ip="192.168.3.1", dest_ip="192.168.4.1", payload="VOIP Packet 1", priority=Priority.HIGH),
                Packet(source_ip="192.168.5.1", dest_ip="192.168.6.1", payload="Video Packet 1", priority=Priority.MEDIUM),
                Packet(source_ip="192.168.7.1", dest_ip="192.168.8.1", payload="VOIP Packet 2", priority=Priority.HIGH),
            ]

        def test_fifo_scheduler(self):
            expected_order = [
                pkt.payload for pkt in self.packets
            ]
            results = [
                result.payload
                for result in asyncio.run(scheduler_fill_first(self.packets, fifo_scheduler))
            ]
            self.assertEqual(results, expected_order)

        def test_priority_scheduler(self):
            expected_order = [
                pkt.payload for pkt in sorted(
                    self.packets, 
                    key=lambda pkt: pkt.priority
                )
            ]
            results = [
                result.payload
                for result in asyncio.run(scheduler_fill_first(self.packets, priority_scheduler))
            ]
            self.assertEqual(results, expected_order)

    unittest.main()
