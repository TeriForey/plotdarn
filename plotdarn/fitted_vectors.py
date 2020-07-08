import numpy as np
import copy
import aacgmv2
import scipy.special


ORDER = 6
DELTA_LAT = 0.05
DELTA_LT = 0.05
RE = 6371e3
ALT = 300e3
BEQ = 31000e-9


def sdarn_plm(l, m, x):
    """
    Calculate the Associated Legendre Polynomial of degree l and order m (0 =< m =< l) for the value x (-1 < x < 1)
    Algorithm from Numerical Recipes
    """
    # Compute P, m, m
    pmm = 1.0
    if m > 0:
        somx2 = np.sqrt((1.0 - x) * (1.0 + x))
        fact = 1.0
        for i in range(1, m + 1):
            pmm = -pmm * fact * somx2
            fact = fact + 2.0
    if l == m:
        return pmm

    # Compute P, m, m+1
    pmmp1 = x * (2 * m + 1) * pmm
    if l == m + 1:
        return pmmp1

    # Compute p, m, l
    for ll in range(m + 2, l + 1):
        pll = (x * (2 * ll - 1) * pmmp1 - (ll + m - 1) * pmm) / (ll - m)
        pmm = pmmp1
        pmmp1 = pll
    return pll


def sdarn_ylm(l, m, theta, phi):
    """
    Calculate the spherical harmonic Ylm of degree l and order m (-l <= m <= l) for the values of
    theta and phi. In general Ylm is complex; return a [Re(Ylm), Im(Ylm)]
    """
    if m >= 0:
        phase = 1
    else:
        phase = ((-1) ** abs(m))
    ylm_intermediate = phase * scipy.special.lpmv(m, l, np.cos(theta))
    return ylm_intermediate * np.cos(m * phi), ylm_intermediate * np.sin(m * phi)


def sdarn_get_potential(coeffs, hmb_lat, mag_lat, mag_LT):
    """
    Expand the spherical harmonic series with the map-pot coefficients
    to give the electrostatic potential at a particular magnetic latitude
    and local time position
    """
    phi = 2 * np.pi * mag_LT / 24
    theta = np.pi * (90 - mag_lat) / (90 - abs(hmb_lat))
    if theta > np.pi:
        return 0
    pot = 0.0
    for l in range(ORDER + 1):
        for m in range(l + 1):
            if l == 0:
                k = 0
            elif m == 0:
                k = l * l
            else:
                k = l * l + 2 * m - 1
            ylm = sdarn_ylm(l, m, theta, phi)
            pot = pot + coeffs[k] * ylm[0] + coeffs[k + 1] * ylm[1]
    return pot


def sdarn_get_efield(coeffs, hmb_lat, mag_lat, mag_LT):
    """
    Determine the meridional and zonal electric field components at a particular
    magnetic latitude and local time. In this version evaluates the potential at
    three locations and finds spatial gradient; a more sophisticated analysis would
    differentiate the spherical harmonic expansion.
    """

    pot0 = sdarn_get_potential(coeffs, hmb_lat, mag_lat, mag_LT)
    pot1 = sdarn_get_potential(coeffs, hmb_lat, mag_lat + DELTA_LAT, mag_LT)
    pot2 = sdarn_get_potential(coeffs, hmb_lat, mag_lat, mag_LT + DELTA_LT)

    e_meridional = (pot1 - pot0) / (2 * np.pi * RE * (DELTA_LAT / 360))
    e_zonal = (pot2 - pot0) / (2 * np.pi * RE * np.sin(np.deg2rad(90 - mag_lat)) * (DELTA_LT / 24))

    return e_meridional, e_zonal


def sdarn_get_vel(coeffs, hmb_lat, mag_lat, mag_LT):
    """
    Determine the meridional and zonal plasma drift velocity components at a particular
    magnetic latitude and local time
    """
    emeri, ezone = sdarn_get_efield(coeffs, hmb_lat, mag_lat, mag_LT)

    b = BEQ * np.sqrt(1 + 3 * np.cos(np.deg2rad(90 - mag_lat)) ** 2) * (RE / (RE + ALT)) ** 3

    v_zonal = emeri / b
    v_meridional = -ezone / b

    return v_meridional, v_zonal


def sdarn_rotate_coeffs(coeffs, ut):
    """
    Rotate map-pot coefficients from magnetic longitude to MLT grid
    """
    d_phi = 2 * np.pi * (ut - 4.73) / 24
    new_coeffs = copy.copy(coeffs)
    for m in range(1, ORDER + 1):
        for l in range(m, ORDER + 1):
            k = l * l + 2 * m - 1
            new_coeffs[k] = coeffs[k] * np.cos(m * d_phi) - coeffs[k + 1] * np.sin(m * d_phi)
            new_coeffs[k + 1] = coeffs[k + 1] * np.cos(m * d_phi) + coeffs[k] * np.sin(m * d_phi)

    return new_coeffs


def sdarn_maglon2MLT(mag_lon, ut):
    """
    convert mag_lon to MLT. Probably won't use this and stick with AACGMv2 method
    """
    return (mag_lon/15 + (ut-4.73) + 48) % 24


def sdarn_get_fitted(coeffs, hmb_lat, mag_lat, mag_LT):
    """
    Calculate fitted vectors with MLT and already rotated coeffs
    """

    # get meridional and zonal plasma drift velocity components
    vmeri, vzone = sdarn_get_vel(coeffs, hmb_lat, mag_lat, mag_LT)

    # Fitted azimuth and magnitude
    fitv_azi = np.degrees(np.arctan2(vzone, vmeri))
    fitv_mag = np.sqrt(vzone ** 2 + vmeri ** 2)

    return fitv_azi, fitv_mag


def fitted_vecs(coeffs, mlat, mlon, dtime, minlat=50):
    ut = (dtime - dtime.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    rotated_coeffs = sdarn_rotate_coeffs(coeffs, ut)
    mlts = aacgmv2.convert_mlt(mlon, dtime)

    azimuths = []
    magnitudes = []

    for i in range(len(mlon)):
        azi, mag = sdarn_get_fitted(rotated_coeffs, minlat, mlat[i], mlts[i])
        azimuths.append(azi)
        magnitudes.append(mag)

    return azimuths, magnitudes


def sdarn_get_fitted_Steve(coeffs, hmb_lat, mag_lat, mag_lon, ut, dtime):
    """
    Calculate fitted vectors azimuth and magnitude using Steve's approximate MLT values.
    """
    # get MLT
    mag_LT = sdarn_maglon2MLT(mag_lon, ut)

    # convert coeffs to MLT
    new_coeffs = sdarn_rotate_coeffs(coeffs, ut)

    # get meridional and zonal plasma drift velocity components
    vmeri, vzone = sdarn_get_vel(new_coeffs, hmb_lat, mag_lat, mag_LT)

    # Fitted azimuth and magnitude
    fitv_azi = np.degrees(np.arctan2(vzone, vmeri))
    fitv_mag = np.sqrt(vzone ** 2 + vmeri ** 2)

    return fitv_azi, fitv_mag


def sdarn_get_fitted_AACGM(coeffs, hmb_lat, mag_lat, mag_lon, ut, dtime):
    """
    Calculate fitted vectors azimuth and magnitude using AACGMv2 MLT values
    """

    # get MLT
    mag_LT = aacgmv2.convert_mlt(mag_lon, dtime)[0]

    # convert coeffs to MLT
    new_coeffs = sdarn_rotate_coeffs(coeffs, ut)

    # get meridional and zonal plasma drift velocity components
    vmeri, vzone = sdarn_get_vel(new_coeffs, hmb_lat, mag_lat, mag_LT)

    # Fitted azimuth and magnitude
    fitv_azi = np.degrees(np.arctan2(vzone, vmeri))
    fitv_mag = np.sqrt(vzone ** 2 + vmeri ** 2)

    return fitv_azi, fitv_mag


def sdarn_get_potential_grid(coeffs, hmb_lat=50):
    pot_grid = np.zeros((80, 80))
    for i in range(0, 80):
        for j in range(0, 80):
            x = i-39.5
            y = j-39.5
            mag_lat = 90 - np.sqrt(x**2 + y**2)
            mag_LT = 24 * np.arctan2(x, -y) / (2 * np.pi)
            pot_grid[i, j] = sdarn_get_potential(coeffs, hmb_lat, mag_lat, mag_LT)
    return pot_grid

