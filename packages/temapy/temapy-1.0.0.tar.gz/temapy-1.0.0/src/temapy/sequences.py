"""
Classes to represent TEMA sequence data in Python.

Users should not need to create their own sequences or samples but
simply edit those that are provided by Temapy.
"""

from enum import Enum


class Sequence:
    """
    Represents a sequence as a dict mapping a frame-index to a Sample. Also
    provides the updated_range, i.e. the range of indexes that have changed
    since the last update, as a tuple.
    """

    def __init__(self, samples, updated_range):
        self.samples = samples
        self.updated_range = updated_range

    @classmethod
    def of_tema_sequence(cls, tema_sequence):
        """
        Factory method to create a new sequence with data copied from the given
        sequence from Tema.

        :param tema_sequence: The sequence to copy as returned from Tema
        :return: A copy of the Tema sequence
        """
        # TODO: Future improvement to utilize the updated range to
        #  minimize Java-Python data transfer
        samples = {}
        for timestamp, tema_sample in tema_sequence.getSamples().items():
            samples[timestamp] = Sample.of_tema_sample(tema_sample)

        updated_range = (
            int(tema_sequence.getUpdatedRange().start()),
            int(tema_sequence.getUpdatedRange().stop()),
        )

        return cls(samples, updated_range)


class Sample:
    """
    Represents a sample as a list of data points and a status.

    For 2D positional data the data components are [x, y], i.e. data[0] will
    give the x component and data[1] the y component.
    """

    def __init__(self, data, status):
        self.data = data
        # TODO: status should be represented as an enum, will be done
        #  when Java side is being implemented.
        self.status = status

    @classmethod
    def of_tema_sample(cls, tema_sample):
        """
        Factory method to create a new sample with data copied from the given
        sample from TEMA.

        NOTE: This method is not intended to be used directly when writing
        scripts.

        :param tema_sample: The sample to copy as returned from Tema.
        :return: A copy of the Tema sample
        """
        data = [float(data_point) for data_point in tema_sample.getData()]
        status = Status(tema_sample.getStatusAsInt())
        return cls(list(data), status)


class Status(Enum):
    """
    Enum for statuses compatible with Tema.

    In the normal case, any sample that is not valid (see Status.is_valid())
    should not be used for calculation.

    Any sample changed by a script should usually be given the Status CALCULATED.
    """

    NONE = 1
    """
    No status or unknown status.
    """

    FAILED = 2
    """
    Failed status. The data of the Sample failed in creation and that the data 
    might not even be readable. Is invalid and cannot be used for calculations. 
    """

    SLEEPING = 3
    """
    Sleeping status. The data of the Sample is currently set to be ignored for 
    calculation. The data may be meaningful but should be considered invalid 
    and not be used for calculations.
    """

    PREDICTED = 4
    """
    Predicted status. Used by trackers for failed samples that are predicted 
    until they are either found again or declared lost. The data of the Sample 
    may be meaningful but should be considered invalid and not be used for 
    calculations.
    """

    MANUAL = 5
    """
    Manual status. The data of the Sample has been set manually and is therefore
    considered to be valid for calculations.
    """

    CALCULATED = 6
    """
    Calculated status. The data of the Sample has been successfully calculated 
    and may be used for further calculations.
    """

    INTERPOLATED = 7
    """
    Interpolated status. Similar to CALCULATED but the data is interpolated from
    other Samples.
    """

    def is_valid(self):
        """
        Checks if the status is noe that is considered valid
        :return: True if the Status is valid
        """
        return self not in [
            Status.NONE,
            Status.FAILED,
            Status.SLEEPING,
            Status.PREDICTED,
        ]
