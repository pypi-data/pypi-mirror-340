# src/ChemInformant/cheminfo_api.py
import sys
import os

# Try to import api_helpers using relative import first
try:
    from . import api_helpers
except ImportError:
    # Fallback might be needed if run directly, but less relevant for installed package
    # For installed package, the relative import should work.
    # Keep the fallback just in case, but it points to potential issues if needed.
    print("Warning: Relative import failed. Attempting fallback for api_helpers.", file=sys.stderr)
    try:
        import api_helpers
    except ImportError:
         # If installed, this path logic might be complex. Let's assume relative works.
         # If it fails install, the structure or setup.py is the issue.
         sys.path.append(os.path.dirname(os.path.abspath(__file__)))
         import api_helpers


# Import required functions from api_helpers
from .api_helpers import ( # Ensure using relative import here too
    get_cid_by_name,
    get_cas_unii,
    get_compound_description,
    get_all_synonyms,
    get_additional_details
)

class ChemInfo:
    """Simplified API for retrieving chemical compound information from PubChem."""

    @staticmethod
    def _get_cid(name_or_cid):
        """Internal helper to get CID, returning None if not found."""
        if isinstance(name_or_cid, int):
            # Assume valid CID if int is passed
            return name_or_cid
        # Use the helper function to get CID by name
        cid = get_cid_by_name(name_or_cid)
        return cid # Returns None if not found by the helper

    @staticmethod
    def cid(name_or_cid):
        """Get the PubChem Compound ID (CID) for a chemical compound."""
        cid = ChemInfo._get_cid(name_or_cid)
        return cid if cid is not None else "Not found"

    @staticmethod
    def cas(name_or_cid):
        """Get the CAS Registry Number for a chemical compound."""
        cid = ChemInfo._get_cid(name_or_cid)
        if cid:
            cas, _ = get_cas_unii(cid)
            return cas # get_cas_unii returns "Not found" appropriately
        return "Not found"

    @staticmethod
    def uni(name_or_cid):
        """Get the UNII code for a chemical compound."""
        cid = ChemInfo._get_cid(name_or_cid)
        if cid:
            _, unii = get_cas_unii(cid)
            return unii # get_cas_unii returns "Not found" appropriately
        return "Not found"

    @staticmethod
    def form(name_or_cid):
        """Get the molecular formula for a chemical compound."""
        cid = ChemInfo._get_cid(name_or_cid)
        if cid:
            props = get_additional_details(cid)
            return props.get('MolecularFormula', 'N/A')
        return "N/A" # Changed from "Not found" for consistency with others

    @staticmethod
    def wgt(name_or_cid):
        """Get the molecular weight for a chemical compound."""
        cid = ChemInfo._get_cid(name_or_cid)
        if cid:
            props = get_additional_details(cid)
            return props.get('MolecularWeight', 'N/A')
        return "N/A"

    @staticmethod
    def smi(name_or_cid):
        """Get the SMILES notation for a chemical compound."""
        cid = ChemInfo._get_cid(name_or_cid)
        if cid:
            props = get_additional_details(cid)
            return props.get('CanonicalSMILES', 'N/A')
        return "N/A"

    @staticmethod
    def iup(name_or_cid):
        """Get the IUPAC name for a chemical compound."""
        cid = ChemInfo._get_cid(name_or_cid)
        if cid:
            props = get_additional_details(cid)
            return props.get('IUPACName', 'N/A')
        return "N/A"

    @staticmethod
    def dsc(name_or_cid):
        """Get the description for a chemical compound."""
        cid = ChemInfo._get_cid(name_or_cid)
        if cid:
            return get_compound_description(cid) # Returns "No description available" appropriately
        return "No description available"

    @staticmethod
    def syn(name_or_cid):
        """Get the synonyms for a chemical compound."""
        cid = ChemInfo._get_cid(name_or_cid)
        if cid:
            return get_all_synonyms(cid) # Returns [] appropriately
        return []

    @staticmethod
    def all(name_or_cid):
        """Get all available information for a chemical compound."""
        cid = ChemInfo._get_cid(name_or_cid)
        if not cid:
            # Use the input name if it was a string, otherwise indicate it was a non-found CID
            compound_identifier = name_or_cid if isinstance(name_or_cid, str) else f"Input CID {name_or_cid}"
            return {"Error": f"Compound '{compound_identifier}' not found"}

        cas, unii = get_cas_unii(cid)
        props = get_additional_details(cid)
        description = get_compound_description(cid)
        synonyms = get_all_synonyms(cid)

        # Try to find a common name from synonyms if input was CID
        common_name = name_or_cid
        if isinstance(name_or_cid, int) and synonyms:
             common_name = synonyms[0] # Or implement logic to find a better common name

        return {
            "Common Name": common_name,
            "CID": cid,
            "CAS": cas,
            "UNII": unii,
            "MolecularFormula": props.get('MolecularFormula', 'N/A'),
            "MolecularWeight": props.get('MolecularWeight', 'N/A'),
            "CanonicalSMILES": props.get('CanonicalSMILES', 'N/A'),
            "IUPACName": props.get('IUPACName', 'N/A'),
            "Description": description,
            "Synonyms": synonyms
        }

    # Legacy method names as aliases for backward compatibility
    CID = cid
    CAS = cas
    UNII = uni
    formula = form
    weight = wgt
    smiles = smi
    iupac_name = iup
    description = dsc
    synonyms = syn