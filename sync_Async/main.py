import asyncio
import aiofiles

async def read_file(file_path):
    print("1")
    async with aiofiles.open(file_path, mode='r') as file:
        contents = await file.read()
        print(contents)
    print("2")

filename = "test.txt"

asyncio.run(read_file(filename))
