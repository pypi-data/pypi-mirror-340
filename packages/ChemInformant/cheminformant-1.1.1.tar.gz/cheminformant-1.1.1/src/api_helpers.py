# src/ChemInformant/api_helpers.py
import requests
import sys # Added for potential error printing

PUBCHEM_API_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

def _make_api_request(url, identifier_type="CID", identifier=None):
    """Helper function to make requests and handle basic errors."""
    try:
        response = requests.get(url, timeout=10) # Added timeout
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        if response.status_code == 200:
            return response.json()
        return None # Should be caught by raise_for_status, but as fallback
    except requests.exceptions.RequestException as e:
        # Log error more informatively
        error_msg = f"API request failed for URL {url}"
        if identifier:
            error_msg += f" ({identifier_type}: {identifier})"
        print(f"{error_msg}: {e}", file=sys.stderr) # Print errors to stderr
        return None
    except Exception as e: # Catch other potential errors like JSONDecodeError
        error_msg = f"An unexpected error occurred processing URL {url}"
        if identifier:
            error_msg += f" ({identifier_type}: {identifier})"
        print(f"{error_msg}: {e}", file=sys.stderr)
        return None


def get_cid_by_name(compound_name):
    """Get the PubChem Compound ID (CID) for a chemical compound."""
    url = f"{PUBCHEM_API_BASE}/compound/name/{compound_name}/cids/JSON"
    data = _make_api_request(url, identifier_type="Name", identifier=compound_name)
    if data and 'IdentifierList' in data and 'CID' in data['IdentifierList']:
        # Check if CID list is not empty
        if data['IdentifierList']['CID']:
            return data['IdentifierList']['CID'][0]
    return None # Return None if not found or error occurs


def get_cas_unii(cid):
    """Get the CAS Registry Number and UNII code for a compound."""
    url = f"{PUBCHEM_API_BASE}/compound/cid/{cid}/synonyms/JSON"
    cas = "Not found"
    unii = "Not found"

    data = _make_api_request(url, identifier="CID", identifier=cid)
    if data and 'InformationList' in data and 'Information' in data['InformationList']:
        info = data['InformationList']['Information']
        if info and 'Synonym' in info[0]:
            synonyms = info[0]['Synonym']

            # Find CAS number (format: ###-##-#, can have more digits)
            for synonym in synonyms:
                parts = synonym.split('-')
                if len(parts) == 3 and all(p.isdigit() for p in parts):
                    cas = synonym
                    break # Found first one

            # Find UNII (10 characters, alphanumeric, often starts with a letter)
            # More robust check: usually uppercase letters and numbers
            for synonym in synonyms:
                if len(synonym) == 10 and synonym.isalnum() and synonym.isupper():
                     unii = synonym
                     break # Found first one

    return cas, unii


def get_compound_description(cid):
    """Get the description of a chemical compound."""
    url = f"{PUBCHEM_API_BASE}/compound/cid/{cid}/description/JSON"
    description = "No description available" # Default value

    data = _make_api_request(url, identifier="CID", identifier=cid)
    if data and 'InformationList' in data and 'Information' in data['InformationList']:
        info = data['InformationList']['Information']
        # Check list is not empty and first item has Description
        if info and 'Description' in info[0]:
            description = info[0]['Description']

    return description


def get_all_synonyms(cid):
    """Get all synonyms for a chemical compound."""
    url = f"{PUBCHEM_API_BASE}/compound/cid/{cid}/synonyms/JSON"
    synonyms = [] # Default to empty list

    data = _make_api_request(url, identifier="CID", identifier=cid)
    if data and 'InformationList' in data and 'Information' in data['InformationList']:
        info = data['InformationList']['Information']
        if info and 'Synonym' in info[0]:
            synonyms = info[0]['Synonym']

    return synonyms


def get_additional_details(cid):
    """Get additional chemical properties for a compound."""
    properties_list = "MolecularFormula,MolecularWeight,CanonicalSMILES,IUPACName"
    url = f"{PUBCHEM_API_BASE}/compound/cid/{cid}/property/{properties_list}/JSON"
    details = {} # Default to empty dict

    data = _make_api_request(url, identifier="CID", identifier=cid)
    if data and 'PropertyTable' in data and 'Properties' in data['PropertyTable']:
        properties = data['PropertyTable']['Properties']
        if properties: # Check if the list is not empty
            details = properties[0] # Get the first dictionary in the list

    # Ensure all expected keys exist, defaulting to 'N/A'
    for prop in properties_list.split(','):
        if prop not in details:
            details[prop] = 'N/A'

    return details