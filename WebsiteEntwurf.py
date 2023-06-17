import streamlit as st
from streamlit_echarts import st_echarts
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import numpy as np
import sqlite3
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import time
import random
import datetime
from faker import Faker
fake = Faker()
from streamlit_echarts import st_echarts
import os




def home_page():

    tab1, tab2, tab3 = st.tabs(["📈 Deskriptive Analyse", "💬 Text Analyse", "😃 Sentimentanalyse"])
    
    #Datenvorbereitung

    # Datenbank-Verbindung herstellen

    current_directory = os.getcwd()

    database_filename = 'database.db'

    database_path = os.path.join(current_directory, database_filename)

    conn = sqlite3.connect(database_path)

    #conn = sqlite3.connect(r'C:\Users\Alex\Desktop\Business\Data Science Bots\Amazon Scraping Projekt\Schreib Vortrag\databaseV2.0.db')

    # Datenbank lesen
    df = pd.read_sql_query("SELECT * from price", conn)
    
    with tab1:
        
        #Anfang Balkendiagramm-----------------
        # Verarbeitung der Daten für das dritte Diagramm
        rating_counts = df['rating'].value_counts(sort=False).head(10).sort_index().astype(float)

        # Umwandlung des Series-Objekts in eine Liste
        rating_counts_values = rating_counts.values.tolist()

        # Umwandlung des Index (Rating) in eine Liste
        rating_values = [float(x) for x in rating_counts.index.tolist()]

        option3 = {
        "title": {
            "text": 'Kundenrezensionen PS5',
            "left": 'center',
            "top": 20,
            "textStyle": {
            "color": '#fff'
            }
        },
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
            "type": 'shadow'
            }
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": True
        },
        "xAxis": [
            {
            "type": 'value',
            "name": 'Anzahl',
            "axisLabel": {
                "color": '#fff'
            }
            }
        ],
        "yAxis": [
            {
            "type": 'category',
            "data": rating_values,
            "axisTick": {
                "alignWithLabel": True
            },
            "axisLabel": {
                "color": '#fff'
            }
            }
        ],
        "series": [
            {
            "name": 'Anzahl der Bewertungen',
            "type": 'bar',
            "data": rating_counts_values,
            "label": {
                "show": True,
                "position": 'right',
                "color": '#fff'
            }
            }
        ]
        }

        st_echarts(options=option3, height="600px", key="unique_key_rating_counts")

        #Ende Balkendiagramm----------------------------------------------------------------


        #Anfang Boxplot -----------------------------------------------------------------------------------

        # Ihre Datenbereinigung und Aggregation hier:
        mean_rating = df['rating'].mean()
        median_rating = df['rating'].median()
        mode_rating = df['rating'].mode()[0]

        # Interaktiver Boxplot für Ratings mit 0-100% Whiskers (entspricht min und max Wert)
        fig1 = go.Figure()
        fig1.add_trace(go.Box(x=df['rating'], quartilemethod="inclusive", name=""))

        # Arithmetisches Mittel, Median und Modus hinzufügen
        fig1.add_trace(go.Scatter(x=[mean_rating, median_rating, mode_rating], y=[0.5, 0.5, 0.5], mode='markers',
                                marker_symbol=['diamond', 'square', 'triangle-up'], marker_color=['red', 'green', 'blue'], 
                                marker_size=[12, 12, 12], name="", hovertemplate=[
                                    f"Arithmetisches Mittel: {mean_rating}",
                                    f"Median: {median_rating}",
                                    f"Modus: {mode_rating}",
                                ]))

        # Achsenbeschriftungen, Titel und Layout anpassen
        fig1.update_layout(
            title="Boxplot der Ratings",
            xaxis_title="Rating",
            yaxis=dict(showticklabels=False, showgrid=False), # Keine Y-Achsenbeschriftung und kein Gitter
            showlegend=False, # Legende ausblenden
            hovermode="closest" # Hover nur über nächstem Punkt anzeigen
        )

        # Diagramm anzeigen
        st.plotly_chart(fig1)


        #Ende Boxplot ------------------------------------------------------------

        #Anfang Histogramm------------------------------------------------------

       
        review_length = df['review_text'].str.len()
        max_length = review_length.max()
        min_length = review_length.min()

        bin_size = 50  # Anpassbare Größe der Bins

        num_bins = int(np.ceil((max_length - min_length) / bin_size))  # Anzahl der Bins berechnen

        review_length_bins = np.linspace(min_length, min_length + num_bins * bin_size, num_bins + 1).tolist()
        review_length_hist, _ = np.histogram(review_length, bins=review_length_bins)

        

        review_length_option = {
            # Optionen bleiben unverändert
            "tooltip": {
                "trigger": 'axis',
                "axisPointer": {
                    "type": 'shadow',
                    "label": {
                        "show": True
                    }
                }
            },
            "toolbox": {
                "show": True,
                "feature": {
                    "mark": {"show": True},
                    "dataView": {"show": True, "readOnly": False},
                    "magicType": {"show": True, "type": ['line', 'bar']},
                    "restore": {"show": True},
                    "saveAsImage": {"show": True}
                }
            },
            "calculable": True,
            "legend": {
                "data": ['Number of Reviews'],
                "itemGap": 5
            },
            "grid": {
                "top": '12%',
                "left": '1%',
                "right": '10%',
                "containLabel": True
            },
            "xAxis": [
                {
                    "type": 'category',
                    "data": [f'{int(bin_start)}-{int(bin_end)}' for bin_start, bin_end in zip(review_length_bins[:-1], review_length_bins[1:])]
                }
            ],
            "yAxis": [
                {
                    "type": 'value',
                    "name": 'Number of Reviews',
                    "axisLabel": {
                        "formatter": '{value}',
                        "interval": 1 
                    }
                }
            ],
            "dataZoom": [
                {
                    "show": True,
                    "start": 0,
                    "end": 13
                },
                {
                    "type": 'inside',
                    "start": 0,
                    "end": 13
                },
                {
                    "show": True,
                    "yAxisIndex": 0,
                    "filterMode": 'empty',
                    "width": 30,
                    "height": '80%',
                    "showDataShadow": False,
                    "left": '93%'
                }
            ],
            "series": [
                {
                    "name": 'Number of Reviews',
                    "type": 'bar',
                    "data": review_length_hist.tolist()
                }
            ]
        }

        # Streamlit Befehl zum Anzeigen des Diagramms
        st_echarts(options=review_length_option, height="600px", key="unique_key10")


        #Ende Histogramm-------------------------------------------------------

        #Anfang Histogramm Helpful-------------------------------------------------------
        # Daten erstellen
        helpful_votes = df['helpful_votes'].values
        max_votes = helpful_votes.max()
        min_votes = helpful_votes.min()

        bin_size = 50  # Anpassbare Größe der Bins

        num_bins = int(np.ceil((max_votes - min_votes) / bin_size))  # Anzahl der Bins berechnen

        votes_bins = np.linspace(min_votes, min_votes + num_bins * bin_size, num_bins + 1).tolist()
        votes_hist, _ = np.histogram(helpful_votes, bins=votes_bins)

        helpful_votes_option = {
            "tooltip": {
                "trigger": 'axis',
                "axisPointer": {
                    "type": 'shadow',
                    "label": {
                        "show": True
                    }
                }
            },
            "toolbox": {
                "show": True,
                "feature": {
                    "mark": {"show": True},
                    "dataView": {"show": True, "readOnly": False},
                    "magicType": {"show": True, "type": ['line', 'bar']},
                    "restore": {"show": True},
                    "saveAsImage": {"show": True}
                }
            },
            "calculable": True,
            "legend": {
                "data": ['Number of Helpful Amount'],
                "itemGap": 5
            },
            "grid": {
                "top": '12%',
                "left": '1%',
                "right": '10%',
                "containLabel": True
            },
            "xAxis": [
                {
                    "type": 'category',
                    "data": [f'{int(bin_start)}-{int(bin_end)}' for bin_start, bin_end in zip(votes_bins[:-1], votes_bins[1:])]
                }
            ],
            "yAxis": [
                {
                    "type": 'value',
                    "name": 'Number of Reviews',
                    "axisLabel": {
                        "formatter": '{value}',
                        "interval": 1 
                    }
                }
            ],
            "dataZoom": [
                {
                    "show": True,
                    "start": 0,
                    "end": 13
                },
                {
                    "type": 'inside',
                    "start": 0,
                    "end": 13
                },
                {
                    "show": True,
                    "yAxisIndex": 0,
                    "filterMode": 'empty',
                    "width": 30,
                    "height": '80%',
                    "showDataShadow": False,
                    "left": '93%'
                }
            ],
            "series": [
                {
                    "name": 'Number of Reviews',
                    "type": 'bar',
                    "data": votes_hist.tolist()
                }
            ]
        }

        # Streamlit Befehl zum Anzeigen des Diagramms
        st_echarts(options=helpful_votes_option, height="600px", key="unique_key11")

        #Ende Histogramm Helpful-------------------------------------------------------


        #Anfang Auswahl Histogramm-------------------------------------------------------
        # Nutzerauswahl erhalten
        selection = st.radio("Select Data to Visualize", ('Review Length', 'Helpful Votes'))

        if selection == 'Review Length':
            # Diagramm für Review-Länge anzeigen
            st_echarts(options=review_length_option, height="600px", key="unique_key_review_length")
        elif selection == 'Helpful Votes':
            # Diagramm für Helpful Votes anzeigen
            st_echarts(options=helpful_votes_option, height="600px", key="unique_key_helpful_votes")

        #Ende Auswahl Histogramm-------------------------------------------------------

        #----- neuer Anfang

        # Diagrammkonfiguration
        # Berechnung der Werte
        df['image_or_video'] = ((df['picture_amount'] > 0) | (df['video_amount'] > 0)).astype(int)
        profile_image_helpful = df.groupby('profile_image')['helpful_votes'].mean().round(2).tolist()
        verified_purchase_helpful = df.groupby('verified_purchase')['helpful_votes'].mean().round(2).tolist()
        vine_helpful = df.groupby('vine_badge')['helpful_votes'].mean().round(2).tolist()
        image_or_video_helpful = df.groupby('image_or_video')['helpful_votes'].mean().round(2).tolist()
        average_helpful = round(df['helpful_votes'].mean(), 2)

        # Diagrammkonfiguration
        pos = "insideBottom"
        rotate = 90
        align = "left"
        vertical_align = "middle"
        distance = 15

        label_option = {
            "show": True,
            "position": pos,
            "distance": distance,
            "align": align,
            "verticalAlign": vertical_align,
            "rotate": rotate,
            "formatter": "{c}  {name|{a}}",
            "fontSize": 16,
            "rich": {
                "name": {
                    "color": "white"}
            }
        }

        helpful_votes_option2 = {
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {
                    "type": "shadow"
                }
            },
            "legend": {
                "data": ["Profilbild", "Verifizierter Kauf", "Vine", "Bild oder Video"]
            },
            "toolbox": {
                "show": True,
                "orient": "vertical",
                "left": "right",
                "top": "center",
                "feature": {
                    "mark": {"show": True},
                    "dataView": {"show": True, "readOnly": False},
                    "magicType": {"show": True, "type": ["line", "bar", "stack"]},
                    "restore": {"show": True},
                    "saveAsImage": {"show": True}
                }
            },
            "xAxis": [
                {
                    "type": "category",
                    "axisTick": {"show": False},
                    "data": ["0", "1"]
                }
            ],
            "yAxis": [
                {
                    "type": "value"
                }
            ],
            "series": [
                {
                    "name": "Profilbild",
                    "type": "bar",
                    "barGap": 0,
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": profile_image_helpful
                },
                {
                    "name": "Verifizierter Kauf",
                    "type": "bar",
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": verified_purchase_helpful
                },
                {
                    "name": "Vine",
                    "type": "bar",
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": vine_helpful
                },
                {
                    "name": "Bild oder Video",
                    "type": "bar",
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": image_or_video_helpful
                },
                {
                    "name": "Durchschnittliche Anzahl von Nützlich-Stimmen",
                    "type": "line",
                    "data": [average_helpful, average_helpful],
                    "itemStyle": {"color": "red"},
                    "lineStyle": {"width": 2},
                    "markLine": {
                        "silent": True,
                        "data": [{"yAxis": average_helpful}]
                    }
                }
            ]
        }

        # Zeichnen des Diagramms
        st_echarts(options=helpful_votes_option2, height="500px", key="unique_key67")


        #--Ende Diagramm für nürtlich Stimmen

        #Anfang für Rating

        # Berechnung der Werte
        df['image_or_video'] = ((df['picture_amount'] > 0) | (df['video_amount'] > 0)).astype(int)
        profile_image_rating = df.groupby('profile_image')['rating'].mean().round(2).tolist()
        verified_purchase_rating = df.groupby('verified_purchase')['rating'].mean().round(2).tolist()
        vine_rating = df.groupby('vine_badge')['rating'].mean().round(2).tolist()
        image_or_video_rating = df.groupby('image_or_video')['rating'].mean().round(2).tolist()
        average_rating = round(df['rating'].mean(), 2)

        # Diagrammkonfiguration
        pos = "insideBottom"
        rotate = 90
        align = "left"
        vertical_align = "middle"
        distance = 15

        label_option = {
            "show": True,
            "position": pos,
            "distance": distance,
            "align": align,
            "verticalAlign": vertical_align,
            "rotate": rotate,
            "formatter": "{c}  {name|{a}}",
            "fontSize": 16,
            "rich": {
                "name": {"color": "white"}  # Beschriftungen auf Weiß setzen
            }
        }

        rating_option2 = {
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {
                    "type": "shadow"
                }
            },
            "legend": {
                "data": ["Profilbild", "Verifizierter Kauf", "Vine", "Bild oder Video"],
                "textStyle": {"color": "white"}  # Legendenbeschriftungen auf Weiß setzen
            },
            "toolbox": {
                "show": True,
                "orient": "vertical",
                "left": "right",
                "top": "center",
                "feature": {
                    "mark": {"show": True},
                    "dataView": {"show": True, "readOnly": False},
                    "magicType": {"show": True, "type": ["line", "bar", "stack"]},
                    "restore": {"show": True},
                    "saveAsImage": {"show": True}
                }
            },
            "xAxis": [
                {
                    "type": "category",
                    "axisTick": {"show": False},
                    "data": ["0", "1"]
                }
            ],
            "yAxis": [
                {
                    "type": "value"
                }
            ],
            "series": [
                {
                    "name": "Profilbild",
                    "type": "bar",
                    "barGap": 0,
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": profile_image_rating
                },
                {
                    "name": "Verifizierter Kauf",
                    "type": "bar",
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": verified_purchase_rating
                },
                {
                    "name": "Vine",
                    "type": "bar",
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": vine_rating
                },
                {
                    "name": "Bild oder Video",
                    "type": "bar",
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": image_or_video_rating
                },
                {
                    "name": "Durchschnittliches Rating",
                    "type": "line",
                    "data": [average_rating, average_rating],
                    "itemStyle": {"color": "red"},
                    "lineStyle": {"width": 2},
                    "markLine": {
                        "silent": True,
                        "data": [{"yAxis": average_rating}]
                    }
                }
            ]
        }

        # Zeichnen des Diagramms
        st_echarts(options=rating_option2, height="500px", key="unique_key68")

        #--Ende Diagramm für Rating 

        #Anfang Diagramm für Review Length------------------------------------------------

        # Berechnung der Werte
        df['review_length'] = df['review_text'].apply(lambda x: len(str(x)))
        df['image_or_video'] = ((df['picture_amount'] > 0) | (df['video_amount'] > 0)).astype(int)
        profile_image_length = df.groupby('profile_image')['review_length'].mean().round(2).tolist()
        verified_purchase_length = df.groupby('verified_purchase')['review_length'].mean().round(2).tolist()
        vine_length = df.groupby('vine_badge')['review_length'].mean().round(2).tolist()
        image_or_video_length = df.groupby('image_or_video')['review_length'].mean().round(2).tolist()
        average_length = round(df['review_length'].mean(), 2)

        # Diagrammkonfiguration
        pos = "insideBottom"
        rotate = 90
        align = "left"
        vertical_align = "middle"
        distance = 15

        label_option = {
            "show": True,
            "position": pos,
            "distance": distance,
            "align": align,
            "verticalAlign": vertical_align,
            "rotate": rotate,
            "formatter": "{c}  {name|{a}}",
            "fontSize": 16,
            "color": "white",  # Datenwerte auf Weiß setzen
            "rich": {
                "name": {"color": "white"}  # Beschriftungen auf Weiß setzen
            }
        }

        review_length_option2 = {
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {
                    "type": "shadow"
                }
            },
            "legend": {
                "data": ["Profilbild", "Verifizierter Kauf", "Vine", "Bild oder Video"],
                "textStyle": {"color": "white"}  # Legendenbeschriftungen auf Weiß setzen
            },
            "toolbox": {
                "show": True,
                "orient": "vertical",
                "left": "right",
                "top": "center",
                "feature": {
                    "mark": {"show": True},
                    "dataView": {"show": True, "readOnly": False},
                    "magicType": {"show": True, "type": ["line", "bar", "stack"]},
                    "restore": {"show": True},
                    "saveAsImage": {"show": True}
                }
            },
            "xAxis": [
                {
                    "type": "category",
                    "axisTick": {"show": False},
                    "data": ["0", "1"]
                }
            ],
            "yAxis": [
                {
                    "type": "value"
                }
            ],
            "series": [
                {
                    "name": "Profilbild",
                    "type": "bar",
                    "barGap": 0,
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": profile_image_length
                },
                {
                    "name": "Verifizierter Kauf",
                    "type": "bar",
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": verified_purchase_length
                },
                {
                    "name": "Vine",
                    "type": "bar",
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": vine_length
                },
                {
                    "name": "Bild oder Video",
                    "type": "bar",
                    "barWidth": 40,
                    "label": label_option,
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": image_or_video_length
                },
                {
                    "name": "Durchschnittliche Länge der Bewertungen",
                    "type": "line",
                    "data": [average_length, average_length],
                    "itemStyle": {"color": "red"},
                    "lineStyle": {"width": 2},
                    "markLine": {
                        "silent": True,
                        "data": [{"yAxis": average_length}]
                    }
                }
            ]
        }

        # Zeichnen des Diagramms
        st_echarts(options=review_length_option2, height="500px", key="unique_key70")

        #Ende Diagramm für Review Length------------------------------------------------

        # Nutzerauswahl erhalten-----------------------------------------------------------------------
        selection = st.radio("Select Data to Visualize", ('Review Length', 'Helpful Votes', 'Rating'))

        if selection == 'Review Length':
            # Diagramm für Review-Länge anzeigen
            st_echarts(options=review_length_option2, height="600px", key="unique_key_review_length2")
        elif selection == 'Helpful Votes':
            # Diagramm für Helpful Votes anzeigen
            st_echarts(options=helpful_votes_option2, height="600px", key="unique_key_helpful_votes2")
        elif selection == 'Rating':
            # Diagramm für Helpful Votes anzeigen
            st_echarts(options=rating_option2, height="600px", key="unique_key_rating")
        # Ende Nutzerauswahl erhalten-----------------------------------------------------------------------

        # Anfang Balekndiagramm Review Länge-----------------------------------------------------------------------
        # Verarbeitung der Daten
        df['review_length'] = df['review_text'].apply(len)
        average_review_length = df.groupby('rating')['review_length'].mean()

        # Runden der Werte auf 2 Nachkommastellen
        average_review_length = average_review_length.round(2)

        # Umwandlung des Series-Objekts in eine Liste
        average_review_length_values = average_review_length.values.tolist()

        # Umwandlung des Index (Rating) in eine Liste
        rating_values = average_review_length.index.tolist()


        option = {
        "title": {
            "text": 'Durchschnittliche Rezensionslänge nach Rating',
            "left": 'center',
            "top": 20,
            "textStyle": {
            "color": '#fff'
            }
        },
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
            "type": 'shadow'
            }
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": True
        },
        "xAxis": [
            {
            "type": 'category',
            "data": rating_values,
            "axisTick": {
                "alignWithLabel": True
            },
            "axisLabel": {
                "color": '#fff'
            }
            }
        ],
        "yAxis": [
            {
            "type": 'value',
            "name": 'Durchschnittliche Rezensionslänge',
            "axisLabel": {
                "color": '#fff'
            }
            }
        ],
        "series": [
            {
            "name": 'Durchschnittliche Rezensionslänge',
            "type": 'bar',
            "barWidth": '60%',
            "data": average_review_length_values,
            "label": {
                "show": True,
                "position": 'top',
                "color": '#fff'
            }
            }
        ]
        }

        st_echarts(options=option, height="600px", key="unique_key_rating71")

        # Ende Balekndiagramm Review Länge-----------------------------------------------------------------------

        # Anfang Balekndiagramm Nützlich Stimmen-----------------------------------------------------------------------

        # Verarbeitung der Daten 
        average_helpful_votes = df.groupby('rating')['helpful_votes'].mean().astype(float)

        # Runden der Werte auf 2 Nachkommastellen
        average_helpful_votes = average_helpful_votes.round(2)

        # Umwandlung des Series-Objekts in eine Liste
        average_helpful_votes_values = average_helpful_votes.values.tolist()

        # Umwandlung des Index (Rating) in eine Liste
        rating_values = [float(x) for x in average_helpful_votes.index.tolist()]

        option2 = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
            "type": 'shadow'
            }
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": True
        },
        "xAxis": [
            {
            "type": 'category',
            "data": rating_values,
            "axisTick": {
                "alignWithLabel": True
            },
            "axisLabel": {
                "color": '#fff',
            }
            }
        ],
        "yAxis": [
            {
            "type": 'value',
            "axisLabel": {
                "color": '#fff'
            }
            }
        ],
        "series": [
            {
            "name": 'Durchschnittliche Anzahl von "Nützlich"-Stimmen',
            "type": 'bar',
            "barWidth": '60%',
            "data": average_helpful_votes_values,
            "label": {
                "show": True,
                "position": 'top',
                "color": '#fff'
            }
            }
        ]
        }

        st_echarts(options=option2, height="600px", key="unique_key_helpful_votes4")

        # Ende Balekndiagramm Nützlich Stimmen-----------------------------------------------------------------------


        # Ende Basis Diagramme-----------------------------------------------------------------------


        #Auswahl für Kreisdiagramme----------------------

        choice = st.radio(
        "Choose a category",
        ('Profilbild', 'Verifizierter Kauf', 'Bilder'),
        key='genre2',
        horizontal=True)

        

        #Ende Auswahl für Kreisdiagramme----------------------


        #Anfang 1. Kreisdiagramm Profilbild----------------------
        
        profile_image_counts = df['profile_image'].value_counts().tolist()
        option_profile_image_counts = {
            "title": {
                "text": 'Verhältnis der vorhandenen Profilbilder',
                "left": 'center',
                "textStyle": {
                    "color": '#FFFFFF'
                }
            },
            "tooltip": {
                "trigger": 'item',
                "formatter": "{a} <br/>{b} : {c} ({d}%)"
            },
            "legend": {
                "orient": 'vertical',
                "left": 'left',
                "textStyle": {
                    "color": '#FFFFFF'
                }
            },
            "series": [
                {
                    "name": 'Anzahl',
                    "type": 'pie',
                    "radius": '50%',
                    "data": [
                        {"value": profile_image_counts[0], "name": 'Mit Profilbild'},
                        {"value": profile_image_counts[1], "name": 'Ohne Profilbild'}
                    ],
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": 'rgba(0, 0, 0, 0.5)'
                        }
                    },
                    "label": {
                        "show": True,
                        "textStyle": {
                                "color": '#FFFFFF'
                            },
                        "formatter": "{b}: {d}%"
                    }
                }
            ]
        }
        #st_echarts(options=option_profile_image_counts, height="500px", key="unique_key_profile_image5")
    
         #Ende  1. Kreisdiagramm Profilbild----------------------


        #Anfang 2. Kreisdiagramm verified_purchase----------------------
        
        verified_purchase_counts = df['verified_purchase'].value_counts().tolist()
        option_verified_purchase_counts = {
            "title": {
                "text": 'Verhältnis der verifizierten Käufe',
                "left": 'center',
                "textStyle": {
                    "color": '#FFFFFF'
                }
            },
            "tooltip": {
                "trigger": 'item',
                "formatter": "{a} <br/>{b} : {c} ({d}%)"
            },
            "legend": {
                "orient": 'vertical',
                "left": 'left',
                "textStyle": {
                    "color": '#FFFFFF'
                }
            },
            "series": [
                {
                    "name": 'Anzahl',
                    "type": 'pie',
                    "radius": '50%',
                    "data": [
                        {"value": verified_purchase_counts[0], "name": 'Nicht verifiziert'},
                        {"value": verified_purchase_counts[1], "name": 'Verifiziert'}
                    ],
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": 'rgba(0, 0, 0, 0.5)'
                        }
                    },
                    "label": {
                        "show": True,
                        "textStyle": {
                                "color": '#FFFFFF'
                            },
                        "formatter": "{b}: {d}%"
                    }
                }
            ]
        }
        #st_echarts(options=option_verified_purchase_counts, height="500px", key="unique_verified_purchase5")
        #Ende  2. Kreisdiagramm Verifizierte Kauf----------------------


        #Anfang 3. Kreisdiagramm Bilder Videos----------------------

        # Berechnen der Anzahl von Bewertungen mit und ohne Bilder oder Videos
        image_video_counts = df['image_or_video'].value_counts().tolist()

        option_image_video_counts = {
            "title": {
                "text": 'Verhältnis der Bewertungen mit Bildern oder Videos',
                "left": 'center',
                "textStyle": {
                    "color": '#FFFFFF'
                }
            },
            "tooltip": {
                "trigger": 'item',
                "formatter": "{a} <br/>{b} : {c} ({d}%)"
            },
            "legend": {
                "orient": 'vertical',
                "left": 'left',
                "textStyle": {
                    "color": '#FFFFFF'
                }
            },
            "series": [
                {
                    "name": 'Anzahl',
                    "type": 'pie',
                    "radius": '50%',
                    "data": [
                        {"value": image_video_counts[0], "name": 'Mit Bildern oder Videos'},
                        {"value": image_video_counts[1], "name": 'Ohne Bilder oder Videos'}
                    ],
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": 'rgba(0, 0, 0, 0.5)'
                        }
                    },
                    "itemStyle": {
                        "normal": {
                            #"color": '#c23531',
                            "shadowBlur": 200,
                            "shadowColor": 'rgba(0, 0, 0, 0.5)'
                        },
                        "emphasis": {
                            #"color": '#e06343'
                        }
                    },
                    "label": {
                        "normal": {
                            "textStyle": {
                                "color": '#FFFFFF'
                            },
                            "formatter": "{b}: {d}%"
                        }
                    },
                    "labelLine": {
                        "normal": {
                            "lineStyle": {
                                #"color": '#FFFFFF'
                            },
                            "smooth": 0.2,
                            "length": 10,
                            "length2": 20
                        }
                    },
                }
            ]
        }
        #st_echarts(options=option_image_video_counts, height="500px", key="unique_key_image_video1")

        #Ende  3. Kreisdiagramm Bilder Videos----------------------


        if choice == 'Profilbild':
            st.write('Sie haben Komödie ausgewählt.')
            st_echarts(options=option_profile_image_counts, height="500px", key="unique_key_profile_image6")

        
        elif choice == 'Verifizierter Kauf':
            st.write('Sie haben Komödie2 ausgewählt.')
            st_echarts(options=option_verified_purchase_counts, height="500px", key=f"unique_verified_purchase{time.time()}")

        else:
            st.write('Sie haben Komödie3 ausgewählt.')
            st_echarts(options=option_image_video_counts, height="500px", key="unique_key_image_video1")

        #Ende Auswahlbereich-----------------------------------------------------------------


        #Anfang Linien Plot Anzahl der Rezensionen im Zeitverlauf not working atm------------------------------------------------

        # Lese die CSV-Datei ein
        data = pd.read_csv(r'C:\Users\Alex\Desktop\Business\Data Science Bots\Amazon Scraping Projekt\Schreib Vortrag\bsr.csv')

        # Konvertiere die 'Time'-Spalte in ein datetime-Objekt
        data['Time'] = pd.to_datetime(data['Time'], format='%d.%m.%Y, %H:%M:%S')

        # Ersetze die leeren Zellen in der 'Sales Rank'-Spalte mit NaN
        data['Sales Rank'] = pd.to_numeric(data['Sales Rank'], errors='coerce')

        # Setze den Index auf die 'Time'-Spalte
        data.set_index('Time', inplace=True)

        # Berechne die Zeiträume, in denen der Bestsellerrang über 1000 war
        data['unavailable'] = data['Sales Rank'] > 600
        unavailability_periods = []
        start = None
        for i in range(len(data)):
            if data['unavailable'].iloc[i] and start is None:
                start = data.index[i]
            elif not data['unavailable'].iloc[i] and start is not None:
                end = data.index[i]
                unavailability_periods.append((start, end))
                start = None
        if start is not None:  # Falls die PS5 am Ende des Datensatzes immer noch nicht verfügbar ist
            unavailability_periods.append((start, data.index[-1]))


        # Vorbereiten der Daten
        df['date_created'] = pd.to_datetime(df['date_created'])
        df.set_index('date_created', inplace=True)  # Setzen Sie date_created als Index
        df_resampled = df.resample('M').count()

        x_data = df_resampled.index.strftime('%Y-%m').tolist()  # Konvertieren der Datumsdaten in Strings für die x-Achse
        y_data = df_resampled['id'].tolist() 

        # Erstellen Sie die markArea-Daten basierend auf den Nichtverfügbarkeitszeiträumen
        mark_areas = [
            [{"xAxis": str(start.strftime('%Y-%m'))}, {"xAxis": str(end.strftime('%Y-%m'))}]
            for start, end in unavailability_periods
        ]

        option = {
            "title": {
                "text": 'Anzahl der Bewertungen im zeitlichen Verlauf',
                "textStyle": {"color": '#fff'}
            },
            "tooltip": {
                "trigger": 'axis',
                "axisPointer": {"type": 'cross'}
            },
            "toolbox": {
                "show": True,
                "feature": {"saveAsImage": {}}
            },
            "xAxis": {
                "type": 'category',
                "boundaryGap": False,
                "data": x_data,
                "axisLine": {"lineStyle": {"color": '#fff'}},
                "axisLabel": {"color": '#fff'}
            },
            "yAxis": {
                "type": 'value',
                "axisLabel": {
                    "formatter": '{value}',
                    "color": '#fff'
                },
                "axisLine": {"lineStyle": {"color": '#fff'}},
                "axisPointer": {"snap": True},
                "splitLine": {"lineStyle": {"color": '#aaa'}}
            },
            "series": [
                {
                    "name": 'Anzahl der Bewertungen',
                    "type": 'line',
                    "smooth": True,
                    "data": y_data,
                    "markArea": {
                        "itemStyle": {"color": 'rgba(255, 0, 0, 0.4)'},
                        "data": mark_areas
                    }
                }
            ]
        }

        st_echarts(options=option, height="600px", key="unique_key4")


        #Ende Linien Plot Anzahl der Rezensionen im Zeitverlauf not working atm------------------------------------------------

        #Anfang Scatterplot-----------------------------

        option = {
            "title": {
                "text": 'Male and female height and weight distribution',
                "subtext": 'Data from: Heinz 2003'
            },
            "grid": {
                "left": '3%',
                "right": '7%',
                "bottom": '7%',
                "containLabel": True
            },
            "tooltip": {
                "showDelay": 0,
                "axisPointer": {
                "show": True,
                "type": 'cross',
                "lineStyle": {
                    "type": 'dashed',
                    "width": 1
                }
                }
            },
            "toolbox": {
                "feature": {
                "dataZoom": {},
                "brush": {
                    "type": ['rect', 'polygon', 'clear']
                }
                }
            },
            "brush": {},
            "legend": {
                "data": ['Female', 'Male'],
                "left": 'center',
                "bottom": 10
            },
            "xAxis": [
                {
                "type": 'value',
                "scale": True,
                "axisLabel": {
                    "formatter": '{value} cm'
                },
                "splitLine": {
                    "show": False
                }
                }
            ],
            "yAxis": [
                {
                "type": 'value',
                "scale": True,
                "axisLabel": {
                    "formatter": '{value} kg'
                },
                "splitLine": {
                    "show": False
                }
                }
            ],
                "series": [
                {
                    "name": "Female",
                    "type": "scatter",
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": [[161.2, 51.6], [167.5, 59.0], [159.5, 49.2], [157.0, 63.0], [155.8, 53.6]],
                    "markArea": {
                        "silent": True,
                        "itemStyle": {
                            "color": "transparent",
                            "borderWidth": 1,
                            "borderType": "dashed"
                        },
                        "data": [
                            [
                                {
                                    "name": "Female Data Range",
                                    "xAxis": "min",
                                    "yAxis": "min"
                                },
                                {
                                    "xAxis": "max",
                                    "yAxis": "max"
                                }
                            ]
                        ]
                    },
                    "markPoint": {
                        "data": [
                            {"type": "max", "name": "Max"},
                            {"type": "min", "name": "Min"}
                        ]
                    },
                    "markLine": {
                        "lineStyle": {
                            "type": "solid"
                        },
                        "data": [{"type": "average", "name": "Average"}, {"xAxis": 160}]
                    }
                },
                {
                    "name": "Male",
                    "type": "scatter",
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": [[174.0, 65.6], [175.3, 71.8], [193.5, 80.7],[181.5, 74.8], [184.0, 86.4], [184.5, 78.4], [175.0, 62.0], [184.0, 81.6],
                        [180.0, 76.6], [177.8, 83.6], [192.0, 90.0], [176.0, 74.6], [174.0, 71.0],
                        [184.0, 79.6], [192.7, 93.8], [171.5, 70.0], [173.0, 72.4], [176.0, 85.9],
                        [176.0, 78.8], [180.5, 77.8], [172.7, 66.2], [176.0, 86.4], [173.5, 81.8],
                        [178.0, 89.6], [180.3, 82.8], [180.3, 76.4], [164.5, 63.2], [173.0, 60.9],
                        [183.5, 74.8], [175.5, 70.0], [188.0, 72.4], [189.2, 84.1], [172.8, 69.1],
                        [170.0, 59.5], [182.0, 67.2], [170.0, 61.3], [177.8, 68.6], [184.2, 80.1],
                        [186.7, 87.8], [171.4, 84.7], [172.7, 73.4], [175.3, 72.1], [180.3, 82.6],
                        [182.9, 88.7], [188.0, 84.1], [177.2, 94.1], [172.1, 74.9], [167.0, 59.1],
                        [169.5, 75.6], [174.0, 86.2], [172.7, 75.3], [182.2, 87.1], [164.1, 55.2],
                        [163.0, 57.0], [171.5, 61.4], [184.2, 76.8], [174.0, 86.8], [174.0, 72.2],
                        [177.0, 71.6], [186.0, 84.8], [167.0, 68.2], [171.8, 66.1], [182.0, 72.0],
                        [167.0, 64.6], [177.8, 74.8], [164.5, 70.0], [192.0, 101.6], [175.5, 63.2],
                        [171.2, 79.1], [181.6, 78.9], [167.4, 67.7], [181.1, 66.0], [177.0, 68.2],
                        [174.5, 63.9], [177.5, 72.0], [170.5, 56.8], [182.4, 74.5], [197.1, 90.9],
                        [180.1, 93.0], [175.5, 80.9], [180.6, 72.7], [184.4, 68.0], [175.5, 70.9],
                        [180.6, 72.5], [177.0, 72.5], [177.1, 83.4], [181.6, 75.5], [176.5, 73.0],
                        [175.0, 70.2], [174.0, 73.4], [165.1, 70.5], [177.0, 68.9], [192.0, 102.3],
                        [176.5, 68.4], [169.4, 65.9], [182.1, 75.7], [179.8, 84.5], [175.3, 87.7]],
                    "markArea": {
                        "silent": True,
                        "itemStyle": {
                            "color": "transparent",
                            "borderWidth": 1,
                            "borderType": "dashed"
                        },
                        "data": [
                            [
                                {
                                    "name": "Male Data Range",
                                    "xAxis": "min",
                                    "yAxis": "min"
                                },
                                {
                                    "xAxis": "max",
                                    "yAxis": "max"
                                }
                            ]
                        ]
                    },
                    "markPoint": {
                        "data": [
                            {"type": "max", "name": "Max"},
                            {"type": "min", "name": "Min"}
                        ]
                    },
                    "markLine": {
                        "lineStyle": {
                            "type": "solid"
                        },
                        "data": [{"type": "average", "name": "Average"}, {"xAxis": 170}]
                        }
                    }
                ]
            }

        st_echarts(options=option, height="500px", key="unique_key7")
    
    
       

    with tab2:
        st.write("Tab 2")



    with tab3:
        st.write("Tab3")


















def about_page():
    st.write("This is the about page")













def contact_page():
    st.write("This is the contact page")














def main():

    st.set_page_config(page_title="🕵️‍♀️ Amazon Sentimentanalyse", page_icon="🕵️‍♂️", layout="centered")
    st.markdown(" <style>iframe{ height: 700px !important } ", unsafe_allow_html=True)


    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Home PS5", "Vergleich", "Scraping"],
            icons=["house", "book", "envelope"],
        )
    if selected == "Home PS5":
        home_page()
    elif selected == "Vergleich":
        about_page()
    elif selected == "Scraping":
        contact_page()











if __name__ == "__main__":
    main()