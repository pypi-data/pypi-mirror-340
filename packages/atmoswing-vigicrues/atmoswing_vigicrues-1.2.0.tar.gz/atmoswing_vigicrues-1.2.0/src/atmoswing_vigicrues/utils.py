import datetime
from pathlib import Path

import numpy as np

import atmoswing_vigicrues as asv


def file_exists(path):
    """
    Contrôle du chemin vers un fichier.

    Parameters
    ----------
    path: str or Path
        Le chemin vers le fichier.

    Returns
    -------
    bool
        Vrai (True) si le fichier existe, faux (False) sinon.

    Examples
    --------
    >>> file_exists(R'C:\\Users\\username\\Documents\\file.txt')
    True
    """
    if type(path) == str:
        path = Path(path)
    if not path.exists():
        return False
    if not path.is_file():
        return False
    return True


def check_file_exists(path):
    """
    Contrôle du chemin vers un fichier et lève une exception si le fichier n'existe pas.

    Parameters
    ----------
    path: str or Path
        Le chemin vers le fichier.

    Raises
    ------
    asv.FilePathError
        Si le chemin n'existe pas.
    asv.Error
        Si le chemin n'est pas un fichier.

    Examples
    --------
    >>> check_file_exists(R'C:\\Users\\username\\Documents\\file.txt')
    """
    if type(path) == str:
        path = Path(path)
    if not path.exists():
        raise asv.FilePathError(path)
    if not path.is_file():
        raise asv.Error(f"Le chemin '{path}' n'est pas un fichier.")


def check_dir_exists(path, create=False):
    """
    Contrôle du chemin vers un répertoire et lève une exception si le répertoire
    n'existe pas.

    Parameters
    ----------
    path: str or Path
        Le chemin vers le répertoire.
    create: bool
        Création du répertoire si celui-ci n'existe pas.

    Raises
    ------
    asv.Error
        Si le chemin n'existe pas.

    Examples
    --------
    >>> check_dir_exists(R'C:\\Users\\username\\Documents\\dir')
    """
    path_output = Path(path)
    if not path_output.exists():
        if create:
            path_output.mkdir(parents=True, exist_ok=True)
        else:
            raise asv.Error(f"Le répertoire '{path}' n'a pas été trouvé.")


def build_date_dir_structure(base, date):
    """
    Construit la structure de répertoires pour une date donnée.

    Parameters
    ----------
    base: str or Path
        Le répertoire de base.
    date: str or datetime.datetime
        La date à utiliser.

    Returns
    -------
    Path
        Le répertoire de base avec la structure de répertoires pour la date.

    Examples
    --------
    >>> build_date_dir_structure(R'D:\\Documents\\dir', '2020-01-01 00:00:00')
    Path('D:\\Documents\\dir\\2020\\01\\01')
    """
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    base = Path(base)
    base = base / date.strftime("%Y")
    base = base / date.strftime("%m")
    base = base / date.strftime("%d")
    return base


def jd_to_date(jd):
    """
    Transforme un nombre de jour julien en date (année, mois, jour).
    De https://gist.github.com/jiffyclub/1294443

    Parameters
    ----------
    jd: float
        Le nombre de jour julien.

    Returns
    -------
    year: int
        L'année.
    month: int
        Le mois.
    day: int
        Le jour.

    Examples
    --------
    >>> jd_to_date(2460096.5)
    (2023, 6, 1)
    """
    jd = jd + 0.5

    f, i = np.modf(jd)
    i = i.astype(int)

    a = np.trunc((i - 1867216.25) / 36524.25)
    b = np.zeros(len(jd))

    idx = tuple([i > 2299160])
    b[idx] = i[idx] + 1 + a[idx] - np.trunc(a[idx] / 4.)
    idx = tuple([i <= 2299160])
    b[idx] = i[idx]

    c = b + 1524
    d = np.trunc((c - 122.1) / 365.25)
    e = np.trunc(365.25 * d)
    g = np.trunc((c - e) / 30.6001)

    day = c - e + f - np.trunc(30.6001 * g)

    month = np.zeros(len(jd))
    month[g < 13.5] = g[g < 13.5] - 1
    month[g >= 13.5] = g[g >= 13.5] - 13
    month = month.astype(int)

    year = np.zeros(len(jd))
    year[month > 2.5] = d[month > 2.5] - 4716
    year[month <= 2.5] = d[month <= 2.5] - 4715
    year = year.astype(int)

    return year, month, day


def days_to_hours_mins(days):
    """
    Transforme un nombre de jours en heures et minutes.

    Parameters
    ----------
    days: float
        Le nombre de jours.

    Returns
    -------
    hour: int
        L'heure.
    minute: int
        La minute.

    Examples
    --------
    >>> days_to_hours_mins(0.5)
    (12, 0)
    """
    hours = days * 24.
    hours, hour = np.modf(hours)

    minutes = hours * 60.
    _, minute = np.modf(minutes)

    return hour.astype(int), minute.astype(int)


def mjd_to_datetime(mjd):
    """
    Transforme un tableau de nombre de jour julien modifié (MJD) en date
    (année, mois, jour, heure, minute).

    Parameters
    ----------
    mjd: ndarray
        Le tableau de nombre de jour julien modifié (MJD).

    Returns
    -------
    date: ndarray
        Le tableau de date.

    Examples
    --------
    >>> mjd_to_datetime(np.array([59215.5, 59216.5]))
    array(['2021-01-01T12:00:00', '2021-01-02T12:00:00'], dtype='datetime64[s]')
    """
    jd = mjd + 2400000.5
    year, month, day = jd_to_date(jd)

    frac_days, day = np.modf(day)
    day = day.astype(int)

    hour, minute = days_to_hours_mins(frac_days)

    date = np.empty(len(mjd), dtype='datetime64[s]')

    for idx, _ in enumerate(year):
        date[idx] = datetime.datetime(year[idx], month[idx], day[idx],
                                      hour[idx], minute[idx], 0, 0)

    return date


def build_cumulative_frequency(size):
    """
    Construit une distribution de fréquence cumulée.

    Parameters
    ----------
    size: int
        La taille de la distribution.

    Returns
    -------
    f: ndarray
        La distribution de fréquence cumulée.

    Examples
    --------
    >>> build_cumulative_frequency(10)
    """
    # Parameters for the estimated distribution from Gringorten (a=0.44, b=0.12).
    # Choice based on [Cunnane, C., 1978, Unbiased plotting positions—A review:
    # Journal of Hydrology, v. 37, p. 205–222.]
    irep = 0.44
    nrep = 0.12

    divisor = 1.0 / (size + nrep)

    f = np.arange(size, dtype=float)
    f += 1.0 - irep
    f *= divisor

    return f
