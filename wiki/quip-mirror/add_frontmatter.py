#!/usr/bin/env python3
"""Add YAML frontmatter to all quip-mirror markdown files using metadata from directory crawl."""
import os
import re
from datetime import datetime

# Metadata collected from Quip directory API crawl (updated_usec, creator_id, folder_path)
# Creator ID mapping (resolved from @mentions in doc content)
CREATORS = {
    "YAT9EAkZs9f": "Richard Williams",
    "LMb9EALbtNs": "Stacey Gu",
    "CHc9EAIyg0X": "Peter Ocampo",
    "HHP9EANvnA1": "Yun-Kang Chu",
}

# Document metadata from directory crawl: quip_id -> (title, updated_usec, creator_id, folder_path)
DOCS = {
    # Root level
    "FZQ9AARARAN": ("MBet Process Improvement", 1725479290793874, "YAT9EAkZs9f", "root"),
    "NXF9AAy02OQ": ("PO Process Options - Paid Search", 1753803542155372, "YAT9EAkZs9f", "root"),
    # Testing root
    "UCa9AAcbP8I": ("Amazon Business - Paid Search Measurement", 1733356813204152, "YAT9EAkZs9f", "Testing"),
    "FAZ9AAzxU6P": ("DG Test results and CPS Y25 Testing Plan", 1764702781393256, "YAT9EAkZs9f", "Testing"),
    "KCY9AAYqWd2": ("PS Testing: Ad Copy Updates", 1773857279635975, "YAT9EAkZs9f", "Testing"),
    "ReG9AAvZFTS": ("PS Testing: Ads & Ad Copy", 1744927670491335, "YAT9EAkZs9f", "Testing"),
    "abc9AAsI8rV": ("PS Testing: Audiences", 1759262380410552, "YAT9EAkZs9f", "Testing"),
    "ePH9AAU0wIA": ("PS Testing: Bidding Algorithms", 1700000965590785, "YAT9EAkZs9f", "Testing"),
    "dKf9AAexRbL": ("PS Testing: CA and IT Carousel", 1772662752405717, "YAT9EAkZs9f", "Testing"),
    "VDf9AA5JiIY": ("PS Testing: CPS", 1759262312350567, "YAT9EAkZs9f", "Testing"),
    "IPB9AAeNAQB": ("PS Testing: Current Weblab/Tests", 1770853194191584, "YAT9EAkZs9f", "Testing"),
    "NQA9AAX2DOp": ("PS Testing: Incrementality Test", 1759262292683919, "YAT9EAkZs9f", "Testing"),
    "WKS9AAlN5pT": ("PS Testing: Secondary Language", 1724255255931836, "YAT9EAkZs9f", "Testing"),
    "YEG9AAoOEiO": ("PS Testing: UK MAC Impact", 1772662816695283, "YAT9EAkZs9f", "Testing"),
    "KBL9AAquAv5": ("PS Testing: US Promo Test", 1765387091454499, "YAT9EAkZs9f", "Testing"),
    "IUA9AAGTmnc": ("US/UK CPS DG Test results", 1753890672398987, "YAT9EAkZs9f", "Testing"),
    # Testing/.JP
    "OcF9AABMjFY": ("2022.10_Yahoo-JP-NB_Experiment", 1771878958767840, "YAT9EAkZs9f", "Testing/.JP"),
    "EGR9AANdsKO": ("2023.01_JP-NB_Experiment-Doc", 1771878964664214, "YAT9EAkZs9f", "Testing/.JP"),
    "fcU9AAjhD9R": ("2023.04_JP_Discovery-Experiment", 1771878977075260, "YAT9EAkZs9f", "Testing/.JP"),
    "SCD9AATSR90": ("2023.10_JP_Pmax-Experiment", 1771878988197020, "YAT9EAkZs9f", "Testing/.JP"),
    "dFZ9AA5fAz2": ("2024 JP NB Tests", 1771878994157810, "YAT9EAkZs9f", "Testing/.JP"),
    "PbI9AAI6SDn": ("2025.06_JP_LP-Experiment", 1769198348574055, "YAT9EAkZs9f", "Testing/.JP"),
    "AeG9AAmSPdu": ("FY25 JP Testing", 1767847020721915, "YAT9EAkZs9f", "Testing/.JP"),
    "CRB9AARVJK8": ("JP NB Test Results 2022", 1771879017341337, "YAT9EAkZs9f", "Testing/.JP"),
    "PSa9AAWBFPB": ("JP Performance: Post-MHLW Normalization Analysis", 1771340364879661, "YAT9EAkZs9f", "Testing/.JP"),
    # Testing/.NA
    "HNL9AA4Zse1": ("Brand Core - Primelis Test", 1755211457996817, "YAT9EAkZs9f", "Testing/.NA"),
    "NXb9AAss6tU": ("CA NB CVR analysis v1.27 v2", 1774980703454335, "YAT9EAkZs9f", "Testing/.NA"),
    "CFL9AACJeKF": ("Testing: Algorithm Stabilization", 1700000994760631, "YAT9EAkZs9f", "Testing/.NA"),
    # Testing/.EU
    "LJb9AAugth6": ("2024.12.10 - IT Bid Modifiers Test", 1739915470172788, "YAT9EAkZs9f", "Testing/.EU"),
    # Testing/Landing Pages
    "LLJ9AAmkj0W": ("2023.11 - Brand LP Test - CPS column", 1706198711595158, "YAT9EAkZs9f", "Testing/Landing Pages"),
    "MQD9AAT1lD8": ("Paid Search MCS LP vs. Email Submit Page Test Results", 1717429005032396, "YAT9EAkZs9f", "Testing/Landing Pages"),
    "AZW9AAdOQYk": ("PS LP Testing: Percolate / Guest", 1767847014948113, "YAT9EAkZs9f", "Testing/Landing Pages"),
    "BLP9AAhFfua": ("PS Testing: Landing Pages (LP)", 1763583966044471, "YAT9EAkZs9f", "Testing/Landing Pages"),
    "KKI9AAboWRC": ("PS Testing: Promo WTS", 1765299847602035, "YAT9EAkZs9f", "Testing/Landing Pages"),
    # Testing/Paid App
    "ARO9AAwdXlU": ("2023.08 - JP App Testing Results", 1700233586136633, "YAT9EAkZs9f", "Testing/Paid App"),
    # Review
    "PcT9AAjVFnR": ("2024 Paid Acq MBR / QBR", 1754673528484915, "LMb9EALbtNs", "Review"),
    "TaH9AAAK0Le": ("2025 Paid Acq MBR / QBR", 1770243990299596, "LMb9EALbtNs", "Review"),
    "JMJ9AAK2OKX": ("2026 Paid Acq MBR / QBR", 1775502534250381, "LMb9EALbtNs", "Review"),
    "TRA9AAguFLk": ("BP Paid Search Review 8/28/23", 1713795087385374, "YAT9EAkZs9f", "Review"),
    "ROf9AAUIHIK": ("BP Paid Search Review 9/26/23", 1708375204874942, "YAT9EAkZs9f", "Review"),
    "ZJR9AAdi0DC": ("Deep Dive & Debate", 1771433337522179, "YAT9EAkZs9f", "Review"),
    "TVV9AAKgfea": ("Global Acq WBR Callouts", 1775653894309319, "YAT9EAkZs9f", "Review"),
    "Zee9AAlSBEB": ("OCI - Paid Search Instructions", 1775578456129839, "YAT9EAkZs9f", "Review"),
    "YKf9AAbVkG8": ("Outbound Marketing Meetings", 1769534845197600, "YAT9EAkZs9f", "Review"),
    "WdY9AAy8tDh": ("Paid Acquisition SIMs", 1771863753374252, "YAT9EAkZs9f", "Review"),
    "GCI9AA5aLG0": ("Y23 CPS Paid Search Review", 1755271606978181, "YAT9EAkZs9f", "Review"),
    # Partnerships/CPS
    "JOK9AAJ1qah": ("CPS meeting notes", 1724189526308302, "YAT9EAkZs9f", "Partnerships/CPS"),
    "DVL9AAJQkxm": ("Y24 Q3 CPS Performance Summary Draft", 1754522346813619, "YAT9EAkZs9f", "Partnerships/CPS"),
    "DQY9AARyPQg": ("CA CPS - Paid Search", 1774981890423261, "YAT9EAkZs9f", "Partnerships/CPS/CA"),
    "QTb9AASIOQn": ("CA MCS Updates", 1763054252955677, "YAT9EAkZs9f", "Partnerships/CPS/CA"),
    "WVY9AApilNf": ("CA Paid Search CPS Pilot Recap", 1709591948076651, "YAT9EAkZs9f", "Partnerships/CPS/CA"),
    "QQW9AADRqL9": ("Paid Search Campaign Request Form - CA CPS", 1674599680340379, "YAT9EAkZs9f", "Partnerships/CPS/CA"),
    "ABW9AA8Xivl": ("EU CPS - Paid Search", 1708094937341172, "YAT9EAkZs9f", "Partnerships/CPS/EU"),
    "UPM9AAnF3ht": ("EU CPS 2023", 1704383212616088, "YAT9EAkZs9f", "Partnerships/CPS/EU"),
    "YLc9AAQDSpu": ("H1 2023 EU5 CPS Paid Search", 1704383247390205, "YAT9EAkZs9f", "Partnerships/CPS/EU"),
    "PRL9AACSMZl": ("JP CPS - Paid Search", 1677791986780085, "YAT9EAkZs9f", "Partnerships/CPS/JP"),
    "Aee9AAqhAAa": ("US CPS - Paid Search", 1708010251504846, "YAT9EAkZs9f", "Partnerships/CPS/US"),
    # Partnerships/AB Seller
    "UML9AAMg0J8": ("2023.01_AB-Seller_Launch", 1707234845672444, "YAT9EAkZs9f", "Partnerships/AB Seller"),
    # Partnerships/Engagement
    "eJR9AANYuIY": ("Existing traffic experience", 1772642333644325, "YAT9EAkZs9f", "Partnerships/Engagement"),
    "XbW9AA3gq9l": ("BP Media Plan - Paid Search", 1704338561131438, "YAT9EAkZs9f", "Partnerships/Engagement/BP"),
    "NNS9AA8S5bA": ("BP Results", 1704340195761490, "YAT9EAkZs9f", "Partnerships/Engagement/BP"),
    "QWe9AAjUSk8": ("Engagement Paid Search Account - Test Planning", 1717603154182266, "YAT9EAkZs9f", "Partnerships/Engagement"),
    # Onboarding
    "TRe9AADWLrk": ("CPS PS Transition Doc", 1739492775657435, "YAT9EAkZs9f", "Onboarding/Docs"),
    "DRd9AAewJmz": ("On-boarding to EU", 1774888883501701, "YAT9EAkZs9f", "Onboarding/Docs"),
    "ETC9AAVBfHC": ("Onboarding Links & Reference", 1760042779427912, "YAT9EAkZs9f", "Onboarding/Docs"),
    "bOO9AAV1PNw": ("Partnership accounts - Onboarding", 1772827951334788, "YAT9EAkZs9f", "Onboarding/Docs"),
    "fQD9AAKPTX0": ("AI resources", 1740698247278269, "YAT9EAkZs9f", "Onboarding"),
    "Mfc9AAnH9Pp": ("Account Creation Checklist", 1768935199381549, "YAT9EAkZs9f", "Onboarding/Account Best Practice"),
    "ZfB9AA8dyA6": ("OCI/ROAS bid strategies", 1759774759178323, "YAT9EAkZs9f", "Onboarding/Account Best Practice"),
    "ISQ9AAo3soI": ("AB Channel Marketing - SQL Databases & Queries", 1724853648992317, "YAT9EAkZs9f", "Onboarding/Data"),
    "JNa9AA24e9W": ("Adobe Activity Map", 1736352380521821, "YAT9EAkZs9f", "Onboarding/Data"),
    "PWB9AAbFqoy": ("Adobe FTP files", 1774548015018945, "YAT9EAkZs9f", "Onboarding/Data"),
    # Planning
    "OAA9AAOTvDS": ("2026 OP1 / OP2", 1767905654305293, "YAT9EAkZs9f", "Planning/OP"),
    "MYP9AAixN3T": ("OP1 2025 - Paid Acquisition", 1738682779457935, "YAT9EAkZs9f", "Planning/OP"),
    "JUE9AAZm6cd": ("OP1 2026 - Paid Acquisition", 1746558012603127, "YAT9EAkZs9f", "Planning/OP"),
    "eFd9AAdpR3K": ("AB Competitors", 1758303909536057, "YAT9EAkZs9f", "Planning"),
    "XWZ9AAnZsPs": ("Project [insert codename here]", 1742925278985328, "YAT9EAkZs9f", "Planning"),
    # Events
    "XNO9AAHRoBN": ("2022 Event Plans: SBM, PEAS, Holiday", 1669924777275605, "YAT9EAkZs9f", "Events"),
    "KDe9AAMBNvL": ("2023 Event Plans", 1742579438708783, "YAT9EAkZs9f", "Events"),
    # Mobile App
    "QYQ9AAmBqdJ": ("App Marketing - Holidays Readiness List", 1724441830461942, "CHc9EAIyg0X", "Mobile App/Paid App"),
    "AKQ9AALzRZN": ("JP - Apple Search Ads", 1700070350874837, "YAT9EAkZs9f", "Mobile App/Paid App"),
    "NJa9AA36eTD": ("AB Mobile App OP1", 1724685024833687, "CHc9EAIyg0X", "Mobile App"),
    # EU
    "OfJ9AAhVjVX": ("EU Callouts notes", 1736555005345073, "YAT9EAkZs9f", "..EU"),
    "bUR9AAl2WjT": ("EU tactical log", 1734643805542959, "YAT9EAkZs9f", "..EU"),
    "ZaW9AAwBxg8": ("Google PO FAQs", 1770240001029551, "YAT9EAkZs9f", "..EU"),
    "dSM9AAaMwDD": ("New EU5 Bidding Strategy", 1703793023289991, "YAT9EAkZs9f", "..EU"),
    "CTM9AAFeei5": ("Paid Search EU5 CVR investigation", 1739475940018013, "YAT9EAkZs9f", "..EU"),
    # JP
    "DWe9AA5KfMp": ("JP 2022 Paid Search", 1673392165994116, "YAT9EAkZs9f", "..JP"),
    "ETF9AASoPAb": ("JP Paid Search Competitive Analysis", 1744064380078154, "YAT9EAkZs9f", "..JP"),
    "XHJ9AAlDwnq": ("JP Transition", 1743527489647266, "YAT9EAkZs9f", "..JP"),
    "aOE9AA8Vhsq": ("AB JP Paid Search Weekly Status", 1678161057989255, "YAT9EAkZs9f", "..JP/Meeting"),
    # ABIX
    "IAJ9AAZJsDL": ("2026 AU Testing", 1773874989581623, "YAT9EAkZs9f", ".ABIX/AU"),
    "JMZ9AAput1I": ("AU PS Launch", 1775147474470521, "YAT9EAkZs9f", ".ABIX/AU"),
    "ZZR9AAs7OfO": ("AU PS Weekly Performance", 1775010640426885, "YAT9EAkZs9f", ".ABIX/AU"),
    "eTF9AAkPHUu": ("AB MX Paid Search Sync", 1774408363596276, "YAT9EAkZs9f", ".ABIX/MX"),
    "EZZ9AAR7EEz": ("MX Audit - Keyword Cleanup Framework", 1756151462294729, "YAT9EAkZs9f", ".ABIX/MX"),
    "GCX9AAbP5Rh": ("MX Transition", 1764178830209117, "YAT9EAkZs9f", ".ABIX/MX"),
    # Creative
    "EPO9AAg62RR": ("MCS Page Creation & Authoring", 1772472805548671, "YAT9EAkZs9f", "Creative"),
}

# Topic inference from folder path
FOLDER_TOPICS = {
    "Testing": ["testing", "experiments", "paid-search"],
    "Testing/.JP": ["testing", "japan", "paid-search"],
    "Testing/.NA": ["testing", "north-america", "paid-search"],
    "Testing/.EU": ["testing", "europe", "paid-search"],
    "Testing/Landing Pages": ["testing", "landing-pages", "conversion"],
    "Testing/Paid App": ["testing", "mobile-app", "paid-app-marketing"],
    "Review": ["review", "mbr", "qbr", "reporting"],
    "Partnerships/CPS": ["cps", "enterprise", "partnerships"],
    "Partnerships/CPS/CA": ["cps", "canada", "partnerships"],
    "Partnerships/CPS/EU": ["cps", "europe", "partnerships"],
    "Partnerships/CPS/JP": ["cps", "japan", "partnerships"],
    "Partnerships/CPS/US": ["cps", "united-states", "partnerships"],
    "Partnerships/AB Seller": ["ab-seller", "partnerships"],
    "Partnerships/Engagement": ["engagement", "partnerships", "existing-customers"],
    "Partnerships/Engagement/BP": ["business-prime", "engagement", "partnerships"],
    "Onboarding": ["onboarding", "reference"],
    "Onboarding/Docs": ["onboarding", "reference", "transition"],
    "Onboarding/Account Best Practice": ["onboarding", "best-practices", "account-management"],
    "Onboarding/Data": ["onboarding", "data", "analytics"],
    "Planning": ["planning", "strategy"],
    "Planning/OP": ["planning", "op1", "op2", "budgets"],
    "Events": ["events", "promotions", "sitelinks"],
    "Mobile App": ["mobile-app", "paid-app-marketing"],
    "Mobile App/Paid App": ["mobile-app", "paid-app-marketing", "apple-search-ads"],
    "..EU": ["europe", "eu5", "paid-search"],
    "..JP": ["japan", "paid-search"],
    "..JP/Meeting": ["japan", "meetings", "status"],
    ".ABIX/AU": ["australia", "abix", "paid-search"],
    ".ABIX/MX": ["mexico", "abix", "paid-search"],
    "Creative": ["creative", "mcs", "landing-pages"],
    "root": ["process", "finance", "paid-search"],
}

MIRROR_ROOT = os.path.expanduser("~/shared/wiki/quip-mirror")

def usec_to_date(usec):
    """Convert microsecond timestamp to YYYY-MM-DD."""
    return datetime.fromtimestamp(usec / 1_000_000).strftime("%Y-%m-%d")

def find_file_for_id(quip_id):
    """Find the markdown file matching a quip_id prefix."""
    for root, dirs, files in os.walk(MIRROR_ROOT):
        for f in files:
            if f.startswith(quip_id) and f.endswith(".md"):
                return os.path.join(root, f)
    return None

def build_frontmatter(quip_id, title, updated_usec, creator_id, folder_path):
    creator_name = CREATORS.get(creator_id, creator_id)
    last_modified = usec_to_date(updated_usec)
    topics = FOLDER_TOPICS.get(folder_path, ["paid-search"])
    source_url = f"https://quip-amazon.com/{quip_id}"

    fm = "---\n"
    fm += f"quip_id: {quip_id}\n"
    fm += f"title: \"{title}\"\n"
    fm += f"source_url: {source_url}\n"
    fm += f"doc_type: document\n"
    fm += f"creator: {creator_name}\n"
    fm += f"last_modified: {last_modified}\n"
    fm += f"quip_folder: {folder_path}\n"
    fm += f"topics: [{', '.join(topics)}]\n"
    fm += f"mirror_date: 2026-04-10\n"
    fm += "---\n"
    return fm

def add_frontmatter_to_file(filepath, frontmatter):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already has frontmatter
    if content.startswith("---\n"):
        return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + "\n" + content)
    return True

def main():
    updated = 0
    skipped = 0
    missing = 0

    for quip_id, (title, updated_usec, creator_id, folder_path) in DOCS.items():
        filepath = find_file_for_id(quip_id)
        if not filepath:
            print(f"MISSING: {quip_id} ({title})")
            missing += 1
            continue

        fm = build_frontmatter(quip_id, title, updated_usec, creator_id, folder_path)
        if add_frontmatter_to_file(filepath, fm):
            updated += 1
        else:
            skipped += 1
            print(f"SKIPPED (already has frontmatter): {quip_id}")

    print(f"\nDone: {updated} updated, {skipped} skipped, {missing} missing")

if __name__ == "__main__":
    main()
