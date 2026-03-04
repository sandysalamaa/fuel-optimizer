#----------------------------------------------------------------------------
# Decodes the polyline geometry returned by the routing API.
#----------------------------------------------------------------------------

import polyline

def decode_geometry(encoded_geometry):
    """
    Takes encoded polyline string from ORS
    Returns list of (lat, lon) tuples
    """
    return polyline.decode(encoded_geometry)