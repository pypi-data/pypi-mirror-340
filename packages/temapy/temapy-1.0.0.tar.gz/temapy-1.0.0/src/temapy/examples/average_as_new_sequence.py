"""
Test script that adds an update action to calculate the average pos of
every sample in two sequences.
"""

from temapy.gateway import TemaGateway
from temapy.sequences import Status


tema_gateway = TemaGateway()


@tema_gateway.update_action(
    input_sequences=("p1_pos", "p2_pos"), output_sequences=("avg_pos",)
)
def average_per_sample(seq_1, seq_2, seq_out):
    """
    calculates the average pos of every sample in two sequences.

    :param seq_1: the first sequence
    :param seq_2: the second sequence
    :param seq_out: sequence to put result in
    :return:
    """
    both_sequences = zip(seq_1.samples.items(), seq_2.samples.values())
    for (time_1, sample_1), sample_2 in both_sequences:
        if seq_1.samples[time_1].status.is_valid():
            seq_out.samples[time_1].data[0] = (sample_1.data[0] + sample_2.data[0]) / 2
            seq_out.samples[time_1].data[1] = (sample_1.data[1] + sample_2.data[1]) / 2
            seq_out.samples[time_1].status = Status.CALCULATED
