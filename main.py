from updatesparser import UpdateParser
from utilities.comparator import compare_to_json
from utilities.sendmessages import send_update
import asyncio

async def main():
    # parser = UpdateParser("http://eng.cu.edu.eg/ar/credit-hour-system/")
    parser = UpdateParser("https://eng.cu.edu.eg/wp-json/wp/v2/pages/1034")
    new_updates = compare_to_json(parser.divinfo_list)
    if new_updates:
        print("New announcements found")
        for update in reversed(new_updates):
            await send_update(update)
    else:
        print("No new updates found.")

if __name__ == "__main__":
    asyncio.run(main())