import tweepy
import pandas as pd
import os
import re
from datetime import datetime
from datetime import timedelta
import dateutil.parser as parser
import requests
import csv

# Replace these with your own API keys and secrets
auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth, wait_on_rate_limit=True)

#api by countapi
countapiID = os.environ['COUNTAPI_TOKEN']
countapi_workspace = "riccardocapelli1.github.io"
countapilink = "http://api.countapi.xyz/hit/"+ countapi_workspace +"/"+ countapiID +"?callback=websiteVisits"
countapi = countapilink.replace(countapilink,f'<script async src="{countapilink}"></script>')

#df Crea una lista dei profili di cui vuoi scaricare i tweet
profiles = ["AirbnbEng","AirbyteHQ","alteryx","anacondainc","ansible","ApacheAirflow","ApacheArrow","ApacheCalcite","ApacheFlink","apachekafka","apachenifi","ApacheParquet","ApachePinot","astronomerio","AtScale","awscloud","Azure","Azure_Synapse","BrooklynData","castordoc_data","ClickHouseDB","census","confluentinc","coursera","dagster","dask_dev","databricks","datacamp","datadoghq","dataddo","datafoldcom","datameer","dataquestio","dbt_labs","DeepMind","DeltaLakeOSS","Docker","druidio","duckdb","duckdblabs","elastic","expectgreatdata","fastdotai","fivetran","getdbt","github","gitlab","googlecloud","GoogleCloudTech","GoogleColab","grafana","HevoData","_hex_tech","HightouchData","hydradatabase","IBMData","Integrateio","jenkinsci","khanacademy","kaggle","kdnuggets","keboola","ksqlDB","kubernetesio","lightdash_devs","LogiAnalytics","mage_ai","mariadb","Materialize","meltanodata","meroxadata","fb_engineering","metabase","MetaphorData","MicroStrategy","ModeAnalytics","moderndatastack","motherduck","montecarlodata","MTL_Analytics","myadverity","MySQL","MuleSoft","neondatabase","NetflixEng","numpy_team","observablehq","openshift","pandas_dev","HitachiVantara","phdatainc","PinterestEng","plotlygraphs","DataPolars","popsql","PostgreSQL","MSPowerBI","PrefectIO","preset_data","prestodb","ProjectJupyter","PyData","ThePSF","qlik","RAPIDSai","realpython","retool","RiveryData","SAPBTP","SASsoftware","ScyllaDB","SkyviaService","singer_io","Sisense","SnowflakeDB","snowplow","SpotifyEng","SQLServer","starburstdata","stitch_data","streamlit","Supermetrics","tableau","Talend","Teradata","HashiCorp","TIBCO","thoughtspot","TDataScience","transformio","trinodb","TwitterEng","UberEng","udacity","y42dotcom","YellowfinBI","Workato"]
count=300

#df2 definire le keyword da cercare
keywords = ["BLOG","CERTIFICATION", "CONFERENCE", "COURSE", "EVENT", "PODCAST", "SUMMIT", "TRAINING","WEBINAR"]
keywords_conference = 'CONFERENCE|SUMMIT'
keywords_certificate = 'CERTIFICATION|COURSE|TRAINING'
keywords_generical = 'BLOG|EVENT|PODCAST|WEBINAR'

# Crea una lista vuota per i tweet
tweets = []
screen_name = []
# Scarica i tweet dei profili specificati
for profile in profiles:
    screen_name = profile
    for tweet in api.user_timeline(screen_name=screen_name, count=count, include_rts=False, tweet_mode="extended"):
        tweets.append([datetime.now(), tweet.created_at, tweet.created_at, tweet.user.screen_name, tweet.full_text])

# Crea un dataframe dei tweet scaricati
df = pd.DataFrame(tweets, columns=['Datetime_now','Created_at', 'Time', 'User', 'Tweet'])

#df Mappa la lista dei profili di cui vuoi scaricare i tweet
profiles_map = {"AirbnbEng":"Airbnb Engineer","AirbyteHQ":"Airbyte","alteryx":"Alteryx","anacondainc":"Anaconda","ansible":"Ansible","ApacheAirflow":"Apache Airflow","ApacheArrow":"Apache Arrow","ApacheCalcite":"Apache Calcite","ApacheFlink":"Apache Flink","apachekafka":"Apache Kafka","apachenifi":"Apache Nifi","ApacheParquet":"Apache Parquet","ApachePinot":"Apache Pinot","astronomerio":"Astronomer.io","AtScale":"AtScale","awscloud":"AWS Cloud","Azure":"Azure","Azure_Synapse":"Azure Synapse","BrooklynData":"Brooklyn Data","castordoc_data":"Castor","ClickHouseDB":"ClickHouse","census":"Census","confluentinc":"Confluent.io","coursera":"Coursera","dagster":"Dagster","dask_dev":"Dask","databricks":"Databricks","datacamp":"DataCamp","datadoghq":"Datadog","dataddo":"Dataddo","datafoldcom":"Datafold","datameer":"Datameer","dataquestio":"Dataquest","dbt_labs":"Dbt labs","DeepMind":"Deep Mind","DeltaLakeOSS":"Delta Lake","Docker":"Docker","druidio":"Druidio","duckdb":"Duck DB","duckdblabs":"Duck DB Labs","elastic":"Elastic","expectgreatdata":"Expect Great Data","fastdotai":"Fast.ai","fivetran":"Fivetran","getdbt":"Getdbt.com","github":"Github","gitlab":"Gitlab","googlecloud":"Google Cloud","GoogleCloudTech":"Google Cloud Tech","GoogleColab":"Google Colab","grafana":"Grafana","HevoData":"Hevo Data","_hex_tech":"Hex","HightouchData":"Hightouch Data","hydradatabase":"Hydra DB","IBMData":"IBM Data","Integrateio":"Integrate.io","jenkinsci":"Jenkins","khanacademy":"Khan Academy","kaggle":"Kaggle","kdnuggets":"Kdnuggets","keboola":"Keboola","ksqlDB":"Ksql","kubernetesio":"kubernetes.io","lightdash_devs":"Lightdash","LogiAnalytics":"Logi Analytics","mage_ai":"Mage.ai","mariadb":"Mariadb","Materialize":"Materialize","meltanodata":"Meltano","meroxadata":"Meroxa","fb_engineering":"Meta Engineer","metabase":"Metabase","MetaphorData":"Metaphor.io","MicroStrategy":"MicroStrategy","ModeAnalytics":"Mode","moderndatastack":"Moderndatastack.xyz","motherduck":"Motherduck","montecarlodata":"Montecarlo","MTL_Analytics":"Montreal Analytics","myadverity":"Myadverity","MySQL":"MySQL","MuleSoft":"MuleSoft","neondatabase":"Neon DB","NetflixEng":"Netflix Engineer","numpy_team":"Numpy","observablehq":"Observable","openshift":"Red Hat Openshift","pandas_dev":"Pandas","HitachiVantara":"Pentaho","phdatainc":"Phdata","PinterestEng":"Pinterest Engineer","plotlygraphs":"Plotly","DataPolars":"Polars","popsql":"Popsql","PostgreSQL":"PostgreSQL","MSPowerBI":"PowerBI","PrefectIO":"Prefect.io","preset_data":"Preset","prestodb":"Presto DB","ProjectJupyter":"Jupyter","PyData":"Py Spark","ThePSF":"Python Foundation","qlik":"Qlik","RAPIDSai":"Rapids AI","realpython":"Real Python","retool":"Retool","RiveryData":"Rivery","SAPBTP":"SAP Analytics","SASsoftware":"SAS","ScyllaDB":"Scylla DB","SkyviaService":"Skyvia","singer_io":"singer.io","Sisense":"Sisense","SnowflakeDB":"Snowflake","snowplow":"Snowplow","SpotifyEng":"Spotify Engineer","SQLServer":"SQL Server","starburstdata":"Starburst","stitch_data":"Stitch","streamlit":"Streamlit","Supermetrics":"Supermetrics","tableau":"Tableau","Talend":"Talend","Teradata":"Teradata","HashiCorp":"Terraform","TIBCO":"Tibco","thoughtspot":"Thoughtspot","TDataScience":"Towards Data Science","transformio":"Transform","trinodb":"Trino DB","TwitterEng":"Twitter Engineer","UberEng":"Uber Engineer","udacity":"Udacity","y42dotcom":"Y42.com","YellowfinBI":"YellowfinBI","Workato":"Workato"}

profiles_weblink = {"AirbnbEng":"https://airbnb.io/","AirbyteHQ":"https://airbyte.io","alteryx":"https://alteryx.com","anacondainc":"https://anaconda.com","ansible":"https://www.ansible.com","ApacheAirflow":"https://airflow.apache.org","ApacheArrow":"https://arrow.apache.org","ApacheCalcite":"https://calcite.apache.org","ApacheFlink":"https://flink.apache.org","apachekafka":"https://kafka.apache.org","apachenifi":"https://nifi.apache.org","ApacheParquet":"https://parquet.apache.org","ApachePinot":"https://pinot.apache.org","astronomerio":"https://astronomer.io","AtScale":"https://atscale.com","awscloud":"https://aws.amazon.com","Azure":"https://azure.com","Azure_Synapse":"https://azure.com/synapse","BrooklynData":"https://brooklyndata.co","castordoc_data":"https://castordoc.com","ClickHouseDB":"https://clickhouse.tech","census":"https://getcensus.com","confluentinc":"https://confluent.io","coursera":"https://coursera.org","dagster":"https://dagster.io","dask_dev":"https://dask.org","databricks":"https://databricks.com","datacamp":"https://linktr.ee/datacamp","datadoghq":"https://datadoghq.com","dataddo":"https://dataddo.com","datafoldcom":"https://datafold.com","datameer":"https://datameer.com","dataquestio":"https://dataquest.io","dbt_labs":"https://getdbt.com","DeepMind":"https://deepmind.com","DeltaLakeOSS":"https://deltalake.io","Docker":"https://docker.com","druidio":"https://druid.io","duckdb":"https://duckdb.org","duckdblabs":"https://duckdb.org","elastic":"https://elastic.co","expectgreatdata":"https://expectgreatdata.com","fastdotai":"https://fast.ai","fivetran":"https://fivetran.com","getdbt":"https://getdbt.com","github":"https://github.com","gitlab":"https://gitlab.com","googlecloud":"https://cloud.google.com","GoogleCloudTech":"https://cloud.withgoogle.com","GoogleColab":"https://colab.research.google.com","grafana":"https://grafana.com","HevoData":"https://hevodata.com","_hex_tech":"https://hex.tech","HightouchData":"https://hightouchdata.com","hydradatabase":"https://hydra.so","IBMData":"https://ibm.com/analytics/data-science","Integrateio":"https://integrate.io","jenkinsci":"https://jenkins.io","khanacademy":"https://khanacademy.org","kaggle":"https://kaggle.com","kdnuggets":"https://kdnuggets.com","keboola":"https://keboola.com","ksqlDB":"https://confluent.io/ksql","kubernetesio":"https://kubernetes.io","lightdash_devs":"https://lightdash.dev","LogiAnalytics":"https://logianalytics.com","mage_ai":"https://mage.ai","mariadb":"https://mariadb.org","Materialize":"https://materialize.com","meltanodata":"https://meltano.com","meroxadata":"https://meroxa.com","fb_engineering":"https://facebook.com/engineering","metabase":"https://metabase.com","MetaphorData":"https://metaphor.io","MicroStrategy":"https://microstrategy.com","ModeAnalytics":"https://mode.com","moderndatastack":"https://moderndatastack.xyz","motherduck":"https://motherduck.io","montecarlodata":"https://montecarlodata.com","MTL_Analytics":"https://montrealanalytics.com","myadverity":"https://myadverity.com","MySQL":"https://mysql.com","MuleSoft":"https://mulesoft.com","neondatabase":"https://neon.tech","NetflixEng":"https://netflixtechblog.com/?gi=81bd8f10bde2","numpy_team":"https://numpy.org","observablehq":"https://observablehq.com","openshift":"https://openshift.com","pandas_dev":"https://pandas.pydata.org","HitachiVantara":"https://hitachivantara.com/en-us/home.html","phdatainc":"https://phdata.io","PinterestEng":"https://pinterestcareers.com","plotlygraphs":"https://plotly.com","DataPolars":"https://pola.rs","popsql":"https://popsql.com","PostgreSQL":"https://postgresql.org","MSPowerBI":"https://powerbi.microsoft.com","PrefectIO":"https://prefect.io","preset_data":"https://preset.io","prestodb":"https://prestodb.io","ProjectJupyter":"https://jupyter.org","PyData":"https://spark.apache.org","ThePSF":"https://python.org/psf","qlik":"https://qlik.com","RAPIDSai":"https://rapids.ai","realpython":"realpython.com","retool":"https://retool.com","RiveryData":"https://rivery.io","SAPBTP":"https://sap.com/sps","SASsoftware":"https://sas.com","ScyllaDB":"https://scylladb.com","SkyviaService":"https://skyvia.com","singer_io":"https://singer.io","Sisense":"https://sisense.com","SnowflakeDB":"https://snowflake.com","snowplow":"https://snowplow.io","SpotifyEng":"https://engineering.atspotify.com","SQLServer":"https://microsoft.com/en-us/sql-server","starburstdata":"https://starburst.io","stitch_data":"https://stitchdata.com","streamlit":"https://streamlit.io","Supermetrics":"https://supermetrics.com","tableau":"https://tableau.com","Talend":"https://talend.com","Teradata":"https://teradata.com","HashiCorp":"https://terraform.io","TIBCO":"https://tibco.com","thoughtspot":"https://thoughtspot.com","TDataScience":"https://towardsdatascience.com","transformio":"https://transform.co","trinodb":"https://trino.io","TwitterEng":"https://blog.twitter.com/engineering/","UberEng":"https://uber.com/blog/engineering/data/","udacity":"https://udacity.com","y42dotcom":"https://y42.com","YellowfinBI":"https://yellowfinbi.com","Workato":"https://workato.com"}

profiles_twitter = {"AirbnbEng":"https://twitter.com/AirbnbEng","AirbyteHQ":"https://twitter.com/AirbyteHQ","alteryx":"https://twitter.com/alteryx","anacondainc":"https://twitter.com/anacondainc","ansible":"https://twitter.com/ansible","ApacheAirflow":"https://twitter.com/ApacheAirflow","ApacheArrow":"https://twitter.com/ApacheArrow","ApacheCalcite":"https://twitter.com/ApacheCalcite","ApacheFlink":"https://twitter.com/ApacheFlink","apachekafka":"https://twitter.com/apachekafka","apachenifi":"https://twitter.com/apachenifi","ApacheParquet":"https://twitter.com/ApacheParquet","ApachePinot":"https://twitter.com/ApachePinot","astronomerio":"https://twitter.com/astronomerio","AtScale":"https://twitter.com/AtScale","awscloud":"https://twitter.com/awscloud","Azure":"https://twitter.com/Azure","Azure_Synapse":"https://twitter.com/Azure_Synapse","BrooklynData":"https://twitter.com/BrooklynData","castordoc_data":"https://twitter.com/castordoc_data","ClickHouseDB":"https://twitter.com/ClickHouseDB","census":"https://twitter.com/census","confluentinc":"https://twitter.com/confluentinc","coursera":"https://twitter.com/coursera","dagster":"https://twitter.com/dagster","dask_dev":"https://twitter.com/dask_dev","databricks":"https://twitter.com/databricks","datacamp":"https://twitter.com/datacamp","datadoghq":"https://twitter.com/datadoghq","dataddo":"https://twitter.com/dataddo","datafoldcom":"https://twitter.com/datafoldcom","datameer":"https://twitter.com/datameer","dataquestio":"https://twitter.com/dataquestio","dbt_labs":"https://twitter.com/dbt_labs","DeepMind":"https://twitter.com/DeepMind","DeltaLakeOSS":"https://twitter.com/DeltaLakeOSS","Docker":"https://twitter.com/Docker","druidio":"https://twitter.com/druidio","duckdb":"https://twitter.com/duckdb","duckdblabs":"https://twitter.com/duckdblabs","elastic":"https://twitter.com/elastic","expectgreatdata":"https://twitter.com/expectgreatdata","fastdotai":"https://twitter.com/fastdotai","fivetran":"https://twitter.com/fivetran","getdbt":"https://twitter.com/getdbt.com","github":"https://twitter.com/github","gitlab":"https://twitter.com/gitlab","googlecloud":"https://twitter.com/googlecloud","GoogleCloudTech":"https://twitter.com/GoogleCloudTech","GoogleColab":"https://twitter.com/GoogleColab","grafana":"https://twitter.com/grafana","HevoData":"https://twitter.com/HevoData","_hex_tech":"https://twitter.com/_hex_tech","HightouchData":"https://twitter.com/HightouchData","hydradatabase":"https://twitter.com/hydradatabase","IBMData":"https://twitter.com/IBMData","Integrateio":"https://twitter.com/Integrateio","jenkinsci":"https://twitter.com/jenkinsci","khanacademy":"https://twitter.com/khanacademy","kaggle":"https://twitter.com/kaggle","kdnuggets":"https://twitter.com/kdnuggets","keboola":"https://twitter.com/keboola","ksqlDB":"https://twitter.com/ksqlDB","kubernetesio":"https://twitter.com/kubernetesio","lightdash_devs":"https://twitter.com/lightdash_devs","LogiAnalytics":"https://twitter.com/LogiAnalytics","mage_ai":"https://twitter.com/mage_ai","mariadb":"https://twitter.com/mariadb","Materialize":"https://twitter.com/Materialize","meltanodata":"https://twitter.com/meltanodata","meroxadata":"https://twitter.com/meroxadata","fb_engineering":"https://twitter.com/fb_engineering","metabase":"https://twitter.com/metabase","MetaphorData":"https://twitter.com/MetaphorData","MicroStrategy":"https://twitter.com/MicroStrategy","ModeAnalytics":"https://twitter.com/ModeAnalytics","moderndatastack":"https://twitter.com/moderndatastack.xyz","motherduck":"https://twitter.com/motherduck","montecarlodata":"https://twitter.com/montecarlodata","MTL_Analytics":"https://twitter.com/MTL_Analytics","myadverity":"https://twitter.com/myadverity","MySQL":"https://twitter.com/MySQL","MuleSoft":"https://twitter.com/MuleSoft","neondatabase":"https://twitter.com/neondatabase","NetflixEng":"https://twitter.com/NetflixEng","numpy_team":"https://twitter.com/numpy_team","observablehq":"https://twitter.com/observablehq","pandas_dev":"https://twitter.com/pandas_dev","HitachiVantara":"https://twitter.com/HitachiVantara","phdatainc":"https://twitter.com/phdatainc","PinterestEng":"https://twitter.com/PinterestEng","plotlygraphs":"https://twitter.com/plotlygraphs","DataPolars":"https://twitter.com/DataPolars","popsql":"https://twitter.com/popsql","PostgreSQL":"https://twitter.com/PostgreSQL","MSPowerBI":"https://twitter.com/MSPowerBI","PrefectIO":"https://twitter.com/PrefectIO","preset_data":"https://twitter.com/preset_data","prestodb":"https://twitter.com/prestodb","ProjectJupyter":"https://twitter.com/ProjectJupyter","PyData":"https://twitter.com/PyData","ThePSF":"https://twitter.com/ThePSF","qlik":"https://twitter.com/qlik","RAPIDSai":"https://twitter.com/RAPIDSai","realpython":"https://twitter.com/realpython","retool":"https://twitter.com/retool","RiveryData":"https://twitter.com/RiveryData","SAPBTP":"https://twitter.com/SAPBTP","SASsoftware":"https://twitter.com/SASsoftware","ScyllaDB":"https://twitter.com/ScyllaDB","SkyviaService":"https://twitter.com/SkyviaService","singer_io":"https://twitter.com/singer_io","Sisense":"https://twitter.com/Sisense","SnowflakeDB":"https://twitter.com/SnowflakeDB","snowplow":"https://twitter.com/snowplow","SpotifyEng":"https://twitter.com/SpotifyEng","SQLServer":"https://twitter.com/SQLServer","starburstdata":"https://twitter.com/starburstdata","stitch_data":"https://twitter.com/stitch_data","streamlit":"https://twitter.com/streamlit","Supermetrics":"https://twitter.com/Supermetrics","tableau":"https://twitter.com/tableau","Talend":"https://twitter.com/Talend","Teradata":"https://twitter.com/Teradata","HashiCorp":"https://twitter.com/HashiCorp","TIBCO":"ttps://twitter.com/TIBCO","thoughtspot":"https://twitter.com/thoughtspot","TDataScience":"https://twitter.com/TDataScience","transformio":"https://https://twitter.com/transformio","trinodb":"https://twitter.com/trinodb","TwitterEng":"https://twitter.com/fb_engineering","UberEng":"https://twitter.com/UberEng","udacity":"https://twitter.com/udacity","y42dotcom":"https://twitter.com/y42dotcom","YellowfinBI":"https://twitter.com/YellowfinBI","Workato":"https://twitter.com/Workato"}

#Create mapping for display name, official website and twitter profile page
df["Profile"] = df["User"].map(profiles_map)
df["Profile_web"] = df["User"].map(profiles_weblink)
df["Profile_twi"] = df["User"].map(profiles_twitter)

# Calcola il primo giorno del mese precedente
df['Datetime_now'] = df['Datetime_now'].dt.strftime("%Y-%m-%d")
df['Datetime_now'] = (pd.to_datetime(df['Datetime_now']) - timedelta(days=60))

#Conversione della colonna Time
df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S').apply(lambda x: 'Posted on: ' + x.strftime('%Y-%m-%d') + '; at: ' + x.strftime('%H:%M'))

#Conversione della colonna User
df["User"] = df["User"].str.upper()

# create copy for argument
df_conference = df.copy()
df_certificate = df.copy()
df_generical = df.copy()

# Filtra il dataframe per i tweet che contengono le parole 
df = df[df['Tweet'].str.contains('Event|event|Conference|conference|Summit|summit|Podcast|podcast|Badge|badge|Certific|certific|Webinar|webinar|free resources|free courses|free learning')]
df = df[~df['Tweet'].str.contains('Of courses|of courses|event log|Event log|CDC event|event systems|event-driven|event data|Event data|event-time|event attribute|Steven|steven|Prevent|prevent|Event streaming|event streaming|streaming event|SSL certificate|end-to-end certificate|GhEvent|EventTimer|ISO 27001 certific')]

### FILTRI SUI DATAFRAME PER IL CONTENUTO DEI TWEET
# Filtra il dataframe per i tweet che contengono le parole "event" o "conference" nel testo
df_conference = df_conference[df_conference['Tweet'].str.contains('Conference|conference|Summit|summit')]
# Filtra i tweet che hanno data maggiore o uguale al primo giorno del mese precedente
df_conference['Created_at'] = df['Created_at'].dt.strftime("%Y-%m-%d")
df_conference['Datetime_now'] = df['Datetime_now'].dt.strftime("%Y-%m-%d")
# Filtra per ottenere le conferenze con date formato stringa
df_conference = df_conference[df_conference['Created_at'] >= df_conference['Datetime_now']]

# Filtra il dataframe per i tweet che contengono le parole "certificate" o "courses" nel testo
df_certificate = df_certificate[df_certificate['Tweet'].str.contains('Badge|badge|Certific|certific|free resources|free courses|free learning')]
df_certificate = df_certificate[~df_certificate['Tweet'].str.contains('Of courses|of courses|SSL certificate|end-to-end certificate|ISO 27001 certific')]

# Filtra il dataframe per i tweet che contengono le parole "event" o "conference" nel testo
df_generical = df_generical[df_generical['Tweet'].str.contains('Blog|blog|Event|event|Podcast|podcast|Webinar|webinar')]
df_generical = df_generical[~df_generical['Tweet'].str.contains('event log|Event log|CDC event|event systems|event-driven|event data|Event data|event-time|event attribute|Steven|steven|Prevent|prevent|Event streaming|event streaming|streaming event|GhEvent|EventTimer')]

# creare una copia del dataframe
df2 = df.copy()

# aggiungere una colonna "keyword" vuota
df2['keyword' ] = ""

# aggiungere una colonna "date" con la data e ora attuali
df2['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Filtra i tweet che hanno data maggiore o uguale al primo giorno del mese precedente
df2['Created_at'] = df2['Created_at'].dt.strftime("%Y-%m-%d")
df2['Datetime_now'] = df2['Datetime_now'].dt.strftime("%Y-%m-%d")

# Filtra per ottenere le conferenze con date formato stringa
df2 = df2[df2['Created_at'] >= df2['Datetime_now']]

# ciclo for per verificare se una stringa contiene una parola chiave
df2['Tweet'] = df2['Tweet'].str.upper()
for index, row in df2.iterrows():
    Tweet = row['Tweet']
    for keyword in keywords:
        if keyword in Tweet:
            df2.at[index, "keyword"] = keyword
            break

# eliminare righe senza keyword
df2 = df2[df2['keyword'] != ""]

# raggruppare i dati per data e keyword e contare le occorrenze
df2 = df2.groupby(['date', 'keyword']).size().reset_index(name='occurrence')

# salvare i dati in un file csv
df2.to_csv("tweet_data.csv", mode='a', header=False, index=False)

# Leggi i dati dal file CSV
columns=['date', 'keyword','occurrence'] 
df3 = pd.read_csv('tweet_data.csv', names=columns, header=None)

df3['date'] = pd.to_datetime(df3['date'])
df3['year_month'] = df3['date'].dt.to_period('M')
df3_grouped = df3.groupby(['year_month','keyword']).agg({'occurrence': 'max'}).reset_index()

df3_conference = df3_grouped.copy()
df3_conference = df3_conference[df3_conference['keyword'].str.contains(keywords_conference)]

df3_certification = df3_grouped.copy()
df3_certification = df3_certification[df3_certification['keyword'].str.contains(keywords_certificate)]

df3_generical = df3_grouped.copy()
df3_generical = df3_generical[df3_generical['keyword'].str.contains(keywords_generical)]

### df3_conference
# Crea una stringa vuota per i dati del grafico
chart_data_conference = ""

# Ciclo for per generare i dati del grafico per ogni keyword
for keyword in df3_conference["keyword"].unique():
    keyword_data = df3_conference[df3_conference["keyword"] == keyword]
    chart_data_conference += f"{{ label: '{keyword}', data: ["
    for index, row in keyword_data.iterrows():
        chart_data_conference += f"{{x: '{row['year_month']}', y: {row['occurrence']}}},"
    chart_data_conference = chart_data_conference[:-1] # Rimuovi l'ultima virgola
    chart_data_conference += "]},\n"

# Rimuovi l'ultima virgola e newline dai dati del grafico
chart_data_conference = chart_data_conference[:-2]
###
googleapi = "https://fonts.googleapis.com/css?family=Inconsolata|Roboto"
googleapi = googleapi.replace(googleapi,f'<link href="{googleapi}" rel="stylesheet" >')

###
# crea contenuto html principale
def make_link(text):
    # Cerca tutte le occorrenze di link nella stringa
    links = re.findall(r'(https?:\/\/\S+)', text)
    # Sostituisci ogni occorrenza di link con il link cliccabile
    for link in links:
        text = text.replace(link, f'<a href="{link}" target="_blank">{link}</a>')
    return text

# Crea una stringa vuota per il contenuto del file HTML
conferences = "conferences, events and summit"
certifications = "certification, courses and trainings"
generic = "blogs, podcasts and webinar"

# Crea una stringa vuota per il contenuto del file HTML
html_content = ""

# Aggiungi il contenuto iniziale del file HTML
html_content  = "<!DOCTYPE html>\n"
html_content += "<html>\n"
html_content += "<head>\n"
html_content += googleapi + "\n"
html_content += "  " + countapi + "\n"
html_content += "  <meta charset='utf-8'>\n"
html_content += "  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=yes'>\n"
html_content += "  <link rel='stylesheet' type='text/css' href='assets/style.css'>\n"
html_content += "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
html_content += "  <script src='assets/script.js'></script>\n"
html_content += "  <script src='assets/load.js'></script>\n"
html_content += "  <title>Data-stack-wall: the essential tool for data practitioners</title>\n"

html_content += "        <div class='container'>\n"
html_content += "                            <li><a href='index.html' class='active'>Conferences & Summit</a></li>\n"
html_content += "                            <li><a href='certificate.html'>Badges, Certificates & Trainings</a></li>\n"
html_content += "                            <li><a href='generic.html'>Blogs, Events, Podcasts & Webinars</a></li>\n"
html_content += "        </div>\n"

# Titolo all'html_content
html_content += "  <h1> Stay up-to-date with " + conferences + "</h1>\n"
html_content += "  <p>A tweet aggregator site of " + conferences + " that brings together valuable resources. Hope you enjoy ;) </p>\n"

# Aggiungi il codice per il grafico all'html_content
html_content += "<div class='container'>\n"
html_content += "<canvas id='myChart'></canvas>\n"
html_content += "</div>\n"
html_content += "  <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>\n"
html_content += "<script>\n"
html_content += "var ctx = document.getElementById('myChart').getContext('2d');\n"
html_content += "var myChart = new Chart(ctx, {\n"
html_content += "  type: 'line',\n"
html_content += "  data: {\n"
html_content += "    datasets: [\n"
html_content += chart_data_conference + "\n"
html_content += "    ]\n"
html_content += "  },\n"
html_content += "  options: {\n"
html_content += "    scales: {\n"
html_content += "      xAxes: [{\n"
html_content += "        type: 'time',\n"
html_content += "        time: {\n"
html_content += "           unit: 'month',\n"
html_content += "           displayFormats: {\n"
html_content += "            month: 'YYYY-MM'\n"
html_content += "           }\n"
html_content += "        }\n"
html_content += "      }],\n"
html_content += "      yAxes: [{\n"
html_content += "        ticks: {\n"
html_content += "          beginAtZero: true\n"
html_content += "        }\n"
html_content += "      }]\n"
html_content += "    }\n"
html_content += "  }\n"
html_content += "});\n"
html_content += "</script>\n"
html_content += "  <p>Last 60 days kewords tweeted by month</p>\n"
html_content += "</head>\n"
html_content += "<body>\n"

#, Crea un dizionario vuoto per gli utenti
users_dict = {}

# Utilizza un ciclo for per aggiungere gli utenti al dizionario e tenere traccia della loro posizione nell'HTML
pos = 0
for _, row in df_conference.iterrows():
    user = row["Profile"]
    if user not in users_dict:
        users_dict[user] = pos
        pos += 1

# Utilizza un ciclo for per creare un elenco di link agli utenti nell'HTML
html_content += "  <h3>List of Authors</h3>\n"
html_content += "  <ul>\n"
for user in users_dict:
    html_content += f"    <li><a href='#user{users_dict[user]}'>{user}</a></li>\n"
html_content += "  </ul>\n"

# Utilizza un ciclo for per iterare attraverso ogni riga del dataframe
current_user = df_conference.iloc[0]["Profile"]
html_content += f"  <h2 class='h2' style='text-transform: uppercase;' id='user{users_dict[current_user]}'>{current_user} </h2><br><a href='{row['Profile_web']}' target='_blank'>Official website</a><br><a href='{row['Profile_twi']}' target='_blank'>Twitter profile</a>\n"

for _, row in df_conference.iterrows():
    user = row["Profile"]
    if user != current_user:
        current_user = user
        
# Crea un'ancora per ogni utente nell'HTML
        html_content += f"  <h2 class='h2' style='text-transform: uppercase;' id='user{users_dict[user]}'>{user}</h2><br><a href='{row['Profile_web']}' target='_blank'>Official website</a><br><a href='{row['Profile_twi']}' target='_blank'>Twitter profile</a>\n"
    date = row["Time"]
    text = make_link(row["Tweet"])
    html_content += f" <h3 date='{date}'>{date}</h3>\n"
    html_content += f"  <p>{text}</p>\n"

html_content += "</body>\n"
html_content += "<footer>\n"
html_content += "  <p>Made with ❤️ for the community by Riccardo</p>\n"
html_content += "</footer>\n"
html_content += "</html>\n"

with open("./index.html", "w") as f:
    f.write(html_content)
###

### df3_conference
# Crea una stringa vuota per i dati del grafico
chart_data_certification = ""

# Ciclo for per generare i dati del grafico per ogni keyword
for keyword in df3_certification["keyword"].unique():
    keyword_data = df3_certification[df3_certification["keyword"] == keyword]
    chart_data_certification += f"{{ label: '{keyword}', data: ["
    for index, row in keyword_data.iterrows():
        chart_data_certification += f"{{x: '{row['year_month']}', y: {row['occurrence']}}},"
    chart_data_certification = chart_data_certification[:-1] # Rimuovi l'ultima virgola
    chart_data_certification += "]},\n"

# Rimuovi l'ultima virgola e newline dai dati del grafico
chart_data_certification = chart_data_certification[:-2]

###
# crea contenuto html principale
def make_link(text):
    # Cerca tutte le occorrenze di link nella stringa
    links = re.findall(r'(https?:\/\/\S+)', text)
    # Sostituisci ogni occorrenza di link con il link cliccabile
    for link in links:
        text = text.replace(link, f'<a href="{link}" target="_blank">{link}</a>')
    return text

# Crea una stringa vuota per il contenuto del file HTML
html_content = ""

# Aggiungi il contenuto iniziale del file HTML
html_content  = "<!DOCTYPE html>\n"
html_content += "<html>\n"
html_content += "<head>\n"
html_content += googleapi + "\n"
html_content += "  " + countapi + "\n"
html_content += "  <meta charset='utf-8'>\n"
html_content += "  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=yes'>\n"
html_content += "  <link rel='stylesheet' type='text/css' href='assets/style.css'>\n"
html_content += "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
html_content += "  <script src='assets/script.js'></script>\n"
html_content += "  <script src='assets/load.js'></script>\n"
html_content += "  <title>Data-stack-wall: the essential tool for data practitioners</title>\n"

html_content += "        <div class='container'>\n"
html_content += "                            <li><a href='index.html'>Conferences & Summit</a></li>\n"
html_content += "                            <li><a href='certificate.html' class='active'>Badges, Certificates & Trainings</a></li>\n"
html_content += "                            <li><a href='generic.html'>Blogs, Events, Podcasts & Webinars</a></li>\n"
html_content += "        </div>\n"

# Titolo all'html_content
html_content += "  <h1> Stay up-to-date with " + certifications + "</h1>\n"
html_content += "  <p>A tweet aggregator site of " + certifications + " that brings together valuable resources. Hope you enjoy ;) </p>\n"

# Aggiungi il codice per il grafico all'html_content
html_content += "<div class='container'>\n"
html_content += "<canvas id='myChart'></canvas>\n"
html_content += "</div>\n"
html_content += "  <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>\n"
html_content += "<script>\n"
html_content += "var ctx = document.getElementById('myChart').getContext('2d');\n"
html_content += "var myChart = new Chart(ctx, {\n"
html_content += "  type: 'line',\n"
html_content += "  data: {\n"
html_content += "    datasets: [\n"
html_content += chart_data_certification + "\n"
html_content += "    ]\n"
html_content += "  },\n"
html_content += "  options: {\n"
html_content += "    scales: {\n"
html_content += "      xAxes: [{\n"
html_content += "        type: 'time',\n"
html_content += "        time: {\n"
html_content += "           unit: 'month',\n"
html_content += "           displayFormats: {\n"
html_content += "            month: 'YYYY-MM'\n"
html_content += "           }\n"
html_content += "        }\n"
html_content += "      }],\n"
html_content += "      yAxes: [{\n"
html_content += "        ticks: {\n"
html_content += "          beginAtZero: true\n"
html_content += "        }\n"
html_content += "      }]\n"
html_content += "    }\n"
html_content += "  }\n"
html_content += "});\n"
html_content += "</script>\n"
html_content += "  <p>Last 60 days kewords tweeted by month</p>\n"
html_content += "</head>\n"
html_content += "<body>\n"

#, Crea un dizionario vuoto per gli utenti
users_dict = {}

# Utilizza un ciclo for per aggiungere gli utenti al dizionario e tenere traccia della loro posizione nell'HTML
pos = 0
for _, row in df_certificate.iterrows():
    user = row["Profile"]
    if user not in users_dict:
        users_dict[user] = pos
        pos += 1

# Utilizza un ciclo for per creare un elenco di link agli utenti nell'HTML
html_content += "  <h3>List of Authors</h3>\n"
html_content += "  <ul>\n"
for user in users_dict:
    html_content += f"    <li><a href='#user{users_dict[user]}'>{user}</a></li>\n"
html_content += "  </ul>\n"

# Utilizza un ciclo for per iterare attraverso ogni riga del dataframe
current_user = df_certificate.iloc[0]["Profile"]
html_content += f"  <h2 class='h2' style='text-transform: uppercase;' id='user{users_dict[current_user]}'>{current_user} </h2><br><a href='{row['Profile_web']}' target='_blank'>Official website</a><br><a href='{row['Profile_twi']}' target='_blank'>Twitter profile</a>\n"

for _, row in df_certificate.iterrows():
    user = row["Profile"]
    if user != current_user:
        current_user = user
        
# Crea un'ancora per ogni utente nell'HTML
        html_content += f"  <h2 class='h2' style='text-transform: uppercase;' id='user{users_dict[user]}'>{user}</h2><br><a href='{row['Profile_web']}' target='_blank'>Official website</a><br><a href='{row['Profile_twi']}' target='_blank'>Twitter profile</a>\n"
    date = row["Time"]
    text = make_link(row["Tweet"])
    html_content += f" <h3 date='{date}'>{date}</h3>\n"
    html_content += f"  <p>{text}</p>\n"

html_content += "</body>\n"
html_content += "<footer>\n"
html_content += "  <p>Made with ❤️ for the community by Riccardo</p>\n"
html_content += "</footer>\n"
html_content += "</html>\n"

with open("./certificate.html", "w") as f:
    f.write(html_content)
###

### df3_conference
# Crea una stringa vuota per i dati del grafico
chart_data_generical = ""

# Ciclo for per generare i dati del grafico per ogni keyword
for keyword in df3_generical["keyword"].unique():
    keyword_data = df3_generical[df3_generical["keyword"] == keyword]
    chart_data_generical += f"{{ label: '{keyword}', data: ["
    for index, row in keyword_data.iterrows():
        chart_data_generical += f"{{x: '{row['year_month']}', y: {row['occurrence']}}},"
    chart_data_generical = chart_data_generical[:-1] # Rimuovi l'ultima virgola
    chart_data_generical += "]},\n"

# Rimuovi l'ultima virgola e newline dai dati del grafico
chart_data_generical = chart_data_generical[:-2]

###
# crea contenuto html principale
def make_link(text):
    # Cerca tutte le occorrenze di link nella stringa
    links = re.findall(r'(https?:\/\/\S+)', text)
    # Sostituisci ogni occorrenza di link con il link cliccabile
    for link in links:
        text = text.replace(link, f'<a href="{link}" target="_blank">{link}</a>')
    return text

# Crea una stringa vuota per il contenuto del file HTML
html_content = ""

# Aggiungi il contenuto iniziale del file HTML
html_content  = "<!DOCTYPE html>\n"
html_content += "<html>\n"
html_content += "<head>\n"
html_content += googleapi + "\n"
html_content += "  " + countapi + "\n"
html_content += "  <meta charset='utf-8'>\n"
html_content += "  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=yes'>\n"
html_content += "  <link rel='stylesheet' type='text/css' href='assets/style.css'>\n"
html_content += "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
html_content += "  <script src='assets/script.js'></script>\n"
html_content += "  <script src='assets/load.js'></script>\n"
html_content += "  <title>Data-stack-wall: the essential tool for data practitioners</title>\n"

html_content += "        <div class='container'>\n"
html_content += "                            <li><a href='index.html'>Conferences & Summit</a></li>\n"
html_content += "                            <li><a href='certificate.html'>Badges, Certificates & Trainings</a></li>\n"
html_content += "                            <li><a href='generic.html' class='active'>Blogs, Events, Podcasts & Webinars</a></li>\n"
html_content += "        </div>\n"

# Titolo all'html_content
html_content += "  <h1> Stay up-to-date with " + generic + "</h1>\n"
html_content += "  <p>A tweet aggregator site of " + generic + " that brings together valuable resources. Hope you enjoy ;) </p>\n"

# Aggiungi il codice per il grafico all'html_content
html_content += "<div class='container'>\n"
html_content += "<canvas id='myChart'></canvas>\n"
html_content += "</div>\n"
html_content += "  <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>\n"
html_content += "<script>\n"
html_content += "var ctx = document.getElementById('myChart').getContext('2d');\n"
html_content += "var myChart = new Chart(ctx, {\n"
html_content += "  type: 'line',\n"
html_content += "  data: {\n"
html_content += "    datasets: [\n"
html_content += chart_data_generical + "\n"
html_content += "    ]\n"
html_content += "  },\n"
html_content += "  options: {\n"
html_content += "    scales: {\n"
html_content += "      xAxes: [{\n"
html_content += "        type: 'time',\n"
html_content += "        time: {\n"
html_content += "           unit: 'month',\n"
html_content += "           displayFormats: {\n"
html_content += "            month: 'YYYY-MM'\n"
html_content += "           }\n"
html_content += "        }\n"
html_content += "      }],\n"
html_content += "      yAxes: [{\n"
html_content += "        ticks: {\n"
html_content += "          beginAtZero: true\n"
html_content += "        }\n"
html_content += "      }]\n"
html_content += "    }\n"
html_content += "  }\n"
html_content += "});\n"
html_content += "</script>\n"
html_content += "  <p>Last 60 days kewords tweeted by month</p>\n"
html_content += "</head>\n"
html_content += "<body>\n"

#, Crea un dizionario vuoto per gli utenti
users_dict = {}

# Utilizza un ciclo for per aggiungere gli utenti al dizionario e tenere traccia della loro posizione nell'HTML
pos = 0
for _, row in df_generical.iterrows():
    user = row["Profile"]
    if user not in users_dict:
        users_dict[user] = pos
        pos += 1

# Utilizza un ciclo for per creare un elenco di link agli utenti nell'HTML
html_content += "  <h3>List of Authors</h3>\n"
html_content += "  <ul>\n"
for user in users_dict:
    html_content += f"    <li><a href='#user{users_dict[user]}'>{user}</a></li>\n"
html_content += "  </ul>\n"

# Utilizza un ciclo for per iterare attraverso ogni riga del dataframe
current_user = df_generical.iloc[0]["Profile"]
html_content += f"  <h2 class='h2' style='text-transform: uppercase;' id='user{users_dict[current_user]}'>{current_user} </h2><br><a href='{row['Profile_web']}' target='_blank'>Official website</a><br><a href='{row['Profile_twi']}' target='_blank'>Twitter profile</a>\n"

for _, row in df_generical.iterrows():
    user = row["Profile"]
    if user != current_user:
        current_user = user
        
# Crea un'ancora per ogni utente nell'HTML
        html_content += f"  <h2 class='h2' style='text-transform: uppercase;' id='user{users_dict[user]}'>{user}</h2><br><a href='{row['Profile_web']}' target='_blank'>Official website</a><br><a href='{row['Profile_twi']}' target='_blank'>Twitter profile</a>\n"
    date = row["Time"]
    text = make_link(row["Tweet"])
    html_content += f" <h3 date='{date}'>{date}</h3>\n"
    html_content += f"  <p>{text}</p>\n"

html_content += "</body>\n"
html_content += "<footer>\n"
html_content += "  <p>Made with ❤️ for the community by Riccardo</p>\n"
html_content += "</footer>\n"
html_content += "</html>\n"

with open("./generic.html", "w") as f:
    f.write(html_content)
###

# write countapi data in csv file
url = "https://api.countapi.xyz/get/"+ countapi_workspace +"/"+ countapiID +"/"
response = requests.get(url)
data = response.json()
value = data["value"]
now = datetime.now()

with open("countapi.csv", "a") as f:
    writer = csv.writer(f)
    writer.writerow([now, value])
    
