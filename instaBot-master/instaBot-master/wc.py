from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
String="aass aasss salsja ssaakk ssaakk ssaakk"
wordcloud=WordCloud(stopwords=STOPWORDS,background_color='white',width=1200,height=1000).generate(String)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
