#STREAMLIT


import requests
import json
import streamlit as st

st.title('Scuole e università vicino a me?')

#This query requires too much time to filter:
#["amenity"~"kindergarten|school|university"]["name"~".*secondaria.*|.*primaria.*|.*infanzia.*|.*università|.*istituto.*", i];

#This query selects amenity tags starting with school, so it avoids music_school amenity tag, for example. It will be enough? Check it out
#["amenity"~"kindergarten|^school|university"];

#if POI["tags"]["amenity"] != 'driving_school'and POI["tags"]["amenity"] != 'music_school' and POI["tags"]["amenity"] != 'language_school':

#41.85704571781067, 12.562532626068288
latitudine_input = st.text_input("Inserire la latitudine: ")
try:
    latitudine = float(latitudine_input)  # Proviamo a convertire l'input in float
    if latitudine < 0:
        st.error("La latitudine deve essere positiva!")
        st.stop()  # Ferma l'esecuzione del codice qui
except ValueError:
    if latitudine_input:  # Se l'utente ha scritto qualcosa di non valido
        st.error("Inserisci una latitudine valida!")
        st.stop()  # Ferma l'esecuzione

longitudine_input = st.text_input("Inserire la longitudine: ")
try:
    longitudine = float(longitudine_input)  # Proviamo a convertire l'input in float
    if longitudine < 0:
        st.error("La longitudine deve essere positiva!")
        st.stop()  # Ferma l'esecuzione del codice qui
except ValueError:
    if longitudine_input:  # Se l'utente ha scritto qualcosa di non valido
        st.error("Inserisci una longitudine valida!")
        st.stop()  # Ferma l'esecuzione

R = st.slider('Raggio, in km, entro il quale si vuole cercare:', 1, 5)  #this is a widget
R = R*1000
radius = str(R)

if st.button("Trova", type="primary"):
  #st.write(f"Le coordinate considerate sono: **{latitudine}**, **{longitudine}**")

  # Query Overpass QL
  query = f"""
  [out:json];
  (
    node(around:{radius}, {latitudine}, {longitudine})
    ["amenity"~"kindergarten|^school|university"];
  );
  out body;
  >;
  """

  # Invia la richiesta all'API
  url = "http://overpass-api.de/api/interpreter"
  response = requests.post(url, data=query)

  # Elabora la risposta JSON
  data = response.json()
  POIs = data["elements"]

  # Stampa il numero di ristoranti trovati
  st.subheader(f"Scuole e/o università trovate nel raggio di {R/1000} km: {len(POIs)}.")
  st.divider()

  scuole_infanzia = []
  scuole = []
  universita = []

  si = 0
  s = 0
  u = 0

  # Stampa i nomi dei ristoranti (se presenti)
  for POI in POIs:
    if POI["tags"]["amenity"] == 'kindergarten':
      si += 1
      if "tags" in POI and "name" in POI["tags"]:
        scuole_infanzia.append(POI["tags"]["name"])
    if POI["tags"]["amenity"] == 'school':
      s += 1
      if "tags" in POI and "name" in POI["tags"]:
        scuole.append(POI["tags"]["name"])
    if POI["tags"]["amenity"] == 'university':
      u += 1
      if "tags" in POI and "name" in POI["tags"]:
        universita.append(POI["tags"]["name"])

  if si > 0:
    if si - len(scuole_infanzia) > 0 and len(scuole_infanzia) > 0:
      st.subheader(f"\nScuole dell\'infanzia trovate: **{si}**. Di cui senza nome: **{si-len(scuole_infanzia)}**\n")
    if si - len(scuole_infanzia) > 0 and len(scuole_infanzia) == 0:
      st.subheader(f"\nScuole dell\'infanzia trovate: **{si}**. Tutte senza nome\n")
    if si - len(scuole_infanzia) == 0:
      st.subheader(f"\nScuole dell\'infanzia trovate: **{si}**.\n")
    if len(scuole_infanzia) > 0:
      for i in range(len(scuole_infanzia)):
        st.write(scuole_infanzia[i])

  st.divider()

  if s > 0:
    if s - len(scuole) > 0 and len(scuole) > 0:
      st.subheader(f"\nScuole trovate: **{s}**. Di cui senza nome: **{s-len(scuole)}**\n")
      for i in range(len(scuole)):
        st.write(scuole[i])
    if s - len(scuole) > 0 and len(scuole) == 0:
      st.subheader(f"\nScuole trovate: **{s}**. Tutte senza nome\n")
    if s - len(scuole) == 0:
      st.subheader(f"\nScuole trovate: **{s}**.\n")
    if len(scuole) > 0:
      for i in range(len(scuole)):
        st.write(scuole[i])

  st.divider()

  if u > 0:
    if u - len(universita) > 0 and len(universita) > 0:
      st.subheader(f"\nUniversità trovate: **{u}**. Di cui senza nome: **{u-len(universita)}**\n")
      for i in range(len(universita)):
        st.write(universita[i])
    if u - len(universita) > 0 and len(universita) == 0:
      st.subheader(f"\nUniversità trovate: **{u}**. Tutte senza nome\n")
    if u - len(universita) == 0:
      st.subheader(f"\nUniversità trovate: **{u}**.\n")
    if len(universita) > 0:
      for i in range(len(universita)):
        st.write(universita[i])
  st.divider()
  st.write(
    "Dati forniti da [OpenStreetMap](https://www.openstreetmap.org) sotto licenza [ODbL](https://opendatacommons.org/licenses/odbl/)."
  )
