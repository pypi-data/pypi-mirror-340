import os

def read_coefficients(instance):
    """
    Read the World Magnetic Model (WMM) coefficients from a file and populate the instance variables.
    
    This function reads spherical harmonic coefficients from a WMM coefficient file (.COF) and
    assigns them to the appropriate arrays in the provided instance. The coefficient file follows
    the standard format used by NOAA's National Centers for Environmental Information (NCEI).
    
    Parameters:
        instance: An instance of WMMv2 or compatible model class that contains the following attributes:
            - coeff_file (str, optional): Custom path to coefficient file
            - epoch (float): Base epoch of the model (will be set from file)
            - defaultDate (float): Default calculation date (will be set to epoch + 2.5 years)
            - c (list): 2D array for Gauss coefficients (gnm, hnm)
            - cd (list): 2D array for secular variation coefficients (dgnm, dhnm)
    
    Notes:
        - If instance.coeff_file is not specified, the default WMM.COF file in the package's
          data directory will be used.
        - The file format is expected to contain:
            * Header line with epoch year 
            * Data lines with: n, m, gnm, hnm, dgnm, dhnm values
                where:
                - n: degree (int)
                - m: order (int)
                - gnm: Gauss coefficient (float, nT)
                - hnm: Gauss coefficient (float, nT)
                - dgnm: Annual rate of change (float, nT/year)
                - dhnm: Annual rate of change (float, nT/year)
        - Coefficients are stored in a specific arrangement in the instance arrays:
            * c[m][n] stores gnm values
            * c[n][m-1] stores hnm values (for m > 0)
            * cd[m][n] stores dgnm values
            * cd[n][m-1] stores dhnm values (for m > 0)
    
    Raises:
        FileNotFoundError: If the coefficient file cannot be found
        ValueError: If the coefficient file format is invalid
    """
    file_path = getattr(instance, 'coeff_file', None)
    if not file_path:
        file_path = os.path.join(os.path.dirname(__file__), "data", "WMM.COF")
    with open(file_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) == 1:
                break
            if len(parts) == 3:
                instance.epoch = float(parts[0])
                instance.defaultDate = instance.epoch + 2.5
            else:
                n = int(parts[0])
                m = int(parts[1])
                gnm = float(parts[2])
                hnm = float(parts[3])
                dgnm = float(parts[4])
                dhnm = float(parts[5])
                if m <= n:
                    instance.c[m][n] = gnm
                    instance.cd[m][n] = dgnm
                    if m != 0:
                        instance.c[n][m - 1] = hnm
                        instance.cd[n][m - 1] = dhnm