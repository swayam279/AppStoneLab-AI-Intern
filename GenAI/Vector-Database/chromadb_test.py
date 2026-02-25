import chromadb

db_path = r"D:\AppStoneLab\GenAI\Vector-Database"
client = chromadb.PersistentClient(path = db_path)

# Created collection
collection = client.create_collection(name = "Anime")
print("Collection Created : ",collection.name)

# added documents and ids.
collection.add(
documents=[
"Naruto is my first anime.",
"Naruto's second sequal is Shipudden.",
"Deathnote has best mystery element in all the anime",
"Levi is indeed a monster."
],
ids = ["Naruto","Naruto Shippuden","Deathnote","Attack on titans"]
)

res = collection.query(
query_texts= ['recommend me an action anime'],
n_results=2
)

print(res)