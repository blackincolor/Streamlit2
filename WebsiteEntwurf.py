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

from collections import Counter
from streamlit_echarts import st_pyecharts
import pandas as pd


from collections import Counter
import re

import subprocess

from pyecharts import options as opts
from pyecharts.charts import Boxplot
from pyecharts import options as opts
from pyecharts.charts import Boxplot, Scatter
from pyecharts.commons.utils import JsCode
import os





def home_page():

    tab1, tab2, tab3 = st.tabs(["📈 Deskriptive Analyse", "💬 Text Analyse", "😃 Sentimentanalyse"])
    



    current_directory = os.getcwd()

    database_filename = 'databaseV3.0.db'

    database_path = os.path.join(current_directory, database_filename)

    conn = sqlite3.connect(database_path)


    
    # Datenbank lesen
    df = pd.read_sql_query("SELECT * from sentiment", conn)



       
    with tab1:
        
        #Anfang Expander für Datenbank---------------------------------------------
        expander = st.expander("Datenbank anzeigen")
        with expander:
            st.dataframe(df)
        #Ende  Expander für Datenbank--------------------------------------------



        
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




        #Anfang Nutzerauswahl Kreisdiagramme
        choice = st.radio(
        "Was soll visualisiert werden?",
        ('Profilbild', 'Verifizierter Kauf', 'Bilder'),
        key='genre2',
        horizontal=True)
        #Ende Nutzerauswahl Kreisdiagramme---------------
        
        
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
                        {"value": profile_image_counts[0], "name": 'Ohne Profilbild'},
                        {"value": profile_image_counts[1], "name": 'Mit Profilbild'}
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
        
        verified_purchase_counts = df['verified_purchase'].value_counts(sort=False).tolist()
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
        df['image_or_video'] = ((df['picture_amount'] > 0) | (df['video_amount'] > 0)).astype(int)
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
                        {"value": image_video_counts[0], "name": 'Ohne Bilder oder Videos'},
                        {"value": image_video_counts[1], "name": 'Mit Bildern oder Videos'}
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
            
            st_echarts(options=option_profile_image_counts, height="500px", key="unique_key_profile_image6")

        
        elif choice == 'Verifizierter Kauf':
            
            st_echarts(options=option_verified_purchase_counts, height="500px", key=f"unique_verified_purchase{time.time()}")

        else:
            st_echarts(options=option_image_video_counts, height="500px", key="unique_key_image_video1")

        #1/4 Auswahl Frage Master Boxplot---------------------------------------------

        visualisation = st.radio(
            "Was soll visualisiert werden?",
            ('Rating', 'Rezensionslänge', 'Nützlich-Stimmen'),
            key='visualisation1',
            horizontal=True)



        #Ende 1/4 Auswahl Frage Master Boxplot---------------------------------------------

        #Anfang Boxplot der Ratings -----------------------------------------------------------------------------------

        fig1 = go.Figure()
        fig1.add_trace(go.Box(x=df['rating'], quartilemethod="inclusive", name="", boxpoints='outliers', whiskerwidth=1.0))

        # Achsenbeschriftungen, Titel und Layout anpassen
        fig1.update_layout(
            title="Boxplot der Ratings",
            xaxis_title="Rating",
            xaxis_range=[1,5],  # Ändern Sie den Bereich auf 1-5
            yaxis=dict(showticklabels=False, showgrid=False), # Keine Y-Achsenbeschriftung und kein Gitter
            showlegend=False, # Legende ausblenden
            hovermode="closest" # Hover nur über nächstem Punkt anzeigen
        )
        #st.plotly_chart(fig1)

        #Ende Boxplot1 Ratings ------------------------------------------------------------
        

        review_length = df['review_text'].str.len()

        # Interaktiver Boxplot für Rezensionslänge mit 0-100% Whiskers (entspricht min und max Wert)
        fig2 = go.Figure()
        fig2.add_trace(go.Box(x=review_length, quartilemethod="inclusive", name="", boxpoints='outliers', whiskerwidth=1.0))

        # Achsenbeschriftungen, Titel und Layout anpassen
        fig2.update_layout(
            title="Boxplot der Rezensionslängen",
            xaxis_title="Rezensionslänge",
            xaxis_range=[0,1000],
            yaxis=dict(showticklabels=False, showgrid=False), # Keine Y-Achsenbeschriftung und kein Gitter
            showlegend=False, # Legende ausblenden
            hovermode="closest" # Hover nur über nächstem Punkt anzeigen
        )
        #st.plotly_chart(fig2)


        #Anfang Boxplot3 Nützlich Stimmen ----------------------

        helpful_votes = df['helpful_votes']

        # Interaktiver Boxplot für Nützliche Stimmen mit 0-100% Whiskers (entspricht min und max Wert)
        fig3 = go.Figure()
        fig3.add_trace(go.Box(x=helpful_votes, quartilemethod="inclusive", name="", boxpoints='outliers', whiskerwidth=1.0))

        # Achsenbeschriftungen, Titel und Layout anpassen
        fig3.update_layout(
            title="Boxplot der nützlichen Stimmen",
            xaxis_title="Nützliche Stimmen",
            xaxis_range=[0,15], # Begrenzt die X-Achse auf 1000
            yaxis=dict(showticklabels=False, showgrid=False), # Keine Y-Achsenbeschriftung und kein Gitter
            showlegend=False, # Legende ausblenden
            hovermode="closest" # Hover nur über nächstem Punkt anzeigen
        )
        #st.plotly_chart(fig3)




        #Ende Boxplot3 Nützlich Stimmen ------------------------------------------------------------


        #Anfang Master Auswahlmenü------------------------------------------------------------

        if visualisation == 'Rating':
            st.plotly_chart(fig1)
        elif visualisation == 'Rezensionslänge':
            st.plotly_chart(fig2)
        else:
            st.plotly_chart(fig3)
        #Ende Master Auswahlmenü------------------------------------------------------------




        #2/4 Auswahl Frage Histogramm---------------------------------------------
        
        if visualisation != 'Rating':
            visualisation2 = st.radio(
                "Was soll visualisiert werden?",
                ('Rezensionslänge', 'Nützlich-Stimmen'),
                key='visualisation2',
                index=('Rezensionslänge', 'Nützlich-Stimmen').index(visualisation) if visualisation in ('Rezensionslänge', 'Nützlich-Stimmen') else 0,
                horizontal=True)



        #Ende 2/4 Auswahl Frage Master Histogramm---------------------------------------------



        #Anfang Histogramm------------------------------------------------------

       
            review_length = df['review_text'].str.len()
            max_length = review_length.max()
            min_length = review_length.min()

            bin_size = 50  # Anpassbare Größe der Bins

            num_bins = int(np.ceil((max_length - min_length) / bin_size))  # Anzahl der Bins berechnen

            review_length_bins = np.linspace(min_length, min_length + num_bins * bin_size, num_bins + 1).tolist()
            review_length_hist, _ = np.histogram(review_length, bins=review_length_bins)

            

            review_length_option = {
                    "title": {  # Titel hinzufügen
                        "text": 'Histogramm der Rezensionslängen',
                        "left": 'center',
                        "top": '5%',  # Setze die Position des Titels nach oben
                        "textStyle": {  # Setze die Farbe des Titels auf Weiß
                            "color": 'white'
        }
                    },
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
            #st_echarts(options=review_length_option, height="600px", key="unique_key10")


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
                                    "title": {  # Titel hinzufügen
                        "text": 'Histogramm der Nützlich-Stimmen',
                        "left": 'center',
                        "top": '5%',  # Setze die Position des Titels nach oben
                        "textStyle": {  # Setze die Farbe des Titels auf Weiß
                            "color": 'white'
        }
                    },
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
            #st_echarts(options=helpful_votes_option, height="600px", key="unique_key11")

            #Ende Histogramm Helpful-------------------------------------------------------


        #Anfang Antwort Histogramm------------------------------------------------------------


            if visualisation2 == 'Rezensionslänge':
                st_echarts(options=review_length_option, height="600px", key="unique_key_review_length")
            else:
                st_echarts(options=helpful_votes_option, height="600px", key="unique_key_helpful_votes")

        #Ende Antwort Histogramm------------------------------------------------------------


        #Anfang 3/4 Auswahl Frage nach Gruppen---------------------------------------------
        visualisation3 = st.radio(
        "Was soll visualisiert werden?",
        ('Rating', 'Rezensionslänge', 'Nützlich-Stimmen'),
        key='visualisation3',
        index=('Rating', 'Rezensionslänge', 'Nützlich-Stimmen').index(visualisation) if visualisation in ('Rating', 'Rezensionslänge', 'Nützlich-Stimmen',) else 0,
        horizontal=True)
        #Ende 3/4 Auswahl Frage nach Gruppen---------------------------------------------

        
        
        
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
                "title": {
                "text": "Nützlich-Stimmen nach verschiedenen Gruppen",
                "top": 20,
                "left": "center", 
                 "textStyle": {"color": "white"}, 
                 },
            "legend": {
                "data": ["Profilbild", "Verifizierter Kauf", "Vine", "Bild oder Video"],
                "textStyle": {"color": "white"} 
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
        #st_echarts(options=helpful_votes_option2, height="500px", key="unique_key67")


        #--Ende Diagramm für nürtlich Stimmen

        #Anfang für Rating-----------------------------

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
            "title": {
                "text": "Rating nach verschiedenen Gruppen",
                "top": 20,
                "left": "center", 
                 "textStyle": {"color": "white"}, 
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
        #st_echarts(options=rating_option2, height="500px", key="unique_key68")

        #--Ende Diagramm für Rating ..................................

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
                            "title": {
                "text": "Rezensionslänge nach verschiedenen Gruppen",
                "top": 20,
                "left": "center", 
                 "textStyle": {"color": "white"}, 
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
        #st_echarts(options=review_length_option2, height="500px", key="unique_key70")

        #Ende Diagramm für Review Length------------------------------------------------

        # Nutzerauswahl erhalten-----------------------------------------------------------------------
            
        


        if visualisation3 == 'Rating':
            st_echarts(options=rating_option2, height="600px", key="unique_key_rating")
            
        elif visualisation3 == 'Rezensionslänge':
            st_echarts(options=review_length_option2, height="600px", key="unique_key_review_length2")
            
        else:
           st_echarts(options=helpful_votes_option2, height="600px", key="unique_key_helpful_votes2")
        # Ende Nutzerauswahl erhalten-----------------------------------------------------------------------



        #Anfang 4/4 Auswahl Frage nach Rating---------------------------------------------

        if visualisation != 'Rating':
            visualisation4 = st.radio(
                "Was soll visualisiert werden?",
                ('Rezensionslänge', 'Nützlich-Stimmen'),
                key='visualisation4',
                index=('Rezensionslänge', 'Nützlich-Stimmen').index(visualisation) if visualisation in ('Rezensionslänge', 'Nützlich-Stimmen') else 0,
                horizontal=True)

        #Ende 4/4 Auswahl Frage nach Rating---------------------------------------------


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

            #st_echarts(options=option, height="600px", key="unique_key_rating71")

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
                        "title": {
                "text": 'Durchschnittliche Nützlich Stimmen nach Rating',
                "left": 'center',
                "top": 20,
                "textStyle": {
                "color": '#fff'
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

            #st_echarts(options=option2, height="600px", key="unique_key_helpful_votes4")

            # Ende Balekndiagramm Nützlich Stimmen-----------------------------------------------------------------------

            if visualisation4 == 'Rezensionslänge':
                st_echarts(options=option, height="600px", key="unique_key_rating71")
            else:
                st_echarts(options=option2, height="600px", key="unique_key_helpful_votes4")






        # Ende Basis Diagramme-----------------------------------------------------------------------



        #components.html("<hr>")


        

        #Anfang besserer Scatterplot-----------------------------

        #Datemaufbereitung

        if df['date_created'].dtype != 'datetime64[ns]':
            df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')

        # Konvertieren Sie das 'date_created' Attribut in eine Zeichenkette im ISO-Format
        df['date_created_str'] = df['date_created'].dt.strftime('%Y-%m-%d')

        df_verified = df[df['verified_purchase'] == True]
        df_unverified = df[df['verified_purchase'] == False]

        # Erzeugen Sie die Datenlisten
        data_verified = df_verified[['id', 'date_created_str']].values.tolist()
        data_unverified = df_unverified[['id', 'date_created_str']].values.tolist()

        df['review_text_length'] = df['review_text'].apply(len)
        df_long_text = df[df['review_text_length'] > 100]

        data_long_text = df_long_text[['id', 'date_created_str']].values.tolist()

        df_long_text = df[df['review_text_length'] > 500]
        data_long_long_text = df_long_text[['id', 'date_created_str']].values.tolist()

        df_low_ratings = df[df['rating'] <= 3]
        data_low_ratings = df_low_ratings[['id', 'date_created_str']].values.tolist()

     

        optiondata = {
            "title": {
                "text": 'Ranking ID über Zeit',
                "textStyle": {
                    "color": "white"
                }
            },
            "legend": {
                "data": ['Verifiziert', 'Nicht verifiziert', 'Textlänge über 100 Zeichen','Textlänge über 500 Zeichen','3 Sterne Rating oder schlechter'],
                "left": 'center',
                "bottom": -8,
                "textStyle": {"color": "white"}, 
                    "selected": {
                        'Verifiziert': True,
                        'Nicht verifiziert': True,
                        'Textlänge über 100 Zeichen': False,
                        'Textlänge über 500 Zeichen': False,
                        '3 Sterne Rating oder schlechter': False}
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
            "xAxis": [
                {
                    "type": 'value',  # This will be the 'id'
                    "scale": True,
                    "axisLabel": {
                        "formatter": 'ID: {value}',
                        "color": "white"  # This changes the color of the axis labels to white
                    },
                    "splitLine": {
                        "show": False
                    }
                }
            ],
            "yAxis": [
                {
                    "type": 'time',  # This will be the 'date_created_str'
                    "scale": True,
                    "axisLabel": {
                        "color": "white"  # This changes the color of the axis labels to white
                    },
                    "splitLine": {
                        "show": False
                    }
                }
            ],
            "series": [
                {
                    "name": "Verifiziert",
                    "type": "scatter",
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": data_verified,
                    # Optional, Sie können markArea, markPoint und markLine auskommentieren, wenn Sie diese nicht benötigen
                },
                {
                    "name": "Nicht verifiziert",
                    "type": "scatter",
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": data_unverified,
                    # Optional, Sie können markArea, markPoint und markLine auskommentieren, wenn Sie diese nicht benötigen
                },
                {
                    "name": "Textlänge über 100 Zeichen",
                    "type": "scatter",
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": data_long_text,
                    # Optional, Sie können markArea, markPoint und markLine auskommentieren, wenn Sie diese nicht benötigen
                },
                {
                    "name": "Textlänge über 500 Zeichen",
                    "type": "scatter",
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": data_long_long_text,
                    # Optional, Sie können markArea, markPoint und markLine auskommentieren, wenn Sie diese nicht benötigen
                },
                {
                    "name": "3 Sterne Rating oder schlechter",
                    "type": "scatter",
                    "emphasis": {
                        "focus": "series"
                    },
                    "data": data_low_ratings,
                    "itemStyle": {
                        "color": "purple"},
                    # Optional, Sie können markArea, markPoint und markLine auskommentieren, wenn Sie diese nicht benötigen
                }
            ]
        }

        st_echarts(options=optiondata, height="500px", key="unique_key8")

        #Ende guter Scatterplot--------------------


        current_directory = os.getcwd()
        csv_filename = 'bsr.csv'
        csv_path = os.path.join(current_directory, csv_filename)
        data = pd.read_csv(csv_path)

        #Anfang Linien Plot Anzahl der Rezensionen im Zeitverlauf not working atm macht irgendwas falsch deswegen am ende------------------------------------------------

        # Lese die CSV-Datei ein
        #data = pd.read_csv(r'C:\Users\Alex\Desktop\Business\Data Science Bots\Amazon Scraping Projekt\Schreib Vortrag\bsr.csv')

        # Konvertiere die 'Time'-Spalte in ein datetime-Objekt
        data['Time'] = pd.to_datetime(data['Time'], format='%d.%m.%Y, %H:%M:%S')

        # Ersetze die leeren Zellen in der 'Sales Rank'-Spalte mit NaN
        data['Sales Rank'] = pd.to_numeric(data['Sales Rank'], errors='coerce')

        # Setze den Index auf die 'Time'-Spalte
        data.set_index('Time', inplace=True)

        # Berechne die Zeiträume, in denen der Bestsellerrang über 1000 war
        data['unavailable'] = data['Sales Rank'] > 400
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


        #Ende Linien Plot Anzahl der Rezensionen im Zeitverlauf------------------------------------------------
        
    

    #Anfang Linien Plot Rating im Zeitverlauf------------------------------------------------
    
        # Vorbereiten der Daten


        current_directory = os.getcwd()
        csv_filename = 'bsr.csv'
        csv_path = os.path.join(current_directory, csv_filename)
        data = pd.read_csv(csv_path)
    

        # Konvertiere die 'Time'-Spalte in ein datetime-Objekt
        data['Time'] = pd.to_datetime(data['Time'], format='%d.%m.%Y, %H:%M:%S')

        # Ersetze die leeren Zellen in der 'Sales Rank'-Spalte mit NaN
        data['Sales Rank'] = pd.to_numeric(data['Sales Rank'], errors='coerce')

        # Setze den Index auf die 'Time'-Spalte
        data.set_index('Time', inplace=True)

        # Berechne die Zeiträume, in denen der Bestsellerrang über 1000 war
        data['unavailable'] = data['Sales Rank'] > 1500
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

        # Durchschnittliche Bewertung pro Tag
        daily_avg_rating = df['rating'].resample('D').mean()

        # Berechnen des gleitenden Durchschnitts mit einem Zeitfenster von 14 Tagen
        rolling_avg_rating = daily_avg_rating.rolling(window=14).mean()

        # Entfernen der NaN-Werte
        rolling_avg_rating = rolling_avg_rating.dropna()

        x_data = rolling_avg_rating.index.strftime('%Y-%m-%d').tolist()  # Konvertieren der Datumsdaten in Strings für die x-Achse
        y_data = rolling_avg_rating.tolist()

        # Erstellen Sie die markArea-Daten basierend auf den Nichtverfügbarkeitszeiträumen
        mark_areas = [
            [{"xAxis": str(start.strftime('%Y-%m-%d'))}, {"xAxis": str(end.strftime('%Y-%m-%d'))}]
            for start, end in unavailability_periods
        ]


        option = {
            "title": {
                "text": 'Durchschnittsbewertung im zeitlichen Verlauf',
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
                "min": 2.5,  # Minimum auf 3 setzen
                "max": 5, 
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
                    "name": 'Durchschnittsbewertung',
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

        st_echarts(options=option, height="600px", width="100%", key="unique_key44")
        




    #Ende Linien Plot Rating im Zeitverlauf------------------------------------------------
    
       

    with tab2:
        st.write("Text Analyse")
        




    with tab3:
        

        # Verarbeitung der Daten für das Balkendiagramm
        data_grouped = df.groupby('rating')['sentiment_score1'].mean().sort_index().round(2)

        # Umwandlung des Series-Objekts in eine Liste
        data_values = data_grouped.values.tolist()

        # Umwandlung des Index (Rating) in eine Liste
        rating_values = [float(x) for x in data_grouped.index.tolist()]

        option = {
            "title": {
                "text": 'Sentiment Score von Google API nach Amazon-Sternebewertung',
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
            "xAxis": {
                "type": 'category',
                "data": rating_values,
                "axisTick": {
                    "alignWithLabel": True
                },
                "axisLabel": {
                    "color": '#fff'
                }
            },
            "yAxis": {
                "type": 'value',
                "name": 'Sentiment Score1',
                "axisLabel": {
                    "color": '#fff'
                }
            },
            "series": [
                {
                    "name": 'Durchschnittliche Sentiment Score1',
                    "type": 'bar',
                    "data": data_values,
                    "label": {
                        "show": True,
                        "position": 'top',
                        "color": '#fff'
                    }
                }
            ]
        }

        st_echarts(options=option, height="600px", key="unique_key_sentiment_score")


        # Verarbeitung der Daten für das Balkendiagramm
        data_grouped = df.groupby('rating')['sentiment_score3'].mean().sort_index().round(2)

        # Umwandlung des Series-Objekts in eine Liste
        data_values = data_grouped.values.tolist()

        # Umwandlung des Index (Rating) in eine Liste
        rating_values = [float(x) for x in data_grouped.index.tolist()]

        option = {
            "title": {
                "text": 'Sentiment Score von TextBlob nach Amazon-Sternebewertung',
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
            "xAxis": {
                "type": 'category',
                "data": rating_values,
                "axisTick": {
                    "alignWithLabel": True
                },
                "axisLabel": {
                    "color": '#fff'
                }
            },
            "yAxis": {
                "type": 'value',
                "name": 'Sentiment Score1',
                "axisLabel": {
                    "color": '#fff'
                }
            },
            "series": [
                {
                    "name": 'Durchschnittliche Sentiment Score1',
                    "type": 'bar',
                    "data": data_values,
                    "label": {
                        "show": True,
                        "position": 'top',
                        "color": '#fff'
                    }
                }
            ]
        }

        st_echarts(options=option, height="600px", key="unique_key_sentiment_score2")


            #Anfang Linien Plot Rating im Zeitverlauf------------------------------------------------
    
        # Vorbereiten der Daten
        # Lese die CSV-Datei ein

        current_directory = os.getcwd()
        csv_filename = 'bsr.csv'
        csv_path = os.path.join(current_directory, csv_filename)
        data = pd.read_csv(csv_path)

        

        # Konvertiere die 'Time'-Spalte in ein datetime-Objekt
        data['Time'] = pd.to_datetime(data['Time'], format='%d.%m.%Y, %H:%M:%S')

        # Ersetze die leeren Zellen in der 'Sales Rank'-Spalte mit NaN
        data['Sales Rank'] = pd.to_numeric(data['Sales Rank'], errors='coerce')

        # Setze den Index auf die 'Time'-Spalte
        data.set_index('Time', inplace=True)

        # Berechne die Zeiträume, in denen der Bestsellerrang über 1000 war
        data['unavailable'] = data['Sales Rank'] > 1500
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

        # Durchschnittliche Bewertung pro Tag
        daily_avg_sentiment_score3 = df['sentiment_score3'].resample('D').mean()

        # Berechnen des gleitenden Durchschnitts mit einem Zeitfenster von 14 Tagen
        rolling_avg_sentiment_score3 = daily_avg_sentiment_score3.rolling(window=14).mean()

        # Entfernen der NaN-Werte
        rolling_avg_sentiment_score3 = rolling_avg_sentiment_score3.dropna()

        x_data = rolling_avg_sentiment_score3.index.strftime('%Y-%m-%d').tolist()  # Konvertieren der Datumsdaten in Strings für die x-Achse
        y_data = rolling_avg_sentiment_score3.tolist()

        # Erstellen Sie die markArea-Daten basierend auf den Nichtverfügbarkeitszeiträumen
        mark_areas = [
            [{"xAxis": str(start.strftime('%Y-%m-%d'))}, {"xAxis": str(end.strftime('%Y-%m-%d'))}]
            for start, end in unavailability_periods
        ]


        option = {
            "title": {
                "text": 'Durchschnittsbewertung im zeitlichen Verlauf',
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
                "min": 2.5,  # Minimum auf 3 setzen
                "max": 5, 
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
                    "name": 'Durchschnittsbewertung',
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

        st_echarts(options=option, height="600px", width="100%", key="unique_key46")
        




    #Ende Linien Plot Rating im Zeitverlauf------------------------------------------------


        















def about_page():
    st.write("Vergleichsseite")

    













def contact_page():
    st.write("Scraping")



    asin = st.text_input('Enter ASIN of the product')

    if asin:
            # Erstellen Sie einen "unendlichen" Fortschrittsbalken und einen Platzhalter für die Statusmeldungen
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Starten Sie den Prozess mit Popen
            process = subprocess.Popen(['python', 'Amazon-Scraper.py', asin], stdout=subprocess.PIPE)

            # Verarbeiten Sie die Ausgabe in Echtzeit
            total_lines_processed = 0
            for line in iter(process.stdout.readline, b''):
                line = line.decode(errors='ignore')


                # Aktualisieren Sie den Fortschrittsbalken und den Status-Text basierend auf der Ausgabe
                if "Seite erfolgreich gescraped" in line:
                    total_lines_processed += 1
                    progress = total_lines_processed / 300  # Hier 300 durch die tatsächliche maximale Anzahl von Seiten ersetzen, die Sie erwarten zu scrapen
                    progress_bar.progress(progress)
                    status_text.text(f'Fetched data for page: {line.split()[-3]}')  # Hier split(-3) verwenden, um die Seitennummer aus Ihrer Ausgabe zu extrahieren

                    process.communicate()

            st.write(f'Finished fetching data for ASIN: {asin}')










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



    html_string='''
    <script>
    // To break out of iframe and access the parent window
    const streamlitDoc = window.parent.document;

    // Make the replacement
    document.addEventListener("DOMContentLoaded", function(event){
            streamlitDoc.getElementsByTagName("footer")[0].innerHTML = 'Made with <a href="https://streamlit.io" target="_blank" style="text-decoration: none; color: white;">Streamlit</a> provided by Aenny, Cornelius, Tim and Alex';
        });
    </script>
    '''
    components.html(html_string)






if __name__ == "__main__":
    main()
