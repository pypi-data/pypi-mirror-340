# ----------------------------
# Imports
# ----------------------------
import requests
from bs4 import BeautifulSoup
# ----------------------------
# Auth Context Manager Class
# ----------------------------
class Auth:
    def __init__(self, tc: str, password: str):
        self.session = requests.Session()
        self.login_url = "https://bilgimerkezi.bilfenlisesi.com/login"
        self.login_payload = f"tc={tc}&password={password}"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.target_url = "https://bilgimerkezi.bilfenlisesi.com" # Target URL after login
        self.verified = False

    def __enter__(self):
        response = self.session.post(self.login_url, data=self.login_payload, headers=self.headers, allow_redirects=False) # Don't auto-redirect

        if response.status_code == 302: # Check for redirect status code
             #Get redirect url
            redirect_url = response.headers.get('Location')
            if redirect_url == '/':
                  # Manual redirect to the final target URL to handle potential JavaScript or further actions
                  response = self.session.get(self.target_url)
                  if response.ok :
                      print("Login successful!")
                      self.verified = True
                  else:
                       print("Secondary redirect failed:", response.status_code)
            else:
                self.verified=False

        else:
            raise("Login failed:", response.status_code)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
# ----------------------------
# Function to Fetch
# ----------------------------
def get_kks_exam_page(session):
    """
    Fetch the KKS exam results page and return its raw HTML.
    """
    url = "https://bilgimerkezi.bilfenlisesi.com/sinav-sonuclari/konu-kavrama"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = session.get(url, headers=headers)
    response.raise_for_status()  # Raises an exception for HTTP errors (4xx/5xx)
    return response.text
def get_profile_page(session):
    """
    Fetch the /profil page and return the raw HTML text.
    """
    url = "https://bilgimerkezi.bilfenlisesi.com/profil"
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    response = session.get(url, headers=headers)
    response.raise_for_status()  # Raises HTTPError for bad responses (4xx/5xx)
    return response.text
def get_club_page(session):
    """
    Fetches the /club page HTML.
    """
    url = "https://bilgimerkezi.bilfenlisesi.com/kulup"
    resp = session.get(url, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    content = resp.text
    return content
def get_written_exam_page(session):
    """
    Fetch the written exam results page and return its raw HTML.
    """
    url = "https://bilgimerkezi.bilfenlisesi.com/sinav-sonuclari/yazili-sinav"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = session.get(url, headers=headers)
    response.raise_for_status()  # Throws an exception for 4xx/5xx errors
    return response.text
# ----------------------------
# Function to Parse
# ----------------------------
def parse_profile_info(html):
    """
    Parse the HTML to extract the student's and parents' information.
    Returns a dictionary with keys 'student' and 'parents'.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Locate the panel containing "ÖĞRENCİ BİLGİLERİ" text
    panel_heading = soup.find("div", class_="panel-heading", text=lambda t: t and "ÖĞRENCİ BİLGİLERİ" in t)
    if not panel_heading:
        return {"error": "Profile panel heading not found."}

    # The panel body is a sibling of the heading
    panel = panel_heading.find_parent("div", class_="panel")
    if not panel:
        return {"error": "Profile panel not found."}

    # There should be two tables with student info and parents info.
    tables = panel.find_all("table", class_="table-profile")
    if len(tables) < 2:
        return {"error": "Expected tables not found in the profile panel."}

    # Student info is assumed to be in the first table.
    student_table = tables[0]
    student_data = {}
    for row in student_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 2:
            label = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            if label:
                student_data[label] = value

    # Parents info is assumed to be in the second table.
    parents_table = tables[1]
    parents_rows = parents_table.find_all("tr")

    # Helper function: convert a <tr> into a list of text values
    def row_to_list(tr):
        return [cell.get_text(strip=True) for cell in tr.find_all(["td", "th"])]

    parsed_rows = [row_to_list(r) for r in parents_rows]

    # We assume that:
    # - Row 0: images (skip)
    # - Row 1: "Adı Soyadı" row
    # - Row 2: "Yakınlık" row
    # - Row 3: "Telefon" row
    # - Row 4: "Meslek" row
    row_labels = []
    row_values = []
    for idx, row_data in enumerate(parsed_rows):
        if idx == 0:
            continue  # skip image row
        if row_data:
            row_labels.append(row_data[0])
            row_values.append(row_data[1:])  # the rest columns are values for each parent

    # Transpose rows so that each column becomes a parent's set of data.
    parents_data = []
    if row_values:
        num_parents = len(row_values[0])
        for i in range(num_parents):
            parent_info = {}
            for j, label in enumerate(row_labels):
                # If a cell is missing, default to empty string
                value = row_values[j][i] if i < len(row_values[j]) else ""
                parent_info[label] = value
            parents_data.append(parent_info)

    return {
        "student": student_data,
        "parents": parents_data
    }
def parse_club_info(html):
    """
    Given the KULÜP page HTML, returns a dictionary of the 3 preferences:
      {
        "Tercih 1": "X Club",
        "Tercih 2": "Z Club",
        "Tercih 3": "Y Club"
      }
    If the user cannot currently make club selections, we can also detect
    and handle that message if needed.
    """
    soup = BeautifulSoup(html, "html.parser")

    # The main area is in <div class="bottom-container">
    bottom_container = soup.find("div", class_="bottom-container")
    if not bottom_container:
        return {"error": "bottom-container not found"}

    # Each Tercih is in a <div class="col-xs-4"> ...
    # We'll look for input elements with "value" in them.
    cols = bottom_container.find_all("div", class_="col-xs-4")

    results = {}
    for col in cols:
        label_el = col.find("label", class_="control-label")
        input_el = col.find("input", {"type": "text"})
        if label_el and input_el:
            label_text = label_el.get_text(strip=True)  # e.g. "Tercih 1"
            chosen_value = input_el.get("value", "")    # e.g. "ROKET KULÜBÜ"
            results[label_text] = chosen_value

    return results
def parse_written_exam(html):
    """
    Parse the HTML of the written exam results page.

    This page displays two tab panes for two terms (e.g., 1. Dönem and 2. Dönem).
    For each term, we will extract exam data from the table by:
      - Using the first cell of each row as the subject name.
      - Using the last cell in the row as the final score.

    Returns a dictionary in the following structure:
      {
        "donem-1": {"MATEMATİK": "100.00", "TARİH": "23.00", ... },
        "donem-2": {"MATEMATİK": "100.00", "TARİH": "100.00", ... }
      }
    """
    soup = BeautifulSoup(html, "html.parser")
    results = {}

    # Locate the container with the tab panes
    tab_content = soup.find("div", class_="tab-content")
    if not tab_content:
        return {"error": "Tab content container not found."}

    # Find all tab panes (each should correspond to a term)
    tab_panes = tab_content.find_all("div", role="tabpanel")
    if not tab_panes:
        return {"error": "No tab panes found."}

    for pane in tab_panes:
        term_id = pane.get("id", "unknown_term")
        term_data = {}
        # Each tab pane should include a table inside a div with class "table-responsive"
        table_container = pane.find("div", class_="table-responsive")
        if not table_container:
            results[term_id] = {"error": "Table container not found."}
            continue

        table = table_container.find("table")
        if not table:
            results[term_id] = {"error": "Table not found."}
            continue

        tbody = table.find("tbody")
        if not tbody:
            results[term_id] = {"error": "Table body not found."}
            continue

        # Process each row in the table body
        for row in tbody.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue
            # The first cell should be the subject name
            subject = cells[0].get_text(strip=True)
            # The final score is assumed to be in the last cell
            final_score = cells[-1].get_text(strip=True)
            term_data[subject] = final_score

        results[term_id] = term_data

    return results
def parse_kks_exam(html):
    """
    Parse the HTML of the KKS exam results page.

    This page displays two tab panes (each for a term, e.g., 1. Dönem and 2. Dönem).
    For each tab pane, the function extracts data from the table:
      - The first column contains the subject name.
      - The last column contains the average (Ortalama) score.

    Returns a dictionary structured as:
        {
          "donem-1": {"TÜRK DİLİ VE EDEBİYATI": "83.67", "FİZİK": "66.67", ... },
          "donem-2": {"TÜRK DİLİ VE EDEBİYATI": "45.59", "İNGİLİZCE": "85.71", ... }
        }
    """
    soup = BeautifulSoup(html, "html.parser")
    results = {}

    # Locate the container holding the tab panes
    tab_content = soup.find("div", class_="tab-content")
    if not tab_content:
        return {"error": "Tab content container not found."}

    # Locate all tab panes (each should have role="tabpanel")
    tab_panes = tab_content.find_all("div", role="tabpanel")
    if not tab_panes:
        return {"error": "No tab panes found."}

    for pane in tab_panes:
        term_id = pane.get("id", "unknown_term")
        term_data = {}

        # Look for the table containing KKS exam scores
        table_container = pane.find("div", class_="table-responsive")
        if not table_container:
            results[term_id] = {"error": "Table container not found."}
            continue

        table = table_container.find("table", class_="karne-table")
        if not table:
            results[term_id] = {"error": "Exam table not found."}
            continue

        tbody = table.find("tbody")
        if not tbody:
            results[term_id] = {"error": "Table body not found."}
            continue

        # Iterate over each row and extract subject and average score.
        for row in tbody.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue
            subject = cells[0].get_text(strip=True)
            # The last cell is expected to be the average ("Ortalama")
            average_score = cells[-1].get_text(strip=True)
            term_data[subject] = average_score

        results[term_id] = term_data

    return results
# ----------------------------
# High-Level Function
# ----------------------------
def get_profile_info(session):
    """
    Fetches the profile page, parses it, and returns the extracted information.
    """
    html = get_profile_page(session)
    data = parse_profile_info(html)
    return data
def get_club_selections(session):
    """
    1) Fetch the /club page
    2) Parse out the current preferences (Tercih 1, 2, 3)
    3) Return them
    """
    html = get_club_page(session)
    data = parse_club_info(html)
    return data
def get_written_exam_info(session):
    """
    High-level function that fetches the written exam page,
    parses it, and returns structured exam data.
    """
    html = get_written_exam_page(session)
    return parse_written_exam(html)
def get_kks_exam_info(session):
    """
    High-level function:
      1. Fetches the KKS exam page.
      2. Parses the page to extract exam data.
      3. Returns the structured exam data.
    """
    html = get_kks_exam_page(session)
    return parse_kks_exam(html)

# ----------------------------
# Main Execution Block
# ----------------------------
if __name__ == "__main__":
    # Replace with your actual TC and password
    tc_number = "tc_number"
    password = "password"

    with Auth(tc_number, password) as auth:
        if auth.verified:
            print("Authentication successful. Proceeding with protected actions...")
            try:
                profile_data = get_profile_info(auth.session)
                print("\n--- Profile Information ---")
                print(profile_data)

                club_data = get_club_selections(auth.session)
                print("\n--- Club Selections ---")
                print(club_data)

                written_exam_data = get_written_exam_info(auth.session)
                print("\n--- Written Exam Results ---")
                print(written_exam_data)

                kks_exam_data = get_kks_exam_info(auth.session)
                print("\n--- KKS Exam Results ---")
                print(kks_exam_data)

            except requests.exceptions.RequestException as e:
                print(f"\nAn error occurred during a data request after successful login: {e}")
            except Exception as e:
                print(f"\nAn unexpected error occurred after login: {e}")
                import traceback
                traceback.print_exc() # Print stack trace for debugging parser issues

        else:
            print("\nAuthentication failed. Cannot proceed to fetch data.")