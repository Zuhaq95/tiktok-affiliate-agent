from ai.creator_normalizer import Normalizer

print("Followers")
print("----------------")
print(Normalizer.followers("11.7K"))
print(Normalizer.followers("250"))
print(Normalizer.followers("1.2M"))

print("\nGMV")
print("----------------")
print(Normalizer.gmv("£174K"))
print(Normalizer.gmv("£2.5M"))
print(Normalizer.gmv("£950"))

print("\nItems Sold")
print("----------------")
print(Normalizer.items_sold("8.1K"))
print(Normalizer.items_sold("340"))

print("\nViews")
print("----------------")
print(Normalizer.avg_views("3.6K"))
print(Normalizer.avg_views("1.8M"))

print("\nEngagement")
print("----------------")
print(Normalizer.engagement("0.3%"))
print(Normalizer.engagement("15%"))