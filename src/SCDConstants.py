# A container to store the various constants to be used at different parts of the program.

class SCDConstants:
    DEFAULT_I2C_BUS = 1
    NUM_CHANNELS = 48
    NUM_DIAGNOSTICS = 8
    CTEST_MIN_SETTLING_TIME_MS = 50
    CTEST_MAX_SETTLING_TIME_MS = 5000
    CTEST_NOM_SETTLING_TIME_MS = 200
    DAC_SETTLING_TIME = 200
    DEFAULT_PERIODIC_READ_INTERVAL_MS = 2000
    # TBD: Move BV_MAX and BV_MIN here.
