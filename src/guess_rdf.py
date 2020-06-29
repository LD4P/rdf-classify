__author__ = "Jeremy Nelson"

# from starlette.application import Starlette  # type: ignore
# import aiohttp  # type: ignore
# import asyncio
# import rdflib  # type: ignore
# from data_loader import process_predicates  # type: ignore


# async def get_rdf(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.read()
#
# app = Starlette()
#
# @app.route("/classify-rdf", methods=["GET"])
# async def classify_rdf(request):
#     rdf = await get_rdf(request.query_params[""])
#     graph = rdflib.ConjunctiveGraph()
#     graph.parse(data=rdf)
#
#     _,_,losses = learner.predict(img)
#     return JSONResponse({
#         "predictions": sorted(
#             zip(cat_learner.data.classes, map(float, losses)),
#             key=lambda p: p[1],
#             reverse=True
#         )
#     })
