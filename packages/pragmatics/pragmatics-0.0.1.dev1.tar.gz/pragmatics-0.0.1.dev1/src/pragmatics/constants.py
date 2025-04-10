
"""Constants

Provides access to universal constants and known values.
"""

# Import statements
from dataclasses import dataclass, field
from enum import Enum

from .collections import ImmutableDict, crystallize, crystalline


@dataclass(frozen=True)
class Elements:
    """Provides access to data from the Periodic Table of the Elements.

    You should not attempt to directly mutate members of this class.
    Instead, should you need to alter the provided default values for
    any reason, you should work with a copy of the data, e.g., via:

    ```
    # Creates a mutable copy of the `Elements.H` object.
    h = Elements.H
    ```

    Attempting to mutate the `Elements` class directly is an error
    in crude 1.0 and will raise `IllegalMutationError`. (For more
    information about the errors and exceptions that ship with the
    crude framework, try `help(crude.exceptions)` or
    `help(crude.errors)`.
    """
    
    H: dict = field(default_factory=lambda: {
          "name": "hydrogen",
         "symbol": "H",
         "number": 1,
         "mass": 1.00794,
         "boilingPoint": -252.87,
         "meltingPoint": -259.14,
         "density": 0.0899,
         "electronegativity": 2.2}
         )
    
    He: dict = field(default_factory=lambda: {
          "name": "helium",
          "symbol": "He",
          "number": 2,
          "mass": 4.002602,
          "boilingPoint": -268.93,
          "meltingPoint": -272.2,
          "density": 0.1785,
          "electronegativity": None}
         )
    
    Li: dict = field(default_factory=lambda: {
          "name": "lithium",
          "symbol": "Li",
          "number": 3,
          "mass": 6.941,
          "boilingPoint": 1342,
          "meltingPoint": 180.54,
          "density": 0.534,
          "electronegativity": 0.98}
         )
    
    Be: dict = field(default_factory=lambda: {
          "name": "beryllium",
          "symbol": "Be",
          "number": 4,
          "mass": 9.012182,
          "boilingPoint": 2970,
          "meltingPoint": 1287,
          "density": 1.85,
          "electronegativity": 1.57}
         )
    
    B: dict = field(default_factory=lambda: {
         "name": "boron",
         "symbol": "B",
         "number": 5,
         "mass": 10.811,
         "boilingPoint": 4000,
         "meltingPoint": 2075,
         "density": 2.34,
         "electronegativity": 2.04}
         )
    
    C: dict = field(default_factory=lambda: {
         "name": "carbon",
         "symbol": "C",
         "number": 6,
         "mass": 12.0107,
         "boilingPoint": 4300,
         "meltingPoint": 3550,
         "density": 2.26,
         "electronegativity": 2.55}
         )
    
    N: dict = field(default_factory=lambda: {
         "name": "nitrogen",
         "symbol": "N",
         "number": 7,
         "mass": 14.0067,
         "boilingPoint": -195.79,
         "meltingPoint": -210.0,
         "density": 0.001251,
         "electronegativity": 3.04}
         )
    
    O: dict = field(default_factory=lambda: {
         "name": "oxygen",
         "symbol": "O",
         "number": 8,
         "mass": 15.9994,
         "boilingPoint": -182.95,
         "meltingPoint": -218.79,
         "density": 0.001429,
         "electronegativity": 3.44}
         )
    
    F: dict = field(default_factory=lambda: {
         "name": "fluorine",
         "symbol": "F",
         "number": 9,
         "mass": 18.9984032,
         "boilingPoint": -188.12,
         "meltingPoint": -219.62,
         "density": 0.001696,
         "electronegativity": 3.98}
         )
    
    Ne: dict = field(default_factory=lambda: {
          "name": "neon",
          "symbol": "Ne",
          "number": 10,
          "mass": 20.1797,
          "boilingPoint": -246.08,
          "meltingPoint": -248.59,
          "density": 0.0009,
          "electronegativity": None}
         )
    
    Na: dict = field(default_factory=lambda: {
          "name": "sodium",
          "symbol": "Na",
          "number": 11,
          "mass": 22.98976928,
          "boilingPoint": 882.9,
          "meltingPoint": 97.72,
          "density": 0.971,
          "electronegativity": 0.93}
         )
    
    Mg: dict = field(default_factory=lambda: {
          "name": "magnesium",
          "symbol": "Mg",
          "number": 12,
          "mass": 24.305,
          "boilingPoint": 1090,
          "meltingPoint": 650,
          "density": 1.738,
          "electronegativity": 1.31}
         )
    
    Al: dict = field(default_factory=lambda: {
          "name": "aluminum",
          "symbol": "Al",
          "number": 13,
          "mass": 26.9815386,
          "boilingPoint": 2519,
          "meltingPoint": 660.32,
          "density": 2.698,
          "electronegativity": 1.61}
         )
    
    Si: dict = field(default_factory=lambda: {
          "name": "silicon",
          "symbol": "Si",
          "number": 14,
          "mass": 28.0855,
          "boilingPoint": 3265,
          "meltingPoint": 1414,
          "density": 2.3296,
          "electronegativity": 1.9}
         )
    
    P: dict = field(default_factory=lambda: {
          "name": "phosphorus",
         "symbol": "P",
         "number": 15,
         "mass": 30.973762,
         "boilingPoint": 280.5,
         "meltingPoint": 44.15,
         "density": 1.82,
         "electronegativity": 2.19}
         )
    
    S: dict = field(default_factory=lambda: {
          "name": "sulfur",
         "symbol": "S",
         "number": 16,
         "mass": 32.065,
         "boilingPoint": 444.6,
         "meltingPoint": 115.21,
         "density": 2.067,
         "electronegativity": 2.58}
         )
    
    Cl: dict = field(default_factory=lambda: {
          "name": "chlorine",
          "symbol": "Cl",
          "number": 17,
          "mass": 35.453,
          "boilingPoint": -34.04,
          "meltingPoint": -101.5,
          "density": 0.003214,
          "electronegativity": 3.16}
         )
    
    Ar: dict = field(default_factory=lambda: {
          "name": "argon",
          "symbol": "Ar",
          "number": 18,
          "mass": 39.948,
          "boilingPoint": -185.85,
          "meltingPoint": -189.34,
          "density": 0.0017837,
          "electronegativity": None}
         )
    
    K: dict = field(default_factory=lambda: {
          "name": "potassium",
         "symbol": "K",
         "number": 19,
         "mass": 39.0983,
         "boilingPoint": 759,
         "meltingPoint": 63.38,
         "density": 0.862,
         "electronegativity": 0.82}
         )
    
    Ca: dict = field(default_factory=lambda: {
          "name": "calcium",
          "symbol": "Ca",
          "number": 20,
          "mass": 40.078,
          "boilingPoint": 1484,
          "meltingPoint": 842,
          "density": 1.54,
          "electronegativity": 1.0}
         )

    Fe: dict = field(default_factory=lambda: {
          "name": "iron",
          "symbol": "Fe",
          "number": 26,
          "mass": 55.845,
          "boilingPoint": 2861,
          "meltingPoint": 1538,
          "density": 7.874,
          "electronegativity": 1.83}
         )
    
    Cu: dict = field(default_factory=lambda: {
          "name": "copper",
          "symbol": "Cu",
          "number": 29,
          "mass": 63.546,
          "boilingPoint": 2562,
          "meltingPoint": 1084.62,
          "density": 8.96,
          "electronegativity": 1.9}
         )
    
    Zn: dict = field(default_factory=lambda: {
          "name": "zinc",
          "symbol": "Zn",
          "number": 30,
          "mass": 65.38,
          "boilingPoint": 907,
          "meltingPoint": 419.53,
          "density": 7.134,
          "electronegativity": 1.65}
         )
    
    Ag: dict = field(default_factory=lambda: {
          "name": "silver",
          "symbol": "Ag",
          "number": 47,
          "mass": 107.8682,
          "boilingPoint": 2162,
          "meltingPoint": 961.78,
          "density": 10.49,
          "electronegativity":1.93}
         )
    
    Au: dict = field(default_factory=lambda: {
          "name": "gold",
          "symbol": "Au",
          "number": 79,
          "mass": 196.966569,
          "boilingPoint": 2856,
          "meltingPoint": 1064.18,
          "density": 19.3,
          "electronegativity": 2.54}
         )
    
    Hg: dict = field(default_factory=lambda: {
          "name": "mercury",
          "symbol": "Hg",
          "number": 80,
          "mass": 200.59,
          "boilingPoint": 356.73,
          "meltingPoint": -38.83,
          "density": 13.546,
          "electronegativity": 2.0}
         )
    
    Pb: dict = field(default_factory=lambda: {
          "name": "lead",
          "symbol": "Pb",
          "number": 82,
          "mass": 207.2,
          "boilingPoint": 1749,
          "meltingPoint": 327.46,
          "density": 11.34,
          "electronegativity": 2.33}
         )
    
    U: dict = field(default_factory=lambda: {
         "name": "uranium",
         "symbol": "U",
         "number": 92,
         "mass": 238.02891,
         "boilingPoint": 4131,
         "meltingPoint": 1135,
         "density": 19.1,
         "electronegativity": 1.38}
         )
    
    Sc: dict = field(default_factory=lambda: {
          "name": "scandium",
          "symbol": "Sc",
          "number": 21,
          "mass": 44.955912,
          "boilingPoint": 2836,
          "meltingPoint": 1541,
          "density": 2.989,
          "electronegativity": 1.36}
         )
    
    Ti: dict = field(default_factory=lambda: {
          "name": "titanium",
          "symbol": "Ti",
          "number": 22,
          "mass": 47.867,
          "boilingPoint": 3287,
          "meltingPoint": 1668,
          "density": 4.54,
          "electronegativity": 1.54}
         )
    
    V: dict = field(default_factory=lambda: {
          "name": "vanadium",
          "symbol": "V",
          "number": 23,
          "mass": 50.9415,
          "boilingPoint": 3407,
          "meltingPoint": 1910,
          "density": 6.11,
          "electronegativity": 1.63}
         )
    
    Cr: dict = field(default_factory=lambda: {
          "name": "chromium",
          "symbol": "Cr",
          "number": 24,
          "mass": 51.9961,
          "boilingPoint": 2671,
          "meltingPoint": 1907,
          "density": 7.19,
          "electronegativity": 1.66}
         )
    
    Mn: dict = field(default_factory=lambda: {
          "name": "manganese",
          "symbol": "Mn",
          "number": 25,
          "mass": 54.938045,
          "boilingPoint": 2061,
          "meltingPoint": 1246,
          "density": 7.43,
          "electronegativity": 1.55}
         )
    
    Co: dict = field(default_factory=lambda: {
          "name": "cobalt",
          "symbol": "Co",
          "number": 27,
          "mass": 58.933195,
          "boilingPoint": 2927,
          "meltingPoint": 1495,
          "density": 8.90,
          "electronegativity": 1.88}
         )
    
    Ni: dict = field(default_factory=lambda: {
          "name": "nickel",
          "symbol": "Ni",
          "number": 28,
          "mass": 58.6934,
          "boilingPoint": 2913,
          "meltingPoint": 1455,
          "density": 8.90,
          "electronegativity": 1.91}
         )
    
    Ga: dict = field(default_factory=lambda: {
          "name": "gallium",
          "symbol": "Ga",
          "number": 31,
          "mass": 69.723,
          "boilingPoint": 2204,
          "meltingPoint": 29.76,
          "density": 5.904,
          "electronegativity": 1.81}
         )
    
    Ge: dict = field(default_factory=lambda: {
          "name": "germanium",
          "symbol": "Ge",
          "number": 32,
          "mass": 72.64,
          "boilingPoint": 2833,
          "meltingPoint": 938.25,
          "density": 5.323,
          "electronegativity": 2.01}
         )
    
    As: dict = field(default_factory=lambda: {
          "name": "arsenic",
          "symbol": "As",
          "number": 33,
          "mass": 74.92160,
          "boilingPoint": 614,  # sublimes
          "meltingPoint": 817,  # at high pressure
          "density": 5.727,
          "electronegativity": 2.18}
         )
    
    Se: dict = field(default_factory=lambda: {
          "name": "selenium",
          "symbol": "Se",
          "number": 34,
          "mass": 78.96,
          "boilingPoint": 685,
          "meltingPoint": 221,
          "density": 4.79,
          "electronegativity": 2.55}
         )
    
    Br: dict = field(default_factory=lambda: {
          "name": "bromine",
          "symbol": "Br",
          "number": 35,
          "mass": 79.904,
          "boilingPoint": 58.8,
          "meltingPoint": -7.3,
          "density": 3.12,
          "electronegativity": 2.96}
         )
    
    Kr: dict = field(default_factory=lambda: {
          "name": "krypton",
          "symbol": "Kr",
          "number": 36,
          "mass": 83.80,
          "boilingPoint": -153.22,
          "meltingPoint": -157.36,
          "density": 0.003733,
          "electronegativity": 3.0}
         )
    
    Rb: dict = field(default_factory=lambda: {
          "name": "rubidium",
          "symbol": "Rb",
          "number": 37,
          "mass": 85.4678,
          "boilingPoint": 688,
          "meltingPoint": 39.31,
          "density": 1.532,
          "electronegativity": 0.82}
         )
    
    Sr: dict = field(default_factory=lambda: {
          "name": "strontium",
          "symbol": "Sr",
          "number": 38,
          "mass": 87.62,
          "boilingPoint": 1382,
          "meltingPoint": 777,
          "density": 2.64,
          "electronegativity": 0.95}
         )
    
    Y: dict = field(default_factory=lambda: {
          "name": "yttrium",
          "symbol": "Y",
          "number": 39,
          "mass": 88.90585,
          "boilingPoint": 3345,
          "meltingPoint": 1522,
          "density": 4.47,
          "electronegativity": 1.22}
         )
    
    Zr: dict = field(default_factory=lambda: {
          "name": "zirconium",
          "symbol": "Zr",
          "number": 40,
          "mass": 91.224,
          "boilingPoint": 4409,
          "meltingPoint": 1855,
          "density": 6.506,
          "electronegativity": 1.33}
         )
    
    Nb: dict = field(default_factory=lambda: {
          "name": "niobium",
          "symbol": "Nb",
          "number": 41,
          "mass": 92.90638,
          "boilingPoint": 4744,
          "meltingPoint": 2477,
          "density": 8.57,
          "electronegativity": 1.6}
         )
    
    Mo: dict = field(default_factory=lambda: {
          "name": "molybdenum",
          "symbol": "Mo",
          "number": 42,
          "mass": 95.94,
          "boilingPoint": 4639,
          "meltingPoint": 2623,
          "density": 10.22,
          "electronegativity": 2.16}
         )
    
    Tc: dict = field(default_factory=lambda: {
          "name": "technetium",
          "symbol": "Tc",
          "number": 43,
          "mass": 98,  # Approximate value
          "boilingPoint": 4265,
          "meltingPoint": 2157,
          "density": 11.5,
          "electronegativity": 1.9}
         )
    
    Ru: dict = field(default_factory=lambda: {
          "name": "ruthenium",
          "symbol": "Ru",
          "number": 44,
          "mass": 101.07,
          "boilingPoint": 4150,
          "meltingPoint": 2334,
          "density": 12.37,
          "electronegativity": 2.2}
         )
    
    Rh: dict = field(default_factory=lambda: {
          "name": "rhodium",
          "symbol": "Rh",
          "number": 45,
          "mass": 102.90550,
          "boilingPoint": 3695,
          "meltingPoint": 1964,
          "density": 12.41,
          "electronegativity": 2.28}
         )
    
    Pd: dict = field(default_factory=lambda: {
          "name": "palladium",
          "symbol": "Pd",
          "number": 46,
          "mass": 106.42,
          "boilingPoint": 2963,
          "meltingPoint": 1555,
          "density": 12.02,
          "electronegativity": 2.2}
         )
    
    Cd: dict = field(default_factory=lambda: {
          "name": "cadmium",
          "symbol": "Cd",
          "number": 48,
          "mass": 112.411,
          "boilingPoint": 767,
          "meltingPoint": 321.07,
          "density": 8.65,
          "electronegativity": 1.69}
         )
    
    In: dict = field(default_factory=lambda: {
          "name": "indium",
          "symbol": "In",
          "number": 49,
          "mass": 114.818,
          "boilingPoint": 2072,
          "meltingPoint": 156.6,
          "density": 7.31,
          "electronegativity": 1.78}
         )
    
    Sn: dict = field(default_factory=lambda: {
          "name": "tin",
          "symbol": "Sn",
          "number": 50,
          "mass": 118.710,
          "boilingPoint": 2602,
          "meltingPoint": 231.93,
          "density": 7.31,
          "electronegativity": 1.96}
         )
    
    Sb: dict = field(default_factory=lambda: {
          "name": "antimony",
          "symbol": "Sb",
          "number": 51,
          "mass": 121.760,
          "boilingPoint": 1587,
          "meltingPoint": 630.63,
          "density": 6.697,
          "electronegativity": 2.05}
         )
    
    Te: dict = field(default_factory=lambda: {
          "name": "tellurium",
          "symbol": "Te",
          "number": 52,
          "mass": 127.60,
          "boilingPoint": 988,
          "meltingPoint": 449.51,
          "density": 6.24,
          "electronegativity": 2.1}
         )
    
    I: dict = field(default_factory=lambda: {
          "name": "iodine",
          "symbol": "I",
          "number": 53,
          "mass": 126.90447,
          "boilingPoint": 184.3,
          "meltingPoint": 113.7,
          "density": 4.94,
          "electronegativity": 2.66}
         )
    
    Xe: dict = field(default_factory=lambda: {
          "name": "xenon",
          "symbol": "Xe",
          "number": 54,
          "mass": 131.293,
          "boilingPoint": -108.1,
          "meltingPoint": -111.8,
          "density": 0.005887,
          "electronegativity": 2.6}
         )
    
    Cs: dict = field(default_factory=lambda: {
          "name": "cesium",
          "symbol": "Cs",
          "number": 55,
          "mass": 132.9054519,
          "boilingPoint": 671,
          "meltingPoint": 28.44,
          "density": 1.873,
          "electronegativity": 0.79}
         )
    
    Ba: dict = field(default_factory=lambda: {
          "name": "barium",
          "symbol": "Ba",
          "number": 56,
          "mass": 137.327,
          "boilingPoint": 1897,
          "meltingPoint": 727,
          "density": 3.594,
          "electronegativity": 0.89}
         )
    
    La: dict = field(default_factory=lambda: {
          "name": "lanthanum",
          "symbol": "La",
          "number": 57,
          "mass": 138.9055,
          "boilingPoint": 3464,
          "meltingPoint": 920,
          "density": 6.145,
          "electronegativity": 1.1}
         )
    
    Ce: dict = field(default_factory=lambda: {
          "name": "cerium",
          "symbol": "Ce",
          "number": 58,
          "mass": 140.116,
          "boilingPoint": 3443,
          "meltingPoint": 798,
          "density": 6.77,
          "electronegativity": 1.12}
         )
    
    Pr: dict = field(default_factory=lambda: {
          "name": "praseodymium",
          "symbol": "Pr",
          "number": 59,
          "mass": 140.90765,
          "boilingPoint": 3520,
          "meltingPoint": 931,
          "density": 6.773,
          "electronegativity": 1.13}
         )
    
    Nd: dict = field(default_factory=lambda: {
          "name": "neodymium",
          "symbol": "Nd",
          "number": 60,
          "mass": 144.242,
          "boilingPoint": 3074,
          "meltingPoint": 1021,
          "density": 7.007,
          "electronegativity": 1.14}
         )
    
    Pm: dict = field(default_factory=lambda: {
          "name": "promethium",
          "symbol": "Pm",
          "number": 61,
          "mass": 145,
          "boilingPoint": 3000,
          "meltingPoint": 1042,
          "density": 7.26,
          "electronegativity": 1.13}
         )
    
    Sm: dict = field(default_factory=lambda: {
          "name": "samarium",
          "symbol": "Sm",
          "number": 62,
          "mass": 150.36,
          "boilingPoint": 1794,
          "meltingPoint": 1074,
          "density": 7.52,
          "electronegativity": 1.17}
         )
    
    Eu: dict = field(default_factory=lambda: {
          "name": "europium",
          "symbol": "Eu",
          "number": 63,
          "mass": 151.964,
          "boilingPoint": 1596,
          "meltingPoint": 822,
          "density": 5.243,
          "electronegativity": 1.2}
         )
    
    Gd: dict = field(default_factory=lambda: {
          "name": "gadolinium",
          "symbol": "Gd",
          "number": 64,
          "mass": 157.25,
          "boilingPoint": 3273,
          "meltingPoint": 1313,
          "density": 7.895,
          "electronegativity": 1.2}
         )
    
    Tb: dict = field(default_factory=lambda: {
          "name": "terbium",
          "symbol": "Tb",
          "number": 65,
          "mass": 158.92535,
          "boilingPoint": 3230,
          "meltingPoint": 1356,
          "density": 8.229,
          "electronegativity": 1.2}
         )
    
    Dy: dict = field(default_factory=lambda: {
          "name": "dysprosium",
          "symbol": "Dy",
          "number": 66,
          "mass": 162.500,
          "boilingPoint": 2567,
          "meltingPoint": 1412,
          "density": 8.55,
          "electronegativity": 1.22}
         )
    
    Ho: dict = field(default_factory=lambda: {
          "name": "holmium",
          "symbol": "Ho",
          "number": 67,
          "mass": 164.93032,
          "boilingPoint": 2700,
          "meltingPoint": 1474,
          "density": 8.795,
          "electronegativity": 1.23}
         )
    
    Er: dict = field(default_factory=lambda: {
          "name": "erbium",
          "symbol": "Er",
          "number": 68,
          "mass": 167.259,
          "boilingPoint": 2868,
          "meltingPoint": 1529,
          "density": 9.066,
          "electronegativity": 1.24}
         )
    
    Tm: dict = field(default_factory=lambda: {
          "name": "thulium",
          "symbol": "Tm",
          "number": 69,
          "mass": 168.93421,
          "boilingPoint": 1950,
          "meltingPoint": 1545,
          "density": 9.321,
          "electronegativity": 1.25}
         )
    
    Yb: dict = field(default_factory=lambda: {
          "name": "ytterbium",
          "symbol": "Yb",
          "number": 70,
          "mass": 173.04,
          "boilingPoint": 1196,
          "meltingPoint": 819,
          "density": 6.965,
          "electronegativity": 1.1}
         )
    
    Lu: dict = field(default_factory=lambda: {
          "name": "lutetium",
          "symbol": "Lu",
          "number": 71,
          "mass": 174.967,
          "boilingPoint": 3402,
          "meltingPoint": 1663,
          "density": 9.84,
          "electronegativity": 1.27}
         )
    
    Hf: dict = field(default_factory=lambda: {
          "name": "hafnium",
          "symbol": "Hf",
          "number": 72,
          "mass": 178.49,
          "boilingPoint": 4603,
          "meltingPoint": 2233,
          "density": 13.31,
          "electronegativity": 1.3}
         )
    
    Ta: dict = field(default_factory=lambda: {
          "name": "tantalum",
          "symbol": "Ta",
          "number": 73,
          "mass": 180.9479,
          "boilingPoint": 5458,
          "meltingPoint": 3017,
          "density": 16.654,
          "electronegativity": 1.5}
         )
    
    W: dict = field(default_factory=lambda: {
          "name": "tungsten",
          "symbol": "W",
          "number": 74,
          "mass": 183.84,
          "boilingPoint": 5555,
          "meltingPoint": 3422,
          "density": 19.25,
          "electronegativity": 2.36}
         )
    
    Re: dict = field(default_factory=lambda: {
          "name": "rhenium",
          "symbol": "Re",
          "number": 75,
          "mass": 186.207,
          "boilingPoint": 5596,
          "meltingPoint": 3186,
          "density": 21.02,
          "electronegativity": 1.9}
         )
    
    Os: dict = field(default_factory=lambda: {
          "name": "osmium",
          "symbol": "Os",
          "number": 76,
          "mass": 190.23,
          "boilingPoint": 5012,
          "meltingPoint": 3033,
          "density": 22.59,
          "electronegativity": 2.2}
         )
    
    Ir: dict = field(default_factory=lambda: {
          "name": "iridium",
          "symbol": "Ir",
          "number": 77,
          "mass": 192.217,
          "boilingPoint": 4428,
          "meltingPoint": 2446,
          "density": 22.56,
          "electronegativity": 2.2}
         )
    
    Pt: dict = field(default_factory=lambda: {
          "name": "platinum",
          "symbol": "Pt",
          "number": 78,
          "mass": 195.084,
          "boilingPoint": 3825,
          "meltingPoint": 1768.3,
          "density": 21.45,
          "electronegativity": 2.28}
         )
    
    Tl: dict = field(default_factory=lambda: {
          "name": "thallium",
          "symbol": "Tl",
          "number": 81,
          "mass": 204.3833,
          "boilingPoint": 1473,
          "meltingPoint": 304,
          "density": 11.85,
          "electronegativity": 2.04}
         )
    
    Bi: dict = field(default_factory=lambda: {
          "name": "bismuth",
          "symbol": "Bi",
          "number": 83,
          "mass": 208.98040,
          "boilingPoint": 1564,
          "meltingPoint": 271.4,
          "density": 9.78,
          "electronegativity": 2.02}
         )
    
    Po: dict = field(default_factory=lambda: {
          "name": "polonium",
          "symbol": "Po",
          "number": 84,
          "mass": 209,
          "boilingPoint": 962,
          "meltingPoint": 254,
          "density": 9.196,
          "electronegativity": 2.0}
         )
    
    At: dict = field(default_factory=lambda: {
          "name": "astatine",
          "symbol": "At",
          "number": 85,
          "mass": 210,
          "boilingPoint": 337,
          "meltingPoint": 302,
          "density": 7, # estimated
          "electronegativity": 2.2}
         )
    
    Rn: dict = field(default_factory=lambda: {
          "name": "radon",
          "symbol": "Rn",
          "number": 86,
          "mass": 222,
          "boilingPoint": -61.7,
          "meltingPoint": -71,
          "density": 0.00973,
          "electronegativity": None}
         )
    
    Fr: dict = field(default_factory=lambda: {
          "name": "francium",
          "symbol": "Fr",
          "number": 87,
          "mass": 223,
          "boilingPoint": 677,
          "meltingPoint": 27,
          "density": 1.87, # estimated
          "electronegativity": 0.7}
         )
    
    Ra: dict = field(default_factory=lambda: {
          "name": "radium",
          "symbol": "Ra",
          "number": 88,
          "mass": 226,
          "boilingPoint": 1737,
          "meltingPoint": 700,
          "density": 5.5,
          "electronegativity": 0.9}
         )
    
    Ac: dict = field(default_factory=lambda: {
          "name": "actinium",
          "symbol": "Ac",
          "number": 89,
          "mass": 227,
          "boilingPoint": 3200, # estimated
          "meltingPoint": 1050,
          "density": 10.07,
          "electronegativity": 1.1}
         )
    
    Th: dict = field(default_factory=lambda: {
          "name": "thorium",
          "symbol": "Th",
          "number": 90,
          "mass": 232.03806,
          "boilingPoint": 4820,
          "meltingPoint": 1750,
          "density": 11.72,
          "electronegativity": 1.3}
         )
    
    Pa: dict = field(default_factory=lambda: {
          "name": "protactinium",
          "symbol": "Pa",
          "number": 91,
          "mass": 231.03588,
          "boilingPoint": 4000, # estimated
          "meltingPoint": 1572,
          "density": 15.37,
          "electronegativity": 1.5}
         )
    
    Np: dict = field(default_factory=lambda: {
          "name": "neptunium",
          "symbol": "Np",
          "number": 93,
          "mass": 237,
          "boilingPoint": 4273,
          "meltingPoint": 644,
          "density": 20.45,
          "electronegativity": 1.36}
         )
    
    Pu: dict = field(default_factory=lambda: {
          "name": "plutonium",
          "symbol": "Pu",
          "number": 94,
          "mass": 244,
          "boilingPoint": 3228,
          "meltingPoint": 640,
          "density": 19.84,
          "electronegativity": 1.28}
         )
      
    Am: dict = field(default_factory=lambda: {
          "name": "americium",
          "symbol": "Am",
          "number": 95,
          "mass": 243,
          "boilingPoint": 2011,
          "meltingPoint": 1176,
          "density": 13.67,
          "electronegativity": 1.3}
         )
    
    Cm: dict = field(default_factory=lambda: {
          "name": "curium",
          "symbol": "Cm",
          "number": 96,
          "mass": 247,
          "boilingPoint": 3110,
          "meltingPoint": 1345,
          "density": 13.51,
          "electronegativity": 1.3}
         )
    
    Bk: dict = field(default_factory=lambda: {
          "name": "berkelium",
          "symbol": "Bk",
          "number": 97,
          "mass": 247,
          "boilingPoint": 2900,  # estimated
          "meltingPoint": 1050,
          "density": 14.78,
          "electronegativity": 1.3}
         )
    
    Cf: dict = field(default_factory=lambda: {
          "name": "californium",
          "symbol": "Cf",
          "number": 98,
          "mass": 251,
          "boilingPoint": 1472,  # estimated
          "meltingPoint": 900,
          "density": 15.1,
          "electronegativity": 1.3}
         )
    
    Es: dict = field(default_factory=lambda: {
          "name": "einsteinium",
          "symbol": "Es",
          "number": 99,
          "mass": 252,
          "boilingPoint": 1269,  # estimated
          "meltingPoint": 860,
          "density": 8.84,  # estimated
          "electronegativity": 1.3}
         )
    
    Fm: dict = field(default_factory=lambda: {
          "name": "fermium",
          "symbol": "Fm",
          "number": 100,
          "mass": 257,
          "boilingPoint": 1800,  # estimated
          "meltingPoint": 1527,
          "density": 9.7,  # estimated
          "electronegativity": 1.3}
         )
    
    Md: dict = field(default_factory=lambda: {
          "name": "mendelevium",
          "symbol": "Md",
          "number": 101,
          "mass": 258,
          "boilingPoint": 1100,  # estimated
          "meltingPoint": 827,
          "density": 10.3,  # estimated
          "electronegativity": 1.3}
         )
    
    No: dict = field(default_factory=lambda: {
          "name": "nobelium",
          "symbol": "No",
          "number": 102,
          "mass": 259,
          "boilingPoint": 1100,  # estimated
          "meltingPoint": 827,
          "density": 9.9,  # estimated
          "electronegativity": 1.3}
         )
    
    Lr: dict = field(default_factory=lambda: {
          "name": "lawrencium",
          "symbol": "Lr",
          "number": 103,
          "mass": 262,
          "boilingPoint": 1900,  # estimated
          "meltingPoint": 1627,
          "density": 15.6,  # estimated
          "electronegativity": 1.3}
         )
    
    Rf: dict = field(default_factory=lambda: {
          "name": "rutherfordium",
          "symbol": "Rf",
          "number": 104,
          "mass": 267,
          "boilingPoint": 5800,  # estimated
          "meltingPoint": 2400,  # estimated
          "density": 23.2,  # estimated
          "electronegativity": None}
         )
    
    Db: dict = field(default_factory=lambda: {
          "name": "dubnium",
          "symbol": "Db",
          "number": 105,
          "mass": 268,
          "boilingPoint": None,  # unknown
          "meltingPoint": None,  # unknown
          "density": 29.3,  # estimated
          "electronegativity": None}
         )
    
    Sg: dict = field(default_factory=lambda: {
          "name": "seaborgium",
          "symbol": "Sg",
          "number": 106,
          "mass": 269,
          "boilingPoint": None,  # unknown
          "meltingPoint": None,  # unknown
          "density": 35.0,  # estimated
          "electronegativity": None}
         )
    
    Bh: dict = field(default_factory=lambda: {
          "name": "bohrium",
          "symbol": "Bh",
          "number": 107,
          "mass": 270,
          "boilingPoint": None,  # unknown
          "meltingPoint": None,  # unknown
          "density": 37.1,  # estimated
          "electronegativity": None}
         )
    
    Hs: dict = field(default_factory=lambda: {
          "name": "hassium",
          "symbol": "Hs",
          "number": 108,
          "mass": 270,
          "boilingPoint": None,  # unknown
          "meltingPoint": None,  # unknown
          "density": 40.7,  # estimated
          "electronegativity": None}
         )
    
    Mt: dict = field(default_factory=lambda: {
          "name": "meitnerium",
          "symbol": "Mt",
          "number": 109,
          "mass": 278,
          "boilingPoint": None,  # unknown
          "meltingPoint": None,  # unknown
          "density": 37.4,  # estimated
          "electronegativity": None}
         )
    
    Ds: dict = field(default_factory=lambda: {
          "name": "darmstadtium",
          "symbol": "Ds",
          "number": 110,
          "mass": 281,
          "boilingPoint": None,  # unknown
          "meltingPoint": None,  # unknown
          "density": 34.8,  # estimated
          "electronegativity": None}
         )
    
    Rg: dict = field(default_factory=lambda: {
          "name": "roentgenium",
          "symbol": "Rg",
          "number": 111,
          "mass": 282,
          "boilingPoint": None,  # unknown
          "meltingPoint": None,  # unknown
          "density": 28.7,  # estimated
          "electronegativity": None}
         )
    
    Cn: dict = field(default_factory=lambda: {
          "name": "copernicium",
          "symbol": "Cn",
          "number": 112,
          "mass": 285,
          "boilingPoint": 357,  # estimated
          "meltingPoint": None,  # unknown
          "density": 14.0,  # estimated
          "electronegativity": None}
         )
    
    Nh: dict = field(default_factory=lambda: {
          "name": "nihonium",
          "symbol": "Nh",
          "number": 113,
          "mass": 286,
          "boilingPoint": 1130,  # estimated
          "meltingPoint": 700,  # estimated
          "density": 16.0,  # estimated
          "electronegativity": None}
         )
    
    Fl: dict = field(default_factory=lambda: {
          "name": "flerovium",
          "symbol": "Fl",
          "number": 114,
          "mass": 289,
          "boilingPoint": 210,  # estimated
          "meltingPoint": 67,  # estimated
          "density": 14.0,  # estimated
          "electronegativity": None}
         )
    
    Mc: dict = field(default_factory=lambda: {
          "name": "moscovium",
          "symbol": "Mc",
          "number": 115,
          "mass": 290,
          "boilingPoint": 1400,  # estimated
          "meltingPoint": 670,  # estimated
          "density": 13.5,  # estimated
          "electronegativity": None}
         )
    
    Lv: dict = field(default_factory=lambda: {
          "name": "livermorium",
          "symbol": "Lv",
          "number": 116,
          "mass": 293,
          "boilingPoint": 1085,  # estimated
          "meltingPoint": 709,  # estimated
          "density": 12.9,  # estimated
          "electronegativity": None}
         )
    
    Ts: dict = field(default_factory=lambda: {
          "name": "tennessine",
          "symbol": "Ts",
          "number": 117,
          "mass": 294,
          "boilingPoint": 610,  # estimated
          "meltingPoint": 723,  # estimated
          "density": 7.2,  # estimated
          "electronegativity": None}
         )
    
    Og: dict = field(default_factory=lambda: {
          "name": "oganesson",
          "symbol": "Og",
          "number": 118,
          "mass": 294,
          "boilingPoint": 350,  # estimated
          "meltingPoint": 325,  # estimated
          "density": 5.0,  # estimated
          "electronegativity": None}
         )

    @crystalline
    def __post_init__(self):
        pass

    @classmethod
    def cp(cls, element_dict) -> dict:
        if isinstance(element_dict, ImmutableDict):
            return dict(element_dict)
        return element_dict.copy()


class Constants(Enum):
    AVOGADRO: float = 6.0221408e+23     # Unitless
    GAS: float = 8.314                  # J/(mol•K)
    PLANCK: float = 6.63e-34            # (kg•m²)/s
    LIGHTSPEED: float = 2.99792458e+8   # m/s


# Reexport members of the `Constants` enum to use convenience aliases.
NA = Constants.AVOGADRO.value
R = Constants.GAS.value
c = Constants.LIGHTSPEED.value
e = Elements()
h = Constants.PLANCK.value

