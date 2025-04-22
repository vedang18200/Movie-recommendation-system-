# import requests

# response = requests.get("https://api.themoviedb.org/3/search/movie", params={
#     "api_key": "073988d015c80aad628573a7de0314d5",
#     "query": "Inception"
# }, timeout=10)  # Added timeout for clearer error

# print(response.status_code)
# print(response.json())


# import requests

# proxies = {
#     "http": "http://51.79.50.31:9300",
#     "https": "http://51.79.50.31:9300",
# }

# try:
#     res = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
#     print("🟢 Proxy works! IP:", res.json())
# except Exception as e:
#     print("❌ Proxy test failed:", e)

from imdb import IMDb

ia = IMDb()

def get_poster(title):
    results = ia.search_movie(title)
    if results:
        movie = results[0]
        ia.update(movie)
        return movie.get('cover url')
    return None

print(get_poster("Chaava"))

