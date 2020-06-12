import recommendation
prefs=recommendation.loadMovieLens()
#print(prefs['87'])
#print(recommendation.getRecommendations(prefs,'87')[0:30])
itemsim = recommendation.calculateSimilarItems(prefs,n=50)
print(recommendation.getRecommendedItems(prefs,itemsim,'87')[0:30])