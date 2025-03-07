#Petrifilm ranges
countable_ranges = {
    "APC Petrifilm": (25, 250),
    "E. Coli Petrifilm": (15, 150),
    "Staph Petrifilm": (1, 100),
    "Yeast Petrifilm": (1, 150),
    "Mold Petrifilm": (1, 150)
}

result_units = {
    "APC Petrifilm": "CFU",
    "E. Coli Petrifilm": "CFU",
    "Staph Petrifilm": "CFU",
    "Yeast Petrifilm": "CFU",
    "Mold Petrifilm": "CFU",
    "Moisture": "%",
    "Received Temp": "\N{DEGREE SIGN}C"
}

pathogen_results = ["Absence", "Presence"]

#Result entry test list types
petrifilm_tests = [2, 3, 4, 5, 6]
pathogen_tests = [7, 8]
chemistry_tests = [1, 9, 10]