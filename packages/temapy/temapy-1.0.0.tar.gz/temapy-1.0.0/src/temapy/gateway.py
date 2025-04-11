"""
Module to set up a connection to a running Tema session.
"""

import argparse
import threading

from py4j.clientserver import ClientServer
from py4j.java_gateway import DEFAULT_PORT
from py4j.java_gateway import JavaGateway, CallbackServerParameters, GatewayParameters

from temapy.sequences import Sequence


class TemaGateway:
    """
    To make your script tema compatible, import and instantiate a
    TemaGateway. Then add your wanted update actions (calculating
    functions) using either the add_update_action function or the
    update_action decorator.

    Typical usage example:

        # Establish connection
        tema_gateway = TemaGateway()

        # Register a calculation function
        @tema_gateway.update_action(
            input_sequences=("seq_1", "seq_2"),
            output_sequences=("seq_3",)
        )
        def my_calculator(first_seq, second_seq, out_seq):
            # your implementation
    """

    class Java:
        """
        This describes to Py4J that the TemaGateway implements the Java
        interface "temapyCallbackInterface". This allows java to call the python
        methods defined in the interface.

        Setting the auto_connect argument to false means that the connection to
        Tema will not be setup automatically and that the self.connect method
        needs to be called to connect to Tema. this can be used to test the
        script without running via Tema.
        """

        implements = ["se.imagesystems.python.temapyCallbackInterface"]

    def __init__(self, auto_connect=True):
        """
        Creates a new TemaGateway that handles communication with Tema and
        allows you to add update actions to modify Tema sequences.

        :param auto_connect: if the gateway should attempt to automatically
               connect to Tema or not.
        """
        self.update_actions = []
        self.input_sequences = {}
        self.output_sequences = {}
        self.shutdown = threading.Event()
        self.tema = None
        self.connection_thread = None
        self.port = None
        self._parse_tema_port()
        if auto_connect:
            self.connect()

    def connect(self):
        """
        Connects temapy to a running Tema application. Should only be called if
        the script is started via Tema.

        If a connection already exist this method does nothing.
        (see request_shutdown(self))
        :return:
        """
        if isinstance(self.tema, ClientServer):
            return
        self._setup_server()
        self._notify_tema()

    def _setup_server(self):
        """
        Creates a client server pair used for sending and receiving commands
        to/from Tema.

        The connection will remain active until the request_shutdown() method is
        called.
        :return:
        """
        # Start py4j Java Gateway with a callback server
        self.tema = JavaGateway(
            gateway_parameters=GatewayParameters(port=self.tema_port),
            # Dynamically allocate a port for the callback server
            callback_server_parameters=CallbackServerParameters(port=0),
            python_server_entry_point=self,
        )

        # Gets the actually allocated port for the callback server
        self.port = self.tema.get_callback_server().get_listening_port()

    def _notify_tema(self):
        """
        Sends the port number of the Python server to Tema so that Tema can
        communicate with python.

        This also indicates to tema that the python process is ready to perform
        calculations.
        :return:
        """
        self.tema.entry_point.setPythonPort(self.port)

    def add_update_action(self, action, *, input_sequences=(), output_sequences=()):
        """
        Adds an update action to be run when Tema calls for a recalculation.

        The action should be a function or other callable that takes sequences
        as input arguments matching the ones supplied in the input_sequences and
        output_sequences arguments in the same order.

        The action should refrain from changing the sequences specified as
        input, as doing so would change the input for subsequent actions in the
        same update. Additionally, changes to input sequences will not be sent
        to Tema.

        Changes made to any sequence specified as output will be copied back
        into tema after all added update actions have run. If multiple actions
        writes to the same output, they will operate on the same sequence and
        might overwrite each other.

        :param action: The action to be performed on the sequences.
        :param input_sequences: The sequences to be used as input to the action
        function.
        :param output_sequences: The sequences to be used as output.
        """

        def do_action():
            # Get the actual output and input sequences
            in_sequences = []
            for wanted_sequence_name in input_sequences:
                try:
                    in_sequences.append(self.input_sequences[wanted_sequence_name])
                except KeyError as e:
                    raise KeyError(
                        f"No input sequence named {wanted_sequence_name}"
                    ) from e
            out_sequences = []
            for wanted_sequence_name in output_sequences:
                try:
                    out_sequences.append(self.output_sequences[wanted_sequence_name])
                except KeyError as e:
                    raise KeyError(
                        f"No output sequence named {wanted_sequence_name}"
                    ) from e

            # Run user action
            action(*in_sequences, *out_sequences)

        self.update_actions.append(do_action)

    def update_action(self, *, input_sequences=(), output_sequences=()):
        """
        Decorator used to add an update action to the given sequences.

        The action should be a function or other callable that takes sequences
        as input arguments matching the ones supplied in the input_sequences and
         output_sequences arguments in the same order.

        The action should refrain from changing the sequences specified as
        input, as doing so would change the input for subsequent actions in the
        same update.

        Changes made to any sequence specified as output will be copied back
        into tema after all added update actions have run. If multiple actions
        writes to the same output, they will operate on the same sequence and
        might overwrite each other.

        :param input_sequences: The sequences to be used as input to the action
        function.
        :param output_sequences: The sequences to be used as output.
        """

        def decorator(action):
            self.add_update_action(
                action,
                input_sequences=input_sequences,
                output_sequences=output_sequences,
            )

            def inner(*args, **kwargs):
                action(*args, **kwargs)

            return inner

        return decorator

    def update(self):
        """
        Performs all registered update actions.
        """
        self._read_sequences_from_tema()
        for action in self.update_actions:
            action()
        self._write_sequences_to_tema()

    def request_shutdown(self):
        """
        Requests that the python-java bridge be shutdown.
        :return:
        """

        def wait_for_shutdown():
            # Wait for shutdown request
            self.shutdown.wait()
            self.shutdown.clear()
            self.tema.shutdown()

        self.connection_thread = threading.Thread(target=wait_for_shutdown)
        self.connection_thread.start()

        self.shutdown.set()

    def _read_sequences_from_tema(self):
        """
        Updates the sequences available to temapy with new input data from tema.

        Runs every time tema calls for an update.
        """
        # FIXME: Future improvement to utilize the updated range to minimize
        #  Java-Python data transfer
        for (
            tema_sequence_name,
            tema_sequence,
        ) in self.tema.entry_point.getInputSequences().items():
            self.input_sequences[str(tema_sequence_name)] = Sequence.of_tema_sequence(
                tema_sequence
            )

        for (
            tema_sequence_name,
            tema_sequence,
        ) in self.tema.entry_point.getOutputSequences().items():
            self.output_sequences[str(tema_sequence_name)] = Sequence.of_tema_sequence(
                tema_sequence
            )

    def _write_sequences_to_tema(self):
        """
        Updates tema with the values of the sequences in temapy.
        """
        # FIXME: Future improvement to utilize the updated range to minimize
        #  Java-Python data transfer
        tema = self.tema.entry_point
        for sequence_name, tema_sequence in tema.getOutputSequences().items():
            if sequence_name not in self.output_sequences:
                continue

            tema_sequence_samples = tema_sequence.getSamples()

            for timestamp, sample in self.output_sequences[
                sequence_name
            ].samples.items():
                java_double_array = self.tema.new_array(
                    self.tema.jvm.double, len(sample.data)
                )

                for i, data_point in enumerate(sample.data):
                    java_double_array[i] = data_point

                tema_sequence_samples[timestamp].setData(java_double_array)
                tema_sequence_samples[timestamp].setStatus(sample.status.value)

    def _parse_tema_port(self):
        """
        Parses the --tema_port program argument if it exists and sets the
        self.tema_port member accordingly.

        If the argument is not specified python will start its server on the
        default port (see py4j.java_gateway.DEFAULT_PORT)
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--tema_port", help="The port the java server is running on"
        )
        args = parser.parse_args()
        if args.tema_port is None:
            self.tema_port = DEFAULT_PORT
            return

        self.tema_port = int(args.tema_port)
