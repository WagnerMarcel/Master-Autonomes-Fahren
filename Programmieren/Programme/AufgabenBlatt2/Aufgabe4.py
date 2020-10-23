# Aufgabenblatt 2 Aufgabe 4
# Pandas ist ein leistungsfähiges Werkzeug zur Datenanalyse und Visualisierung. 
# In dieser Aufgabe soll Pandas zur Analyse des Google Play Store-Datensatzes verwendet werden. 
# Eine Kopie findensie im Canvas, das Original stammt vonhttps://www.kaggle.com/lava18/google-play-store-apps/.Bearbeiten sie die Visualisierungen in den folgenden Punkten:
# 1. Laden Sie die Datensätze googleplaystoreuserreviews.csv und googleplaystore.csv als Pandas DataFrames. Verwenden Sie die Funktion pd.readcsv().
# 2. Löschen Sie jede Rezension, die weder eine TranslatedReview noch ein Sentiment enthält. Die Funktion pd.dropna ist dabei hilfreich.
# 3. Entfernen Sie alle Anwendungen, deren Rating ungültig ist (>5)
# 4. Erstellen Sie ein Tortendiagramm mit den Android Ver Anforderungen für die verschiedenen Anwendungen. 
#    Fassen Sie alle Versionen, die weniger als 5% der gesamten Anwendungen ausmachen, in einer einzigen Kategorie Sonstige zusammen. 
#    Verwenden Sie dieFunktiondf.valuecounts()
# 5. Erstellen Sie ein ähnliches Tortendiagramm für app Category. Gruppieren Sie in diesemFall Kategorien, die weniger als 3% der Anwendungen ausmachen.
# 6. Zeigen Sie Histogramme der Ratings und Reviews über alle Apps hinweg, mit jeweils 20 Klassen.
# 7. Kombinieren Sie die beiden DataFrames zu einem einzigen, basierend auf den AppNamen. 
#    Sie sollten sicherstellen, dass alle Anwendungen aus dem Apps-DataFrame beibehaltenwerden und keine darüber hinausgehende Anwendung hinzugefügt wird. 
#    Die Funktion pd.merge kann das tun.
# 8. Gruppieren Sie die SentimentDaten nach gerundeter Rating und erstellen Sie ein Balkendiagramm, in dem Sie die verschiedenen Bewertungen gruppiert nach Rating anzeigen.
#    Verwenden Sie pd.groupby,np.round und df.unstack.
# Author: Marcel Wagner
# Studiengang: Master Autonomes Fahren
# Datum: 23.10.2020

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

playstore = pd.read_csv('google_playstore/googleplaystore.csv')
reviews = pd.read_csv('google_playstore/googleplaystore_user_reviews.csv')
reviews.dropna(subset=['Sentiment', 'Translated_Review'], thresh=2, inplace=True)
playstore = playstore[playstore['Rating'] <= 5]
# print(playstore.columns.values)
# print(reviews.columns.values)

# 4.
androidVersions = playstore['Android Ver'].value_counts(normalize=True)
androidVersionsSonst = 0
androidVersionsLabel = []
androidVersionsValue = []
for index, value in androidVersions.items():
   if value < 0.05:
      androidVersionsSonst = androidVersionsSonst + value
   else:
      androidVersionsLabel.append(str(index))
      androidVersionsValue.append(value)
androidVersionsLabel.append(str('Sonstige'))
androidVersionsValue.append(androidVersionsSonst)

ax1 = plt.subplot(2,2,1)
ax1.pie(androidVersionsValue, labels=androidVersionsLabel)

# 5.
appCategory = playstore['Category'].value_counts(normalize=True)
appCategorySonst = 0
appCategoryLabel = []
appCategoryValue = []
for index, value in appCategory.items():
   if value < 0.03:
      appCategorySonst = appCategorySonst + value
   else:
      appCategoryLabel.append(str(index))
      appCategoryValue.append(value)
appCategoryLabel.append(str('Sonstige'))
appCategoryValue.append(appCategorySonst)

ax2 = plt.subplot(2,2,2)
ax2.pie(appCategoryValue, labels=appCategoryLabel)

# 6.
ax3 = plt.subplot(2,2,3)
ax3.hist(playstore['Rating'], bins=20)
print(playstore['Reviews'])
ax4 = plt.subplot(2,2,4)
# Dieses Histogramm dauert ewig und sieht anders aus als bei ihm aber ich check nicht, was er genau von uns will
# ax4.hist(playstore['Reviews'], bins=20)

# 7.
merged = playstore.merge(reviews, left_on='App', right_on='App')

# 8.
subset = merged[['Sentiment', 'Rating']].copy()
subset['Count'] = 1
aggregatedSubset = subset.round(0).groupby(['Rating', 'Sentiment']).count().unstack()
aggregatedSubset.plot.bar()


plt.show()