from geopy.distance import geodesic
  
SEDI = {
    Padova:{coordinate:(45.415158315584215, 11.8896580400549),
        testo:"Padova, From Farm to Fork.\nVia Niccolò Tommaseo, 59, 35131 Padova PD",
        link:"https://www.google.com/maps/dir/?api=1&destination=Via%20Niccol%C3%B2%20Tommaseo,%2059,%2035131%20Padova%20PD,%20Italia"},
    Pordenone:{coordinate:(45.94138790346552, 12.870402184527704),
        testo:"Pordenone, Digital Twin @LEF.\nVia Casabianca, 3, 33078 Zona Industriale Ponte Rosso PN",
        link:"https://www.google.com/maps/dir/?api=1&destination=Via%20Casabianca,%203,%2033078%20Zona%20Industriale%20Ponte%20Rosso%20PN,%20Italia"},
    Trieste:{coordinate:(45.72610621029036, 13.713786232463175),
        testo:"Trieste, Digital Twin @SISSA.\nVia Beirut, 2, 34151 Grignano TS",
        link:"https://www.google.com/maps/dir/?api=1&destination=Via%20Beirut,%202,%2034151%20Grignano%20TS,%20Italia"},
    Verona:{coordinate:(45.427846699639296, 10.983970831830348),
        testo:"Verona, Fabbrica del Vino.\nVia Santa Teresa, 12, 37135 Verona VR",
        link:"https://www.google.com/maps/dir/?api=1&destination=Via%20Santa%20Teresa,%2012,%2037135%20Verona%20VR,%20Italia"},
    Rovereto:{coordinate:(45.910270578080386, 11.032921620200522),
        testo:"Rovereto, M2M in Manifacturing.\nPolo Tecnologico Rovereto, Via Fortunato Zeni, 8, 38068 Rovereto TN",
        link:"https://www.google.com/maps/dir/?api=1&destination=Via%20Fortunato%20Zeni,%208,%2038068%20Rovereto%20TN,%20Italia"},
    Bolzano:{coordinate:(46.5284852672285, 11.307583576417715),
        testo:"Bolzano, H2M in Manifacturing.\nVia Alessandro Volta, 13, 39100 Bolzano BZ",
        link:"https://www.google.com/maps/dir/?api=1&destination=Via%20Alessandro%20Volta,%2013,%2039100%20Bolzano%20BZ,%20Italia"}
}


def nearest_production(posizione):
    sede="Padova"
    for elem in SEDI.keys():
        if geodesic(SEDI.sede.coordinate,(posizione.latitude,posizione.longitude))>geodesic(SEDI.elem.coordinate,(posizione.latitude,posizione.longitude)):
            sede=elem
    return [SEDI.sede.testo,SEDI.sede.link]



  
