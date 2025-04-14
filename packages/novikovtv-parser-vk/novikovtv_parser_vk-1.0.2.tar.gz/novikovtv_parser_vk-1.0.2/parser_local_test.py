# import asyncio
# import os
# from dotenv import load_dotenv
#
# from novikovtv_parser_vk.parser.main import make_csv_text
#
# load_dotenv()
# async def do_parse():
#     login = os.getenv("LOGIN")
#     password = os.getenv("PASSWORD")
#     max_communities = int(os.getenv("MAX_COMMUNITIES"))
#     web_driver_path = os.getenv("WEB_DRIVER_PATH")
#     chrome_path = os.getenv("CHROME_PATH")
#     search_query = 'Novikov TV'
#
#     csv_text = await make_csv_text(
#         web_driver_path,
#         chrome_path,
#         login,
#         password,
#         search_query,
#         max_communities
#     )
#
#     print(csv_text)
#
# asyncio.run(do_parse())