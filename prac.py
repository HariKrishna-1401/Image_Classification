import requests, pickle
import bs4 as bs

#### This scraper gets course codes from LiTH ####

payload = {
    "-Maxrecords": "2500",
    "kp_programkod": "",
    "kp_institution": "",
    "kp_termin_ber": "",
    "kp_period_ber": "",
    "kp_schemablock": "",
    "kp_huvudomrade_sv": "",
    "kp_utb_niva": "",
    "kp_kurskod": "",
    "kp_kursnamn_sv": "",
    "kp_kursinnehall_sv": "",
    "-Search": "S%C3%B6k",
}

institutions = {
    'CTE',
    'EKI',
    'ESI',
    'IBK',
    'IDA',
    'IEI',
    'IFM',
    'IHM',
    'IKE',
    'IKK',
    'IKP',
    'IMH',
    'IMK',
    'IMT',
    'IMV',
    'IPE',
    'ISAK',
    'ISK',
    'ISV',
    'ISY',
    'ITN',
    'ITUF',
    'MAI',
    'TEMA',
    'TFK'
}

levels = {"G1", "G2", "A"}

url_swe = "http://kdb-5.liu.se/liu/lith/studiehandboken/search_10/search_response_sv.lasso"
url_eng = "http://kdb-5.liu.se/liu/lith/studiehandboken/search_17/search_response_sv.lasso"

def get_course_codes(institution, level, url_str):
    payload["kp_institution"] = institution
    payload["kp_utb_niva"] = level

    res = requests.post(url=url_str,
                        data=payload)
    try:
        res.raise_for_status()
    except Exception as e:
        print("{}/{} raised an exception: {}".format(institution, level, e))

    soup = bs.BeautifulSoup(res.text, "lxml")

    table = soup.find("table")
    table_rows = table.find_all("tr")

    rows = []
    course_codes = []
    for tr in table_rows:
        td = tr.find_all("td")
        rows.append([i.text for i in td])
        row = [i.text for i in td]
        if len(row) == 4 and row[1] != '\xa0':
            course_codes.append(row[1])

    return course_codes


all_codes = dict()
total = 0
for inst in institutions:
    inst_dict = dict()
    for lev in levels:
        codes = set()
        [codes.add(c) for c in get_course_codes(inst, lev, url_eng)]
        [codes.add(c) for c in get_course_codes(inst, lev, url_swe)]
        inst_dict[lev] = codes
        total += len(codes)
        print("Gathered {} codes from {} at level {}.".format(len(codes), inst, lev))

    all_codes[inst] = inst_dict

print("Total courses gathered: {}".format(total))
print("Dumping to pickle object 'course_codes.p', a dictionary of dictionaries holding sets.\n"
      "The format is: {'institution': {'course level': <set of course codes>} }")

pickle.dump(all_codes, open("course_codes.p", "wb"))