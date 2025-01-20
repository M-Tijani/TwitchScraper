import asyncio
from scrap import askfortwitchcategory

async def main():
    print("Please enter the category you want to scrap: ")
    textinput = input()
    await askfortwitchcategory(textinput)

if __name__ == "__main__":
    asyncio.run(main())
